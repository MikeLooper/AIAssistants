"""
job_search_agent.py — Main entry point for the Job Search Agent.

Usage:
    python job_search_agent.py
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from extractors.dispatcher import get_extractor
from matcher import compute_match
from reporter import generate_report

BASE_DIR = Path(__file__).resolve().parent
REPORT_BASE = Path(r"C:\Working\Storage\Dev\GitHub\AIAssistants\job-search\reports")
DEFAULT_URLS_PATH = BASE_DIR / "urls.txt"
DEFAULT_ATTRIBUTES_PATH = BASE_DIR / "attributes.txt"
DEFAULT_TARGETS_PATH = BASE_DIR / "targets.txt"
DEFAULT_MATCH_PCT = 75


def load_lines(path: str) -> list[str]:
    """Return non-blank, non-comment lines from a text file."""
    result = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                result.append(stripped)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Job Search Agent")
    parser.add_argument(
        "--urls",
        default=str(DEFAULT_URLS_PATH),
        help=f"Path to search-URL list file (default: {DEFAULT_URLS_PATH})",
    )
    parser.add_argument(
        "--attributes",
        default=str(DEFAULT_ATTRIBUTES_PATH),
        help=f"Path to attributes list file (default: {DEFAULT_ATTRIBUTES_PATH})",
    )
    parser.add_argument(
        "--targets",
        default=str(DEFAULT_TARGETS_PATH),
        help=f"Path to target rules file (default: {DEFAULT_TARGETS_PATH})",
    )
    parser.add_argument(
        "--match-pct",
        default=DEFAULT_MATCH_PCT,
        type=int,
        help=(
            "Minimum match percentage to flag a job as recommended (0-100) "
            f"(default: {DEFAULT_MATCH_PCT})"
        ),
    )
    args = parser.parse_args()

    urls       = load_lines(args.urls)
    attributes = load_lines(args.attributes)
    targets    = load_lines(args.targets)
    match_pct  = args.match_pct

    if not urls:
        print("ERROR: No URLs found in", args.urls, file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.now().strftime("1%Y-%m-%d_%H-%M")
    report_dir = REPORT_BASE / timestamp
    report_dir.mkdir(parents=True, exist_ok=True)

    all_results: list[dict] = []

    for url in urls:
        print(f"\n{'='*60}")
        print(f"Processing: {url}")
        print('='*60)

        extractor = get_extractor(url)
        try:
            jobs = extractor.extract(url, attributes)
        except Exception as exc:  # noqa: BLE001
            print(f"  ERROR extracting jobs from {url}: {exc}", file=sys.stderr)
            all_results.append({"url": url, "jobs": [], "error": str(exc)})
            continue

        scored_jobs = []
        for job in jobs:
            score, details = compute_match(job["attributes"], targets)
            job["match_score"]   = score
            job["match_details"] = details
            job["recommended"]   = score >= match_pct
            scored_jobs.append(job)
            flag = "✅ RECOMMENDED" if job["recommended"] else ""
            print(f"  [{score:3d}%] {job['attributes'].get('Job Title','(no title)')}"
                  f"  {flag}")

        all_results.append({"url": url, "jobs": scored_jobs})

    # Write JSON
    json_path = report_dir / "report.json"
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"generated": timestamp, "match_pct": match_pct,
                   "results": all_results}, fh, indent=2)

    # Write HTML
    html_path = generate_report(all_results, match_pct, timestamp, report_dir)
    os.startfile(str(html_path))

    print(f"\n{'='*60}")
    print(f"Report written to: {report_dir}")
    print(f"  HTML: {html_path.name}")
    print(f"  JSON: {json_path.name}")


if __name__ == "__main__":
    main()
