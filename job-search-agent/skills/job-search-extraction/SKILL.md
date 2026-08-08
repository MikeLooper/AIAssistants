---
name: job-search-extraction
description: "Use when the job-search agent needs to route a job search URL to the runtime extractor path (Dice, LinkedIn, Glassdoor, or generic fallback) and run the extraction workflow for that site."
---

# Job Search Extraction Skill

## Objective
Route each search URL to the correct site extractor by domain, then run that extractor's workflow to collect raw job listing and detail text for each candidate job.

For card-based job boards (left listing column + right details pane), extraction must iterate every visible job card, click each card, wait for the right-side details pane to update, and then extract data from that selected job before moving to the next card.

## URL Routing Rules
Map URL hostnames to runtime extraction branches:
- `dice.com` -> Dice branch
- `linkedin.com` -> LinkedIn branch
- `glassdoor.com` -> Glassdoor branch
- `greenhouse.io` -> Generic fallback branch
- `remotive.com` -> Generic fallback branch
- any other domain -> Generic fallback branch

Execution order for each URL:
1. Detect site from URL hostname and choose the runtime branch.
2. Navigate with Playwright and collect candidate cards or links.
3. For card-based pages:
	- identify all visible cards in the left results panel,
	- click each card one-by-one,
	- wait for the right details pane to refresh for that selected card,
	- extract `job_url` and right-pane detail text for that selected card.
4. Extract attributes using the runtime helpers and configured aliases.
5. Emit one normalized record per selected card that satisfies the extraction contract below.

## Extraction Contract
Each extracted job record should include:
- `source_url`
- `source_site`
- `job_url` (if available)
- `attributes` map where keys are items from `attributes.txt`

## Card-Based Page Requirement
When a board shows a list of cards and a details pane:
- Do not stop after the first selected/default card.
- Process each visible card in the list during the run.
- Read attributes from the right-side selected detail pane, not only from list snippets.
- Capture the selected job's canonical URL for each card record.

## Execution Safety and Reliability
- If a URL fails extraction, continue processing remaining URLs and record the error in result metadata.
- Never stop the entire run for one board failure.
- If no jobs are extracted for a URL, still emit a result entry with an empty `jobs` array.
- Deduplicate candidates by `job_url` and title.
