---
name: review-software-quality
description: 'Reviews source code against ISO/IEC 25010 quality characteristics, cyclomatic complexity, duplication and common code smells, plus design pattern usage/misuse and architecture layering, coupling and cloud pattern fit. Use when the compliance-reviewer orchestrator delegates the Software Quality subject (covering the Software Quality, Design Patterns and Architecture Patterns sub-subjects in one pass).'
user-invocable: false
---

# Review: Software Quality

Assesses source code against the ISO/IEC 25010 quality model, complexity/duplication/code-smell checks, appropriate use of design patterns, and architecture layering/coupling — merged into one skill (one subagent pass per batch) because these three used to review largely the same files and repeatedly flagged the same god-object/high-coupling issues under different subjects. Each checklist item still carries its original `subSubject` (`Software Quality`, `Design Patterns` or `Architecture Patterns`) so the report keeps the same breakdown.

## Inputs

All source files in scope (sampled if the repo is very large), entry points, module/project folder structure, IaC files, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. For each file, look for excessive function/method length, deep nesting, high cyclomatic complexity (many branches in one function), duplicated blocks, long parameter lists, and god-classes/god-functions (`subSubject: Software Quality`).
3. Identify design patterns in use (factory, builder, strategy, observer, decorator, singleton, repository, etc.), judge whether each fits its problem, and flag anti-patterns: singleton misuse for shared mutable state, excessive inheritance depth, inappropriate static state, pattern applied without a matching problem (`subSubject: Design Patterns`). Do not re-flag a god-class already reported under `SQ-04` — `DP-03` was folded into it.
4. Infer layering (e.g. presentation/API, business logic, data access) from folder and namespace structure; flag layer violations, assess coupling/cohesion between modules, and check whether cloud design patterns (retry, circuit breaker, cache-aside, queue-based load leveling, strangler fig) are used where the architecture needs resilience/scale (`subSubject: Architecture Patterns`). `AP-05` (cloud resilience patterns) may overlap in evidence with `review-reliability`'s retry/circuit-breaker checks — that cross-subject duplicate is resolved by `compliance-report`'s aggregate step, not here.
5. Map Software Quality findings to the relevant ISO/IEC 25010 characteristic (functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability, portability) in the finding's `title`/`recommendation`.
6. Note strengths where a module is clearly well factored, a pattern clearly simplifies the design, or layering/cohesion is clean.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
