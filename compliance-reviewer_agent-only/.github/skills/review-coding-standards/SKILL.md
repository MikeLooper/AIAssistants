---
name: review-coding-standards
description: 'Reviews code against a generic coding-standards core plus C#, Java and Python language-specific style guides. Use when the compliance-reviewer orchestrator delegates the Implementation / Coding Standards subject.'
user-invocable: false
---

# Review: Coding Standards

Assesses code against a language-agnostic core plus the C#, Java and Python style guides, loaded only for detected languages.

## Inputs

All source files in scope (sampled if very large), per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` (generic core) and, for each detected language, `references/languages/<id>.md`.
2. Check naming conventions, formatting/indentation consistency, and comment quality against the generic core.
3. For each detected language, check the language-specific conventions (e.g. C# naming/casing, Java style guide rules, PEP 8).
4. Note strengths where a module is a good example of the applicable standard.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
