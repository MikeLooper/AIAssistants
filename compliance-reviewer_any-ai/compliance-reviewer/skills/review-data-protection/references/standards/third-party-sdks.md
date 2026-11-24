# Third-party SDK data collection (error trackers, APM) — localized summary

- Sources: docs.sentry.io — "Data Collected" pages for .NET, Java, Python (SDK 3.x) and JavaScript (page text at
  retrieval 2026-11-24, recorded as text hashes in `pins.json`); learn.microsoft.com — Application Insights FAQ
  (`ms.date` 2026-05-03)
- Localized: 2026-11-24 · Elements: docs.sentry.io 4 (cap 100), learn.microsoft.com 1 (cap 100)
- Applies only when the SDK is in the files: Sentry rows by platform (`Sentry` NuGet package / `io.sentry` / `sentry-sdk`
  / `@sentry/*`), Application Insights when its SDK or the Azure Monitor OpenTelemetry distro is referenced. Language
  detection doesn't gate these rows.
- Level: `MUST` for "do not" guidance; **(Default)** marks an element that states SDK behaviour or a default. Defaults
  stated here are the only SDK defaults a worker may rely on. Levels are informational: every Finding takes its
  check's default severity.
- Ownership: telemetry attributes and custom telemetry content belong to `review-observability` (OBS-10); these rows
  judge only the SDK switches that send user data, and URLs.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Pinned version | Source name for `Finding.standard` |
|-----|---------------|----------------|------------------------------------|
| sdn | https://docs.sentry.io/platforms/dotnet/data-management/data-collected/ | page at retrieval 2026-11-24 (Sentry .NET 7.0.1) | Sentry for .NET — Data Collected |
| sjv | https://docs.sentry.io/platforms/java/data-management/data-collected/ | page at retrieval 2026-11-24 | Sentry for Java — Data Collected |
| spy | https://docs.sentry.io/platforms/python/data-management/data-collected/ | page at retrieval 2026-11-24 (SDK 3.x) | Sentry for Python — Data Collected |
| sjs | https://docs.sentry.io/platforms/javascript/data-management/data-collected/ | page at retrieval 2026-11-24 | Sentry for JavaScript — Data Collected |
| aip | https://learn.microsoft.com/azure/azure-monitor/app/application-insights-faq | ms.date 2026-05-03 | Microsoft Learn — Application Insights FAQ |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| TPS-01 | SHOULD | **(Default)** Sentry .NET: `SendDefaultPii` is off by default. When `true`, the SDK sends cookies, logged-in user information (email, user ID, username), the user's IP address, the full absolute request URI and the machine name. The request query string is always sent. | `o.SendDefaultPii = true`; `"SendDefaultPii": true` in `appsettings*.json` | DPR-04 | sdn#information-about-logged-in-user, sdn#cookies, sdn#users-ip-address, sdn#request-url, sdn#request-query-string |
| TPS-02 | SHOULD | **(Default)** Sentry Java: `dataCollection.userInfo` defaults to `true`, adding user identity (including Spring Security usernames) and the user's IP address; headers, cookies and query parameters use deny-lists by default; Spring MVC request bodies are collected only once `maxRequestBodySize` is set (default `NONE`). | no `dataCollection.userInfo=false` where personal data flows; `maxRequestBodySize` raised on personal-data endpoints | DPR-04 | sjv#information-about-logged-in-user, sjv#users-ip-addresses, sjv#request-body |
| TPS-03 | SHOULD | **(Default)** Sentry Python (SDK 3.x): `data_collection.user_info` defaults to `True` (user id, email, username, IP address); request headers, cookies and query parameters are sent with deny-list scrubbing; JSON and form request bodies, local variables in stack frames (not scrubbed by default) and gen-AI inputs and outputs are collected by default. | `sentry_sdk.init(...)` with no `data_collection` limits (`user_info`, `http_bodies`, `stack_frame_variables`, `gen_ai`) in an app that handles personal data | DPR-04 | spy#information-about-logged-in-user, spy#request-body, spy#local-variables-in-stack-trace, spy#llm-inputs-and-responses |
| TPS-04 | SHOULD | **(Default)** Sentry JavaScript: the user's IP address is sent by default (`dataCollection.userInfo`); on the server, incoming-request cookies and the full query string are collected by default (values of sensitive keys filtered); data set with `Sentry.setUser()` is always sent. | `Sentry.init` without `dataCollection` limits; `Sentry.setUser({ email, … })` | DPR-04 | sjs#users-ip-address-and-location, sjs#cookies, sjs#request-query-string, sjs#information-about-logged-in-user |
| TPS-05 | MUST | Application Insights: don't put sensitive data in URLs (request URLs are collected as telemetry). | personal data in routes or query strings of an app instrumented with Application Insights | DPR-03 | aip#privacy-and-responsible-use |
