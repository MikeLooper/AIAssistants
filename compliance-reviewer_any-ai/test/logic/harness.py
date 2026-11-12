"""Shared harness for the Compliance Reviewer validation tests (Python 3.10+, stdlib only).

Each test script (test_api_dotnet.py, ...) calls ``main(kind, lang)``. The harness:

1. resolves the AI tool (``--tool``, ``COMPLIANCE_TEST_TOOL``, the VS Code chat that started it, or Claude),
2. runs the reviewer headlessly against one app in programmatic mode,
3. scores the run's transition files against ``answer_key.json`` (the data form of test/README.md),
4. writes a JSON and Markdown result and exits 0 (pass), 1 (fail) or 2 (error: the review never produced a scorable run).

Pass rule: the run completed, at least ``--min-found`` percent of the seeded flaws were found, and
no *unexpected* finding has severity Error. Misses and unexpected Warning/Information findings are
only reported.
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
import time
from dataclasses import dataclass, field
from pathlib import Path

LOGIC_DIR = Path(__file__).resolve().parent
TEST_DIR = LOGIC_DIR.parent
REPO_ROOT = TEST_DIR.parent  # compliance-reviewer_any-ai: the reviewer's workspace
ANSWER_KEY = LOGIC_DIR / "answer_key.json"
DEFAULT_RESULTS_DIR = LOGIC_DIR / "results"
TRANSITIONS_DIR = REPO_ROOT / "transitions"

TOOLS = ("claude", "copilot")
LANGS = ("dotNET", "java", "python")
KINDS = ("apis", "uis")
BUILD_OUTPUT_DIRS = ("bin", "obj", "target", "__pycache__", ".venv")

EXIT_PASS, EXIT_FAIL, EXIT_ERROR = 0, 1, 2

# Claude Code session variables that make a child `claude` think it is nested inside this session.
# Auth/provider variables (e.g. CLAUDE_CODE_USE_BEDROCK) are deliberately kept.
_CLAUDE_SESSION_VARS = (
    "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION",
    "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_MESSAGING_SOCKET", "CLAUDE_CODE_MESSAGING_TOKEN",
    "CLAUDE_PID", "CLAUDE_CODE_SSE_PORT",
)

CLAUDE_ALLOWED_TOOLS = (
    "Read,Grep,Glob,Write,Edit,Agent,Task,Skill,TodoWrite,"
    "Bash(git -C:*),"
    "Bash(python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py:*)"
)


# --------------------------------------------------------------------------- tool selection


def detect_tool(explicit: str | None = None, env: dict | None = None) -> tuple[str, str]:
    """Return (tool, reason). Order: explicit > COMPLIANCE_TEST_TOOL > VS Code chat > claude."""
    env = os.environ if env is None else env
    if explicit and explicit != "auto":
        return explicit, "--tool"
    from_env = (env.get("COMPLIANCE_TEST_TOOL") or "").strip().lower()
    if from_env and from_env != "auto":
        if from_env not in TOOLS:
            raise ValueError(f"COMPLIANCE_TEST_TOOL must be one of {TOOLS} or auto, got {from_env!r}")
        return from_env, "COMPLIANCE_TEST_TOOL"
    # Started from the Claude Code chat (VS Code extension or CLI): it sets CLAUDECODE=1.
    if env.get("CLAUDECODE") == "1" or env.get("CLAUDE_CODE_ENTRYPOINT"):
        where = env.get("CLAUDE_CODE_ENTRYPOINT") or "claude"
        return "claude", f"started from Claude Code ({where})"
    # Otherwise, inside VS Code the chat window is GitHub Copilot Chat (agent mode runs commands in
    # the integrated terminal, which sets TERM_PROGRAM=vscode).
    if env.get("TERM_PROGRAM") == "vscode" or env.get("VSCODE_PID") or env.get("VSCODE_IPC_HOOK_CLI"):
        return "copilot", "started from VS Code (not Claude Code), so GitHub Copilot"
    return "claude", "default"


# --------------------------------------------------------------------------- answer key


@dataclass
class Flaw:
    id: str
    title: str
    checks: list[str]
    locations: list[str]  # relative to the app dir; empty = whole app


@dataclass
class AppKey:
    kind: str
    lang: str
    flaws: list[Flaw]
    incidental: list[str]

    @property
    def app_rel(self) -> str:
        return f"test/{self.kind}/{self.lang}"

    @property
    def app_dir(self) -> Path:
        return TEST_DIR / self.kind / self.lang

    @property
    def name(self) -> str:
        return f"{self.kind}-{self.lang}"


def load_app_key(kind: str, lang: str, path: Path = ANSWER_KEY) -> AppKey:
    data = json.loads(path.read_text(encoding="utf-8"))["kinds"][kind]
    flaws = [Flaw(f["id"], f["title"], f["checks"], f["locations"][lang]) for f in data["flaws"]]
    return AppKey(kind, lang, flaws, data["incidentalChecks"])


def check_matches(check_id: str, patterns: list[str]) -> bool:
    cid = (check_id or "").strip().upper()
    for p in patterns:
        p = p.upper()
        if (p.endswith("*") and cid.startswith(p[:-1])) or cid == p:
            return True
    return False


def _norm(path: str) -> str:
    p = (path or "").replace("\\", "/").strip().lower()
    while p.startswith("./"):
        p = p[2:]
    return p


def location_matches(evidence: list[dict], locations: list[str]) -> bool:
    if not locations:
        return True
    for ev in evidence or []:
        f = _norm(ev.get("file", ""))
        for loc in locations:
            loc = _norm(loc)
            if f == loc or f.endswith("/" + loc):
                return True
    return False


# --------------------------------------------------------------------------- scoring


_SUBJECT_FILE_RE = re.compile(r"^\d{2}-review-.+\.json$")


def load_run(run_dir: Path) -> dict:
    """Read a run's raw per-subject findings (before dedup) and its aggregate (after dedup)."""
    raw: list[dict] = []
    for f in sorted(run_dir.iterdir()):
        if f.is_file() and _SUBJECT_FILE_RE.match(f.name):
            data = json.loads(f.read_text(encoding="utf-8-sig"))
            for finding in data.get("findings") or []:
                finding = dict(finding)
                finding["_skill"] = data.get("skill")
                raw.append(finding)
    agg_file = run_dir / "90-aggregate.json"
    aggregate = json.loads(agg_file.read_text(encoding="utf-8-sig")) if agg_file.exists() else None
    state_file = run_dir / "state.json"
    state = json.loads(state_file.read_text(encoding="utf-8-sig")) if state_file.exists() else {}
    return {"raw": raw, "aggregate": aggregate, "state": state}


