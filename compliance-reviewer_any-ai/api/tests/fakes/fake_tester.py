"""Stand-in for test/logic/test_*.py in the API tests. FAKE_TESTER_MODE picks the outcome:
pass (default), fail, error, none (writes no result), sleep (waits 60 s)."""
import argparse
import json
import os
import sys
import time
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--tool")
p.add_argument("--model")
p.add_argument("--min-found")
p.add_argument("--timeout")
p.add_argument("--results-dir")
p.add_argument("--progress")
p.add_argument("--no-build", action="store_true")
a = p.parse_args()
app = Path(sys.argv[0]).stem.replace("test_", "")  # e.g. api_dotnet
kind, lang = app.split("_")
app = f"{kind}s-" + {"dotnet": "dotNET", "java": "java", "python": "python"}[lang]
mode = os.environ.get("FAKE_TESTER_MODE", "pass")
print("ARGS " + json.dumps(sys.argv[1:]), flush=True)
if mode == "sleep":
    time.sleep(60)
if mode == "none":
    sys.exit(2)
out = Path(a.results_dir) / "2026-11-16_120000-claude"
out.mkdir(parents=True, exist_ok=True)
verdict = mode
result = {"app": app, "verdict": verdict, "runId": "r1", "overallScore": 55, "overallBand": "Fair"}
if verdict == "error":
    result["error"] = "build failed"
(out / f"{app}-result.json").write_text(json.dumps(result))
(out / f"{app}-result.md").write_text(f"# {app} - {verdict.upper()}\n")
if verdict != "error":
    (out / f"{app}-report.md").write_text("# Reviewer report\n")
sys.exit({"pass": 0, "fail": 1}.get(verdict, 2))
