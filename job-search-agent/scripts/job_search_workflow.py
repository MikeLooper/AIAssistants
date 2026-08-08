from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import re
from typing import Any

from job_search_extractor import read_non_comment_lines, read_alias_terms, run_extraction

try:
    from jinja2 import Template
except Exception:  # pragma: no cover
    Template = None


def normalize_amount(raw: str) -> int | None:
    value = raw.strip().lower().replace("$", "").replace(",", "")
    match = re.fullmatch(r"(\d+(?:\.\d+)?)(k)?", value)
    if not match:
        return None
    number = float(match.group(1))
    if match.group(2):
        number *= 1000
    return int(number)


def parse_salary_range(raw: str) -> tuple[int | None, int | None]:
    if not raw:
        return (None, None)
    matches = re.findall(r"\$?\d[\d,]*(?:\.\d+)?[kK]?", raw)
    numbers = [n for n in (normalize_amount(item) for item in matches) if n is not None]
    text = raw.lower()
    if "up to" in text and numbers:
        return (None, numbers[0])
    if raw.strip().endswith("+") and numbers:
        return (numbers[0], None)
    if len(numbers) >= 2:
        lo = min(numbers[0], numbers[1])
        hi = max(numbers[0], numbers[1])
        return (lo, hi)
    if len(numbers) == 1:
        return (numbers[0], numbers[0])
    return (None, None)


def salary_includes(salary_value: str, target_amount: int) -> bool:
    lo, hi = parse_salary_range(salary_value)
    if lo is None and hi is None:
        return False
    if lo is None:
        return target_amount <= (hi or -1)
    if hi is None:
        return target_amount >= lo
    return lo <= target_amount <= hi


def parse_target_rules(target_lines: list[str]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for line in target_lines:
        salary_match = re.match(r"(?i)^\s*salary\s+range\s+includes\s+(.+?)\s*$", line)
        if salary_match:
            parsed.append({"type": "salary_includes", "rule": line, "amount_raw": salary_match.group(1).strip()})
            continue

        attr_match = re.match(r"^([^=]+)=(.+)$", line)
        if attr_match:
            attr_name = attr_match.group(1).strip()
            options = [x.strip() for x in re.split(r"(?i)\s+OR\s+", attr_match.group(2).strip()) if x.strip()]
            parsed.append({"type": "attr_or", "rule": line, "attribute": attr_name, "options": options})
    return parsed


def score_job(attributes: dict[str, str], parsed_rules: list[dict[str, Any]], match_pct: int) -> tuple[int, list[dict[str, Any]], bool]:
    details: list[dict[str, Any]] = []
    matched_count = 0

    for rule in parsed_rules:
        if rule["type"] == "salary_includes":
            extracted_value = attributes.get("Salary Range", "")
            target_amount = normalize_amount(rule["amount_raw"]) or 0
            matched = salary_includes(extracted_value, target_amount)
            reason = "Salary range includes target amount" if matched else "Salary range did not include target amount"
        else:
            extracted_value = attributes.get(rule["attribute"], "")
            extracted_lower = extracted_value.lower()
            hit = next((opt for opt in rule["options"] if opt.lower() in extracted_lower), None)
            matched = hit is not None
            reason = f"Matched option '{hit}'" if matched else "No option matched"

        if matched:
            matched_count += 1

        details.append(
            {
                "rule": rule["rule"],
                "matched": matched,
                "extracted_value": extracted_value,
                "reason": reason,
            }
        )

    total_rules = len(parsed_rules)
    score = int(round((matched_count / total_rules) * 100)) if total_rules else 0
    recommended = score >= match_pct if total_rules else False
    return score, details, recommended


def render_fallback_html(timestamp: str, match_pct: int, results: list[dict[str, Any]], total_jobs: int, recommended_count: int) -> str:
    lines = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'><title>Job Search Report</title></head><body>",
        f"<h1>Job Search Report</h1><p>Generated: {timestamp} | Threshold: {match_pct}%</p>",
        f"<p>Total jobs: {total_jobs} | Recommended: {recommended_count}</p>",
    ]
    for result in results:
        lines.append(f"<h2>{result['url']}</h2>")
        if result.get("error"):
            lines.append(f"<p>Error: {result['error']}</p>")
            continue
        if not result.get("jobs"):
            lines.append("<p>No jobs found.</p>")
            continue
        for job in result["jobs"]:
            lines.append(f"<h3>{job['attributes'].get('Job Title','(no title)')}</h3>")
            lines.append(f"<p><a href='{job.get('job_url','')}'>{job.get('job_url','(no URL)')}</a></p>")
            lines.append(f"<p>Score: {job.get('match_score', 0)}% | Recommended: {job.get('recommended', False)}</p>")
    lines.append("</body></html>")
    return "\n".join(lines)


