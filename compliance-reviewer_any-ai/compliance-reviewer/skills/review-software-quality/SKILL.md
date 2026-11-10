---
name: review-software-quality
description: 'Reviews source code for function size, complexity, duplication and other code smells, exception design, design-pattern fit and misuse, layering, cycles, cohesion, cross-cutting placement and architecture-style constraints, plus generic and per-language (C#, Java, Python) coding standards, against local summaries of ISO/IEC 25010:2023, a local Software Quality Rubric, Azure Architecture Center styles, Martin Fowler, Microsoft C# conventions, Google Java Style and PEP 8/257. Use when the compliance-reviewer orchestrator delegates the Software Quality subject (Software Quality, Design Patterns, Architecture Patterns and Coding Standards sub-subjects in one pass).'
user-invocable: false
---

# Review: Software Quality

Assesses source code against a local Software Quality Rubric (thresholds plus confirmation), localized
architecture-style and layering guidance, and per-language style guides, and classifies every finding by an
ISO/IEC 25010:2023 sub-characteristic. Four sub-subjects run in one pass; each checklist item keeps its
`subSubject` (`Software Quality`, `Design Patterns`, `Architecture Patterns`, `Coding Standards`).

## Inputs

The capped, sampled list of non-test source files assigned by `compliance-inventory` (entry points plus
representative files per layer/folder), plus any formatter/analyzer configuration and project-reference files it
lists. Review only those files.

## Standards (local, authoritative)

- `references/standards/software-quality-rubric.md` — SQR-01…SQR-37. Always load.
- `references/standards/iso-25010.md` — ISO-01…ISO-40 (classification only). Always load.
- `references/standards/azure-architecture.md` — AAS-01…AAS-20. Always load.
- `references/standards/fowler-bliki.md` — MFB-01…MFB-06. Always load.
- `references/standards/fowler-refactoring-catalog.md` — FRC-01…FRC-23 (remedies only). Always load.
- `references/standards/microsoft-csharp.md` — MSC-01…MSC-24. Load only if C# is detected.
- `references/standards/google-java-style.md` — GJS-01…GJS-34. Load only if Java is detected.
- `references/standards/python-peps.md` — PEP-01…PEP-23. Load only if Python is detected.
- `references/standards/google-typescript-style.md` — GTS-01…GTS-23. Load only if JavaScript/TypeScript is detected.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, the always-loaded standards files, and for each
   detected language its `references/languages/<id>.md` and the standards file it points to. For any other
   language (e.g. JavaScript/TypeScript) use the generic rubric elements only and add
   `localized-standard-gap: no language standard for <language>` to `notes` once.
2. Skip generated and vendored files (`*.g.cs`, `*.Designer.cs`, `*.generated.*`, migrations, `*_pb2.py`, `obj/`,
   `target/`, `build/`, `node_modules/`, `vendor/`, files headed "auto-generated"); note any skipped.
3. Evidence rule: a rubric threshold is a trigger, not a verdict. Fail only when the threshold is exceeded **and**
   reading the code confirms the smell (MFB-05). State the counted value in the evidence excerpt; confidence
   `medium` unless the value is at least twice the threshold.
4. Team conventions: if the target documents its own convention (`.editorconfig`, formatter or Checkstyle config,
   written style guide), judge CS-02/CS-05 consistency against it instead of the guide's default; a documented
   convention the code breaks still fails.
5. Software Quality (SQ-01…SQ-06, SQ-08), Design Patterns (DP-01, DP-02, DP-04…DP-06), Architecture Patterns
   (AP-01…AP-04, AP-06, AP-07) and Coding Standards (CS-01…CS-05): for each check evaluate only the elements it
   lists whose "Applies when" condition holds; if none apply, mark the check N/A with that reason. AP-07 is N/A
   unless at least two independently deployable units are in the files.
6. Retired IDs — SQ-07, AP-05, DP-03, CS-CS-01…05, CS-JV-01…05, CS-PY-01…05 — are not evaluated and not written to
   `checkResults`.
7. Boundaries: don't fail for swallowed, ignored or unchecked errors or resources on security-relevant exception
   paths (review-security-operational SEC-OP-02/SEC-OP-10), blocking on async results or singleton bottlenecks
   (review-performance PERF-02/PERF-08), retries, circuit breakers, timeouts or redundancy (review-reliability),
   repository layout, debt markers or superseded code (review-maintainability), CI gating of analyzers
   (review-software-lifecycle SL-11), API contracts (review-api-design) or externalized configuration
   (review-twelve-factor). Out-of-order workflow execution is judged here (SQR-37 under AP-02; decision D-5,
   2026-11-09); whether the caller is authorized for each step stays with review-security-identity-access SEC-IA-02.
8. Classification: append the best-fitting ISO element to each SQ/DP/AP finding title, e.g.
   `[ISO 25010:2023 Maintainability › Analysability, ISO-29]` (the rubric's ISO column is the default).
9. Severity: every Finding takes the check's default severity from `checklist.md`;
   `checkResults.severityIfFailed` is always that default.
10. Citations: `standard` = "<source name> — <element ID>" of the failed element (source names in each standards
    file header); `url` = citation base + page path + "#" + primary anchor, or for rubric elements the
    `docs/reports/`-relative path + `#sqr-NN`. Name the matching FRC remedy (with its URL) in `recommendation`;
    never put an FRC or ISO element in `standard`. `urlsFetched` stays empty.
11. Note strengths where a module is clearly well factored, a pattern clearly simplifies the design, layering is
    clean, or a file is a good example of its language standard.

## Output

Labels: copy `subject`/`subSubject` from `references/checklist.md` (the `Subject:` line and the check's `Sub-subject`
column); never invent or combine labels. Follow `compliance-review-core`'s `finding-schema.md`.
