# Azure SDK general guidelines (telemetry and distributed tracing) — localized summary

- Source site: azure.github.io/azure-sdk
- Pinned document: `general_azurecore.html` (sections "Telemetry policy" and "Distributed tracing policy"), built from Azure/azure-sdk `docs/general/azurecore.md` @ ce65374d0d4ea008fc607312daa53e503adbeb78 (2025-07-30)
- Citation base: https://azure.github.io/azure-sdk/general_azurecore.html (the published page has no commit permalink; the pinned commit above identifies the localized text)
- Localized: 2026-11-07 · Elements: 5 (cap 100)
- Source name for `Finding.standard`: `Azure SDK General Guidelines`
- The source is written for **client libraries**. AZ-100 tells services to follow it, so each element restates the client rule as what the **service** must accept, propagate or capture. Level keeps the client rule's rendered wording (DO / YOU SHOULD), which sets the severity.

| ID | Level | Scope | Requirement for the service (summary) | Applies when | Anchor(s) |
|----|-------|-------|---------------------------------------|--------------|-----------|
| SDK-01 | DO / YOU SHOULD | A | Accept the full SDK `User-Agent` without rejecting or truncating it: `[<appId> ]azsdk-<lang>-<package>/<version> … (<platform>)`, wrapper libraries listed outermost-first, application ID ≤ 24 characters. Capture it in request telemetry. | all ops | azurecore-http-telemetry-useragent, azurecore-http-telemetry-useragent-stacking, azurecore-http-telemetry-useragent-stacking-core, azurecore-http-telemetry-appid, azurecore-http-telemetry-appid-length |
| SDK-02 | YOU SHOULD | A | Capture `X-MS-UserAgent` (sent when a platform can't set `User-Agent`) in queryable request logs. | all ops | azurecore-http-telemetry-x-ms-useragent |
| SDK-03 | YOU SHOULD | A | Capture `X-MS-AZSDK-Telemetry` (`key=value;…`, e.g. `class`, `method`) in queryable logs; never require or expect personal data in it. | all ops | azurecore-http-telemetry-dynamic |
| SDK-04 | DO | G | Accept W3C Trace Context headers (`traceparent`, `tracestate`) and continue the caller's trace, using the incoming context as the parent span. | all ops | azurecore-http-tracing-pass-context, azurecore-http-tracing-accept-context |
| SDK-05 | DO | G | Instrument request handling with OpenTelemetry and populate span attributes per the Azure tracing conventions. | all ops | azurecore-http-tracing-opentelemetry, azurecore-http-tracing-opentelemetry-conventions |