@dataclass
class Score:
    found: list[dict] = field(default_factory=list)   # {flaw, title, findingIds}
    missed: list[dict] = field(default_factory=list)  # {flaw, title, checks, locations}
    unexpected_errors: list[dict] = field(default_factory=list)
    unexpected_other: list[dict] = field(default_factory=list)
    related: list[dict] = field(default_factory=list)      # expected check, other location
    incidental: list[dict] = field(default_factory=list)
    total: int = 0
    min_found_pct: float = 90.0

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
        return self.coverage_ok and not self.unexpected_errors


def _brief(f: dict) -> dict:
    ev = (f.get("evidence") or [{}])[0]
    loc = ev.get("file", "")
    if ev.get("lineStart"):
        loc += f":{ev['lineStart']}"
    return {"id": f.get("id"), "checkId": f.get("checkId"), "severity": f.get("severity"),
            "title": f.get("title"), "location": loc}


def score_run(run: dict, key: AppKey, min_found_pct: float) -> Score:
    s = Score(total=len(key.flaws), min_found_pct=min_found_pct)

    # 1. Flaw coverage, against the raw per-subject findings so cross-subject dedup can't hide a hit.
    for flaw in key.flaws:
        hits = [f for f in run["raw"]
                if check_matches(f.get("checkId"), flaw.checks) and location_matches(f.get("evidence"), flaw.locations)]
        if hits:
            s.found.append({"flaw": flaw.id, "title": flaw.title,
                            "findingIds": sorted({h.get("id") for h in hits if h.get("id")})})
        else:
            s.missed.append({"flaw": flaw.id, "title": flaw.title, "checks": flaw.checks,
                             "locations": flaw.locations or ["(whole app)"]})

    # 2. Classify the deduplicated findings (each reported issue counted once).
    findings = (run["aggregate"] or {}).get("findings") or run["raw"]
    for f in findings:
        cid, ev = f.get("checkId"), f.get("evidence")
        if any(check_matches(cid, fl.checks) and location_matches(ev, fl.locations) for fl in key.flaws):
            continue  # a seeded flaw
        if check_matches(cid, key.incidental):
            s.incidental.append(_brief(f))
        elif any(check_matches(cid, fl.checks) for fl in key.flaws):
            s.related.append(_brief(f))
        elif (f.get("severity") or "").lower() == "error":
            s.unexpected_errors.append(_brief(f))
        else:
            s.unexpected_other.append(_brief(f))
    return s


