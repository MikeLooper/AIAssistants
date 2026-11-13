"""Run the Compliance Reviewer headlessly against an application directory (Python 3.10+, stdlib only).

The script:

1. resolves the AI tool (``--tool``, ``COMPLIANCE_REVIEW_TOOL``, the chat that started it, or Claude),
2. runs the reviewer in programmatic mode (no interview, no chat) against the directory you name,
3. prints the finished report,
4. prints a run summary: duration, cost and token usage.

Run it from anywhere; the review always runs with the ``compliance-reviewer_any-ai`` folder as the
working directory, so transition files go to ``transitions/<runId>/`` and the report to ``docs/reports/``.

Examples::

    python scripts/run_review.py C:\\src\\myapp
    python scripts/run_review.py ../myapp --subjects review-testing,review-maintainability
    python scripts/run_review.py C:\\src\\myapp --tool copilot --model gpt-5
    python scripts/run_review.py C:\\src\\myapp --out-file C:\\out\\myapp-review.md --no-report

Exit codes: 0 review completed, 1 review failed, 2 the review could not run (tool missing, timeout,
bad arguments, no status from the tool).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent  # compliance-reviewer_any-ai: the reviewer's workspace
TRANSITIONS_DIR = REPO_ROOT / "transitions"

TOOLS = ("claude", "copilot")
EXIT_OK, EXIT_FAILED, EXIT_ERROR = 0, 1, 2

# Claude Code session variables that make a child `claude` think it is nested inside this session.
# Auth/provider variables (e.g. CLAUDE_CODE_USE_BEDROCK) are deliberately kept.
_CLAUDE_SESSION_VARS = (
    "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION",
    "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_MESSAGING_SOCKET", "CLAUDE_CODE_MESSAGING_TOKEN",
    "CLAUDE_PID", "CLAUDE_CODE_SSE_PORT",
)

# Tools a headless Claude review needs. The reviewer's own rules keep the target read-only.
CLAUDE_ALLOWED_TOOLS = (
    "Read,Grep,Glob,Write,Edit,Agent,Task,Skill,TodoWrite,"
    "Bash(git -C:*),"
    "Bash(python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py:*)"
)

# Default USD price per GitHub Copilot premium request, used only for the cost estimate.
DEFAULT_COPILOT_REQUEST_USD = 0.04

# Anthropic API list prices in USD per million tokens, used for the token-cost breakdown:
# (input, output, cache read, 5-minute cache write, 1-hour cache write). Prices as of 2026-11-03;
# override or extend them with --prices FILE. Keys match model names by prefix (longest wins).
MODEL_PRICES: dict[str, tuple[float, float, float, float, float]] = {
    "claude-fable-5-2": (8.00, 40.00, 0.20, 10.00, 16.00),
    "claude-mythos-5-2": (8.00, 40.00, 0.20, 10.00, 16.00),
    "claude-fable-5-1": (10.00, 50.00, 0.25, 12.50, 20.00),
    "claude-mythos-5-1": (10.00, 50.00, 0.25, 12.50, 20.00),
    "claude-fable-5": (10.00, 50.00, 1.00, 12.50, 20.00),
    "claude-mythos-5": (10.00, 50.00, 1.00, 12.50, 20.00),
    "claude-opus-5-5": (4.00, 20.00, 0.20, 5.00, 8.00),
    "claude-opus-5": (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-opus-4-8": (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-opus-4-7": (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-opus-4-6": (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-opus-4-5": (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-sonnet-5-5": (2.00, 10.00, 0.10, 2.50, 4.00),
    "claude-sonnet-5": (2.00, 10.00, 0.20, 2.50, 4.00),
    "claude-sonnet-4": (3.00, 15.00, 0.30, 3.75, 6.00),  # Sonnet 4, 4.5 and 4.6
    "claude-haiku-5-5": (0.10, 0.50, 0.01, 0.125, 0.20),  # prompts up to 100K tokens
    "claude-haiku-4-5": (1.00, 5.00, 0.10, 1.25, 2.00),
}

_DONE_STEP_STATES = ("completed", "skipped")
_POLL_SECONDS = 5


# --------------------------------------------------------------------------- helpers


def fmt_elapsed(seconds: float) -> str:
    m, s = divmod(int(round(seconds)), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m:02d}m {s:02d}s" if h else f"{m}m {s:02d}s"


def fmt_tokens(n: float | int | None) -> str:
    if n is None:
        return "-"
    n = float(n)
    for unit, size in (("M", 1e6), ("k", 1e3)):
        if n >= size:
            return f"{n / size:.1f}{unit}"
    return f"{int(n)}"


def _norm(path: str) -> str:
    return path.replace("\\", "/").lower().rstrip("/")


def detect_tool(explicit: str | None, env: dict | None = None) -> tuple[str, str]:
    """Return (tool, reason). Order: --tool > COMPLIANCE_REVIEW_TOOL > the chat that started us > claude."""
    env = os.environ if env is None else env
    if explicit and explicit != "auto":
        return explicit, "--tool"
    from_env = (env.get("COMPLIANCE_REVIEW_TOOL") or "").strip().lower()
    if from_env and from_env != "auto":
        if from_env not in TOOLS:
            raise ValueError(f"COMPLIANCE_REVIEW_TOOL must be one of {TOOLS} or auto, got {from_env!r}")
        return from_env, "COMPLIANCE_REVIEW_TOOL"
    if env.get("CLAUDECODE") == "1" or env.get("CLAUDE_CODE_ENTRYPOINT"):
        return "claude", "started from Claude Code"
    if env.get("TERM_PROGRAM") == "vscode" or env.get("VSCODE_PID") or env.get("VSCODE_IPC_HOOK_CLI"):
        return "copilot", "started from VS Code (not Claude Code), so GitHub Copilot"
    return "claude", "default"


def target_arg(target: Path) -> str:
    """Path as the reviewer should see it: relative to the workspace when inside it, else absolute."""
    try:
        return target.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return target.as_posix()


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------------- command


def reviewer_args(args: argparse.Namespace, target: Path, out_file: Path) -> str:
    parts = [f'"{target_arg(target)}"' if " " in target_arg(target) else target_arg(target),
             f"--subjects {args.subjects}"]
    if args.advanced:
        parts += ["--advanced", f"--analyzers {args.analyzers}"]
    out = out_file.as_posix()
    parts += ["--programmatic", "--output file", f'--out-file "{out}"' if " " in out else f"--out-file {out}"]
    return " ".join(parts)


def build_command(tool: str, args: argparse.Namespace, target: Path, out_file: Path) -> list[str]:
    rargs = reviewer_args(args, target, out_file)
    add_dirs: list[str] = []
    for d in (target, out_file.parent):
        if not is_within(d, REPO_ROOT) and str(d) not in add_dirs:
            add_dirs.append(str(d))
    if tool == "claude":
        cmd = [shutil.which("claude") or "claude", "-p", f"/compliance-reviewer {rargs}",
               "--output-format", "json",
               "--allowedTools", ",".join([CLAUDE_ALLOWED_TOOLS] + list(args.allow_tool or []))]
    else:
        prompt = ("Follow the instructions in .github/prompts/compliance-review.prompt.md exactly. "
                  f"User input: {rargs}")
        cmd = [shutil.which("copilot") or "copilot", "-p", prompt, "--allow-all-tools"]
    for d in add_dirs:
        cmd += ["--add-dir", d]
    if args.model:
        cmd += ["--model", args.model]
    return cmd + list(args.tool_arg or [])


def child_env(tool: str) -> dict:
    env = dict(os.environ)
    if tool == "claude":
        for v in _CLAUDE_SESSION_VARS:
            env.pop(v, None)
    return env


# --------------------------------------------------------------------------- progress


def find_run_dir(target: Path, started: float) -> Path | None:
    """Newest run under transitions/ for this target that started after `started`."""
    if not TRANSITIONS_DIR.is_dir():
        return None
    want = {_norm(target_arg(target)), _norm(str(target))}
    best: tuple[float, Path] | None = None
    for d in TRANSITIONS_DIR.iterdir():
        st = d / "state.json"
        try:
            if not (d.is_dir() and st.exists() and st.stat().st_mtime >= started - 5):
                continue
            tp = _norm(json.loads(st.read_text(encoding="utf-8-sig")).get("targetPath", ""))
        except (OSError, json.JSONDecodeError):
            continue
        if tp in want or any(w.endswith(tp) or tp.endswith(w) for w in want if tp):
            mtime = st.stat().st_mtime
            if best is None or mtime > best[0]:
                best = (mtime, d)
    return best[1] if best else None


def read_state(run_dir: Path | None) -> dict | None:
    if not run_dir:
        return None
    try:
        return json.loads((run_dir / "state.json").read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


class Progress:
    """Prints a line to stderr when the reviewer finishes a step, plus a heartbeat every `interval` s."""

    def __init__(self, target: Path, started: float, interval: float):
        self.target, self.started, self.interval = target, started, interval
        self.run_dir: Path | None = None
        self.seen: set[str] = set()
        self.last_print = started

    def say(self, msg: str) -> None:
        print(f"  [{fmt_elapsed(time.time() - self.started)}] {msg}", file=sys.stderr, flush=True)
        self.last_print = time.time()

    def poll(self) -> None:
        if self.interval <= 0:
            return
        if self.run_dir is None:
            self.run_dir = find_run_dir(self.target, self.started)
            if self.run_dir:
                self.say(f"reviewer started run {self.run_dir.name}")
        state = read_state(self.run_dir)
        steps = (state or {}).get("steps") or {}
        subjects = (state or {}).get("subjects") or []
        total = max(len(steps), len(subjects) + 5) if subjects else len(steps)
        done = [n for n, s in steps.items() if s in _DONE_STEP_STATES]
        for step in [n for n in done if n not in self.seen]:
            self.seen.add(step)
            self.say(f"step {len(self.seen)}/{total} done: {step}")
        if time.time() - self.last_print >= self.interval:
            if state:
                current = next((n for n, s in steps.items() if s not in _DONE_STEP_STATES), None)
                self.say(f"still running: {len(done)}/{total} steps done"
                         + (f", working on {current}" if current else ""))
            else:
                self.say("still running: waiting for the reviewer to start its run")


# --------------------------------------------------------------------------- output parsing


_STATUS_RE = re.compile(r"\{[^{}]*\"status\"[^{}]*\}")


def parse_status(text: str) -> dict | None:
    """Find the reviewer's one-line programmatic JSON status in the tool's output."""
    for m in reversed(_STATUS_RE.findall(text or "")):
        try:
            obj = json.loads(m)
        except json.JSONDecodeError:
            continue
        if obj.get("status") in ("completed", "failed"):
            return obj
    return None


def model_price(name: str, prices: dict) -> tuple[str, dict] | None:
    """Price entry for a model name as a tool reports it (e.g. 'claude-opus-4-8[1m]',
    'claude-sonnet-4.5', 'anthropic.claude-haiku-4-5-20251001'). Longest matching key wins."""
    n = re.sub(r"\[.*?\]", "", (name or "").lower()).strip().replace(".", "-")
    n = re.sub(r"^(anthropic-|us-anthropic-|eu-anthropic-)", "", n)
    n = re.sub(r"-\d{8}$|@\d{8}$", "", n)
    if not n.startswith("claude-"):
        n = "claude-" + n
    best = None
    for key in prices:
        k = key.lower()
        if n == k or n.startswith(k + "-"):
            if best is None or len(k) > len(best):
                best = key
    return (best, prices[best]) if best else None


def token_costs(model: str, tokens: dict, prices: dict, reported_usd: float | None = None) -> dict | None:
    """Cost of each token type for one model at the price table's rates.

    Tools report cache-write tokens without splitting them into 5-minute and 1-hour writes, which are
    priced differently. When the tool also reports the model's total cost and the remainder after
    input, output and cache reads falls between the all-5-minute and all-1-hour cache-write cost,
    that remainder is used as the cache-write cost; otherwise the 5-minute price is used."""
    match = model_price(model, prices)
    if not match:
        return None
    key, p = match
    tok = {t: float(tokens.get(t) or 0) for t in ("input", "output", "cacheRead", "cacheWrite")}
    rows = {
        "input": {"tokens": tok["input"], "usdPerMTok": p["input"]},
        "output": {"tokens": tok["output"], "usdPerMTok": p["output"]},
        "cacheRead": {"tokens": tok["cacheRead"], "usdPerMTok": p["cacheRead"]},
    }
    for r in rows.values():
        r["usd"] = r["tokens"] * r["usdPerMTok"] / 1e6
    base = sum(r["usd"] for r in rows.values())
    lo = tok["cacheWrite"] * p["cacheWrite5m"] / 1e6
    hi = tok["cacheWrite"] * p["cacheWrite1h"] / 1e6
    write = {"tokens": tok["cacheWrite"], "usdPerMTok": p["cacheWrite5m"], "usd": lo,
             "usdPerMTokRange": [p["cacheWrite5m"], p["cacheWrite1h"]], "basis": "5-minute write price"}
    if reported_usd is not None and tok["cacheWrite"] and lo - 0.005 <= reported_usd - base <= hi + 0.005:
        write["usd"] = min(max(reported_usd - base, lo), hi)
        write["usdPerMTok"] = write["usd"] / tok["cacheWrite"] * 1e6
        write["basis"] = "derived from the reported total (a mix of 5-minute and 1-hour writes)"
    rows["cacheWrite"] = write
    total = base + write["usd"]
    for r in rows.values():
        r["share"] = r["usd"] / total if total else 0.0
    return {"priceKey": key, "rows": rows, "totalUsd": total, "reportedUsd": reported_usd}


def load_prices(path: str | None) -> dict:
    prices = {k: dict(zip(("input", "output", "cacheRead", "cacheWrite5m", "cacheWrite1h"), v))
              for k, v in MODEL_PRICES.items()}
    if path:
        for k, v in json.loads(Path(path).read_text(encoding="utf-8-sig")).items():
            prices[k] = {**prices.get(k, {}), **v}
            if "input" in v:  # fill unstated cache prices with the usual multipliers
                prices[k].setdefault("cacheRead", v["input"] * 0.1)
                prices[k].setdefault("cacheWrite5m", v["input"] * 1.25)
                prices[k].setdefault("cacheWrite1h", v["input"] * 2)
    return prices


def claude_usage(envelope: dict, prices: dict) -> dict:
    models = {}
    for name, u in (envelope.get("modelUsage") or {}).items():
        models[name] = {
            "inputTokens": u.get("inputTokens"),
            "outputTokens": u.get("outputTokens"),
            "cacheReadTokens": u.get("cacheReadInputTokens"),
            "cacheWriteTokens": u.get("cacheCreationInputTokens"),
            "costUsd": u.get("costUSD"),
            "costBasis": u.get("costBasis"),
        }
        models[name]["tokenCosts"] = token_costs(name, {
            "input": u.get("inputTokens"), "output": u.get("outputTokens"),
            "cacheRead": u.get("cacheReadInputTokens"), "cacheWrite": u.get("cacheCreationInputTokens"),
        }, prices, u.get("costUSD"))
    subagents = (envelope.get("subagent_stats") or {}).get("spawned")
    return {
        "costUsd": envelope.get("total_cost_usd"),
        "costIsEstimate": False,
        "apiDurationSeconds": (envelope.get("duration_api_ms") or 0) / 1000 or None,
        "turns": envelope.get("num_turns"),
        "subagents": subagents,
        "models": models,
    }


_PREMIUM_RE = re.compile(r"Total usage est:\s*([\d.]+)\s+Premium request", re.I)
_API_DUR_RE = re.compile(r"Total duration \(API\):\s*(.+)", re.I)


_COUNT_RE = re.compile(r"([\d.,]+)\s*([kmb]?)\s+(input|output|cache read|cache write)", re.I)
_TOKEN_KEYS = {"input": "input", "output": "output", "cache read": "cacheRead", "cache write": "cacheWrite"}


def _count(num: str, suffix: str) -> float:
    return float(num.replace(",", "")) * {"": 1, "k": 1e3, "m": 1e6, "b": 1e9}[suffix.lower()]


def copilot_usage(text: str, request_usd: float, prices: dict) -> dict:
    """Copilot CLI prints a usage block: "Total usage est: N Premium requests", then "Usage by model:"
    with one line per model, e.g. "claude-sonnet-4.5  1.2m input, 45.6k output, 0 cache read, ..."."""
    lines = (text or "").splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip().lower().startswith("total usage est")), None)
    block = []
    if start is not None:
        for ln in lines[start:]:
            if not ln.strip() and block and not block[-1].strip():
                break
            block.append(ln.rstrip())
    models = {}
    by_model = next((i for i, ln in enumerate(block) if ln.strip().lower().startswith("usage by model")), None)
    for ln in block[by_model + 1:] if by_model is not None else []:
        counts = _COUNT_RE.findall(ln)
        if not counts or not ln.strip():
            continue
        name = ln.strip().split()[0]
        tokens = {_TOKEN_KEYS[kind.lower()]: _count(n, s) for n, s, kind in counts}
        models[name] = {"inputTokens": tokens.get("input"), "outputTokens": tokens.get("output"),
                        "cacheReadTokens": tokens.get("cacheRead"), "cacheWriteTokens": tokens.get("cacheWrite"),
                        "costUsd": None, "tokenCosts": token_costs(name, tokens, prices)}
    m = _PREMIUM_RE.search(text or "")
    requests = float(m.group(1)) if m else None
    api = _API_DUR_RE.search(text or "")
    return {
        "premiumRequests": requests,
        "costUsd": round(requests * request_usd, 2) if requests is not None else None,
        "costIsEstimate": True,
        "requestUsd": request_usd,
        "apiDuration": api.group(1).strip() if api else None,
        "models": models,
        "usageBlock": [ln for ln in block if ln.strip()],
    }


# --------------------------------------------------------------------------- run


def run(args: argparse.Namespace) -> int:
    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        print(f"error: target directory not found: {target}", file=sys.stderr)
        return EXIT_ERROR
    if target == REPO_ROOT or is_within(REPO_ROOT, target):
        print("error: the target must not be (or contain) the Compliance Reviewer workspace", file=sys.stderr)
        return EXIT_ERROR

    try:
        tool, reason = detect_tool(args.tool)
        prices = load_prices(args.prices)
    except (ValueError, OSError, TypeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return EXIT_ERROR

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    work_dir = Path(tempfile.gettempdir()) / "compliance-review-runs" / f"{stamp}-{target.name}"
    if args.out_file:
        out_file = Path(args.out_file).expanduser().resolve()
        if is_within(out_file, target):
            print("error: --out-file must not be inside the target (the target is read-only)", file=sys.stderr)
            return EXIT_ERROR
    else:
        out_file = work_dir / f"{target.name}-compliance-review.md"
    log_file = work_dir / f"{tool}.log"

    cmd = build_command(tool, args, target, out_file)
    if args.dry_run:
        print(f"tool: {tool} ({reason})\ncwd:  {REPO_ROOT}\ncmd:  {subprocess.list2cmdline(cmd)}")
        return EXIT_OK
    out_file.parent.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    if not shutil.which(cmd[0]):
        print(f"error: '{tool}' CLI not found on PATH. "
              + ("Install Claude Code (https://claude.com/claude-code) and sign in." if tool == "claude"
                 else "Install GitHub Copilot CLI (npm install -g @github/copilot) and sign in."),
              file=sys.stderr)
        return EXIT_ERROR

    print(f"Compliance review of {target}\n  tool: {tool} ({reason})"
          + (f", model {args.model}" if args.model else "")
          + f"\n  subjects: {args.subjects}, advanced: {'on' if args.advanced else 'off'}"
          + f"\n  started {dt.datetime.now():%Y-%m-%d %H:%M:%S}; this usually takes several minutes ...",
          file=sys.stderr, flush=True)

    started = time.time()
    deadline = started + args.timeout * 60
    progress = Progress(target, started, args.progress)
    proc = subprocess.Popen(cmd, cwd=REPO_ROOT, env=child_env(tool), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True,
                            encoding="utf-8", errors="replace")
    timed_out = False
    while True:
        try:
            stdout, stderr = proc.communicate(timeout=max(0.1, min(_POLL_SECONDS, deadline - time.time())))
            break
        except subprocess.TimeoutExpired:
            if time.time() >= deadline:
                proc.kill()
                stdout, stderr = proc.communicate()
                timed_out = True
                break
            progress.poll()
        except KeyboardInterrupt:
            proc.kill()
            proc.communicate()
            print("\ninterrupted; the run can be resumed with 'resume run <id>'", file=sys.stderr)
            return EXIT_ERROR
    duration = time.time() - started
    rc = proc.returncode
    log_file.write_text(f"$ {subprocess.list2cmdline(cmd)}\n# exit code: {rc}\n\n## stdout\n{stdout}\n\n"
                        f"## stderr\n{stderr}\n", encoding="utf-8")

    # ---- parse the tool's output
    text, usage = stdout, {}
    if tool == "claude":
        try:
            envelope = json.loads(stdout)
            text = envelope.get("result") or ""
            usage = claude_usage(envelope, prices)
        except (json.JSONDecodeError, AttributeError):
            pass
    else:
        usage = copilot_usage(f"{stdout}\n{stderr}", args.copilot_request_usd, prices)
    status = parse_status(text) or {}
    run_dir = (TRANSITIONS_DIR / status["runId"]) if status.get("runId") else None
    if not (run_dir and run_dir.is_dir()):
        run_dir = find_run_dir(target, started)
    state = read_state(run_dir) or {}

    # ---- present the report
    report_file = Path(status["reportFile"]) if status.get("reportFile") else (out_file if out_file.exists() else None)
    docs_copy = (REPO_ROOT / state["reportPath"]) if state.get("reportPath") else None
    outcome = status.get("status") or ("timed out" if timed_out else "error")
    if outcome == "completed" and report_file and report_file.exists() and not args.no_report:
        print(report_file.read_text(encoding="utf-8-sig"))

    # ---- summary
    if not args.out_file and outcome == "completed" and docs_copy and docs_copy.exists():
        report_file = docs_copy  # the temporary --out-file copy is not worth pointing at
    summary = {
        "status": outcome,
        "target": str(target),
        "tool": tool,
        "model": args.model,
        "runId": status.get("runId") or (run_dir.name if run_dir else None),
        "reportFile": str(report_file) if report_file else None,
        "docsReport": str(docs_copy) if docs_copy else None,
        "overallScore": status.get("overallScore"),
        "overallBand": status.get("overallBand"),
        "durationSeconds": round(duration, 1),
        "exitCode": rc,
        "log": str(log_file),
        "usage": usage,
    }
    if outcome == "failed":
        summary["error"] = f"step {status.get('step')}: {status.get('error')}"
    elif outcome != "completed":
        summary["error"] = (f"timed out after {args.timeout} min" if timed_out else
                            f"no programmatic status line in the {tool} output (exit code {rc})"
                            + (f"; stderr: {stderr.strip()[:300]}" if stderr.strip() else ""))
    print_summary(summary)
    if args.summary_json:
        Path(args.summary_json).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    if outcome == "completed":
        return EXIT_OK
    return EXIT_FAILED if outcome == "failed" else EXIT_ERROR


def print_summary(s: dict) -> None:
    u = s.get("usage") or {}
    rows = [("Status", s["status"]), ("Target", s["target"]),
            ("Tool", s["tool"] + (f" ({s['model']})" if s.get("model") else ""))]
    if s.get("runId"):
        rows.append(("Run ID", s["runId"]))
    if s.get("overallScore") is not None:
        rows.append(("Overall score", f"{s['overallScore']} ({s.get('overallBand') or '-'})"))
    if s.get("reportFile"):
        rows.append(("Report", s["reportFile"]))
    if s.get("error"):
        rows += [("Error", s["error"]), ("Tool log", s["log"])]

    rows.append(("Duration", fmt_elapsed(s["durationSeconds"]) + " (wall clock)"))
    if u.get("apiDurationSeconds"):
        rows.append(("API time", fmt_elapsed(u["apiDurationSeconds"]) + " (model calls, summed; can exceed wall clock with parallel subagents)"))
    elif u.get("apiDuration"):
        rows.append(("API time", u["apiDuration"]))
    if u.get("turns") is not None:
        rows.append(("Turns", f"{u['turns']}" + (f", {u['subagents']} subagents" if u.get("subagents") else "")))

    if s["tool"] == "claude":
        if u.get("costUsd") is not None:
            basis = {m.get("costBasis") for m in (u.get("models") or {}).values()} - {None}
            note = " (at API list prices, as reported by Claude Code; a subscription plan bills differently)" if "list" in basis else ""
            rows.append(("Cost", f"${u['costUsd']:.2f}{note}"))
        else:
            rows.append(("Cost", "not reported by the tool"))
    else:
        if u.get("premiumRequests") is not None:
            rows.append(("Cost", f"{u['premiumRequests']:g} premium requests, est. ${u['costUsd']:.2f} "
                                 f"at ${u['requestUsd']:.2f}/request (included requests on your plan cost nothing extra)"))
        else:
            rows.append(("Cost", "not reported by the tool"))

    width = max(len(k) for k, _ in rows)
    out = ["", "=" * 72, "Run summary", "=" * 72]
    out += [f"{k:<{width}}  {v}" for k, v in rows]
    out += token_cost_lines(s["tool"], u.get("models") or {})
    if u.get("usageBlock"):
        out.append("")
        out += ["Copilot usage:"] + [f"  {ln.strip()}" for ln in u["usageBlock"]]
    out.append("=" * 72)
    # The summary goes to stdout after the report so both can be captured together.
    print("\n".join(out), flush=True)


_TOKEN_LABELS = {"input": "Input", "output": "Output", "cacheRead": "Cache read", "cacheWrite": "Cache write"}


def token_cost_lines(tool: str, models: dict) -> list[str]:
    """Token costs: one table per model with the tokens, rate, cost and cost share of each token type."""
    if not models:
        return []
    title = ("Token costs (Anthropic API list prices)" if tool == "claude" else
             "Token costs (API list-price equivalent; Copilot bills premium requests, not tokens)")
    out = ["", title, "-" * 72]
    notes: list[str] = []
    grand, all_priced = 0.0, True
    for name, m in models.items():
        tc = m.get("tokenCosts")
        if not tc:
            all_priced = False
            out.append(f"{name}: no price on file (add one with --prices); tokens: "
                       f"{fmt_tokens(m.get('inputTokens'))} input, {fmt_tokens(m.get('outputTokens'))} output, "
                       f"{fmt_tokens(m.get('cacheReadTokens'))} cache read, "
                       f"{fmt_tokens(m.get('cacheWriteTokens'))} cache write")
            continue
        out.append(name + (f"  (priced as {tc['priceKey']})" if tc["priceKey"] != name else ""))
        out.append(f"  {'Token type':<13} {'Tokens':>9} {'$/MTok':>9} {'Cost':>10} {'Share':>7}")
        for key, label in _TOKEN_LABELS.items():
            r = tc["rows"][key]
            mark = ""
            if key == "cacheWrite" and r["tokens"]:
                mark = " *" if r["basis"].startswith("derived") else " +"
            out.append(f"  {label:<13} {fmt_tokens(r['tokens']):>9} {'$' + format(r['usdPerMTok'], '.2f'):>9} "
                       f"{'$' + format(r['usd'], '.2f'):>10} {r['share']:>7.0%}{mark}")
            lo, hi = r.get("usdPerMTokRange") or (0, 0)
            if mark == " *":
                notes.append(f"* {name}: cache-write rate derived from the reported cost (between the 5-minute "
                             f"${lo:.2f} and 1-hour ${hi:.2f} rates); the tool doesn't split writes by duration.")
            elif mark == " +":
                notes.append(f"+ {name}: cache writes priced at the 5-minute rate; 1-hour writes cost ${hi:.2f}/MTok.")
        total_tokens = sum(tc["rows"][k]["tokens"] for k in _TOKEN_LABELS)
        line = f"  {'Total':<13} {fmt_tokens(total_tokens):>9} {'':>9} {'$' + format(tc['totalUsd'], '.2f'):>10}"
        if tc.get("reportedUsd") is not None and abs(tc["reportedUsd"] - tc["totalUsd"]) >= 0.01:
            line += f"   (tool reported ${tc['reportedUsd']:.2f})"
        out.append(line)
        grand += tc["totalUsd"]
    if len(models) > 1 and grand:
        out.append(f"All models: ${grand:.2f}" + ("" if all_priced else " (priced models only)"))
    return out + notes


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    env = os.environ
    p = argparse.ArgumentParser(
        description="Run the Compliance Reviewer headlessly against an application directory, print the "
                    "report, then report the run's duration and cost.")
    p.add_argument("target", help="Application code directory to review (read-only; may be outside this workspace).")
    p.add_argument("--tool", choices=("auto",) + TOOLS, default="auto",
                   help="AI tool that runs the review (default: auto; also COMPLIANCE_REVIEW_TOOL).")
    p.add_argument("--model", help="Model name, passed to the tool's --model option.")
    p.add_argument("--subjects", default="all", help="'all' or comma-separated skill names (default: all).")
    p.add_argument("--advanced", action="store_true",
                   help="Turn on advanced usage (IaC review and CLI analyzers).")
    p.add_argument("--analyzers", default="auto", help="Analyzers to run with --advanced (default: auto).")
    p.add_argument("--out-file", help="Also keep the report at this path (default: only docs/reports/).")
    p.add_argument("--no-report", action="store_true", help="Don't print the report; print only the run summary.")
    p.add_argument("--summary-json", help="Write the run summary (status, duration, cost, tokens) as JSON here.")
    p.add_argument("--timeout", type=float, default=float(env.get("COMPLIANCE_REVIEW_TIMEOUT_MIN", 60)),
                   help="Time limit in minutes (default: 60; also COMPLIANCE_REVIEW_TIMEOUT_MIN).")
    p.add_argument("--progress", type=float, default=30,
                   help="Heartbeat interval in seconds for progress lines on stderr; 0 turns progress off (default: 30).")
    p.add_argument("--copilot-request-usd", type=float, default=DEFAULT_COPILOT_REQUEST_USD,
                   help=f"Price per Copilot premium request for the cost estimate (default: {DEFAULT_COPILOT_REQUEST_USD}).")
    p.add_argument("--prices",
                   help="JSON file of USD-per-million-token prices that override or extend the built-in table, "
                        "keyed by model, e.g. {\"claude-opus-5-5\": {\"input\": 4, \"output\": 20, \"cacheRead\": 0.2, "
                        "\"cacheWrite5m\": 5, \"cacheWrite1h\": 8}}. Unstated cache prices default to 0.1x, "
                        "1.25x and 2x the input price.")
    p.add_argument("--allow-tool", action="append",
                   help="Claude only: add a tool rule to the allowed list, e.g. \"Bash(dotnet list:*)\"; repeat for more.")
    p.add_argument("--tool-arg", action="append",
                   help="Extra argument for the AI tool's CLI; repeat for more, e.g. --tool-arg=--max-budget-usd --tool-arg=5.")
    p.add_argument("--dry-run", action="store_true", help="Print the command that would run, then stop.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass
    return run(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
