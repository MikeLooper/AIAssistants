# Microsoft Azure REST API Guidelines — localized summary

- Source site: github.com/microsoft/api-guidelines
- Pinned document: azure/Guidelines.md @ 15c12663c363250bea4d60aa054e81466a1f0106 (2026-10-22)
- Citation base: https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md
- Localized: 2026-11-07 · Elements: 110 (approved exception to the 100 cap)
- Source name for `Finding.standard`: `Microsoft Azure REST API Guidelines`
- Scope column: G = generic HTTP/REST practice; A = Azure-specific mechanism (header/parameter names, formats). Both apply to every target.
- Anchor(s): the primary anchor first; merged elements list every source anchor they absorb.

## URLs and idempotency

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-001 | DO | G | kebab-case (preferred) or camelCase URL path segments; camelCase when the segment names a JSON field. | routes | http-url-casing |
| AZ-002 | DO | G | Service-defined path segments are case-sensitive; a case mismatch fails with 404. | routes | http-url-case-sensitivity |
| AZ-003 | DO | G | Service-defined path segments use only `0-9 A-Z a-z - . _ ~`; `:` only to mark an action. | routes | http-url-allowed-characters |
| AZ-004 | YOU SHOULD | G | Restrict user-supplied path parameter values to the same set (no `:`). | path params | http-url-allowed-characters-2 |
| AZ-005 | YOU SHOULD | G | Keep URLs readable; avoid UUIDs and %-encoding where possible. | routes | http-url-should-be-readable |
| AZ-006 | DO | G | Return 414 when a URL exceeds 2083 characters. | routes | http-url-length |
| AZ-007 | DO | G | URLs returned in headers/bodies use correct casing and one consistent form, regardless of the URL used to reach the resource. | URLs returned | http-url-return-casing, http-url-return-consistent-form |
| AZ-008 | DO | G | Path shape `/<service-root>/<resource-collection>/<resource-id>`; collection names unabbreviated and plural; IDs are raw, URL-escaped values with no quoting. Host part: AZ-109. | routes | http-url-pattern |
| AZ-009 | DO | G | All HTTP methods are idempotent. | all ops | http-all-methods-idempotent |
| AZ-010 | YOU SHOULD | G | Create resources with PUT or PATCH. | create ops | http-use-put-or-patch |
| AZ-011 | YOU MAY | G | POST may create, but must then be idempotent and return 201 with the created resource's URL. | POST create | http-post-must-be-idempotent |

## Status codes

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-012 | DO | G | Synchronous success codes: PATCH/PUT 200 or 201; POST-create 201 with the resource URL; POST-action 200; GET (item or list) 200; DELETE 204. | all ops | http-success-status-codes |
| AZ-013 | DO | G | PUT/POST/DELETE that complete asynchronously return 202 and follow the LRO pattern. | LRO | http-lro-status-code |
| AZ-014 | DO | G | Method names are case-sensitive and uppercase. | routes | http-method-casing |
| AZ-015 | DO | G | PUT/PATCH/POST/GET return the resource state with 200/201. | resource ops | http-return-resource |
| AZ-016 | DO | G | DELETE returns 204 with no body, even if the resource doesn't exist (no 404). | DELETE | http-delete-returns-204 |
| AZ-017 | DO | G | Synchronous POST actions return 200 with a body (an empty object is allowed). | actions | http-post-action-returns-200, actions-synchronous-success-status-code |
| AZ-018 | DO | G | 403 when access is denied, unless that leaks the resource's existence; then 404. | authz | http-return-403-vs-404 |
| AZ-019 | DO | G | Honor `If-Match`, `If-None-Match`, `If-Modified-Since`, `If-Unmodified-Since` (return ETag/last-modified); return a precondition-failed error if a precondition can't be verified. | resource ops | http-support-optimistic-concurrency, condreq-support, condreq-unsupported-error |