# --------------------------------------------------------------------------- invocation


@dataclass
class Invocation:
    status: str                 # completed | failed | error
    run_id: str | None = None
    run_dir: Path | None = None
    report_file: str | None = None
    overall_score: float | None = None
    overall_band: str | None = None
    error: str | None = None
    duration_s: float = 0.0
    cost_usd: float | None = None
    command: list[str] = field(default_factory=list)


def preflight(key: AppKey, allow_build_output: bool) -> str | None:
    if not key.app_dir.is_dir():
        return f"app directory not found: {key.app_dir}"
    present = [str(p.relative_to(key.app_dir)) for d in BUILD_OUTPUT_DIRS for p in key.app_dir.rglob(d) if p.is_dir()]
    if present and not allow_build_output:
        return ("build output present (would add findings outside the answer key; see test/README.md): "
                + ", ".join(sorted(present)) + ". Delete it or pass --allow-build-output.")
    return None


def build_command(tool: str, key: AppKey, out_file: Path, model: str | None, extra: list[str]) -> list[str]:
    args = f"{key.app_rel} --subjects all --programmatic --output file --out-file {out_file.as_posix()}"
    if tool == "claude":
        exe = shutil.which("claude") or "claude"
        cmd = [exe, "-p", f"/compliance-reviewer {args}", "--output-format", "json",
               "--allowedTools", CLAUDE_ALLOWED_TOOLS, "--add-dir", str(out_file.parent)]
    else:
        exe = shutil.which("copilot") or "copilot"
        prompt = ("Follow the instructions in .github/prompts/compliance-review.prompt.md exactly. "
                  f"User input: {args}")
        cmd = [exe, "-p", prompt, "--allow-all-tools", "--add-dir", str(out_file.parent)]
    if model:
        cmd += ["--model", model]
    return cmd + list(extra)


def _child_env(tool: str) -> dict:
    env = dict(os.environ)
    if tool == "claude":
        for v in _CLAUDE_SESSION_VARS:
            env.pop(v, None)
    return env


_JSON_OBJ_RE = re.compile(r"\{[^{}]*\"status\"[^{}]*\}")


def parse_status(text: str) -> dict | None:
    """Find the reviewer's one-line programmatic JSON status in the tool's output."""
    for m in reversed(_JSON_OBJ_RE.findall(text or "")):
        try:
            obj = json.loads(m)
        except json.JSONDecodeError:
            continue
        if obj.get("status") in ("completed", "failed"):
            return obj
    return None


def _find_run_dir(key: AppKey, started: float) -> Path | None:
    """Fallback when the status line is missing: newest run for this target started after `started`."""
    if not TRANSITIONS_DIR.is_dir():
        return None
    candidates = []
    for d in TRANSITIONS_DIR.iterdir():
        st = d / "state.json"
        if d.is_dir() and st.exists() and st.stat().st_mtime >= started - 5:
            try:
                tp = json.loads(st.read_text(encoding="utf-8-sig")).get("targetPath", "")
            except (OSError, json.JSONDecodeError):
                continue
            if _target_matches(tp, key):
                candidates.append((st.stat().st_mtime, d))
    return max(candidates)[1] if candidates else None


def _target_matches(target_path: str, key: AppKey) -> bool:
    t = _norm(target_path).rstrip("/")
    return t.endswith(_norm(key.app_rel)) or t == _norm(str(key.app_dir))


_DONE_STEP_STATES = ("completed", "skipped")
_POLL_SECONDS = 5  # how often the run folder is checked for step changes


