"""Run all three Unit Test Coverage Reviewer validation tests, serially (default) or in parallel.

Usage:
  python test/logic/test_all.py [--parallel] [--tool claude|copilot] [--min-found 90] [--only dotNET,python]

Exit code: 0 all passed, 1 at least one failed, 2 at least one could not be scored.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import harness

# Each test gets its own harness-assigned Run ID, so parallel runs can't collide. The stagger only spreads out
# the start-up load on the AI tool (rate limits).
STAGGER_SECONDS = 10


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Run all three Unit Test Coverage Reviewer validation tests.")
    harness.add_common_args(p)
    p.add_argument("--parallel", action="store_true", help="Run the three reviews concurrently.")
    p.add_argument("--only", help="Comma-separated subset of dotNET, java, python (apis-dotNET etc. also accepted).")
    args = p.parse_args(argv)

    langs = list(harness.LANGS)
    if args.only:
        wanted = {a.strip().lower().removeprefix(f"{harness.KIND}-") for a in args.only.split(",") if a.strip()}
        langs = [l for l in harness.LANGS if l.lower() in wanted]
        unknown = wanted - {l.lower() for l in langs}
        if unknown:
            p.error(f"unknown app(s): {', '.join(sorted(unknown))}; choose from {', '.join(harness.LANGS)}")

    tool, reason = harness.detect_tool(args.tool)
    args.tool = tool  # resolve once so every test uses the same tool
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    session_dir = None if args.dry_run else (args.results_dir / f"{stamp}-{tool}-all").resolve()
    print(f"Running {len(langs)} test(s) {'in parallel' if args.parallel else 'serially'} with {tool} ({reason}).",
          flush=True)

    if args.parallel and not args.dry_run:
        with ThreadPoolExecutor(max_workers=len(langs)) as pool:
            futures = []
            for i, lang in enumerate(langs):
                if i:
                    time.sleep(STAGGER_SECONDS)
                futures.append(pool.submit(harness.run_test, lang, args, session_dir))
            results = [f.result() for f in futures]
    else:
        results = []
        for lang in langs:
            r = harness.run_test(lang, args, session_dir)
            if r["verdict"] != "dry-run":
                print(harness.summarize(r), flush=True)
            results.append(r)

    if args.dry_run:
        return harness.EXIT_PASS

    verdicts = [r["verdict"] for r in results]
    lines = ["# Unit Test Coverage Reviewer validation — all tests", "",
             f"- Tool: {tool} ({reason})", f"- Mode: {'parallel' if args.parallel else 'serial'}",
             f"- Required share of gaps: {args.min_found:g}%",
             f"- Passed {verdicts.count('pass')}, failed {verdicts.count('fail')}, errors {verdicts.count('error')}", "",
             "| App | Verdict | Gaps found | Missed | False positives | Other problems | Reviewer problem % | Details |",
             "|---|---|---|---|---|---|---|---|"]
    for r in results:
        s = r.get("score")
        if s:
            missed = ", ".join(g["id"] for g in s["gaps"] if g["status"] != "found") or "—"
            fps = ", ".join(c["id"] for c in s["falsePositives"]) or "—"
            pct = (r.get("metrics") or {}).get("problemPct")
            lines.append(f"| {r['app']} | {r['verdict']} | {len(s['found'])}/{s['total']} ({s['foundPct']:.0f}%) | "
                         f"{missed} | {fps} | {len(s['unscoredProblems'])} | {pct + '%' if pct else '—'} | "
                         f"[result]({r['app']}-result.md) |")
        else:
            lines.append(f"| {r['app']} | {r['verdict']} | — | — | — | — | — | {r.get('error')} |")
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (session_dir / "summary.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")

    print()
    for r in results:
        print(harness.summarize(r))
    print(f"\nSummary: {session_dir / 'summary.md'}")
    return harness.exit_code(verdicts)


if __name__ == "__main__":
    sys.exit(main())