def write_reports(report_dir: Path, payload: dict[str, Any], template_path: Path) -> None:
    report_json_path = report_dir / "report.json"
    report_json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    total_jobs = sum(len(item.get("jobs", [])) for item in payload["results"])
    recommended_count = sum(
        1 for item in payload["results"] for job in item.get("jobs", []) if job.get("recommended")
    )

    if Template is not None and template_path.exists():
        html_template = Template(template_path.read_text(encoding="utf-8"))
        html = html_template.render(
            timestamp=payload["generated"],
            match_pct=payload["match_pct"],
            results=payload["results"],
            total_jobs=total_jobs,
            recommended=recommended_count,
        )
    else:
        html = render_fallback_html(
            timestamp=payload["generated"],
            match_pct=payload["match_pct"],
            results=payload["results"],
            total_jobs=total_jobs,
            recommended_count=recommended_count,
        )

    (report_dir / "report.html").write_text(html, encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run full job-search workflow: per-card extraction -> scoring -> report generation."
    )
    parser.add_argument("--settings-dir", default="settings", help="Settings directory path (default: settings).")
    parser.add_argument("--match-pct", type=int, default=75, help="Recommendation threshold percent (default: 75).")
    parser.add_argument("--url", action="append", help="Optional URL override. Provide more than once for multiple URLs.")
    parser.add_argument("--headless", action="store_true", help="Run extraction browser in headless mode.")
    parser.add_argument("--max-cards", type=int, default=50, help="Max job cards per URL.")
    parser.add_argument("--open-report", action="store_true", help="Open generated report.html after run.")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    settings_dir = Path(args.settings_dir)

    attributes = read_non_comment_lines(settings_dir / "attributes.txt")
    targets = read_non_comment_lines(settings_dir / "targets.txt")
    language_aliases = read_alias_terms(settings_dir / "programminglanguages.txt")
    tool_aliases = read_alias_terms(settings_dir / "tools.txt")

    urls = args.url if args.url else read_non_comment_lines(settings_dir / "urls.txt")
    if not urls:
        raise SystemExit("No active URLs found. Check settings/urls.txt and remove comment markers.")

    extraction = run_extraction(
        urls=urls,
        requested_attributes=attributes,
        language_aliases=language_aliases,
        tool_aliases=tool_aliases,
        headless=bool(args.headless),
        max_cards=max(1, args.max_cards),
    )

    parsed_rules = parse_target_rules(targets)
    scored_results: list[dict[str, Any]] = []

    for result in extraction["results"]:
        if result.get("error"):
            scored_results.append({"url": result["url"], "error": result["error"], "jobs": []})
            continue

        scored_jobs: list[dict[str, Any]] = []
        for job in result.get("jobs", []):
            attrs = job.get("attributes", {})
            score, match_details, recommended = score_job(attrs, parsed_rules, args.match_pct)
            scored_jobs.append(
                {
                    "job_url": job.get("job_url", ""),
                    "attributes": attrs,
                    "source_url": job.get("source_url", result["url"]),
                    "source_site": job.get("source_site", result.get("site", "")),
                    "match_score": score,
                    "match_details": match_details,
                    "recommended": recommended,
                }
            )

        scored_results.append({"url": result["url"], "jobs": scored_jobs})

    now = datetime.now()
    stamp = now.strftime("%Y-%m-%d_%H-%M")
    report_dir = Path("reports") / stamp
    report_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated": stamp,
        "match_pct": args.match_pct,
        "results": scored_results,
    }

    write_reports(report_dir, payload, Path("templates") / "report.html.j2")

    total_jobs = sum(len(item.get("jobs", [])) for item in scored_results)
    recommended_count = sum(
        1 for item in scored_results for job in item.get("jobs", []) if job.get("recommended")
    )

    summary = {
        "inputs": {
            "urls": "settings/urls.txt" if args.url is None else "--url overrides",
            "attributes": "settings/attributes.txt",
            "targets": "settings/targets.txt",
            "programminglanguages": "settings/programminglanguages.txt",
            "tools": "settings/tools.txt",
            "match_pct": args.match_pct,
        },
        "output_dir": str(report_dir),
        "files": [str(report_dir / "report.json"), str(report_dir / "report.html")],
        "total_jobs": total_jobs,
        "recommended": recommended_count,
        "failures": extraction["summary"].get("failures", []),
    }

    print(json.dumps(summary, indent=2))

    if args.open_report:
        try:
            import webbrowser

            webbrowser.open((report_dir / "report.html").resolve().as_uri())
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
