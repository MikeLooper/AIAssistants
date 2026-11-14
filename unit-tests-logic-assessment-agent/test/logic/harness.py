"""Shared harness for the Unit Test Coverage Reviewer validation tests (Python 3.10+, stdlib only).

Each test script (test_api_dotnet.py, test_api_java.py, test_api_python.py) calls ``main(lang)``. The harness:

1. builds a copy of the app and runs its unit tests, so the answer key is checked against suites that compile and pass,
2. resolves the AI tool (``--tool``, ``COVERAGE_TEST_TOOL``, the VS Code chat that started it, or Claude),
3. runs the Unit Test Coverage Reviewer agent headlessly against the app, with a Run ID chosen by the harness,
4. scores the run's stage-3 audit (``transitions/03-assertion-audit-<runId>.md``) against ``answer_key.json``
   (the data form of the answer key in test/README.md),
5. writes a JSON and Markdown result and exits 0 (pass), 1 (fail) or 2 (error: no scorable run).

The reviewer writes Markdown, not JSON, so scoring parses its tables: each row is assigned a source unit and a
method (from the row itself or the nearest heading), its condition text is matched against the answer key's
regular expressions, and its Classification column (Covered / Partially Covered / Uncovered) is read.

Pass rule: at least ``--min-found`` percent of the seeded gaps were found, and no control path (a path the unit
tests cover with strong assertions) was classified Uncovered.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

LOGIC_DIR = Path(__file__).resolve().parent
TEST_DIR = LOGIC_DIR.parent
REPO_ROOT = TEST_DIR.parent  # unit-tests-logic-assessment-agent: the reviewer's workspace
ANSWER_KEY = LOGIC_DIR / "answer_key.json"
DEFAULT_RESULTS_DIR = LOGIC_DIR / "results"
TRANSITIONS_DIR = REPO_ROOT / "transitions"
DOCS_DIR = REPO_ROOT / "docs"
AGENT_NAME = "unit-test-coverage-reviewer"
AGENT_FILE = REPO_ROOT / ".github" / "agents" / f"{AGENT_NAME}.agent.md"

TOOLS = ("claude", "copilot")
LANGS = ("dotNET", "java", "python")
KIND = "apis"
BUILD_OUTPUT_DIRS = ("bin", "obj", "target", "__pycache__", ".venv")
# test/Directory.Build.props sends MSBuild output for every project under test/ here, outside the apps.
MSBUILD_OUTPUT_ROOT = TEST_DIR / ".build-output"
PREFLIGHT_ATTEMPTS = 5
PREFLIGHT_SETTLE_SECONDS = 2.0

EXIT_PASS, EXIT_FAIL, EXIT_ERROR = 0, 1, 2
CLASSES = ("covered", "partial", "uncovered")

# Claude Code session variables that make a child `claude` think it is nested inside this session.
# Auth/provider variables (e.g. CLAUDE_CODE_USE_BEDROCK) are deliberately kept.
_CLAUDE_SESSION_VARS = (
    "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION",
    "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_MESSAGING_SOCKET", "CLAUDE_CODE_MESSAGING_TOKEN",
    "CLAUDE_PID", "CLAUDE_CODE_SSE_PORT",
)

# The agent declares tools [read, search, edit]; these are their Claude Code equivalents.
CLAUDE_ALLOWED_TOOLS = "Read,Grep,Glob,Write,Edit,TodoWrite,Task,Agent"


# --------------------------------------------------------------------------- tool selection


def detect_tool(explicit: str | None = None, env: dict | None = None) -> tuple[str, str]:
    """Return (tool, reason). Order: explicit > COVERAGE_TEST_TOOL > VS Code chat > claude."""
    env = os.environ if env is None else env
    if explicit and explicit != "auto":
        return explicit, "--tool"
    from_env = (env.get("COVERAGE_TEST_TOOL") or "").strip().lower()
    if from_env and from_env != "auto":
        if from_env not in TOOLS:
            raise ValueError(f"COVERAGE_TEST_TOOL must be one of {TOOLS} or auto, got {from_env!r}")
        return from_env, "COVERAGE_TEST_TOOL"
    if env.get("CLAUDECODE") == "1" or env.get("CLAUDE_CODE_ENTRYPOINT"):
        where = env.get("CLAUDE_CODE_ENTRYPOINT") or "claude"
        return "claude", f"started from Claude Code ({where})"
    if env.get("TERM_PROGRAM") == "vscode" or env.get("VSCODE_PID") or env.get("VSCODE_IPC_HOOK_CLI"):
        return "copilot", "started from VS Code (not Claude Code), so GitHub Copilot"
    return "claude", "default"


# --------------------------------------------------------------------------- answer key


@dataclass
class Unit:
    name: str
    pattern: re.Pattern
    methods: list[str]


@dataclass
class Entry:
    id: str
    title: str
    unit: str
    method: str | None
    match: list[re.Pattern]
    exclude: re.Pattern | None
    accept: list[str] = field(default_factory=list)  # gaps only
    category: str = ""
    mapping_fallback: bool = False


@dataclass
class AppKey:
    lang: str
    units: dict[str, Unit]
    source: dict[str, str]
    tests: dict[str, str]
    gaps: list[Entry]
    controls: list[Entry]

    @property
    def app_rel(self) -> str:
        return f"test/{KIND}/{self.lang}"

    @property
    def app_dir(self) -> Path:
        return TEST_DIR / KIND / self.lang

    @property
    def name(self) -> str:
        return f"{KIND}-{self.lang}"


def _entry(d: dict) -> Entry:
    return Entry(id=d["id"], title=d["title"], unit=d["unit"], method=d.get("method"),
                 match=[re.compile(p) for p in d.get("match", [])],
                 exclude=re.compile(d["exclude"]) if d.get("exclude") else None,
                 accept=d.get("accept", []), category=d.get("category", ""),
                 mapping_fallback=bool(d.get("mappingFallback")))


def load_app_key(lang: str, path: Path = ANSWER_KEY) -> AppKey:
    data = json.loads(path.read_text(encoding="utf-8"))
    app = data["apps"][lang]
    units = {n: Unit(n, re.compile(u["pattern"]), u["methods"]) for n, u in app["units"].items()}
    return AppKey(lang, units, app["source"], app["tests"],
                  [_entry(g) for g in data["gaps"]], [_entry(c) for c in data["controls"]])


# --------------------------------------------------------------------------- Markdown table parsing


def norm(text: str) -> str:
    """Lower-case, underscores removed: todo_service / TodoService / todoService all read 'todoservice'."""
    return (text or "").lower().replace("_", "")


def split_cells(line: str) -> list[str]:
    """Split a Markdown table row into cells, ignoring '|' inside `code spans` or escaped as '\\|'."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, in_code, i = [], [], False, 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_BOLD_LINE_RE = re.compile(r"^\*\*(.+?)\*\*[:.]?\s*$")
