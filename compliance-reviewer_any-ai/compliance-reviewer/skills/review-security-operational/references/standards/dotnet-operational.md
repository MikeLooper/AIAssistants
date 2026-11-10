# .NET / ASP.NET Core operational security guidance — localized summary

- Sources: cheatsheetseries.owasp.org — OWASP .NET Security Cheat Sheet @ OWASP/CheatSheetSeries
  3cfa49de48236c667ddf1d0f9dc79e13e672b56d (2026-10-18), configuration/deployment and data-protection sections only;
  learn.microsoft.com — ASP.NET Core 10.0 (`view=aspnetcore-10.0`) and .NET logging pages (per-page `ms.date` below)
- Localized: 2026-11-08 · Elements: 16 — cheatsheetseries.owasp.org 5 (site total 52 with `owasp-operational.md`,
  cap 100); learn.microsoft.com 11 (cap 100)
- Applies when language `csharp` is detected. ASP.NET Core elements (DNO-03, -04, -06 … -12, -14) apply when
  `Microsoft.AspNetCore.*` or `Microsoft.NET.Sdk.Web` is used; DNO-05 when ASP.NET Core Data Protection is configured;
  DNO-13 when the app is Azure-hosted or uses `Azure.Extensions.AspNetCore.Configuration.Secrets`; DNO-01, -02, -15,
  -16 always. ERR-06 (in `owasp-operational.md`) applies only to .NET Framework Web API projects.
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element it supports
  and name the DNO element in the recommendation. Where vendor guidance is weaker than an OWASP element, the OWASP
  element decides. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only .NET defaults a worker may rely on. Serilog, NLog and log4net sink, enricher and
  destructuring defaults are **not** localized: report only explicit insecure settings there, and add a
  `localized-standard-gap` note for a missing setting.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| dnet | https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html | 3cfa49de (2026-10-18) | OWASP .NET Security Cheat Sheet |
