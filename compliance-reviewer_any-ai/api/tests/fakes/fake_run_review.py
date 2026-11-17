"""Stand-in for scripts/run_review.py in the API tests. Its behaviour is chosen by marker files in the target:
FAIL -> the reviewer reports a failure (exit 1); SLEEP -> waits 60 s; CRASH -> exits 2 with no summary;
otherwise it writes a report and a completed summary (exit 0)."""
import argparse
import json
import sys
import time
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("target")
p.add_argument("--tool")
p.add_argument("--model")
p.add_argument("--subjects")
p.add_argument("--out-file")
p.add_argument("--summary-json")
p.add_argument("--no-report", action="store_true")
p.add_argument("--timeout")
p.add_argument("--progress")
p.add_argument("--advanced", action="store_true")
p.add_argument("--analyzers")
a = p.parse_args()
target = Path(a.target)
print("ARGS " + json.dumps(sys.argv[1:]), flush=True)
print("FILES " + json.dumps(sorted(x.relative_to(target).as_posix() for x in target.rglob("*") if x.is_file())), flush=True)
if (target / "SLEEP").exists():
    time.sleep(60)
if (target / "CRASH").exists():
    print("boom", flush=True)
    sys.exit(2)
if (target / "FAIL").exists():
    Path(a.summary_json).write_text(json.dumps({"status": "failed", "error": "step 01: inventory failed"}))
    sys.exit(1)
Path(a.out_file).write_text(f"# Report for {target.name}\n\nScore 87\n", encoding="utf-8")
Path(a.summary_json).write_text(json.dumps({"status": "completed", "runId": "2026-11-16_1200-" + target.name,
                                            "overallScore": 87, "overallBand": "Good", "usage": {"costUsd": 1.5}}))
print("done", flush=True)