## Query parameters and headers

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-020 | DO | G | camelCase query parameter names. | query params | http-query-names-casing |
| AZ-021 | DO | G | Validate every query parameter and request header value; fail with 400 and the standard error body. | params/headers | http-parameter-validation |
| AZ-022 | DO | G | Parameter string formats: booleans `true`/`false`; integers within ±2^53−1; floats IEEE-754 binary64; UUID without braces; header dates IMF-fixdate; query date-time RFC 3339 (≤ 3 fractional digits); byte arrays base64; arrays comma-separated (preferred) or repeated `name=value`. | params | http-parameter-serialization |
| AZ-023 | DO | A | Support the standard headers: `authorization`, `x-ms-useragent`, `content-type`, `content-length`, `x-ms-request-id`, `x-ms-error-code`, `azure-deprecating`. | headers | http-header-support-standard-headers |
| AZ-024 | DO | G | Header names are kebab-case. | custom headers | http-header-names-casing |
| AZ-025 | DO | G | Compare header names case-insensitively; values case-sensitively when the header requires it. | headers | http-header-names-case-sensitivity, http-header-values-case-sensitivity |
| AZ-026 | DO | G | Accept HTTP-Date in headers and return IMF-fixdate (e.g. `Sun, 06 Nov 1994 08:49:37 GMT`). | date headers | http-header-date-values |
| AZ-027 | DO | A | Generate an opaque value that uniquely identifies the request, return it in `x-ms-request-id`, and include it in error logs. | all ops | http-header-request-id |
| AZ-028 | DO NOT | G | Fail requests because of unrecognized headers (including distributed-tracing headers). | headers | http-allow-unrecognized-headers, telemetry-allow-unrecognized-headers |
| AZ-029 | DO NOT | G | Use an `x-` prefix for new custom headers (RFC 6648), unless the header already exists in production. | custom headers | http-no-x-custom-headers |

## REST resource design

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-030 | DO | G | Clear, consistent naming; resource paths that make sense; few required query parameters and JSON fields. | routes/DTOs | rest-clear-naming, rest-paths-make-sense, rest-simplify-operations |
| AZ-031 | DO | G | Response codes and bodies let callers diagnose and fix their own problems. | all ops | rest-use-standard-status-codes |
| AZ-032 | DO | G | Define explicit string contracts (min/max length, legal characters, case sensitivity, standard formats). | string fields/params | rest-specify-string-value-constraints, json-specify-string-constraints |
| AZ-033 | DO | G | One JSON schema per URL path for the PUT request/response, PATCH response, GET response and POST request/response; the PATCH request has the same fields with none required. | resource DTOs | rest-response-body-is-resource-schema |
| AZ-034 | DO | G | Define each field's mutability (create / update / read-only); a passed read-only field fails unless it matches the current value. | resource DTOs | rest-field-mutability |
| AZ-035 | DO | G | Keep fields simple and the hierarchy shallow. | DTOs | rest-flat-is-better-than-nested |
| AZ-036 | DO | G | GET retrieves resources and returns JSON. | GET | rest-get-returns-json-body |
| AZ-037 | DO | G | Create/update with PATCH using JSON Merge Patch (`application/merge-patch+json`, RFC 7396). | PATCH | rest-patch-use-merge-patch |
| AZ-038 | DO | G | PUT with JSON for wholesale create/replace. | PUT | rest-put-for-create-or-replace |
| AZ-039 | DO | G | DELETE removes a resource. | delete ops | rest-delete-resource |
| AZ-040 | DO | G | 400 with the standard error body for malformed requests or any JSON field name/value not understood by that version. | PUT/PATCH/POST | rest-fail-for-unknown-fields |
| AZ-041 | DO NOT / YOU MAY | G | Never return secrets in GET responses; return them via POST only if absolutely necessary. | secret fields | rest-no-secrets-in-get-response, rest-secrets-allowed-in-post-response |
| AZ-042 | DO NOT | G | Add fields whose values are easily computed from other fields. | DTOs | rest-no-computable-fields |
| AZ-043 | DO | G | PUT/PATCH processing: unknown/invalid or read-only field → 400; missing mandatory field → 400; create → 201; PATCH create-field mismatch on an existing resource → 409; update/replace → 200. | PUT/PATCH | rest-put-patch-status-codes |