_SEPARATOR_CELL_RE = re.compile(r"^:?-{2,}:?$")
_NON_CONDITION_HEADER_RE = re.compile(r"note|test|assert|strength|link|evidence|source|location|remediation|reason", re.I)
_PATH_ID_RE = re.compile(r"\bP-\d+", re.I)


@dataclass
class Row:
    headings: list[str]          # outermost first
    header: list[str]
    cells: list[str]
    source: str = ""             # which artifact the row came from

    @property
    def text(self) -> str:
        return " | ".join(self.cells)

    @property
    def condition_text(self) -> str:
        """The row without its test-case, assertion, notes and link columns: what the path *is*, which is what
        the answer key's patterns describe (notes like "no test uses a blank title" would otherwise mislead them)."""
        if len(self.header) != len(self.cells):
            return self.text
        keep = [c for h, c in zip(self.header, self.cells) if not _NON_CONDITION_HEADER_RE.search(h)]
        return " | ".join(keep) if keep else self.text

    @property
    def classification(self) -> str | None:
        for i, h in enumerate(self.header):
            if "classif" in h.lower() and i < len(self.cells):
                return classify(self.cells[i])
        return classify(self.text)


def classify(text: str) -> str | None:
    t = (text or "").lower()
    if "partial" in t:
        return "partial"
    if "uncovered" in t or "not covered" in t:
        return "uncovered"
    if "covered" in t:
        return "covered"
    return None


def parse_tables(text: str, source: str = "") -> list[Row]:
    """Every data row of every Markdown table, with the headings it sits under."""
    headings: dict[int, str] = {}
    rows: list[Row] = []
    header: list[str] | None = None
    for line in (text or "").splitlines():
        s = line.strip()
        m = _HEADING_RE.match(s)
        bold = None if m else _BOLD_LINE_RE.match(s)
        if m or bold:
            level = len(m.group(1)) if m else 7  # a bold-only line acts as the deepest heading
            headings = {k: v for k, v in headings.items() if k < level}
            headings[level] = (m.group(2) if m else bold.group(1)).strip()
            header = None
            continue
        if s.startswith("|"):
            cells = split_cells(s)
            if header is None:
                header = cells
                continue
            if all(_SEPARATOR_CELL_RE.match(c) for c in cells if c):
                continue
            rows.append(Row([headings[k] for k in sorted(headings)], header, cells, source))
        else:
            header = None
    return rows


def _earliest(text: str, candidates: dict[str, re.Pattern]) -> str | None:
    best, best_pos = None, None
    for name, pat in candidates.items():
        m = pat.search(text)
        if m and (best_pos is None or m.start() < best_pos):
            best, best_pos = name, m.start()
    return best


_METHOD_HEADING_RE = re.compile(r"\b(method|function|constructor|property|ctor)\b|\w\(", re.I)
_VS_RE = re.compile(r"\s+(vs\.?|versus|↔|<->)\s+", re.I)


def _unit_heading(row: Row, key: AppKey) -> tuple[int, str | None]:
    """(index of the nearest heading that identifies the row's unit, that unit), or (-1, None).

    A "<source> vs <tests>" heading identifies its unit by the source side only: in
    "errors.py vs tests/test_todo_service.py" the unit is errors.py (not a scored unit), not the service."""
    pats = {n: u.pattern for n, u in key.units.items()}
    for i in range(len(row.headings) - 1, -1, -1):
        h = row.headings[i]
        parts = _VS_RE.split(h, maxsplit=1)
        if len(parts) > 1:
            return i, _earliest(norm(parts[0]), pats)
        u = _earliest(norm(h), pats)
        if u:
            return i, u
    return -1, None


def row_unit(row: Row, key: AppKey) -> str | None:
    """The source unit a row belongs to: the nearest heading that names one, else the row itself."""
    i, unit = _unit_heading(row, key)
    if i >= 0:
        return unit
    return _earliest(norm(row.text), {n: u.pattern for n, u in key.units.items()})


