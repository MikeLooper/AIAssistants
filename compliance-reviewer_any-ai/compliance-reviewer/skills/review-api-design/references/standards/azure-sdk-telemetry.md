# Azure SDK general guidelines (telemetry and distributed tracing) — localized summary

- Source site: azure.github.io/azure-sdk
- Pinned document: `general_azurecore.html` (sections "Telemetry policy" and "Distributed tracing policy"), built from Azure/azure-sdk `docs/general/azurecore.md` @ ce65374d0d4ea008fc607312daa53e503adbeb78 (2025-07-30)
- Citation base: https://azure.github.io/azure-sdk/general_azurecore.html (the published page has no commit permalink; the pinned commit above identifies the localized text)
- Localized: 2026-11-07 · Generalized: 2026-11-12 · Elements: 5 IDs, 2 active (cap 100); SDK-01 … SDK-03 retired
- Source name for `Finding.standard`: `Azure SDK General Guidelines`
- The source is written for **client libraries**; each element restates a client rule as what the **service** must accept, propagate or capture. Only its generic trace-context rules are kept: the Azure SDK `User-Agent` format and the `x-ms-*` telemetry headers (SDK-01 … SDK-03) were retired on 2026-11-12 because they apply only to Azure SDK callers. G† = generalized locally (see `azure-rest-api-guidelines.md`). Level keeps the client rule's rendered wording (DO / YOU SHOULD), which sets the severity.

| ID | Level | Scope | Requirement for the service (summary) | Applies when | Anchor(s) |
|----|-------|-------|---------------------------------------|--------------|-----------|
| SDK-01 (retired) | — | — | *(retired 2026-11-12, Azure-only: Azure SDK `User-Agent` format)* | — | azurecore-http-telemetry-useragent, azurecore-http-telemetry-useragent-stacking, azurecore-http-telemetry-useragent-stacking-core, azurecore-http-telemetry-appid, azurecore-http-telemetry-appid-length |
| SDK-02 (retired) | — | — | *(retired 2026-11-12, Azure-only: `X-MS-UserAgent` header)* | — | azurecore-http-telemetry-x-ms-useragent |
| SDK-03 (retired) | — | — | *(retired 2026-11-12, Azure-only: `X-MS-AZSDK-Telemetry` header)* | — | azurecore-http-telemetry-dynamic |
| SDK-04 | DO | G | Accept W3C Trace Context headers (`traceparent`, `tracestate`) and continue the caller's trace, using the incoming context as the parent span. | all ops | azurecore-http-tracing-pass-context, azurecore-http-tracing-accept-context |
| SDK-05 | DO | G† | Instrument request handling with OpenTelemetry and populate span attributes per the OpenTelemetry HTTP semantic conventions (the source names the Azure tracing conventions, which build on them). | all ops | azurecore-http-tracing-opentelemetry, azurecore-http-tracing-opentelemetry-conventions |