## Errors

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-044 | DO | A | Return an `x-ms-error-code` header with a string error code on errors. | error responses | rest-error-code-header |
| AZ-045 | DO | A | The top-level body `error.code` equals the `x-ms-error-code` header value. | error responses | rest-error-code-header-and-body-match |
| AZ-046 | DO / YOU MAY | G | Error body: `{ "error": { "code"*, "message"*, "target", "details": [ErrorDetail], "innererror": { "code", "innererror" } } }`; extra properties allowed and outside the API contract. | error responses | rest-error-response-body-structure, rest-error-non-api-contract-fields, rest-error-additional-properties-allowed |
| AZ-047 | DO / YOU MAY | G | Unique, descriptive error codes for errors callers can recover from at runtime; common usage errors may share a few codes. | error codes | rest-descriptive-error-code-values, rest-error-code-grouping |
| AZ-048 | DO / YOU MAY | G | Document top-level error codes as part of the API contract; they may be modelled as an extensible (model-as-string) enum. | error codes | rest-document-error-code-values, rest-error-code-enum |
| AZ-049 | YOU SHOULD NOT | G | Add new top-level error codes without bumping the API version. | versioned APIs | rest-add-codes-in-new-api-version |
| AZ-050 | YOU SHOULD NOT | G | Document individual error status codes in OpenAPI when the `default` response describes them adequately. | OpenAPI spec | rest-error-use-default-response |