def row_method(row: Row, key: AppKey, unit: str) -> str | None:
    """The method a row belongs to (one of its unit's known methods).

    A heading below the unit heading (e.g. "Method: `TodoService.create_todo`") decides: it names a known method
    or the row belongs to some other method. Without such a heading, the method is read from the row's cells."""
    methods = key.units[unit].methods if unit in key.units else []
    if not methods:
        return None
    pats = {m: re.compile(re.escape(m)) for m in methods}
    i, _ = _unit_heading(row, key)
    deeper = row.headings[i + 1:] if i >= 0 else []
    if deeper:
        return _earliest(norm(deeper[-1]), pats)
    if i >= 0:  # the unit heading may name the method too: "Method: `TodoService.rename_todo`"
        found = _earliest(norm(row.headings[i]), pats)
        if found or _METHOD_HEADING_RE.search(row.headings[i]):
            return found  # a method heading for some other method ("Method: `Repo.__init__`") gives None
    return _earliest(norm(row.condition_text), pats) or _earliest(norm(row.text), pats)


def row_matches(row: Row, entry: Entry, key: AppKey) -> bool:
    unit = row_unit(row, key)
    if unit != entry.unit:
        return False
    if entry.method and row_method(row, key, unit) != entry.method:
        return False
    text = row.condition_text.lower()
    if not all(p.search(text) for p in entry.match):
        return False
    return not (entry.exclude and entry.exclude.search(text))


_NO_TEST_RE = re.compile(r"(no test|unmapped|not mapped|no (unit )?test suite|no matching test|untested)", re.I)


def mapping_says_untested(rows: list[Row], unit: str, key: AppKey) -> Row | None:
    for r in rows:
        if row_unit(r, key) == unit and _NO_TEST_RE.search(r.text):
            return r
    return None


# --------------------------------------------------------------------------- scoring


@dataclass
class RunFiles:
    run_id: str
    manifest: Path | None
    mapping: Path | None
    control_flow: Path | None
    audit: Path | None
    report: Path | None

    def present(self) -> list[Path]:
        return [p for p in (self.manifest, self.mapping, self.control_flow, self.audit, self.report) if p]


def locate_run(run_id: str, transitions: Path = TRANSITIONS_DIR, docs: Path = DOCS_DIR) -> RunFiles:
    def f(p: Path) -> Path | None:
        return p if p.is_file() and p.stat().st_size > 0 else None
    return RunFiles(run_id, f(transitions / f"run-{run_id}.md"), f(transitions / f"01-test-mapping-{run_id}.md"),
                    f(transitions / f"02-control-flow-{run_id}.md"), f(transitions / f"03-assertion-audit-{run_id}.md"),
                    f(docs / f"coverage-review-{run_id}.md"))


def _read(p: Path | None) -> str:
    return p.read_text(encoding="utf-8-sig", errors="replace") if p else ""


def _brief(r: Row) -> dict:
    text = r.text if len(r.text) <= 220 else r.text[:217] + "..."
    return {"section": (r.headings[-1] if r.headings else ""), "row": text,
            "classification": r.classification, "source": r.source}


@dataclass
class Score:
    gaps: list[dict] = field(default_factory=list)      # {id, title, status, classifications, rows}
    controls: list[dict] = field(default_factory=list)  # {id, title, status, classifications, rows}
    unscored_problems: list[dict] = field(default_factory=list)
    total: int = 0
    min_found_pct: float = 90.0
    metrics: dict = field(default_factory=dict)

    @property
    def found(self) -> list[dict]:
        return [g for g in self.gaps if g["status"] == "found"]

    @property
    def missed(self) -> list[dict]:
        return [g for g in self.gaps if g["status"] != "found"]

    @property
    def false_positives(self) -> list[dict]:
        return [c for c in self.controls if c["status"] == "false-positive"]

    @property
    def found_pct(self) -> float:
        return 100.0 * len(self.found) / self.total if self.total else 100.0

    @property
    def required(self) -> int:
        return math.ceil(self.total * self.min_found_pct / 100.0 - 1e-9)

    @property
    def coverage_ok(self) -> bool:
        return len(self.found) >= self.required

    @property
    def passed(self) -> bool:
        return self.coverage_ok and not self.false_positives


def _match_rows(rows: list[Row], entry: Entry, key: AppKey) -> list[Row]:
    return [r for r in rows if r.classification and row_matches(r, entry, key)]


