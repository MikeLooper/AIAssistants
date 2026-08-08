---
name: job-search-scoring
description: "Use when the job-search agent needs to evaluate settings/targets.txt rules against extracted job attributes, compute match percentage, and mark recommended jobs against a threshold."
---

# Job Search Scoring Skill

## Objective
Evaluate each extracted job against the configured target rules, compute a match score, and flag recommendations.

## Required Inputs
- `targets`: ordered list of raw target rule strings from the `job-search-config` skill.
- `match_pct`: recommendation threshold (0-100).
- A job record with `extracted_attributes` (or `attributes`) produced by the `job-search-attributes` skill.

## Target Matching Rules
Support all three formats exactly:
1. Exact attribute match: `AttributeName=Value`
2. OR options: `AttributeName=Value1 OR Value2 OR Value3`
3. Salary inclusion: `Salary Range Includes <amount>`

Matching behavior:
- Case-insensitive substring matching for attribute rules.
- OR matches if any option is found.
- Salary inclusion matches if the normalized numeric amount is contained by the extracted salary range semantics.

Salary normalization examples:
- `200000`, `200K`, `$200K`, `$200,000` -> `200000`

Salary range semantics examples:
- `$150K-$250K` includes `200K`
- `Up to $300K` includes amounts `<= 300K`
- `$200K+` includes amounts `>= 200K`

## Scoring and Recommendation
For each job:
- Evaluate every rule and produce rule-level details:
  - `rule`
  - `matched` (boolean)
  - `extracted_value`
  - `reason`
- Compute:
  - `matched_count`
  - `total_rules`
  - `match_percentage = (matched_count / total_rules) * 100`
- Recommendation flag:
  - `is_recommended = match_percentage >= match_pct`
  - `recommendation_label = "RECOMMENDED"` when true
- If `total_rules` is 0, set `match_percentage = 0` and `is_recommended = false` rather than dividing by zero.

## Output Contract
Attach to each job record:
- `match_score`: integer percentage score for the job.
- `match_details`: array of per-rule evaluations (`rule`, `matched`, `extracted_value`, `reason`).
- `recommended`: boolean flag indicating threshold pass/fail.
