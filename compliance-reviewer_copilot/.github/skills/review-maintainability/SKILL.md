---
name: review-maintainability
description: 'Reviews modularity, readability, documentation and technical debt. Use when the compliance-reviewer orchestrator delegates the Operations / Maintainability subject.'
user-invocable: false
---

# Review: Maintainability

Assesses modularity, readability, documentation completeness, and signs of accumulated technical debt.

## Inputs

README/docs files, folder structure, module boundaries, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check the repo has a README covering setup, running, and testing instructions.
3. Check module/folder boundaries are clear and consistent with the architecture (cross-check with `review-software-quality`'s Architecture Patterns sub-subject without duplicating its findings).
4. Look for TODO/FIXME/HACK markers or deprecated-but-still-used code as technical debt signals.
5. Check onboarding friction: are prerequisites, environment variables, and build/run steps documented?

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