def _fmt_elapsed(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m{s:02d}s" if h else f"{m}m{s:02d}s"


def read_progress(run_dir: Path) -> dict | None:
    """Summarize a run's state.json: completed steps, estimated total, and the step now in progress."""
    try:
        state = json.loads((run_dir / "state.json").read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None  # missing, or caught mid-write; try again on the next poll
    steps = state.get("steps") or {}
    done = [name for name, st in steps.items() if st in _DONE_STEP_STATES]
    pending = [name for name, st in steps.items() if st not in _DONE_STEP_STATES]
    # The steps map fills in as the run goes, so estimate the total from the subject list:
    # 00-init, 01-inventory, 02-analyzers, one per subject, 90-aggregate, 99-report.
    subjects = state.get("subjects") or []
    total = max(len(steps), len(subjects) + 5) if subjects else len(steps)
    return {"done": done, "total": total, "current": pending[0] if pending else None,
            "status": state.get("status")}


class ProgressReporter:
    """Prints signs of life while the AI tool runs: a line when the reviewer finishes a step
    (read from its transitions/<runId>/state.json) and a heartbeat every `interval` seconds."""

    def __init__(self, key: AppKey, started: float, interval: float):
        self.key, self.started, self.interval = key, started, interval
        self.run_dir: Path | None = None
        self.seen_done: set[str] = set()
        self.last_print = started

    def _say(self, msg: str) -> None:
        print(f"  {self.key.name} [{_fmt_elapsed(time.time() - self.started)}] {msg}", flush=True)
        self.last_print = time.time()

    def poll(self) -> None:
        if self.interval <= 0:
            return
        if self.run_dir is None:
            self.run_dir = _find_run_dir(self.key, self.started)
            if self.run_dir:
                self._say(f"reviewer started run {self.run_dir.name}")
        prog = read_progress(self.run_dir) if self.run_dir else None
        if prog:
            new = [s for s in prog["done"] if s not in self.seen_done]
            self.seen_done.update(new)
            for step in new:
                self._say(f"step {len(self.seen_done)}/{prog['total']} done: {step}")
        if time.time() - self.last_print >= self.interval:
            if prog:
                cur = f", working on {prog['current']}" if prog["current"] else ""
                self._say(f"still running: {len(prog['done'])}/{prog['total']} steps done{cur}")
            else:
                self._say("still running: waiting for the reviewer to start its run")


def invoke(tool: str, key: AppKey, out_file: Path, log_file: Path, timeout_min: float,
           model: str | None, extra: list[str], progress_interval: float = 30) -> Invocation:
    cmd = build_command(tool, key, out_file, model, extra)
    inv = Invocation(status="error", command=cmd)
    if not shutil.which(cmd[0]):
        inv.error = (f"'{tool}' CLI not found on PATH. "
                     + ("Install Claude Code (https://claude.com/claude-code)." if tool == "claude"
                        else "Install GitHub Copilot CLI (npm install -g @github/copilot) and sign in."))
        return inv
    started = time.time()
    deadline = started + timeout_min * 60
    reporter = ProgressReporter(key, started, progress_interval)
    proc = subprocess.Popen(cmd, cwd=REPO_ROOT, env=_child_env(tool), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True,
                            encoding="utf-8", errors="replace")
    while True:
        try:
            # communicate() may be retried after TimeoutExpired without losing output.
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
    inv.duration_s = time.time() - started
    if progress_interval > 0:
        print(f"  {key.name} [{_fmt_elapsed(inv.duration_s)}] {tool} finished (exit code {rc}); scoring ...",
              flush=True)
    log_file.write_text(f"$ {' '.join(cmd)}\n# exit code: {rc}\n\n## stdout\n{stdout}\n\n## stderr\n{stderr}\n",
                        encoding="utf-8")

    text = stdout
    if tool == "claude":
        try:
            envelope = json.loads(stdout)
            text = envelope.get("result") or ""
            inv.cost_usd = envelope.get("total_cost_usd")
        except (json.JSONDecodeError, AttributeError):
            pass
    status = parse_status(text)
    if status:
        inv.run_id = status.get("runId")
        inv.report_file = status.get("reportFile")
        inv.overall_score = status.get("overallScore")
        inv.overall_band = status.get("overallBand")
        inv.status = status["status"]
        if inv.status == "failed":
            inv.error = f"reviewer failed at step {status.get('step')}: {status.get('error')}"
    if inv.run_id and (TRANSITIONS_DIR / inv.run_id).is_dir():
        inv.run_dir = TRANSITIONS_DIR / inv.run_id
    else:
        inv.run_dir = _find_run_dir(key, started)
        if inv.run_dir and not inv.run_id:
            inv.run_id = inv.run_dir.name
    if inv.status == "error":
        inv.error = (f"no programmatic status line in the {tool} output (exit code {rc}); see {log_file}"
                     + (f"; stderr: {stderr.strip()[:300]}" if stderr.strip() else ""))
    return inv


# --------------------------------------------------------------------------- reporting


def render_markdown(r: dict) -> str:
    s = r.get("score") or {}
    lines = [f"# {r['app']} — {r['verdict'].upper()}", ""]
    lines += [f"- Tool: {r['tool']} ({r['toolReason']})",
              f"- Run: `{r.get('runId')}`" + (f" — report: {r['reportFile']}" if r.get("reportFile") else ""),
              f"- Reviewer score: {r.get('overallScore')} ({r.get('overallBand')})",
              f"- Duration: {r.get('durationSeconds', 0):.0f} s" + (f", cost ${r['costUsd']:.2f}" if r.get("costUsd") else "")]
    if r.get("error"):
        lines += ["", f"**Error:** {r['error']}"]
    if s:
        lines += [f"- Flaws found: {len(s['found'])}/{s['total']} ({s['foundPct']:.0f}%; "
                  f"need {s['required']} for {s['minFoundPct']:g}%)",
                  f"- Unexpected Error findings: {len(s['unexpectedErrors'])}", ""]
        lines += ["## Seeded flaws", "", "| Flaw | Result | Findings |", "|---|---|---|"]
        rows = {x["flaw"]: ("found", ", ".join(x["findingIds"])) for x in s["found"]}
        rows.update({x["flaw"]: ("**missed**", "expected " + ", ".join(x["checks"]) + " in " + ", ".join(x["locations"]))
                     for x in s["missed"]})
        for flaw_id in sorted(rows, key=lambda i: int(i[1:])):
            lines.append(f"| {flaw_id} | {rows[flaw_id][0]} | {rows[flaw_id][1]} |")
        for title, items in (("Unexpected Error findings (fail the test)", s["unexpectedErrors"]),
                             ("Unexpected Warning/Information findings (reported only)", s["unexpectedOther"]),
                             ("Expected checks at other locations (reported only)", s["related"])):
            if items:
                lines += ["", f"## {title}", "", "| Id | Check | Severity | Location | Title |", "|---|---|---|---|---|"]
                lines += [f"| {i['id']} | {i['checkId']} | {i['severity']} | {i['location']} | {i['title']} |" for i in items]
        lines += ["", f"Expected incidental findings (not scored): {len(s['incidental'])}"]
    return "\n".join(lines) + "\n"


def summarize(r: dict) -> str:
    s = r.get("score")
    if not s:
        return f"[{r['verdict'].upper()}] {r['app']} ({r['tool']}): {r.get('error')}"
    miss = ", ".join(x["flaw"] for x in s["missed"]) or "none"
    return (f"[{r['verdict'].upper()}] {r['app']} ({r['tool']}): {len(s['found'])}/{s['total']} flaws "
            f"({s['foundPct']:.0f}%, need {s['minFoundPct']:g}%), missed: {miss}; "
            f"unexpected errors: {len(s['unexpectedErrors'])}, unexpected warn/info: {len(s['unexpectedOther'])}")


# --------------------------------------------------------------------------- entry point


def add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--tool", choices=("auto",) + TOOLS, default="auto",
                   help="AI tool to run the reviewer with (default: auto; env COMPLIANCE_TEST_TOOL).")
    p.add_argument("--min-found", type=float, default=float(os.environ.get("COMPLIANCE_TEST_MIN_FOUND", 90)),
                   metavar="PCT", help="Percent of seeded flaws that must be found (default 90; env COMPLIANCE_TEST_MIN_FOUND).")
    p.add_argument("--timeout", type=float, default=float(os.environ.get("COMPLIANCE_TEST_TIMEOUT_MIN", 60)),
                   metavar="MIN", help="Per-review timeout in minutes (default 60).")
    p.add_argument("--progress", type=float, default=float(os.environ.get("COMPLIANCE_TEST_PROGRESS_SEC", 30)),
                   metavar="SEC", help="While a review runs, print each completed reviewer step and a "
                                       "heartbeat every SEC seconds (default 30; 0 = quiet).")
    p.add_argument("--model", help="Model passed to the AI tool's --model option.")
    p.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR, help="Where results are written.")
    p.add_argument("--allow-build-output", action="store_true",
                   help="Run even if bin/obj/target/__pycache__/.venv exist in the app.")
    p.add_argument("--dry-run", action="store_true", help="Print the command that would run and exit.")
    p.add_argument("--tool-arg", action="append", default=[], metavar="ARG",
                   help="Extra argument for the AI tool CLI (repeatable), e.g. --tool-arg=--max-budget-usd --tool-arg=5")


