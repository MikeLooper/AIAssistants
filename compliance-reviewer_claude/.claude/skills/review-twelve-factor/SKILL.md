---
name: review-twelve-factor
description: 'Reviews an application against the Twelve-Factor App methodology, one check per factor. Use when the compliance-reviewer orchestrator delegates the Application Design / Twelve-Factor subject.'
user-invocable: false
---

# Review: Twelve-Factor App

One check per factor from https://12factor.net/, each linked to its own page.

## Inputs

Config files, `Dockerfile`, `docker-compose*.yml`, entry point files, dependency manifests, `.env.example`, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Evaluate each of the twelve factors against the files in scope. Mark N/A only if a factor genuinely doesn't apply (rare).
3. For factors that reference config/secrets, cross-check with what `review-security-operational` finds on Secrets Management, but only raise a finding here for the twelve-factor angle (config stored in env vs. in code).

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
