---
name: review-monitoring
description: 'Reviews alerting rules and dashboards-as-code. Use when the compliance-reviewer orchestrator delegates the Operations / Monitoring subject; N/A when no infrastructure-as-code is found.'
user-invocable: false
---

# Review: Monitoring

Assesses alerting rules and dashboards-as-code — the parts of monitoring that can only be evaluated from infrastructure-as-code. Health check endpoints and SLO/SLI documentation are reviewed by `review-observability` instead, since they're visible from source/docs alone.

This subject is entirely IaC-driven: when `compliance-inventory` reports `iacFound: false`, the orchestrator marks it `applicable: false` and skips the subagent call rather than invoking this skill.

## Inputs

Alert/dashboard-as-code files, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check alerting rules exist for key failure conditions (error rate, latency, resource exhaustion), ideally as code rather than only click-ops.
3. Check dashboards are defined as code/config in the repo, not only manually built in a portal.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
