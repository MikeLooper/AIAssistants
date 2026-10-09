---
name: review-api-design
description: 'Reviews whether an OpenAPI spec exists, is valid, and matches the implementation, and checks the implementation against the Microsoft Azure REST API Guidelines. Use when the compliance-reviewer orchestrator delegates the API Design subject. Marked N/A when no API is found.'
user-invocable: false
---

# Review: API Design

Checks the OpenAPI/Swagger spec (existence, validity, match to implementation) and the Microsoft Azure API Guidelines, with severity taken from the guideline's own DO / YOU SHOULD / YOU MAY wording.

## Inputs

`openapi.*`, `swagger.*`, controllers/routers, API DTOs, per `compliance-inventory`. If `compliance-inventory` found no API spec and no controllers/routers, mark this whole subject N/A with a `notes` explanation — do not fabricate findings.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. If an OpenAPI/Swagger file exists, check it's syntactically valid and that its paths/schemas match the actual routes/DTOs found in code.
3. If no spec file exists but routes/controllers do, raise SQ-level finding that no spec exists, and review the routes directly against the Azure API Guidelines checklist.
4. Apply the DO → Error, YOU SHOULD → Warning, YOU MAY → Information mapping from `compliance-review-core`'s `severity-and-scoring.md`.
5. If neither a spec nor routes/controllers exist, return `checkResults` with every item `N/A` and `notes: "No API found in scope"`.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
