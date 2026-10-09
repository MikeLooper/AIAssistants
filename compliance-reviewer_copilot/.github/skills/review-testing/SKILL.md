---
name: review-testing
description: 'Reviews the test pyramid balance, coverage signals and test quality. Use when the compliance-reviewer orchestrator delegates the Implementation / Testing subject.'
user-invocable: false
---

# Review: Testing

Assesses the test pyramid balance (unit/integration/E2E), coverage signals, and the quality of the tests themselves.

## Inputs

Test folders, test config, CI test steps, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Count/estimate the proportion of unit vs. integration vs. end-to-end tests; flag an inverted pyramid (many slow E2E tests, few fast unit tests).
3. Check coverage signals: a coverage tool/config exists and CI enforces or reports a threshold.
4. Check test quality: tests assert real behavior (not just "no exception thrown"), avoid over-mocking that hides real bugs, and have clear arrange/act/assert structure.
5. Check CI actually runs the test suite on every change (cross-reference with `review-software-lifecycle` findings without duplicating them).

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
