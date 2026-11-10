---
name: review-maintainability
description: 'Reviews README and onboarding docs, repository layout, documented prerequisites and configuration, technical-debt markers, deprecated code, contributing guide, change history, architecture docs and doc accuracy, against a local maintainability rubric. Use when the compliance-reviewer orchestrator delegates the Maintainability subject.'
user-invocable: false
---

# Review: Maintainability

Assesses how easily a new developer can understand, set up, change and extend the repository, using the local
Compliance Reviewer Maintainability Rubric.

## Inputs

`README*`, `CONTRIBUTING*`, `CHANGELOG*`, the docs folder (including ADRs), the folder structure listing, config
templates (`.env.example`), toolchain pin files, package manifests and a few representative source files, per
`compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/maintainability-rubric.md` — MR-01…MR-36. Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md` and the rubric.
2. For each check (MAINT-01…MAINT-10), evaluate only the elements it lists whose "Applies when" condition holds.
   If none apply, mark the check N/A with that reason.
3. Missing documents: report one only when the folder listing (or the folder where it would be) is in the file list
   and the document is absent; otherwise mark the check N/A ("documentation location not in scope"). Use confidence
   `Medium` for missing-document findings and `High` when the evidence is in a file you read.
4. Docs in sync (MAINT-09): you may open the manifest or config file a document refers to, to confirm a command,
   key, version or path.
5. MAINT-04 and MAINT-05 judge only the source files in this subject's list. Add
   `scope: <N> reviewed source files, not repo-wide` to `notes`. With no source files, mark both N/A
   ("no source files in scope").
6. Ownership: MAINT-02 judges repository-level layout and naming only (code-level cohesion, layering and cycles belong
   to `review-software-quality`). MAINT-05 judges reachable superseded code only (dead or commented-out code belongs to
   `review-software-quality` SQ-08). MR-15 judges placeholders only (real secrets belong to the security skills).
   Doc comments on public APIs belong to `review-software-quality` CS-04. License files and codes of conduct are
   judged here (MAINT-10; never a license-compatibility verdict on dependencies, which no subject judges since DEP-06
   was retired); `SECURITY.md` belongs to `review-software-lifecycle`.
7. Severity: every Finding takes the check's default severity from `checklist.md`; `checkResults.severityIfFailed`
   is always that default.
8. Citations: `standard` = "Compliance Reviewer Maintainability Rubric — <element ID>"; `url` = the rubric's
   citation base + "#" + lower-case element ID (e.g. `…/maintainability-rubric.md#mr-14`). Give each distinct
   element violation its own finding. `urlsFetched` stays empty.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
