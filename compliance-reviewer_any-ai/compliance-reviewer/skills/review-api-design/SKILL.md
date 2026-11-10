---
name: review-api-design
description: 'Reviews whether an OpenAPI spec exists, is valid, and matches the implementation, and checks the implementation against the Microsoft Azure REST API Guidelines. Use when the compliance-reviewer orchestrator delegates the API Design subject. Marked N/A when no API is found.'
user-invocable: false
---

# Review: API Design

Checks the OpenAPI/Swagger spec (existence, validity, match to implementation) and the Microsoft Azure REST API Guidelines (plus the Azure SDK telemetry guidance they reference), using local, version-pinned summaries of those standards. Severity comes from each element's own normative wording.

## Inputs

`openapi.*`, `swagger.*`, controllers/routers, API DTOs, error-handling middleware, serializer/versioning config,
LRO/status-monitor endpoints, per `compliance-inventory`. If `compliance-inventory` found no API spec and no
controllers/routers, mark this whole subject N/A with a `notes` explanation — do not fabricate findings.

## Standards (local, authoritative)

- `references/standards/openapi-specification.md` — OAS-01…OAS-43. Load only when a spec file is in scope.
- `references/standards/azure-rest-api-guidelines.md` — AZ-001…AZ-110. Load when routes/controllers or a spec are in scope.
- `references/standards/azure-sdk-telemetry.md` — SDK-01…SDK-05. Load with the Azure file.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md` and the standards files that apply (above).
2. If a spec exists, read its `openapi`/`swagger` value and apply only the OAS elements for that version (Ver column).
   Evaluate API-02 and API-03 with the OAS elements `checklist.md` lists for them, against the actual routes/DTOs.
3. If no spec exists but routes/controllers do, fail API-01 (raise an API-01 finding), mark API-02/API-03 N/A
   ("no spec"), and review the routes directly against the AZ and SDK elements.
4. For each check API-04…API-15, evaluate only the elements it lists whose "Applies when" condition holds in the
   files; if none apply, mark the check N/A with that reason (e.g. API-13 when no long-running operations exist).
   Scope `A` (Azure-specific) elements apply to every target. Versioning is judged only under API-07.
5. Severity: each Finding takes the failed element's level — DO/DO NOT/MUST/MUST NOT/REQUIRED/SHALL → Error;
   (YOU) SHOULD/(YOU) SHOULD NOT/RECOMMENDED → Warning; (YOU) MAY/OPTIONAL → Information; REVIEW → the check's
   default. For a merged element with mixed levels, use the level of the part that failed.
   `checkResults.severityIfFailed` is always the check's default severity from `checklist.md`.
6. Citations: `standard` = "<source name> — <element ID>" (source name from the standards file header);
   `url` = the file's citation base + "#" + primary anchor (first anchor listed). Use the version-matched OAS base
   URL. `urlsFetched` stays empty.
7. If neither a spec nor routes/controllers exist, return `checkResults` with every item `N/A` and
   `notes: "No API found in scope"`.
8. Boundaries: **owned here** — request-ID and `traceparent` headers documented in the contract (API-15); the
   throttling and overload response contract (`429`/`503`, `Retry-After`, retryability in error bodies); caching
   headers/ETags on HTTP APIs, pagination, the long-running-operation 202/status contract (API-13) and rate-limit
   responses; the Problem Details error format, method semantics and idempotency (AZ-009) and status-code choice,
   including 403 vs 404 (AZ-018); the API contract and its documentation (spec, versioning under API-07), including
   schema completeness in the spec (e.g. `additionalProperties`). **Don't fail for** whether a caller is authorized
   for a resource (review-security-identity-access SEC-IA-01/02; this skill judges only which status code is
   returned); runtime input validation and size limits (review-security-input-injection IV-06, IV-04);
   version-revealing headers, `405`/`415` handling, `Accept` reflection, credentials in request URLs and `no-store`
   on sensitive responses (review-security-web-api SEC-WA-07 … SEC-WA-10); request-ID/`traceparent` propagation and
   tracing in code (review-observability OBS-02/03); whether the service limits load (review-reliability AZRL-32)
   or honours `Retry-After` on outbound calls (AZRL-09); contract tests (review-testing TST-09); code-level design
   of controllers (review-software-quality).

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