def score_run(audit_rows: list[Row], key: AppKey, min_found_pct: float, mapping_rows: list[Row] | None = None,
              report_rows: list[Row] | None = None) -> Score:
    s = Score(total=len(key.gaps), min_found_pct=min_found_pct)
    mapping_rows = mapping_rows or []
    report_rows = report_rows or []
    matched_ids: set[int] = set()

    for g in key.gaps:
        rows = _match_rows(audit_rows, g, key)
        if not rows:  # not located in the stage-3 audit: fall back to the final report's tables
            rows = _match_rows(report_rows, g, key)
        matched_ids.update(id(r) for r in rows)
        hits = [r for r in rows if r.classification in g.accept]
        status = "found" if hits else ("misclassified" if rows else "not located")
        evidence = hits or rows
        if not hits and g.mapping_fallback:
            m = mapping_says_untested(mapping_rows, g.unit, key)
            if m:
                status, evidence = "found", [m]
        s.gaps.append({"id": g.id, "title": g.title, "category": g.category, "status": status,
                       "expected": g.accept, "classifications": sorted({r.classification for r in rows}),
                       "rows": [_brief(r) for r in evidence[:3]]})

    for c in key.controls:
        rows = _match_rows(audit_rows, c, key) or _match_rows(report_rows, c, key)
        matched_ids.update(id(r) for r in rows)
        classes = {r.classification for r in rows}
        if not rows:
            status = "not located"
        elif "covered" in classes:
            status = "confirmed"
        elif "uncovered" in classes:
            status = "false-positive"
        else:
            status = "disputed"  # only Partially Covered
        s.controls.append({"id": c.id, "title": c.title, "status": status, "classifications": sorted(classes),
                           "rows": [_brief(r) for r in rows[:3]]})

    for r in audit_rows:
        if (r.classification in ("partial", "uncovered") and id(r) not in matched_ids
                and _PATH_ID_RE.search(r.text)):  # skip tally rows
            s.unscored_problems.append(_brief(r))
    return s


_METRIC_PATTERNS = {
    "totalPaths": r"total logical paths[^|\n]*\|\s*\**\s*([\d,]+)",
    "totalProblems": r"total problems[^|\n]*\|\s*\**\s*([\d,]+)",
    "problemPct": r"problem percentage[^|\n]*\|\s*\**\s*([\d.,]+)\s*%",
    "severity": r"critical\s*/\s*high\s*/\s*medium\s*/\s*low[^|\n]*\|\s*\**\s*([\d\s/]+)",
}


def report_metrics(report_text: str) -> dict:
    out = {}
    for k, pat in _METRIC_PATTERNS.items():
        m = re.search(pat, report_text or "", re.I)
        if m:
            v = m.group(1).strip()
            out[k] = " / ".join(x.strip() for x in v.split("/")) if k == "severity" else v.replace(",", "")
    return out


def manifest_targets_app(manifest_text: str, key: AppKey) -> bool:
    t = (manifest_text or "").replace("\\", "/").lower()
    return key.app_rel.lower() in t or str(key.app_dir).replace("\\", "/").lower() in t


# --------------------------------------------------------------------------- build


def find_build_output(app_dir: Path) -> list[Path]:
    found = sorted({p for d in BUILD_OUTPUT_DIRS for p in app_dir.rglob(d) if p.is_dir()}, key=lambda p: len(p.parts))
    outer: list[Path] = []
    for p in found:
        if not any(o in p.parents for o in outer):
            outer.append(p)
    return outer


def clean_build_output(app_dir: Path) -> list[str]:
    removed = []
    for p in find_build_output(app_dir):
        shutil.rmtree(p, ignore_errors=True)
        if not p.exists():
            removed.append(p.relative_to(app_dir).as_posix())
    return removed


def redirected_output_dir(project_dir: Path) -> Path | None:
    try:
        return MSBUILD_OUTPUT_ROOT / project_dir.resolve().relative_to(TEST_DIR)
    except ValueError:
        return None


