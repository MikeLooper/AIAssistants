# Maintenance — API Design localized standards

**Maintainers only. Workers never load this file.** Design decisions are recorded inline where they apply (DEC-n: this skill's localization decisions; D-n and C-n: cross-skill decisions and follow-ups); the planning documents they came from aren't kept in this repo.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| spec.openapis.org | openapi-specification.md | 43 | 100 | — |
| github.com/microsoft/api-guidelines | azure-rest-api-guidelines.md | 110 IDs (107 active) | 100 | Approved exception (DEC-3, 2026-11-07); covers 201 of 227 source anchors; 3 retired (DEC-4, 2026-11-12) |
| azure.github.io/azure-sdk | azure-sdk-telemetry.md | 5 IDs (2 active) | 100 | Covers 11 of 12 anchors in the two sections; SDK-01 … SDK-03 retired (DEC-4, 2026-11-12) |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID.
- Level is the source's own word, verbatim (or `REVIEW` for a locally derived rule). Merged elements list each level.
- Primary anchor first; list every absorbed anchor so coverage stays auditable.
- Keep rows to one line (≈ 200 characters where possible).
- Every active AZ/SDK ID must be listed by exactly one check in `../checklist.md`; every OAS ID by API-01, API-02 or API-03.
- **No Azure-only elements (DEC-4, 2026-11-12).** The checks must apply to any HTTP API, Azure-hosted or not. When a source rule names an Azure-only mechanism (an `x-ms-*` or `azure-*` header, the `api-version` parameter or its date format, Azure error codes, Azure host names, Azure SDK telemetry), either generalize it (Scope `G†`: keep the intent and level, accept any equivalent generic mechanism, and name the Azure form as one example that satisfies it) or retire it when nothing generic is left. Don't add Scope `A` rows. On refresh, re-apply the same generalization to changed source text.
- Don't add elements for caller authorization (review-security-identity-access), runtime input validation and size limits (review-security-input-injection), version headers, `405`/`415`, `Accept` reflection, credentials in URLs or `no-store` (review-security-web-api), trace propagation in code (review-observability), load limiting or outbound `Retry-After` handling (review-reliability), contract tests (review-testing) or controller code design (review-software-quality). See `SKILL.md` step 8.

## Refresh procedure

1. **Cadence:** quarterly; or when the Azure guideline's History table gains an entry; or when run notes contain ≥ 3 `localized-standard-gap` entries for this skill.
2. **Detect drift:**
   - Azure guidelines: compare the latest commit SHA of `azure/Guidelines.md` (`https://api.github.com/repos/microsoft/api-guidelines/commits?path=azure/Guidelines.md&per_page=1`) with the pinned SHA. If different, diff the two versions and their anchor lists.
   - Azure SDK: same for `Azure/azure-sdk` `docs/general/azurecore.md`.
   - OAS: check spec.openapis.org for new patch or minor releases (e.g. `v3.1.3`, `v3.3.0`).
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep each site ≤ 100 elements unless an exception is recorded above. Update the coverage map below, the pinned SHAs/versions and retrieval date in each file header and in `../sources.md`. If a pinned URL changes, update `compliance-review-core/references/approved-sources.md` too.
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo).
   - Script-check: element IDs are contiguous; checklist mapping rule above holds; every listed anchor exists in its pinned source; every normative source anchor is in the coverage map (Azure: anchors followed by a `**DO**`/`**YOU SHOULD**`/… marker; SDK: `azurecore-http-telemetry-*` and `azurecore-http-tracing-*`); OAS anchors exist on each pinned page.
   - Run a review against a small sample API repo (with spec, without spec, with an LRO): `validate` passes, `13-review-api-design.json` has `urlsFetched: []`, all 15 checks present, citations use pinned URLs and element IDs.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-api-design` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-07 — initial localization

- Snapshot: `azure/Guidelines.md` @ `15c12663c363250bea4d60aa054e81466a1f0106`; OAS v3.0.4, v3.1.2, v3.2.1, v2.0 (no newer patch pages existed); `Azure/azure-sdk` `docs/general/azurecore.md` @ `ce65374d0d4ea008fc607312daa53e503adbeb78` and the published `general_azurecore.html`.
- Script verification: 227 normative Azure anchors (144 DO, 26 YOU SHOULD, 28 YOU MAY, 20 DO NOT, 9 YOU SHOULD NOT) → 201 covered, 26 not localized, 0 unaccounted; 12 SDK anchors → 11 covered, 1 client-only; all OAS anchors present on all three 3.x pages.
- Corrections made while checking rows against the pinned text (differences from the plan's proposed inventory):
  - OAS-04: YAML 1.2 is RECOMMENDED, not MUST; level `MUST / RECOMMENDED`.
  - OAS-05, OAS-07, OAS-17, OAS-25: rules differ between versions (`x-oai-`/`x-oas-` reserved only in 3.1+; server-variable `enum` SHOULD in 3.0 vs MUST in 3.1+; GET/HEAD/DELETE bodies "SHALL be ignored" in 3.0 vs "SHOULD be avoided" in 3.1+; discriminator property SHOULD be required in 3.0/3.1, optional with `defaultMapping` in 3.2). Ver set to `differs`.
  - OAS-16: level is SHALL (source wording). OAS-21: `default` is MAY, not SHOULD. OAS-26: level SHOULD NOT (source wording).
  - OAS-22, OAS-27, OAS-28, OAS-30, OAS-33, OAS-36: the spec has no normative keyword for these, so they are `REVIEW` rules. OAS-27/28/30/33/36 are spec-vs-implementation checks and moved from API-02 to API-03; OAS-22 stays in API-02.
  - AZ-033: the source's shared schema covers PUT request/response, PATCH response, GET response and POST request/response (not list items); PATCH request has the same fields with none required.
  - Minor wording added from the source: AZ-011, AZ-022, AZ-029, AZ-034, AZ-055, AZ-064, AZ-082 (`top` minimum 1, default unlimited), AZ-084, AZ-090, AZ-095.
  - SDK levels use the rendered wording on the published page (DO / YOU SHOULD); the Markdown source uses MUST / SHOULD.

### 2026-11-12 — Azure-only mechanisms generalized or retired (DEC-4)

- Goal: the API Design checks apply to any HTTP API (e.g. any ASP.NET Core API), not only Azure services. Pins unchanged.
- Generalized (`G†`): AZ-023 (standard headers without `x-ms-*`), AZ-027 (request ID in any consistent header or error-body field), AZ-044/AZ-045 (machine-readable error code; header optional), AZ-046 (RFC 9457 Problem Details or the source's `error` object), AZ-069 (colon or verb sub-path action URLs), AZ-085 (any one explicit versioning mechanism, including a path segment), AZ-086 (any documented version scheme), AZ-087 (descriptive error code, not the Azure code names), AZ-090 (`Deprecation`/`Sunset` headers or an equivalent), AZ-108 (offset unit stated), AZ-110 (any client request-ID header name), SDK-05 (OpenTelemetry HTTP semantic conventions).
- Wording only (`api-version` → the API's version parameter, if any): AZ-075, AZ-093, AZ-102, AZ-106.
- Retired: AZ-088 (no version in path: Azure convention; AZ-085 now allows any mechanism), AZ-100 (pointer to Azure SDK telemetry), AZ-109 (Azure host pattern), SDK-01 … SDK-03 (Azure SDK `User-Agent`, `X-MS-UserAgent`, `X-MS-AZSDK-Telemetry`).
- Checklist: API-04 no longer judges hosts; API-07 no longer fails path versioning; API-15 lists AZ-027, AZ-110, SDK-04, SDK-05. Check count unchanged (15), but API-04, API-05, API-07, API-10, API-15 findings from runs before and after this date aren't directly comparable.

## Open items

- Follow-ups outside this skill: reviewed and closed in the cross-skill follow-up pass of 2026-11-09. Open hand-offs: none.

## localized-standard-gap log

| Date | Gap (from run notes) | Resolution |
|---|---|---|
| — | none recorded yet | — |

## Anchor coverage map

### Azure REST API Guidelines (227 normative anchors, document order)

| Source anchor | Element / status |
|---|---|
| http-url-pattern | AZ-008 (AZ-109 retired 2026-11-12) |
| http-url-casing | AZ-001 |
| http-url-length | AZ-006 |
| http-url-case-sensitivity | AZ-002 |
| http-url-return-casing | AZ-007 |
| http-url-allowed-characters | AZ-003 |
| http-url-allowed-characters-2 | AZ-004 |
| http-url-should-be-readable | AZ-005 |
| http-url-allowed-characters-3 | not localized — Permissive YOU MAY with no failure condition |
| http-direct-endpoints | AZ-109 (retired 2026-11-12, Azure-only) |
| http-url-return-consistent-form | AZ-007 |
| http-url-parameter-values | not localized — Permissive YOU MAY with no failure condition |
| http-all-methods-idempotent | AZ-009 |
| http-use-put-or-patch | AZ-010 |
| http-post-must-be-idempotent | AZ-011 |
| http-success-status-codes | AZ-012 |
| http-lro-status-code | AZ-013 |
| http-method-casing | AZ-014 |
| http-return-resource | AZ-015 |
| http-delete-returns-204 | AZ-016 |
| http-post-action-returns-200 | AZ-017 |
| http-return-403-vs-404 | AZ-018 |
| http-support-optimistic-concurrency | AZ-019 |
| http-query-names-casing | AZ-020 |
| http-parameter-validation | AZ-021 |
| http-parameter-serialization | AZ-022 |
| http-header-support-standard-headers | AZ-023 |
| http-header-names-casing | AZ-024 |
| http-header-names-case-sensitivity | AZ-025 |
| http-header-values-case-sensitivity | AZ-025 |
| http-header-date-values | AZ-026 |
| http-header-request-id | AZ-027 |
| http-allow-unrecognized-headers | AZ-028 |
| http-no-x-custom-headers | AZ-029 |
| rest-clear-naming | AZ-030 |
| rest-paths-make-sense | AZ-030 |
| rest-simplify-operations | AZ-030 |
| rest-specify-string-value-constraints | AZ-032 |
| rest-use-standard-status-codes | AZ-031 |
| rest-response-body-is-resource-schema | AZ-033 |
| rest-field-mutability | AZ-034 |
| rest-flat-is-better-than-nested | AZ-035 |
| rest-get-returns-json-body | AZ-036 |
| rest-patch-use-merge-patch | AZ-037 |
| rest-put-for-create-or-replace | AZ-038 |
| rest-delete-resource | AZ-039 |
| rest-fail-for-unknown-fields | AZ-040 |
| rest-secrets-allowed-in-post-response | AZ-041 |
| rest-no-secrets-in-get-response | AZ-041 |
| rest-no-computable-fields | AZ-042 |
| rest-put-patch-status-codes | AZ-043 |
| rest-error-code-header | AZ-044 |
| rest-error-code-enum | AZ-048 |
| rest-add-codes-in-new-api-version | AZ-049 |
| rest-descriptive-error-code-values | AZ-047 |
| rest-error-code-grouping | AZ-047 |
| rest-error-code-header-and-body-match | AZ-045 |
| rest-error-response-body-structure | AZ-046 |
| rest-document-error-code-values | AZ-048 |
| rest-error-non-api-contract-fields | AZ-046 |
| rest-error-additional-properties-allowed | AZ-046 |
| rest-error-use-default-response | AZ-050 |
| json-field-name-casing | AZ-051 |
| json-field-names-case-sensitivity | AZ-052 |
| json-field-values-case-sensitivity | AZ-052 |
| json-field-values-ids | AZ-053 |
| json-null-response-values | AZ-054 |
| json-null-resquest-values | AZ-055 |
| json-integer-values | AZ-056 |
| json-specify-string-constraints | AZ-032 |
| json-use-standard-string-formats | AZ-057 |
| json-should-be-round-trippable | AZ-057 |
| json-date-time-is-rfc3339 | AZ-058 |
| json-durations-use-fixed-time-intervals | AZ-059 |
| json-rfc3339-time-intervals-allowed | AZ-059 |
| json-uuid-is-rfc4412 | AZ-060 |
| json-may-nest-for-grouping | AZ-061 |
| json-use-arrays-for-ordering | AZ-061 |
| json-prefer-objects-over-arrays | AZ-061 |
| json-use-extensible-enums | AZ-062 |
| json-document-extensible-enums | AZ-063 |
| json-return-extensible-enum-value | AZ-064 |
| json-accept-extensible-enum-value | AZ-064 |
| json-removing-enum-value-is-breaking | AZ-065 |
| json-use-discriminator-for-polymorphism | AZ-066 |
| json-polymorphism-kind-extensible | AZ-067 |
| json-polymorphism-kind-immutable | AZ-067 |
| json-polymorphism-versioning | AZ-068 |
| json-polymorphism-arrays | AZ-068 |
| actions-url-pattern-for-resource-action | AZ-069 |
| actions-url-pattern-for-collection-action | AZ-069 |
| actions-use-post-method | AZ-070 |
| actions-support-repeatability-headers | AZ-072 |
| actions-synchronous-success-status-code | AZ-017 |
| actions-action-name-is-verb | AZ-069 |
| actions-no-actions-for-crud | AZ-071 |
| collections-response-is-object | AZ-073 |
| collections-support-server-driven-paging | AZ-074 |
| collections-use-get-method | AZ-080 |
| collections-items-have-id-and-etag | AZ-077 |
| collections-document-pagination-reliability | AZ-078 |
| collections-include-nextlink-for-more-results | AZ-075 |
| collections-nextlink-includes-all-query-params | AZ-075 |
| collections-response-array-name | AZ-073 |
| collections-no-nextlink-on-last-page | AZ-076 |
| collections-nextlink-value-never-null | AZ-076 |
| collections-avoid-count-property | AZ-079 |
| collections-query-options | AZ-080 |
| collections-error-on-unknown-parameter | AZ-081 |
| collections-parameter-names-case-sensitivity | AZ-080 |
| collections-select-expand-ordering | AZ-083 |
| collections-query-options-ordering | AZ-083 |
| collections-query-options-no-dollar-sign | AZ-080 |
| collections-filter-param | AZ-080 |
| collections-filter-behavior | AZ-084 |
| collections-filter-unknown-operator | AZ-081 |
| collections-filter-operator-ordering | AZ-084 |
| collections-filter-functions | AZ-080 |
| collections-orderby-param | AZ-080 |
| collections-orderby-ordering | AZ-084 |
| collections-orderby-null-ordering | AZ-084 |
| collections-orderby-behavior | AZ-084 |
| collections-orderby-inherent-sort-order | AZ-084 |
| collections-orderby-unsupported-field | AZ-081 |
| collections-consistent-options-with-pagination | AZ-083 |
| collections-skip-param-definition | AZ-082 |
| collections-skip-param | AZ-080 |
| collections-top-param | AZ-080 |
| collections-top-behavior | AZ-082 |
| collections-maxpagesize-param | AZ-080 |
| collections-maxpagesize-definition | AZ-082 |
| collections-maxpagesize-might-return-fewer | AZ-082 |
| versioning-review-required | not localized — Organizational process (Stewardship Board approval); not observable in code |
| versioning-api-version-query-param | AZ-085 |
| versioning-date-based-versioning | AZ-086 |
| versioning-api-version-missing | AZ-087 |
| versioning-api-version-unsupported | AZ-087 |
| versioning-use-later-date | AZ-086 |
| versioning-no-breaking-changes | AZ-089 |
| versioning-no-version-in-path | AZ-088 (retired 2026-11-12, Azure convention) |
| versioning-use-later-date-2 | AZ-086 |
| versioning-preview-goes-ga-within-one-year | not localized — Needs release history (Git/release data), which reviews may not read |
| versioning-use-extensible-enums | AZ-062 |
| deprecation-header | AZ-090 |
| deprecation-header-value | AZ-090 |
| deprecation-header-review | not localized — Organizational process (Breaking Change Reviewer approval); not observable in code |
| repeatability-headers | AZ-072 |
| lro-response-time | AZ-091 |
| lro-no-patch-lro | AZ-091 |
| lro-valid-inputs-synchronously | AZ-092 |
| lro-returns-operation-location | AZ-093 |
| lro-operation-location-includes-api-version | AZ-093 |
| lro-put-response-headers | AZ-101 |
| lro-create-init | AZ-102 |
| lro-put-operation-id-request-header | AZ-094 |
| lro-put-operation-id-default-is-guid | AZ-094 |
| lro-put-operation-id-unique-except-retries | AZ-094 |
| lro-put-valid-inputs-synchronously | AZ-092 |
| lro-put-returns-200-or-201 | AZ-102 |
| lro-put-returns-operation-id-header | AZ-094 |
| lro-put-returns-operation-location | AZ-102 |
| lro-put-operation-location-includes-api-version | AZ-102 |
| lro-delete | AZ-103 |
| lro-delete-operation-id-request-header | AZ-094 |
| lro-delete-operation-id-default-is-guid | AZ-094 |
| lro-delete-returns-202 | AZ-093 |
| lro-delete-returns-only-202 | AZ-093 |
| lro-existing-resource | AZ-104 |
| lro-no-post-create | AZ-091 |
| lro-operation-id-request-header | AZ-094 |
| lro-operation-id-default-is-guid | AZ-094 |
| lro-operation-id-unique-except-retries | AZ-094 |
| lro-returns-202 | AZ-093 |
| lro-returns-only-202 | AZ-093 |
| lro-returns-status-monitor | AZ-095 |
| lro-action-no-resource | AZ-105 |
| lro-put-action-operation-endpoint | AZ-105 |
| lro-put-action-operation-id-in-path | AZ-105 |
| lro-put-action-returns-201 | AZ-105 |
| lro-put-action-returns-status-monitor | AZ-105 |
| lro-put-action-status-monitor-url | AZ-105 |
| lro-status-monitor-structure | AZ-095 |
| lro-poll | AZ-106 |
| lro-status-monitor-get-returns-200 | AZ-096 |
| lro-status-monitor-accepts-any-api-version | AZ-106 |
| lro-status-monitor-includes-all-fields | AZ-095 |
| lro-status-monitor-post-action-result | AZ-095 |
| lro-status-monitor-no-resource-result | AZ-095 |
| lro-status-monitor-retry-after | AZ-096 |
| lro-status-monitor-retention | AZ-096 |
| lro-list-status-monitors | AZ-107 |
| lro-put-action-list-status-monitors | AZ-107 |
| lro-list-status-monitors-filter | AZ-107 |
| byos-pattern | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-prefix-for-folder | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-allow-container-reuse | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-authorization | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-define-rbac-roles | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-rbac-compatibility | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-include-downstream-errors | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-sas-token | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-http-insecure | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-http-status-code | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-include-storage-error | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-support-single-object | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-last-modified | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-folder-support | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-extensions | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-location-and-delimiter | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-directory-last-modified | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-sas-for-input-location | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| byos-sas-for-output-location | not localized — BYOS: applies only to services that read/write customer Azure Storage |
| condreq-support | AZ-019 |
| condreq-unsupported-error | AZ-019 |
| condreq-return-etags | AZ-097 |
| condreq-for-read-behavior | AZ-098 |
| condreq-behavior | AZ-098 |
| condreq-etag-is-hash | AZ-099 |
| condreq-etag-hash-entire-resource | AZ-099 |
| condreq-strong-etag-for-range-requests | AZ-099 |
| condreq-timestamp-precision | not localized — Permissive YOU MAY with no failure condition |
| condreq-weak-etags-allowed | not localized — Permissive YOU MAY with no failure condition |
| condreq-etag-depends-on-encoding | AZ-099 |
| substrings-return-value-for-each-encoding | AZ-108 |
| substrings-return-value-structure | AZ-108 |
| telemetry-headers | AZ-100 (retired 2026-11-12, Azure-only) |
| telemetry-allow-unrecognized-headers | AZ-028 |
| distributed-tracing--telemetry (heading; correlation-header table, no item anchor) | AZ-110 |

Non-normative anchors in the file (section headings, retired-link placeholders), not counted: `http`, `rest`, `json`, `actions`, `collections`, `collections-`, `versioning`, `deprecation`, `repeatability`, `put-operation-with-additional-long-running-processing`, `post-or-delete-lro-pattern`, `byos`, `condreq`, `condreq-support-etags-consistently`, `condreq-for-read`, `condreq-no-pessimistic-update` (the last three are subsumed by `condreq-support`), `substrings`, `telemetry`.

### Azure SDK general guidelines — Telemetry policy and Distributed tracing policy (12 anchors)

| Source anchor | Element / status |
|---|---|
| azurecore-http-telemetry-useragent | SDK-01 (retired 2026-11-12, Azure-only) |
| azurecore-http-telemetry-useragent-stacking | SDK-01 (retired 2026-11-12, Azure-only) |
| azurecore-http-telemetry-useragent-stacking-core | SDK-01 (retired 2026-11-12, Azure-only) |
| azurecore-http-telemetry-appid | SDK-01 (retired 2026-11-12, Azure-only) |
| azurecore-http-telemetry-appid-length | SDK-01 (retired 2026-11-12, Azure-only) |
| azurecore-http-telemetry-x-ms-useragent | SDK-02 (retired 2026-11-12, Azure-only) |
| azurecore-http-telemetry-dynamic | SDK-03 (retired 2026-11-12, Azure-only) |
| azurecore-http-tracing-opentelemetry | SDK-05 |
| azurecore-http-tracing-accept-context | SDK-04 |
| azurecore-http-tracing-pass-context | SDK-04 |
| azurecore-http-tracing-create-span | client-only — a child span per REST call the client makes; nothing for a service to do |
| azurecore-http-tracing-opentelemetry-conventions | SDK-05 |