| ms-err | https://learn.microsoft.com/aspnet/core/fundamentals/error-handling?view=aspnetcore-10.0 | ASP.NET Core 10.0, ms.date 2026-10-27 | Microsoft Learn — Handle errors in ASP.NET Core (10.0) |
| ms-env | https://learn.microsoft.com/aspnet/core/fundamentals/environments?view=aspnetcore-10.0 | ASP.NET Core 10.0, ms.date 2026-11-04 | Microsoft Learn — ASP.NET Core runtime environments (10.0) |
| ms-sec | https://learn.microsoft.com/aspnet/core/security/app-secrets?view=aspnetcore-10.0 | ASP.NET Core 10.0, ms.date 2026-05-13 | Microsoft Learn — Safe storage of app secrets in development (10.0) |
| ms-kv | https://learn.microsoft.com/aspnet/core/security/key-vault-configuration?view=aspnetcore-10.0 | ASP.NET Core 10.0, ms.date 2026-05-13 | Microsoft Learn — Azure Key Vault configuration provider (10.0) |
| ms-hlog | https://learn.microsoft.com/aspnet/core/fundamentals/http-logging/?view=aspnetcore-10.0 | ASP.NET Core 10.0, ms.date 2025-04-25 | Microsoft Learn — HTTP logging in ASP.NET Core (10.0) |
| ms-log | https://learn.microsoft.com/dotnet/core/extensions/logging/overview | ms.date 2025-10-21 | Microsoft Learn — Logging in .NET |
| ms-red | https://learn.microsoft.com/dotnet/core/extensions/data-redaction | ms.date 2025-03-21 | Microsoft Learn — Data redaction in .NET |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| DNO-01 | MUST | Keep secrets out of source code and checked-in configuration. | credentials in `appsettings*.json`, `web.config`, code | SEC-OP-05 | dnet#configuration-and-deployment |
| DNO-02 | MUST | Use User Secrets only for development (it isn't encrypted storage); get production credentials from a managed secret store. | `AddUserSecrets` outside Development; production secrets in user-secrets docs/scripts | SEC-OP-06 | dnet#configuration-and-deployment |
| DNO-03 | MUST | Run production apps outside the Development environment. | `ASPNETCORE_ENVIRONMENT=Development` in production Dockerfile/manifests/launch config | SEC-OP-07 | dnet#configuration-and-deployment |
| DNO-04 | MUST | Use exception-handling middleware that returns generic errors; keep stack traces, credentials and request details out of responses. | no `UseExceptionHandler` in non-Development pipeline | SEC-OP-01 | dnet#configuration-and-deployment |
| DNO-05 | MUST | Protect ASP.NET Core Data Protection keys: when overriding key persistence, configure encryption at rest and restrict access to the key repository. | `PersistKeysTo*` without `ProtectKeysWith*` | SEC-OP-06 | dnet#encryption-for-storage, dnet#data-protection |
| DNO-06 | MUST | **(Default)** The developer exception page is on by default only in Development, for apps built with `WebApplication.CreateBuilder`; older templates call `UseDeveloperExceptionPage`. It shows stack trace, query, cookies and headers. Don't enable it outside Development. | `app.UseDeveloperExceptionPage()` not gated on `IsDevelopment()` | SEC-OP-07 | ms-err#developer-exception-page |
| DNO-07 | MUST | **(Default)** If the environment isn't set, it is Production, which disables most debugging features; `DOTNET_ENVIRONMENT`, if present, takes precedence over `ASPNETCORE_ENVIRONMENT` for `CreateBuilder` apps. | environment variables set to Development in deployment files | SEC-OP-07 | ms-env#environment-variables-that-determine-the-runtime-environment, ms-env#environments |
| DNO-08 | MUST | Non-Development pipelines call `UseExceptionHandler` with a path, a lambda, or `AddProblemDetails()`; registered `IExceptionHandler`s are never called without it. | `AddExceptionHandler<T>()` but no `UseExceptionHandler()` | SEC-OP-01 | ms-err#exception-handler-page, ms-err#iexceptionhandler, ms-err#configure-useexceptionhandler-when-using-iexceptionhandler |
| DNO-09 | MUST | Error pages, lambdas and `IExceptionHandler`s don't serve sensitive error information (exception messages, details) to clients. | `exceptionHandlerPathFeature.Error.Message` written to the response | SEC-OP-01 | ms-err#access-the-exception-and-original-routing-details, ms-err#exception-handler-lambda |
| DNO-10 | MUST | **(Default)** From .NET 10, when an `IExceptionHandler` returns `true`, logs and metrics for that exception are suppressed by default (.NET 8/9 always emitted them); log in the handler or set `SuppressDiagnosticsCallback`. | `TryHandleAsync` returns `true` without logging | SEC-OP-02 | ms-err#iexceptionhandler, ms-err#suppressdiagnosticscallback |
| DNO-11 | SHOULD | **(Default)** Environment variables are commonly stored as plain, unencrypted text and are readable by untrusted parties if the machine or process is compromised. | (supports SMG-07 recommendations; never fails on its own) | SEC-OP-06 | ms-sec#work-with-environment-variables |
| DNO-12 | MUST | **(Default)** Secret Manager stores values unencrypted in a JSON file in the user profile, outside the project tree; it's for development only and isn't a trusted store. | code reading `secrets.json` paths; Secret Manager referenced for production | SEC-OP-06 | ms-sec#use-the-secret-manager-tool |
| DNO-13 | SHOULD | Azure-hosted apps authenticate to Key Vault with a managed identity (`DefaultAzureCredential`) instead of client secrets or certificates kept in configuration. | Key Vault client secret/`ClientSecretCredential` values in config | SEC-OP-06 | ms-kv#use-managed-identities-for-azure-resources, ms-kv#use-application-id-and-x509-certificate-for-non-azure-hosted-apps |
| DNO-14 | MUST | **(Default)** HTTP logging logs request/response properties and headers by default (`LoggingFields` = `RequestPropertiesAndHeaders \| ResponsePropertiesAndHeaders`), header values only for names in `RequestHeaders`/`ResponseHeaders` (others `[Redacted]`), bodies only when enabled; it can log PII. Don't allowlist sensitive headers or log sensitive bodies. | `RequestHeaders.Add("Authorization")`; `HttpLoggingFields.RequestBody`/`All` | SEC-OP-03 | ms-hlog#http-logging-in-aspnet-core, ms-hlog#loggingfields, ms-hlog#requestheaders-and-responseheaders |
| DNO-15 | SHOULD | Use the .NET redaction framework (`AddRedaction` with data classification) when logging potentially sensitive data. | sensitive fields logged without redaction | SEC-OP-03 | ms-red#logging-sensitive-information |
| DNO-16 | SHOULD | Use log message templates with named placeholders and arguments, not string interpolation (analyzer CA2254: template should be a static expression). | `_logger.LogInformation($"User {name}")` | SEC-OP-04 | ms-log#log-message-template, ms-log#log-message-template-formatting |
