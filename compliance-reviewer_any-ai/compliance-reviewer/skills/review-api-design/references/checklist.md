# Checklist — API Design

Subject: API Design

Each check is evaluated only against the elements it lists, in the local files under `standards/`. A Finding's severity comes from the failed element's level (see `SKILL.md`); `severityIfFailed` is always the check's default severity below.

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|------------------|----------|--------|
| API-01 | OpenAPI Specification | An OpenAPI/Swagger spec exists for the API | Warning | OAS-01–OAS-03 | openapi-specification.md |
| API-02 | OpenAPI Specification | The spec is structurally valid for its declared OAS version | Error | OAS-01–OAS-26, OAS-29, OAS-31, OAS-32, OAS-34, OAS-35, OAS-37, OAS-43 | openapi-specification.md |
| API-03 | Spec Drift | The spec's paths, parameters, schemas, status codes and security match the implementation | Error | OAS-27, OAS-28, OAS-30, OAS-33, OAS-36, OAS-38–OAS-42 (+ OAS-26, OAS-29 where they reveal drift) | openapi-specification.md |
| API-04 | URLs & Resources | Resource-oriented, consistently cased and readable URLs and hosts; actions follow the action pattern | Error | AZ-001–AZ-008, AZ-030, AZ-069, AZ-071, AZ-109 | azure-rest-api-guidelines.md |
| API-05 | Status Codes & Errors | Correct HTTP status codes and a consistent, documented error shape | Error | AZ-012, AZ-015–AZ-018, AZ-031, AZ-040, AZ-043–AZ-050 | azure-rest-api-guidelines.md |
| API-06 | Pagination | Collection endpoints support server-driven pagination correctly | Warning | AZ-073–AZ-079 | azure-rest-api-guidelines.md |
| API-07 | Versioning | The API is versioned explicitly, without path versions or in-version breaking changes | Warning | AZ-085–AZ-090 | azure-rest-api-guidelines.md |
| API-08 | Filtering & Sorting | Collections support filtering/sorting/field selection correctly (if offered) | Information | AZ-080–AZ-084 | azure-rest-api-guidelines.md |
| API-09 | Method Semantics | HTTP method semantics, idempotency and a single resource schema | Error | AZ-009–AZ-011, AZ-014, AZ-033–AZ-039, AZ-041, AZ-070, AZ-072 | azure-rest-api-guidelines.md |
| API-10 | Query Parameters & Headers | Query-parameter and header conventions and validation | Error | AZ-020–AZ-026, AZ-028, AZ-029 | azure-rest-api-guidelines.md |
| API-11 | JSON Representation | JSON representation conventions (casing, nulls, numbers, dates, IDs, string contracts, substring offsets) | Error | AZ-032, AZ-042, AZ-051–AZ-061, AZ-108 | azure-rest-api-guidelines.md |
| API-12 | Enums & Polymorphism | Evolvable enums and polymorphic types | Warning | AZ-062–AZ-068 | azure-rest-api-guidelines.md |
| API-13 | Long-Running Operations | Long-running operations follow the matching LRO pattern (N/A when none exist) | Error | AZ-013, AZ-091–AZ-096, AZ-101–AZ-107 | azure-rest-api-guidelines.md |
| API-14 | Conditional Requests | Conditional requests and ETags | Warning | AZ-019, AZ-097–AZ-099 | azure-rest-api-guidelines.md |
| API-15 | Correlation & Telemetry | Request correlation, telemetry and distributed-tracing headers are accepted, propagated and captured | Warning | AZ-027, AZ-100, AZ-110, SDK-01–SDK-05 | azure-rest-api-guidelines.md, azure-sdk-telemetry.md |
