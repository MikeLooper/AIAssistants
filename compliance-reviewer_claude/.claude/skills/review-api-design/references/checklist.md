# Checklist — API Design

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| API-01 | An OpenAPI/Swagger spec exists for the API | Warning | https://spec.openapis.org/oas/latest.html |
| API-02 | The spec is syntactically valid per the OpenAPI Specification | Error | https://spec.openapis.org/oas/latest.html |
| API-03 | The spec's paths and schemas match the implemented routes/DTOs | Error | https://spec.openapis.org/oas/latest.html |
| API-04 | Services **DO** use consistent, resource-oriented URL naming and versioning (Azure Guidelines DO) | Error | https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#url-structure |
| API-05 | Services **DO** return appropriate HTTP status codes and a consistent error shape (Azure Guidelines DO) | Error | https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#http-status-codes |
| API-06 | Services **SHOULD** support pagination for collection endpoints (Azure Guidelines YOU SHOULD) | Warning | https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#collections |
| API-07 | Services **SHOULD** version the API explicitly (Azure Guidelines YOU SHOULD) | Warning | https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#versioning |
| API-08 | Services **MAY** support field selection/filtering on collections (Azure Guidelines YOU MAY) | Information | https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#collections |
