---
name: job-search-reporting
description: "Use when the job-search agent needs to write the timestamped report.json and report.html output for a job-search run, using templates/report.html.j2 when present."
---

# Job Search Reporting Skill

## Objective
Write the final `report.json` and `report.html` artifacts for a job-search run into a timestamped directory, then make the HTML report available to the user.

## Required Inputs
- `generated`: timestamp string for the run.
- `match_pct`: recommendation threshold used.
- `results`: array of per-URL results, each with `url` and `jobs` (may be empty when no jobs are found).
- Each job includes `job_url`, `attributes`, `match_score`, `match_details`, `recommended` (see `job-search-attributes` and `job-search-scoring` skills for how these are produced).

## Report Output Requirements
Create timestamped output folder under `reports/`:
- Naming format: `YYYY-MM-DD_HH-MM`
- Write:
  - `report.json`: full raw results and scoring details
  - `report.html`: rendered via `templates/report.html.j2` if present, otherwise fallback HTML

### report.json shape
Top-level fields:
- `generated`: timestamp string for the run
- `match_pct`: recommendation threshold used
- `results`: array of per-URL extraction results

Each item in `results`:
- `url`: source search URL
- `jobs`: array of extracted job records (may be empty when no jobs are found)

Each job in `jobs`:
- `job_url`: job detail URL
- `attributes`: extracted attributes object, in this order when present:
  1. `Job Title`
  2. `Programming Language`
  3. `Tools`
  4. `Salary Range`
  - Append any additional attributes after these four, preserving original `attributes.txt` order.
- `match_score`: integer percentage score for the job
- `match_details`: array of per-rule evaluations, each with `rule`, `matched`, `extracted_value`, `reason`
- `recommended`: boolean flag indicating threshold pass/fail

Example shape:
```json
{
  "generated": "2026-08-07_19-23",
  "match_pct": 75,
  "results": [
    {
      "url": "https://example.com/jobs?q=architect",
      "jobs": [
        {
          "job_url": "https://example.com/job/123",
          "attributes": {
            "Job Title": "Solutions Architect",
            "Programming Language": "Python, Java",
            "Tools": "AWS, EC2, CI/CD",
            "Salary Range": "$170k - $220k"
          },
          "match_score": 66,
          "match_details": [
            {
              "rule": "Job Title=Solutions Architect",
              "matched": true,
              "extracted_value": "Solutions Architect",
              "reason": "Substring match on extracted Job Title"
            }
          ],
          "recommended": false
        }
      ]
    }
  ]
}
```

### report.html rendering
Render from `templates/report.html.j2` when present, otherwise use a fallback HTML version.

Top-level template inputs:
- `timestamp` (displayed in title and meta line)
- `match_pct` (displayed as match threshold in meta line)
- `results` (per-URL sections)
- `total_jobs` (summary bar)
- `recommended` (summary bar)

Summary bar values shown:
- `Search URLs`: `results | length`
- `Total jobs found`: `total_jobs`
- `Recommended`: `recommended`

Per URL section behavior:
- Always show `result.url` in URL header
- If `result.error` exists, show an error box
- Else if `result.jobs` is empty, show a no-jobs message
- Else render job cards

Per job card values:
- title from `job.attributes['Job Title']` (fallback `(no title)`)
- job link from `job.job_url` (fallback `(no URL)`)
- score badge from `job.match_score`
- recommendation badge when `job.recommended` is true
- match table rows from `job.match_details` with `rule`, `matched`, `extracted_value`, `reason`

## Execution Safety and Reliability
- If no jobs are extracted, still emit reports with zero counts.
- Never let a rendering failure drop the raw `report.json`; write JSON first, then render HTML.

## Output Response Contract
After writing reports, report back:
1. Exact output directory and generated files.
2. Total jobs extracted and recommended count.
3. Whether `--open-report` was requested; when requested, runtime attempts to open the HTML report in the system browser.