def run_test(kind: str, lang: str, args: argparse.Namespace, session_dir: Path | None = None) -> dict:
    key = load_app_key(kind, lang)
    min_found = args.min_found
    if not 0 <= min_found <= 100:
        raise SystemExit("--min-found must be between 0 and 100")
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")

    if getattr(args, "score_only", None):
        tool, reason = "n/a", "--score-only"
    else:
        tool, reason = detect_tool(args.tool)
    out_dir = (session_dir or (args.results_dir / f"{stamp}-{tool}")).resolve()
    result = {"app": key.name, "target": key.app_rel, "tool": tool, "toolReason": reason,
              "minFoundPct": min_found, "startedAt": dt.datetime.now().isoformat(timespec="seconds")}

    if args.dry_run:
        cmd = build_command(tool, key, out_dir / f"{key.name}-report.md", args.model, args.tool_arg)
        print(f"{key.name}: tool={tool} ({reason})\n  cwd: {REPO_ROOT}\n  " + subprocess.list2cmdline(cmd))
        return {**result, "verdict": "dry-run"}

    out_dir.mkdir(parents=True, exist_ok=True)
    if getattr(args, "score_only", None):
        run_dir = Path(args.score_only).resolve()
        inv = Invocation(status="completed", run_id=run_dir.name, run_dir=run_dir)
        agg = run_dir / "90-aggregate.json"
        if agg.exists():
            a = json.loads(agg.read_text(encoding="utf-8-sig"))
            inv.overall_score, inv.overall_band = a.get("overallScore"), a.get("overallBand")
    else:
        problem = preflight(key, args.allow_build_output)
        if problem:
            result.update(verdict="error", error=problem)
            return _finish(result, out_dir, key)
        print(f"{key.name}: running the reviewer with {tool} ({reason}) ...", flush=True)
        inv = invoke(tool, key, out_dir / f"{key.name}-report.md", out_dir / f"{key.name}-{tool}.log",
                     args.timeout, args.model, args.tool_arg, args.progress)

    result.update(runId=inv.run_id, runDir=str(inv.run_dir) if inv.run_dir else None, reportFile=inv.report_file,
                  overallScore=inv.overall_score, overallBand=inv.overall_band,
                  durationSeconds=round(inv.duration_s, 1), costUsd=inv.cost_usd, command=inv.command)

    if inv.status != "completed" or not inv.run_dir:
        result.update(verdict="error", error=inv.error or "review did not complete")
        return _finish(result, out_dir, key)
    run = load_run(inv.run_dir)
    target = (run["state"] or {}).get("targetPath", "")
    if target and not _target_matches(target, key):
        result.update(verdict="error",
                      error=f"run {inv.run_id} reviewed {target!r}, not {key.app_rel} (runId collision?)")
        return _finish(result, out_dir, key)
    if run["aggregate"] is None:
        result.update(verdict="error", error=f"{inv.run_dir} has no 90-aggregate.json")
        return _finish(result, out_dir, key)

    s = score_run(run, key, min_found)
    result["score"] = {"total": s.total, "found": s.found, "missed": s.missed, "foundPct": round(s.found_pct, 1),
                       "required": s.required, "minFoundPct": min_found, "coverageOk": s.coverage_ok,
                       "unexpectedErrors": s.unexpected_errors, "unexpectedOther": s.unexpected_other,
                       "related": s.related, "incidental": s.incidental}
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


def main(kind: str, lang: str, argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=f"Validate the Compliance Reviewer against test/{kind}/{lang}.")
    add_common_args(p)
    p.add_argument("--score-only", metavar="RUN_DIR",
                   help="Skip the review; score an existing transitions/<runId> folder.")
    args = p.parse_args(argv)
    r = run_test(kind, lang, args)
    if r["verdict"] == "dry-run":
        return EXIT_PASS
    print(render_markdown(r))
    print(summarize(r))
    print(f"Result: {r['resultFile']}")
    return exit_code([r["verdict"]])
