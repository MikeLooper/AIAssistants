# Sources — API Design (localized)

Standards are localized in `references/standards/`. Do not fetch these sources during a review.

| Source | Pinned version | Retrieved | Elements | Local file |
|---|---|---|---|---|
| OpenAPI Specification (spec.openapis.org) | v3.0.4 / v3.1.2 / v3.2.1 (+ v2.0 detection) | 2026-11-07 | 43 / 100 | standards/openapi-specification.md |
| Microsoft Azure REST API Guidelines (github.com/microsoft/api-guidelines) | azure/Guidelines.md @ 15c12663 (2026-10-22) | 2026-11-07 (generalized 2026-11-12) | 107 active of 110 (approved exception) | standards/azure-rest-api-guidelines.md |
| Azure SDK general guidelines — telemetry & tracing (azure.github.io/azure-sdk) | docs/general/azurecore.md @ ce65374d (2025-07-30) | 2026-11-07 (generalized 2026-11-12) | 2 active of 5 / 100 | standards/azure-sdk-telemetry.md |

Severity follows the element's own wording; see `SKILL.md` step 5.

The Azure guideline is used only for its generic REST practice. Elements that named an Azure-only mechanism were generalized (Scope `G†`) or retired on 2026-11-12, so no check requires `x-ms-*` headers, `api-version`, Azure host names or the Azure SDK telemetry headers.