def build_steps(key: AppKey) -> list[list[str]]:
    """Commands that build the app and run its unit tests, from the app (copy) directory."""
    if key.lang == "dotNET":
        return [["dotnet", "test", "--nologo", "-v", "q"]]
    if key.lang == "java":
        return [["mvn", "-B", "-q", "clean", "verify"]]
    return [[sys.executable, "-m", "compileall", "-q", "."],
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"]]


def _build_env() -> dict:
    env = dict(os.environ)
    if os.name == "nt" and "trustStoreType" not in env.get("MAVEN_OPTS", ""):
        env["MAVEN_OPTS"] = (env.get("MAVEN_OPTS", "") + " -Djavax.net.ssl.trustStoreType=Windows-ROOT").strip()
    return env


def fresh_build(key: AppKey, log_file: Path, timeout_min: float, work_dir: Path) -> tuple[str | None, dict]:
    """Delete old build output in the app, then build and unit-test a copy of it in work_dir (deleted afterwards)."""
    info: dict = {"removedBefore": clean_build_output(key.app_dir), "commands": [], "log": str(log_file)}
    started = time.time()
    log, error = [], None
    if work_dir.exists():
        shutil.rmtree(work_dir)
    shutil.copytree(key.app_dir, work_dir, ignore=shutil.ignore_patterns(*BUILD_OUTPUT_DIRS))
    for step in build_steps(key):
        exe = shutil.which(step[0])
        if not exe:
            error = (f"'{step[0]}' not found on PATH, so {key.app_rel} can't be built and tested "
                     "(see the prerequisites in test/README.md, or pass --no-build).")
            break
        info["commands"].append(subprocess.list2cmdline(step))
        try:
            proc = subprocess.run([exe] + step[1:], cwd=work_dir, env=_build_env(), capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL,
                                  timeout=timeout_min * 60)
            rc, out, err = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as e:
            rc, out, err = None, e.stdout or "", f"timed out after {timeout_min} min"
        log.append(f"$ {subprocess.list2cmdline(step)}\n# exit code: {rc}\n\n## stdout\n{out}\n\n## stderr\n{err}\n")
        if rc != 0:
            error = f"build or unit tests failed ({subprocess.list2cmdline(step)}, exit code {rc}); see {log_file}"
            break
    info["durationSeconds"] = round(time.time() - started, 1)
    shutil.rmtree(work_dir, ignore_errors=True)
    redirected = redirected_output_dir(work_dir)
    if redirected:
        shutil.rmtree(redirected, ignore_errors=True)
        for parent in redirected.parents:
            if parent == MSBUILD_OUTPUT_ROOT or MSBUILD_OUTPUT_ROOT not in parent.parents:
                break
            try:
                parent.rmdir()
            except OSError:
                break
    try:
        work_dir.parent.rmdir()
    except OSError:
        pass
    log_file.write_text("\n".join(log) or "(no build command ran)\n", encoding="utf-8")
    info["status"] = "failed" if error else "succeeded"
    return error, info


def preflight(key: AppKey, attempts: int = PREFLIGHT_ATTEMPTS, settle_seconds: float = PREFLIGHT_SETTLE_SECONDS) -> str | None:
    """Make sure the app holds no build output just before the review starts (IDE tooling can recreate it)."""
    if not key.app_dir.is_dir():
        return f"app directory not found: {key.app_dir}"
    present: list[str] = []
    for attempt in range(max(1, attempts)):
        present = [p.relative_to(key.app_dir).as_posix() for p in find_build_output(key.app_dir)]
        if not present:
            if attempt == 0:
                return None
            time.sleep(settle_seconds)
            if not find_build_output(key.app_dir):
                return None
            continue
        print(f"{key.name}: build output reappeared ({', '.join(present)}); deleting it "
              f"(attempt {attempt + 1}/{attempts}) ...", flush=True)
        clean_build_output(key.app_dir)
        time.sleep(settle_seconds)
    present = [p.relative_to(key.app_dir).as_posix() for p in find_build_output(key.app_dir)] or present
    return f"build output kept reappearing in {key.app_rel} after {attempts} clean-ups: " + ", ".join(present) + "."


# --------------------------------------------------------------------------- invocation

_RUN_ID_LOCK = threading.Lock()
_LAST_RUN_ID: list[dt.datetime] = []


def new_run_id(transitions: Path = TRANSITIONS_DIR) -> str:
    """A fresh YYYYMMDD-HHmmss Run ID, unique within this process and unused in transitions/."""
    with _RUN_ID_LOCK:
        t = dt.datetime.now().replace(microsecond=0)
        if _LAST_RUN_ID and t <= _LAST_RUN_ID[0]:
            t = _LAST_RUN_ID[0] + dt.timedelta(seconds=1)
        while (transitions / f"run-{t:%Y%m%d-%H%M%S}.md").exists():
            t += dt.timedelta(seconds=1)
        _LAST_RUN_ID[:] = [t]
        return f"{t:%Y%m%d-%H%M%S}"


def review_request(key: AppKey, run_id: str) -> str:
    """The task given to the agent. Identical for both tools."""
    return (
        f"Review the unit test coverage of the workspace subfolder `{key.app_rel}` (the scope is that folder only: "
        "its source files and its unit test files). "
        "This is a headless, non-interactive run: do not ask questions; where something is ambiguous, make a "
        "reasonable assumption and note it in the report. Ignore the model-selection instructions. "
        f"Start a fresh review and use Run ID `{run_id}` (use exactly this value instead of reading the clock). "
        "Complete all four stages and persist every artifact: "
        f"`transitions/run-{run_id}.md`, `transitions/01-test-mapping-{run_id}.md`, "
        f"`transitions/02-control-flow-{run_id}.md`, `transitions/03-assertion-audit-{run_id}.md` and "
        f"`docs/coverage-review-{run_id}.md`. "
        "In the stage-3 audit tables, give every logical path its own row (do not merge or abbreviate paths) and "
        "name the method each path belongs to, either in the row or in the table's heading."
    )


def build_command(tool: str, key: AppKey, run_id: str, model: str | None, extra: list[str]) -> list[str]:
    request = review_request(key, run_id)
    if tool == "claude":
        exe = shutil.which("claude") or "claude"
        prompt = (
            f"Act as the agent defined in `.github/agents/{AGENT_NAME}.agent.md`: read that file and follow its "
            "constraints and workflow exactly. Its four skills are at `.github/skills/<skill-name>/SKILL.md`; read "
            "each skill file before you run its stage and follow it. " + request)
        cmd = [exe, "-p", prompt, "--output-format", "json", "--allowedTools", CLAUDE_ALLOWED_TOOLS]
    else:
        exe = shutil.which("copilot") or "copilot"
        cmd = [exe, "-p", request, "--agent", AGENT_NAME, "--add-dir", str(REPO_ROOT), "--trust-folder",
               "--allow-all-tools", "--no-ask-user"]
    if model:
        cmd += ["--model", model]
    return cmd + list(extra)


def _child_env(tool: str) -> dict:
    env = dict(os.environ)
    if tool == "claude":
        for v in _CLAUDE_SESSION_VARS:
            env.pop(v, None)
    return env


@dataclass
class Invocation:
    status: str                  # completed | incomplete | error
    run_id: str
    files: RunFiles | None = None
    error: str | None = None
    duration_s: float = 0.0
    cost_usd: float | None = None
    exit_code: int | None = None
    command: list[str] = field(default_factory=list)


_POLL_SECONDS = 5
_STAGES = (("manifest", "run manifest written"), ("mapping", "stage 1 (test mapping) done"),
           ("control_flow", "stage 2 (control flow) done"), ("audit", "stage 3 (assertion audit) done"),
           ("report", "stage 4 (report) done"))


def _fmt_elapsed(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m{s:02d}s" if h else f"{m}m{s:02d}s"


class ProgressReporter:
    """Prints a line when a stage artifact of the run appears, plus a heartbeat every `interval` seconds."""

    def __init__(self, key: AppKey, run_id: str, started: float, interval: float):
        self.key, self.run_id, self.started, self.interval = key, run_id, started, interval
        self.seen: set[str] = set()
        self.last_print = started

    def _say(self, msg: str) -> None:
        print(f"  {self.key.name} [{_fmt_elapsed(time.time() - self.started)}] {msg}", flush=True)
        self.last_print = time.time()

    def poll(self) -> None:
        if self.interval <= 0:
            return
        files = locate_run(self.run_id)
        for attr, label in _STAGES:
            if attr not in self.seen and getattr(files, attr):
                self.seen.add(attr)
                self._say(label)
        if time.time() - self.last_print >= self.interval:
            done = sum(1 for a, _ in _STAGES[1:] if a in self.seen)
            self._say(f"still running: {done}/4 stages done")


def invoke(tool: str, key: AppKey, run_id: str, log_file: Path, timeout_min: float, model: str | None,
           extra: list[str], progress_interval: float = 30) -> Invocation:
    cmd = build_command(tool, key, run_id, model, extra)
    inv = Invocation(status="error", run_id=run_id, command=cmd)
    if not shutil.which(cmd[0]):
        inv.error = (f"'{tool}' CLI not found on PATH. "
                     + ("Install Claude Code (https://claude.com/claude-code)." if tool == "claude"
                        else "Install GitHub Copilot CLI (npm install -g @github/copilot) and sign in."))
        return inv
    started = time.time()
    deadline = started + timeout_min * 60
    reporter = ProgressReporter(key, run_id, started, progress_interval)
    proc = subprocess.Popen(cmd, cwd=REPO_ROOT, env=_child_env(tool), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    while True:
        try:
            stdout, stderr = proc.communicate(timeout=max(0.1, min(_POLL_SECONDS, deadline - time.time())))
            rc = proc.returncode
            break
        except subprocess.TimeoutExpired:
            if time.time() >= deadline:
                proc.kill()
                stdout, _ = proc.communicate()
                stderr, rc = f"timed out after {timeout_min} min", None
                break
            reporter.poll()
    reporter.poll()
    inv.duration_s = time.time() - started
    inv.exit_code = rc
    if progress_interval > 0:
        print(f"  {key.name} [{_fmt_elapsed(inv.duration_s)}] {tool} finished (exit code {rc}); scoring ...", flush=True)
    log_file.write_text(f"$ {subprocess.list2cmdline(cmd)}\n# exit code: {rc}\n\n## stdout\n{stdout}\n\n"
                        f"## stderr\n{stderr}\n", encoding="utf-8")
    if tool == "claude":
        try:
            inv.cost_usd = json.loads(stdout).get("total_cost_usd")
        except (json.JSONDecodeError, AttributeError):
            pass
    inv.files = locate_run(run_id)
    if inv.files.audit:
        inv.status = "completed" if inv.files.report else "incomplete"
        if not inv.files.report:
            inv.error = f"no final report docs/coverage-review-{run_id}.md (stage 4 did not finish); scored stage 3 only"
    else:
        have = ", ".join(p.name for p in inv.files.present()) or "none"
        inv.error = (f"the run produced no stage-3 audit transitions/03-assertion-audit-{run_id}.md "
                     f"({tool} exit code {rc}; artifacts found: {have}); see {log_file}"
                     + (f"; stderr: {stderr.strip()[:300]}" if (stderr or "").strip() else ""))
    return inv


# --------------------------------------------------------------------------- reporting

_STATUS_LABEL = {"found": "found", "misclassified": "**missed** (classified Covered)",
                 "not located": "**missed** (no matching row)", "confirmed": "confirmed Covered",
                 "false-positive": "**FALSE POSITIVE** (Uncovered)", "disputed": "disputed (Partially Covered)"}


def _cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ")


def render_markdown(r: dict) -> str:
    s = r.get("score") or {}
    lines = [f"# {r['app']} — {r['verdict'].upper()}", ""]
    lines += [f"- Tool: {r['tool']} ({r['toolReason']})",
              f"- Run ID: `{r.get('runId')}`" + (f" — report: {r['reportFile']}" if r.get("reportFile") else ""),
              f"- Duration: {r.get('durationSeconds', 0):.0f} s" + (f", cost ${r['costUsd']:.2f}" if r.get("costUsd") else "")]
    if r.get("build"):
        b = r["build"]
        lines.append(f"- Fresh build and unit-test run: {b['status']}"
                     + (f" ({'; '.join(b['commands'])}, {b['durationSeconds']:.0f} s)" if b.get("commands") else "")
                     + (f"; old build output deleted: {', '.join(b['removedBefore'])}" if b.get("removedBefore") else ""))
    if r.get("metrics"):
        m = r["metrics"]
        lines.append("- Reviewer metrics: " + ", ".join(f"{k} {v}" for k, v in m.items()))
    if r.get("warning"):
        lines += [f"- Warning: {r['warning']}"]
    if r.get("error"):
        lines += ["", f"**Error:** {r['error']}"]
    if s:
        lines += [f"- Gaps found: {len(s['found'])}/{s['total']} ({s['foundPct']:.0f}%; "
                  f"need {s['required']} for {s['minFoundPct']:g}%)",
                  f"- Control paths classified Uncovered (false positives): {len(s['falsePositives'])}", ""]
        lines += ["## Seeded gaps", "", "| Gap | Category | Result | Classified as | Matching row |", "|---|---|---|---|---|"]
        for g in s["gaps"]:
            row = g["rows"][0]["row"] if g["rows"] else "—"
            lines.append(f"| {g['id']} {_cell(g['title'])} | {g['category']} | {_STATUS_LABEL[g['status']]} | "
                         f"{', '.join(g['classifications']) or '—'} | {_cell(row)} |")
        lines += ["", "## Control paths (should be Covered)", "", "| Control | Result | Classified as | Matching row |",
                  "|---|---|---|---|"]
        for c in s["controls"]:
            row = c["rows"][0]["row"] if c["rows"] else "—"
            lines.append(f"| {c['id']} {_cell(c['title'])} | {_STATUS_LABEL[c['status']]} | "
                         f"{', '.join(c['classifications']) or '—'} | {_cell(row)} |")
        up = s["unscoredProblems"]
        lines += ["", f"## Other problems reported (not scored): {len(up)}", ""]
        if up:
            lines += ["| Section | Classification | Row |", "|---|---|---|"]
            lines += [f"| {_cell(u['section'])} | {u['classification']} | {_cell(u['row'])} |" for u in up[:60]]
            if len(up) > 60:
                lines.append(f"| … | | {len(up) - 60} more in the JSON result |")
    return "\n".join(lines) + "\n"


def summarize(r: dict) -> str:
    s = r.get("score")
    if not s:
        return f"[{r['verdict'].upper()}] {r['app']} ({r['tool']}): {r.get('error')}"
    miss = ", ".join(g["id"] for g in s["gaps"] if g["status"] != "found") or "none"
    fps = ", ".join(c["id"] for c in s["falsePositives"]) or "none"
    return (f"[{r['verdict'].upper()}] {r['app']} ({r['tool']}): {len(s['found'])}/{s['total']} gaps "
            f"({s['foundPct']:.0f}%, need {s['minFoundPct']:g}%), missed: {miss}; false positives: {fps}; "
            f"other problems reported: {len(s['unscoredProblems'])}")


# --------------------------------------------------------------------------- entry point


def add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--tool", choices=("auto",) + TOOLS, default="auto",
                   help="AI tool to run the reviewer with (default: auto; env COVERAGE_TEST_TOOL).")
    p.add_argument("--min-found", type=float, default=float(os.environ.get("COVERAGE_TEST_MIN_FOUND", 90)),
                   metavar="PCT", help="Percent of seeded gaps that must be found (default 90; env COVERAGE_TEST_MIN_FOUND).")
    p.add_argument("--timeout", type=float, default=float(os.environ.get("COVERAGE_TEST_TIMEOUT_MIN", 60)),
                   metavar="MIN", help="Per-review timeout in minutes (default 60; env COVERAGE_TEST_TIMEOUT_MIN).")
    p.add_argument("--progress", type=float, default=float(os.environ.get("COVERAGE_TEST_PROGRESS_SEC", 30)),
                   metavar="SEC", help="Print each finished stage and a heartbeat every SEC seconds (default 30; 0 = quiet).")
    p.add_argument("--model", help="Model passed to the AI tool's --model option.")
    p.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR, help="Where results are written.")
    p.add_argument("--no-build", action="store_true",
                   help="Skip the fresh build and unit-test run. Old build output is still deleted.")
    p.add_argument("--build-timeout", type=float, default=float(os.environ.get("COVERAGE_TEST_BUILD_TIMEOUT_MIN", 15)),
                   metavar="MIN", help="Time limit for each build command, in minutes (default 15).")
    p.add_argument("--dry-run", action="store_true", help="Print the commands that would run and exit.")
    p.add_argument("--tool-arg", action="append", default=[], metavar="ARG",
                   help="Extra argument for the AI tool CLI (repeatable), e.g. --tool-arg=--max-budget-usd --tool-arg=5")


_RUN_ID_RE = re.compile(r"(\d{8}-\d{6})")


def resolve_score_only(arg: str) -> RunFiles:
    """--score-only takes a Run ID, or the path of any artifact of the run (its folder is then used)."""
    p = Path(arg)
    m = _RUN_ID_RE.search(p.name if p.suffix else arg)
    if not m:
        raise SystemExit(f"--score-only: no Run ID (YYYYMMDD-HHmmss) in {arg!r}")
    run_id = m.group(1)
    if p.suffix and p.exists():
        transitions = p.resolve().parent
        docs = transitions.parent / "docs"
        if p.name.startswith("coverage-review-"):
            docs, transitions = transitions, transitions.parent / "transitions"
        return locate_run(run_id, transitions, docs if docs.is_dir() else DOCS_DIR)
    return locate_run(run_id)


def _copy_artifacts(files: RunFiles, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for p in files.present():
        shutil.copy2(p, dest / p.name)


def run_test(lang: str, args: argparse.Namespace, session_dir: Path | None = None) -> dict:
    key = load_app_key(lang)
    if not 0 <= args.min_found <= 100:
        raise SystemExit("--min-found must be between 0 and 100")
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    score_only = getattr(args, "score_only", None)
    tool, reason = ("n/a", "--score-only") if score_only else detect_tool(args.tool)
    out_dir = (session_dir or (args.results_dir / f"{stamp}-{'score-only' if score_only else tool}")).resolve()
    result = {"app": key.name, "target": key.app_rel, "tool": tool, "toolReason": reason,
              "minFoundPct": args.min_found, "startedAt": dt.datetime.now().isoformat(timespec="seconds")}

    if args.dry_run:
        run_id = "<runId>"
        print(f"{key.name}: delete build output ({', '.join(BUILD_OUTPUT_DIRS)}) in {key.app_dir}")
        if not args.no_build:
            print(f"{key.name}: build and unit-test a copy of the app in {out_dir / 'build' / key.name}")
            for step in build_steps(key):
                print("  " + subprocess.list2cmdline(step))
        cmd = build_command(tool, key, run_id, args.model, args.tool_arg)
        print(f"{key.name}: tool={tool} ({reason})\n  cwd: {REPO_ROOT}\n  " + subprocess.list2cmdline(cmd))
        return {**result, "verdict": "dry-run"}

    out_dir.mkdir(parents=True, exist_ok=True)
    if score_only:
        files = resolve_score_only(score_only)
        inv = Invocation(status="completed" if files.audit else "error", run_id=files.run_id, files=files,
                         error=None if files.audit else f"no 03-assertion-audit-{files.run_id}.md found for {score_only}")
    else:
        problem = None
        if not key.app_dir.is_dir():
            problem = f"app directory not found: {key.app_dir}"
        elif args.no_build:
            result["build"] = {"status": "skipped (--no-build)", "removedBefore": clean_build_output(key.app_dir)}
        else:
            print(f"{key.name}: deleting old build output, then building and unit-testing {key.app_rel} ...", flush=True)
            problem, result["build"] = fresh_build(key, out_dir / f"{key.name}-build.log", args.build_timeout,
                                                   out_dir / "build" / key.name)
            if not problem:
                print(f"{key.name}: build and unit tests passed in {result['build']['durationSeconds']:.0f} s", flush=True)
        problem = problem or preflight(key)
        if problem:
            result.update(verdict="error", error=problem)
            return _finish(result, out_dir, key)
        if not AGENT_FILE.is_file():
            result.update(verdict="error", error=f"agent definition not found: {AGENT_FILE}")
            return _finish(result, out_dir, key)
        run_id = new_run_id()
        print(f"{key.name}: running the reviewer with {tool} ({reason}), Run ID {run_id} ...", flush=True)
        inv = invoke(tool, key, run_id, out_dir / f"{key.name}-{tool}.log", args.timeout, args.model,
                     args.tool_arg, args.progress)

    files = inv.files
    result.update(runId=inv.run_id, durationSeconds=round(inv.duration_s, 1), costUsd=inv.cost_usd,
                  command=inv.command, reportFile=str(files.report) if files and files.report else None,
                  artifacts=[str(p) for p in files.present()] if files else [])
    if files and files.present():
        _copy_artifacts(files, out_dir / f"{key.name}-artifacts")
    if inv.status == "error" or not files or not files.audit:
        result.update(verdict="error", error=inv.error or "review did not complete")
        return _finish(result, out_dir, key)
    if inv.error:
        result["warning"] = inv.error

    manifest_text = _read(files.manifest)
    if manifest_text and not manifest_targets_app(manifest_text, key):
        result.update(verdict="error", error=f"run {inv.run_id} does not name {key.app_rel} as its target root")
        return _finish(result, out_dir, key)

    report_text = _read(files.report)
    s = score_run(parse_tables(_read(files.audit), "03-assertion-audit"), key, args.min_found,
                  mapping_rows=parse_tables(_read(files.mapping), "01-test-mapping"),
                  report_rows=parse_tables(report_text, "coverage-review"))
    result["metrics"] = report_metrics(report_text)
    result["score"] = {"total": s.total, "found": s.found, "foundPct": round(s.found_pct, 1), "required": s.required,
                       "minFoundPct": args.min_found, "coverageOk": s.coverage_ok, "gaps": s.gaps,
                       "controls": s.controls, "falsePositives": s.false_positives,
                       "unscoredProblems": s.unscored_problems}
    result["verdict"] = "pass" if s.passed else "fail"
    return _finish(result, out_dir, key)


def _finish(result: dict, out_dir: Path, key: AppKey) -> dict:
    result["finishedAt"] = dt.datetime.now().isoformat(timespec="seconds")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{key.name}-result.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (out_dir / f"{key.name}-result.md").write_text(render_markdown(result), encoding="utf-8")
    result["resultFile"] = str(out_dir / f"{key.name}-result.md")
    return result


def exit_code(verdicts: list[str]) -> int:
    if any(v == "error" for v in verdicts):
        return EXIT_ERROR
    if any(v == "fail" for v in verdicts):
        return EXIT_FAIL
    return EXIT_PASS


def main(lang: str, argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=f"Validate the Unit Test Coverage Reviewer against test/{KIND}/{lang}.")
    add_common_args(p)
    p.add_argument("--score-only", metavar="RUN",
                   help="Skip the review; score an existing run, given its Run ID or the path of one of its artifacts.")
    args = p.parse_args(argv)
    r = run_test(lang, args)
    if r["verdict"] == "dry-run":
        return EXIT_PASS
    print(render_markdown(r))
    print(summarize(r))
    print(f"Result: {r['resultFile']}")
    return exit_code([r["verdict"]])