## JSON

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-051 | DO | G | camelCase JSON field names; acronyms not upper-cased. | DTOs | json-field-name-casing |
| AZ-052 | DO | G | JSON field names and values are case-sensitive. | DTOs | json-field-names-case-sensitivity, json-field-values-case-sensitivity |
| AZ-053 | DO | G | Unique-ID values are opaque strings compared case-sensitively. | ID fields | json-field-values-ids |
| AZ-054 | DO NOT | G | Send null-valued fields to clients; omit them instead. | responses | json-null-response-values |
| AZ-055 | DO | G | Accept null field values only in JSON Merge Patch requests (null = delete the field; 400 if it can't be deleted). | requests | json-null-resquest-values |
| AZ-056 | DO | G | Integers stay within the JSON-safe range (±2^53−1). | numeric fields | json-integer-values |
| AZ-057 | DO | G | Well-known, parseable string formats; values round-trip across languages. | DTOs | json-use-standard-string-formats, json-should-be-round-trippable |
| AZ-058 | DO | G | Date-times are RFC 3339. | date fields | json-date-time-is-rfc3339 |
| AZ-059 | DO / YOU MAY | G | Durations are fixed-unit numbers with the unit in the field name (`ttlSeconds`); RFC 3339/ISO 8601 intervals only when callers need calendar intervals. | duration fields | json-durations-use-fixed-time-intervals, json-rfc3339-time-intervals-allowed |
| AZ-060 | DO | G | UUIDs follow RFC 4122. | UUID fields | json-uuid-is-rfc4412 |
| AZ-061 | YOU SHOULD / YOU MAY | G | Prefer objects over arrays; arrays only when order matters; objects may group sub-fields. | DTOs | json-prefer-objects-over-arrays, json-use-arrays-for-ordering, json-may-nest-for-grouping |

## Enums and polymorphism

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-062 | YOU SHOULD | G | Use extensible enums (string-modelled) unless the value set will never change. | enums | json-use-extensible-enums, versioning-use-extensible-enums |
| AZ-063 | DO | G | Document that new enum values may appear. | enums | json-document-extensible-enums |
| AZ-064 | YOU SHOULD NOT / YOU MAY | G | Don't accept extensible-enum values not defined for the requested version; the service may return such values. | enums | json-accept-extensible-enum-value, json-return-extensible-enum-value |
| AZ-065 | DO NOT | G | Remove enum values (breaking change). | enums | json-removing-enum-value-is-breaking |
| AZ-066 | DO | G | Polymorphic types have a discriminator field (e.g. `kind`) and carry the kind-specific fields in the body. | polymorphic DTOs | json-use-discriminator-for-polymorphism |
| AZ-067 | YOU SHOULD / YOU SHOULD NOT | G | The discriminator is an extensible enum and cannot be changed by PATCH. | polymorphic DTOs | json-polymorphism-kind-extensible, json-polymorphism-kind-immutable |
| AZ-068 | YOU SHOULD NOT | G | Don't use arrays of polymorphic objects on updatable resources, or return polymorphic properties not defined for the requested version. | polymorphic DTOs | json-polymorphism-arrays, json-polymorphism-versioning |

## Actions

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-069 | YOU SHOULD | G | Action URLs `/<collection>/<id>:<action>` and `/<collection>:<action>`, with a verb as the action name. | actions | actions-url-pattern-for-resource-action, actions-url-pattern-for-collection-action, actions-action-name-is-verb |
| AZ-070 | DO | G | Actions use POST. | actions | actions-use-post-method |
| AZ-071 | DO NOT | G | Use actions for behaviour expressible as standard Create/Read/Update/Delete/List operations. | actions | actions-no-actions-for-crud |
| AZ-072 | DO / YOU SHOULD | G | Support `Repeatability-Request-ID` / `Repeatability-First-Sent` (OASIS Repeatable Requests) for POST that must be retry-safe. | non-idempotent POST | actions-support-repeatability-headers, repeatability-headers |

## Collections and query options

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-073 | DO / YOU SHOULD | G | List responses are an object with a top-level array, named `value` unless a better name exists. | list ops | collections-response-is-object, collections-response-array-name |
| AZ-074 | YOU SHOULD | G | Support server-driven paging whenever a collection could grow large. | list ops | collections-support-server-driven-paging |
| AZ-075 | DO | G | `nextLink` is an absolute URL that includes every query parameter the service needs (incl. `api-version`). | paged lists | collections-include-nextlink-for-more-results, collections-nextlink-includes-all-query-params |
| AZ-076 | DO NOT | G | Return `nextLink` on the last page, or with a null value. | paged lists | collections-no-nextlink-on-last-page, collections-nextlink-value-never-null |
| AZ-077 | DO | G | Every list item includes `id` and `etag` (if supported; quotes escaped). | list ops | collections-items-have-id-and-etag |
| AZ-078 | DO | G | Document that items may be skipped or duplicated across pages. | paged lists | collections-document-pagination-reliability |
| AZ-079 | YOU SHOULD NOT | G | Return a total `count` of the collection. | list ops | collections-avoid-count-property |
| AZ-080 | YOU MAY / DO / DO NOT | G | May offer a GET list endpoint and `filter`, `orderby`, `skip`, `top`, `maxpagesize`, `select`, `expand` (and filter functions); these names are case-sensitive and not `$`-prefixed. | list ops | collections-query-options, collections-use-get-method, collections-filter-param, collections-orderby-param, collections-skip-param, collections-top-param, collections-maxpagesize-param, collections-filter-functions, collections-parameter-names-case-sensitivity, collections-query-options-no-dollar-sign |
| AZ-081 | DO | G | Return an error for an unsupported query parameter, filter operator or orderby field. | list ops | collections-error-on-unknown-parameter, collections-filter-unknown-operator, collections-orderby-unsupported-field |
| AZ-082 | DO | G | `skip`: integer, default and minimum 0. `top`: integer, minimum 1, default unlimited; returns up to `top` items starting at `skip`. `maxpagesize`: optional integer with a default, documented as possibly returning fewer items. | query options | collections-skip-param-definition, collections-top-behavior, collections-maxpagesize-definition, collections-maxpagesize-might-return-fewer |
| AZ-083 | DO | G | Apply query options in the documented order, with `select`/`expand` last; keep the same filter and sort across all pages. | query options | collections-query-options-ordering, collections-select-expand-ordering, collections-consistent-options-with-pagination |
| AZ-084 | DO | G | Filter/sort semantics: drop items where the filter is false, null or references properties hidden by permissions; ascending by default; nulls sort first; use the type's natural order; standard operator precedence; ties broken by the next expression. | filter/orderby | collections-filter-behavior, collections-filter-operator-ordering, collections-orderby-ordering, collections-orderby-null-ordering, collections-orderby-behavior, collections-orderby-inherent-sort-order |

## Versioning and deprecation

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-085 | DO | A | Require an `api-version` query parameter on every operation. | all ops | versioning-api-version-query-param |
| AZ-086 | DO / DO NOT | A | Version values are `YYYY-MM-DD` (with `-preview` for previews); each new preview has a later date; a GA version doesn't reuse its preview's date. | versions | versioning-date-based-versioning, versioning-use-later-date, versioning-use-later-date-2 |
| AZ-087 | DO | A | A missing or unsupported version returns 400 with code `MissingApiVersionParameter` / `UnsupportedApiVersionValue`. | all ops | versioning-api-version-missing, versioning-api-version-unsupported |
| AZ-088 | DO NOT | G | Put a version segment in any operation path. | routes | versioning-no-version-in-path |
| AZ-089 | DO NOT | G | Make breaking changes within an existing API version. | versioned APIs | versioning-no-breaking-changes |
| AZ-090 | DO | A | Send `azure-deprecating` only when the operation will stop working and the client must act; the value is a semicolon-delimited list (what, when, URL). | deprecations | deprecation-header, deprecation-header-value |

## Long-running operations

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-091 | DO / DO NOT | G | Use an LRO when p99 latency is over 1 s; never make PATCH an LRO; never use a long-running POST to create (use PUT). | slow ops | lro-response-time, lro-no-patch-lro, lro-no-post-create |
| AZ-092 | DO | G | Validate as much as practical synchronously before starting an LRO. | LRO | lro-valid-inputs-synchronously, lro-put-valid-inputs-synchronously |
| AZ-093 | DO / YOU SHOULD / YOU SHOULD NOT | G | Every LRO initiation returns an absolute `operation-location` header to the status monitor (SHOULD carry the request's `api-version`). DELETE and POST-action LROs return 202 and no other 2xx, even if already complete. PUT-based patterns: AZ-102, AZ-105. | LRO | lro-returns-operation-location, lro-operation-location-includes-api-version, lro-delete-returns-202, lro-delete-returns-only-202, lro-returns-202, lro-returns-only-202 |
| AZ-094 | DO | G | Accept a client `Operation-Id` header, generate an ID (typically a GUID) if absent, return it in `Operation-Id`, and answer 409 on reuse unless the request is an identical retry. | LRO | lro-put-operation-id-request-header, lro-put-operation-id-default-is-guid, lro-put-operation-id-unique-except-retries, lro-put-returns-operation-id-header, lro-delete-operation-id-request-header, lro-delete-operation-id-default-is-guid, lro-operation-id-request-header, lro-operation-id-default-is-guid, lro-operation-id-unique-except-retries |
| AZ-095 | DO / DO NOT | G | Status monitor body: `id`, `status` ∈ NotStarted/Running/Succeeded/Failed/Canceled, `error` on failure, `result` only for action LROs (never for resource LROs), `kind` when polymorphic, plus any values needed to form the GET; POST-action LROs return it in the body. | LRO | lro-status-monitor-structure, lro-status-monitor-includes-all-fields, lro-status-monitor-post-action-result, lro-status-monitor-no-resource-result, lro-returns-status-monitor |
| AZ-096 | DO | G | GET on the status monitor returns 200, includes an integer-seconds `retry-after` until terminal, and the monitor is kept for a publicly documented period (≥ 24 h) after completion. | LRO | lro-status-monitor-get-returns-200, lro-status-monitor-retry-after, lro-status-monitor-retention |

## Conditional requests and telemetry

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-097 | YOU SHOULD | G | Return an `ETag` from any operation that returns or updates a resource. | resource ops | condreq-return-etags |
| AZ-098 | DO | G | Conditional behaviour: GET `If-None-Match` match → 304; PUT/PATCH `If-None-Match: *` with an existing resource → 412; `If-Match` mismatch → 412; DELETE `If-Match` match → 204, mismatch → 412. | conditional headers | condreq-for-read-behavior, condreq-behavior |
| AZ-099 | YOU SHOULD / DO | G | ETag is a hash of the whole representation (strong if range requests are supported) and differs per content encoding. | ETags | condreq-etag-is-hash, condreq-etag-hash-entire-resource, condreq-strong-etag-for-range-requests, condreq-etag-depends-on-encoding |
| AZ-100 | DO | A | Support telemetry headers and OpenTelemetry per the Azure SDK client guidelines (`azure-sdk-telemetry.md`, SDK-01 … SDK-05). | all ops | telemetry-headers |

## Long-running operation patterns

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-101 | DO | G | LRO initiation responses include any extra headers needed to build the GET poll request (e.g. `location`). | LRO | lro-put-response-headers |
| AZ-102 | DO / YOU SHOULD | G | Create-or-replace with long-running processing: `PUT` (optional `operation-id` header) returns 201 (create) or 200 (replace), not 202; body = the resource, same schema as the request; `Operation-Id` header; SHOULD add absolute `Operation-Location` with the request's `api-version`. Idempotent retry → same response; non-idempotent repeat → overwrite or 409. | PUT LRO | lro-create-init, lro-put-returns-200-or-201, lro-put-returns-operation-location, lro-put-operation-location-includes-api-version |
| AZ-103 | DO | G | DELETE LRO: `DELETE` (optional `operation-id`) returns 202 with `operation-id` and `operation-location`; 400 if a request body is sent. | DELETE LRO | lro-delete |
| AZ-104 | DO | G | LRO action on an existing resource: `POST <resource>:<action>` (optional `operation-id`) returns 202 with `operation-id`, `operation-location` and a status-monitor body; an idempotent retry returns the same response. | POST-action LRO | lro-existing-resource |
| AZ-105 | DO / YOU SHOULD | G | LRO action with no related resource (e.g. batch): `PUT <operation-endpoint>/<operation-id>`; operation ID required as the final path segment; SHOULD use one endpoint per action; returns 201 with `operation-location` and a status monitor holding status, request parameters and the eventual result or error; SHOULD serve the monitor from GET on the same URL and use it as `operation-location`. | resource-less LRO | lro-action-no-resource, lro-put-action-operation-endpoint, lro-put-action-operation-id-in-path, lro-put-action-returns-201, lro-put-action-returns-status-monitor, lro-put-action-status-monitor-url |
| AZ-106 | DO / YOU SHOULD | G | Polling: `GET <operation-endpoint>/<operation-id>` returns 200 with the status monitor (plus `retry-after` while not terminal) and SHOULD accept any valid `api-version`, not only the one used to start the operation. | LRO | lro-poll, lro-status-monitor-accepts-any-api-version |
| AZ-107 | YOU MAY / YOU SHOULD | G | Status-monitor collections: MAY support a GET list; SHOULD support listing for resource-less LRO actions; SHOULD support `filter` on `kind` for polymorphic monitor collections. | LRO | lro-list-status-monitors, lro-put-action-list-status-monitors, lro-list-status-monitors-filter |

## Substrings, service host and correlation

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| AZ-108 | DO | G | Every string offset or length in a response is an object `{ "utf8": int, "utf16": int, "codePoint": int }`, all three required. | responses with text offsets/lengths | substrings-return-value-for-each-encoding, substrings-return-value-structure |
| AZ-109 | DO / YOU MAY | A | Service host follows `https://<tenant>.<region>.<service>.<cloud>/<service-root>/…`; region matches an Azure location name; cloud is an Azure cloud domain. A direct endpoint URL `https://<tenant>-<service-root>.<service>.<cloud>/…` MAY be offered. | Azure-hosted endpoints, base URLs in config/spec `servers` | http-url-pattern, http-direct-endpoints |
| AZ-110 | MUST / SHOULD | A | `x-ms-client-request-id`: optional undecorated caller GUID; when present the service MUST log it and must not assume it is unique. `x-ms-request-id`: service-generated, globally unique (MUST), SHOULD be logged with traces. | all ops | distributed-tracing--telemetry |
