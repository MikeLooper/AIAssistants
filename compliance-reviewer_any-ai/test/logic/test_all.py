"""Run all nine Compliance Reviewer validation tests (APIs, UIs and MCP servers), serially (default) or in parallel.

Usage:
  python test/logic/test_all.py [--parallel] [--tool claude|copilot] [--min-found 90] [--only apis-java,uis-python,mcps-dotNET]

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

APPS = [(kind, lang) for kind in harness.KINDS for lang in harness.LANGS]

# The reviewer names runs `<YYYY-MM-DD_HHmm>-<short-target-name>`, so apis/X, uis/X and mcps/X started in the
# same minute could get the same runId. In parallel mode each kind starts this many seconds after the previous one.
STAGGER_SECONDS = 120


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Run all nine Compliance Reviewer validation tests.")
    harness.add_common_args(p)
    p.add_argument("--parallel", action="store_true", help="Run the nine reviews concurrently (staggered by kind).")
    p.add_argument("--only", help="Comma-separated subset, e.g. apis-dotNET,uis-java,mcps-python.")
    args = p.parse_args(argv)

    apps = APPS
    if args.only:
        wanted = {a.strip().lower() for a in args.only.split(",")}
        apps = [a for a in APPS if f"{a[0]}-{a[1]}".lower() in wanted]
        unknown = wanted - {f"{k}-{l}".lower() for k, l in apps}
        if unknown:
            p.error(f"unknown app(s): {', '.join(sorted(unknown))}; choose from "
                    + ", ".join(f"{k}-{l}" for k, l in APPS))

    tool, reason = harness.detect_tool(args.tool)
    args.tool = tool  # resolve once so every test uses the same tool
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    session_dir = None if args.dry_run else (args.results_dir / f"{stamp}-{tool}-all").resolve()
    print(f"Running {len(apps)} test(s) {'in parallel' if args.parallel else 'serially'} with {tool} ({reason}).",
          flush=True)

    if args.parallel and not args.dry_run:
        with ThreadPoolExecutor(max_workers=len(apps)) as pool:
            futures, last_kind = [], None
            for kind, lang in apps:
                if last_kind and kind != last_kind:
                    print(f"Waiting {STAGGER_SECONDS} s before starting the {kind} reviews (avoids runId collisions)...",
                          flush=True)
                    time.sleep(STAGGER_SECONDS)
                last_kind = kind
                futures.append(pool.submit(harness.run_test, kind, lang, args, session_dir))
            results = [f.result() for f in futures]
    else:
        results = []
        for kind, lang in apps:
            r = harness.run_test(kind, lang, args, session_dir)
            if r["verdict"] != "dry-run":
                print(harness.summarize(r), flush=True)
            results.append(r)

    if args.dry_run:
        return harness.EXIT_PASS

    verdicts = [r["verdict"] for r in results]
    lines = ["# Compliance Reviewer validation — all tests", "",
             f"- Tool: {tool} ({reason})", f"- Mode: {'parallel' if args.parallel else 'serial'}",
             f"- Required share of flaws: {args.min_found:g}%",
             f"- Passed {verdicts.count('pass')}, failed {verdicts.count('fail')}, errors {verdicts.count('error')}", "",
             "| App | Verdict | Flaws found | Missed | Unexpected errors | Unexpected warn/info | Reviewer score | Details |",
             "|---|---|---|---|---|---|---|---|"]
    for r in results:
        s = r.get("score")
        if s:
            lines.append(f"| {r['app']} | {r['verdict']} | {len(s['found'])}/{s['total']} ({s['foundPct']:.0f}%) | "
                         f"{', '.join(x['flaw'] for x in s['missed']) or '—'} | {len(s['unexpectedErrors'])} | "
                         f"{len(s['unexpectedOther'])} | {r.get('overallScore')} ({r.get('overallBand')}) | "
                         f"[result]({r['app']}-result.md) |")
        else:
            lines.append(f"| {r['app']} | {r['verdict']} | — | — | — | — | — | {r.get('error')} |")
    summary = "\n".join(lines) + "\n"
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "summary.md").write_text(summary, encoding="utf-8")
    (session_dir / "summary.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")

    print()
    for r in results:
        print(harness.summarize(r))
    print(f"\nSummary: {session_dir / 'summary.md'}")
    return harness.exit_code(verdicts)


if __name__ == "__main__":
    sys.exit(main())
