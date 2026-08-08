# Job Search Agent Workspace

## What This Agent Is For

The job-search agent is for repeatable, criteria-based job market analysis.

Use it when you want to:
- Search across multiple job boards from one run.
- Extract the same attributes from every listing.
- Apply consistent matching rules to all results.
- Use configured language and tool discovery data to extract and normalize values.
- Rank and recommend listings by match percentage.
- Produce machine-readable and human-readable reports.

## What It Can Accomplish

The agent can:
- Read and parse input configuration files: settings/urls.txt, settings/attributes.txt, settings/targets.txt, settings/programminglanguages.txt, and settings/tools.txt.
- Ignore comments and blank lines in those files.
- Route each URL to an extractor type by domain: Dice, LinkedIn, Glassdoor, Greenhouse, Remotive, or Generic fallback.
- Extract requested attributes for each discovered job.
- Evaluate each job against target rules: exact attribute match, OR match, and salary inclusion.
- Compute match percentage per job.
- Mark jobs as RECOMMENDED when score meets threshold.
- Generate timestamped report artifacts: report.html and report.json.
- Continue processing when one source fails, and record partial failures.

## Quick Start (60 Seconds)

First run checklist:
1. Open and confirm your search URLs in [settings/urls.txt](settings/urls.txt).
2. Open and confirm extracted fields in [settings/attributes.txt](settings/attributes.txt).
3. Open and confirm match rules in [settings/targets.txt](settings/targets.txt).
4. Review language aliases in [settings/programminglanguages.txt](settings/programminglanguages.txt) and tool aliases in [settings/tools.txt](settings/tools.txt).
4. Run this in chat: "Run the job-search workflow using default workspace inputs and a 75 percent threshold."
5. Check the newest timestamped folder under [reports](reports) for report.html and report.json.

If you are testing quickly, start with 1-2 URLs and a lower threshold like 70.

This workspace contains a custom AI agent named job-search that runs a configuration-driven job search analysis workflow.

The agent is designed to help you evaluate job listings at scale by reading a list of search URLs, extracting selected attributes, scoring listings against target rules, and generating report outputs.

## Core AI Objects In This Workspace

1. Agent definition: [.github/agents/job-search.agent.md](.github/agents/job-search.agent.md)
- Owns the end-to-end workflow directly: defines mission, behavior, success criteria, tool scope, and the order in which it applies the skills below.

2. Skill definitions, each focused on one stage of the pipeline:
- [.github/skills/job-search-config/SKILL.md](.github/skills/job-search-config/SKILL.md) — loads and parses the input files and resolves the match threshold.
- [.github/skills/job-search-extraction/SKILL.md](.github/skills/job-search-extraction/SKILL.md) — routes each URL to a site extractor and runs the raw extraction workflow (logic files under `Extractors/`).
- [.github/skills/job-search-attributes/SKILL.md](.github/skills/job-search-attributes/SKILL.md) — turns raw listing/detail text into requested attributes (Job Title, Programming Language, Tools, Salary Range).
- [.github/skills/job-search-scoring/SKILL.md](.github/skills/job-search-scoring/SKILL.md) — evaluates target rules, computes match percentage, and marks recommendations.
- [.github/skills/job-search-reporting/SKILL.md](.github/skills/job-search-reporting/SKILL.md) — writes report.json/report.html and opens the HTML report.

## Input Files

- URL list: [settings/urls.txt](settings/urls.txt). One URL per line, supports comments with #.
- Attribute list: [settings/attributes.txt](settings/attributes.txt). One attribute name per line.
- Target rules: [settings/targets.txt](settings/targets.txt). One matching rule per line, supports comments with #.
- Programming-language aliases: [settings/programminglanguages.txt](settings/programminglanguages.txt). One discovery/reporting value per line; use the left side of a colon for discovery and the right side for reporting.
- Tool aliases: [settings/tools.txt](settings/tools.txt). One discovery/reporting value per line; use the left side of a colon for discovery and the right side for reporting.

## Output Files

Each run should write to a timestamped folder under [reports](reports):
- reports/YYYY-MM-DD_HH-MM/report.html
- reports/YYYY-MM-DD_HH-MM/report.json

The JSON report should include:
- Generated timestamp
- Threshold used
- Summary counts
- Per-job scoring details and match explanations

## How To Use

Use direct instructions in chat targeting the job-search agent behavior.
The agent uses [settings/urls.txt](settings/urls.txt), [settings/attributes.txt](settings/attributes.txt), [settings/targets.txt](settings/targets.txt), [settings/programminglanguages.txt](settings/programminglanguages.txt), and [settings/tools.txt](settings/tools.txt) by default and does not require file path parameters.

You can also run the concrete workflow runner directly:

`python.exe scripts/job_search_workflow.py --headless --max-cards 10`

This command runs the full pipeline end-to-end:
1. Per-card click/read extraction via [scripts/job_search_extractor.py](scripts/job_search_extractor.py)
2. Target-rule scoring from [settings/targets.txt](settings/targets.txt)
3. Report generation to `reports/YYYY-MM-DD_HH-MM/report.json` and `report.html`

## Example Usage Prompts

Use any of these as copy/paste prompts.

1. Most basic run
"Run the job-search workflow."

2. Run with defaults
"Run the job-search workflow using default workspace inputs with a 75 percent threshold. Generate report outputs and summarize recommended jobs."

3. Custom threshold
"Run the job-search workflow with match threshold 70. Show routing by site, total extracted jobs, recommended count, and output folder path."

4. Troubleshooting-oriented run
"Execute the job-search workflow and include all partial failures per URL, including extractor type used and reason for failure."

5. Focused salary targeting
"Use the existing configuration and run scoring with emphasis on Salary Range Includes rules. Report how many jobs include 180K or higher."

6. Quick audit summary
"Run the job-search agent and return only summary metrics: total jobs, recommended jobs, counts by site, and report file locations."

## Recommended Rule Examples

Add lines like these to [settings/targets.txt](settings/targets.txt):

Job Title=Engineer OR Developer OR Architect
Programming Language=C# OR .NET OR Java
Salary Range Includes 150K

## Operational Notes

- LinkedIn extraction may require non-headless execution behavior.
- If one source fails, the workflow should continue with remaining URLs.
- If no jobs are extracted, reports should still be generated with zero-count summaries.

## Template

If present, this template is used for HTML rendering:
- [templates/report.html.j2](templates/report.html.j2)

## Workspace Layout

- [settings/attributes.txt](settings/attributes.txt)
- [settings/targets.txt](settings/targets.txt)
- [settings/urls.txt](settings/urls.txt)
- [settings/programminglanguages.txt](settings/programminglanguages.txt)
- [settings/tools.txt](settings/tools.txt)
- [reports](reports)
- [templates/report.html.j2](templates/report.html.j2)
- [.github/agents/job-search.agent.md](.github/agents/job-search.agent.md)
- [.github/skills/job-search-config/SKILL.md](.github/skills/job-search-config/SKILL.md)
- [.github/skills/job-search-extraction/SKILL.md](.github/skills/job-search-extraction/SKILL.md)
- [.github/skills/job-search-attributes/SKILL.md](.github/skills/job-search-attributes/SKILL.md)
- [.github/skills/job-search-scoring/SKILL.md](.github/skills/job-search-scoring/SKILL.md)
- [.github/skills/job-search-reporting/SKILL.md](.github/skills/job-search-reporting/SKILL.md)
- [scripts/job_search_extractor.py](scripts/job_search_extractor.py)
- [scripts/job_search_workflow.py](scripts/job_search_workflow.py)
