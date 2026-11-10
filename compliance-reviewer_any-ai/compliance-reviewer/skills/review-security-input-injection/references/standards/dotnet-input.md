# .NET / ASP.NET Core / EF Core input & injection guidance — localized summary

- Sources: cheatsheetseries.owasp.org — OWASP .NET Security Cheat Sheet (input-handling and legacy sections only)
  @ OWASP/CheatSheetSeries 3cfa49de48236c667ddf1d0f9dc79e13e672b56d (2026-10-18); learn.microsoft.com pages below
  (ASP.NET Core 10.0, .NET 10; unversioned pages pinned by `ms.date`)
- Localized: 2026-11-08 · Elements: 15 — cheatsheetseries.owasp.org 6 (counted with `owasp-input-injection.md`: 66, cap 100);
  learn.microsoft.com 9 (cap 100)
- Applies when language `csharp` is detected. EF Core elements (NET-01, NET-02, NET-07) apply when
  `Microsoft.EntityFrameworkCore*` is referenced; ASP.NET Core elements (NET-03, NET-10 … NET-14) when
  `Microsoft.AspNetCore.*`/`Microsoft.NET.Sdk.Web` is used; NET-06 only for legacy ASP.NET (`System.Web`); runtime
  elements (NET-04, NET-05, NET-08, NET-09, NET-15) always.
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element it supports
  and name the NET element in the recommendation. Where vendor guidance is weaker than an OWASP element (e.g. EF Core's
  advice to "sanitize" dynamic column names), the OWASP element (SQL-04, SQL-05) decides. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only .NET defaults a worker may rely on. `XmlDocument`/`XmlTextReader` defaults on .NET
  Framework are **not** localized: report only explicit insecure settings there, and add a `localized-standard-gap` note
  for a missing setting.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor; for `dtd` and `arg` (API reference pages
  without section ids) the citation base alone. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| dnet | https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html | commit 3cfa49de (2026-10-18) | OWASP .NET Security Cheat Sheet |
| efsql | https://learn.microsoft.com/ef/core/querying/sql-queries | `ms.date` 2022-09-19 | Microsoft Learn — EF Core SQL Queries |
| upl | https://learn.microsoft.com/aspnet/core/mvc/models/file-uploads?view=aspnetcore-10.0 | ASP.NET Core 10.0 (`ms.date` 2026-10-03) | Microsoft Learn — Upload files in ASP.NET Core |
| axss | https://learn.microsoft.com/aspnet/core/security/cross-site-scripting?view=aspnetcore-10.0 | ASP.NET Core 10.0 (`ms.date` 2026-05-13) | Microsoft Learn — Prevent XSS in ASP.NET Core |
| val | https://learn.microsoft.com/aspnet/core/mvc/models/validation?view=aspnetcore-10.0 | ASP.NET Core 10.0 (`ms.date` 2026-10-26) | Microsoft Learn — Model validation in ASP.NET Core |
| dtd | https://learn.microsoft.com/dotnet/api/system.xml.xmlreadersettings.dtdprocessing?view=net-10.0 | .NET 10 | Microsoft Learn — XmlReaderSettings.DtdProcessing |
| bf | https://learn.microsoft.com/dotnet/standard/serialization/binaryformatter-security-guide | `ms.date` 2022-03-02 | Microsoft Learn — BinaryFormatter security guide |
| arg | https://learn.microsoft.com/dotnet/api/system.diagnostics.processstartinfo.argumentlist?view=net-10.0 | .NET 10 | Microsoft Learn — ProcessStartInfo.ArgumentList |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| NET-01 | MUST | Prefer EF LINQ; for SQL text use `FromSql`/`FromSqlInterpolated`; never concatenate untrusted values into SQL passed to `FromSqlRaw` or other command APIs. | `FromSqlRaw($"… {input}")`; `SqlCommand` with concatenated text | SEC-II-02 | dnet#sql-injection, dnet#input-handling |
| NET-02 | MUST | Parameters are values, not identifiers: map dynamic table/column names to a fixed allowlist; parameterization doesn't replace a minimal-privilege DB account. | dynamic identifiers from input | SEC-II-03 | dnet#sql-injection |
| NET-03 | MUST | Don't bypass Razor encoding with `Html.Raw`/`HtmlString` for untrusted content; HTML encoding isn't safe inside JS, CSS or URLs; user HTML goes through a maintained sanitizer. | `@Html.Raw(Model.UserText)`; `new HtmlString(input)` | SEC-II-08 | dnet#cross-site-scripting-xss |
| NET-04 | MUST | Prefer a data-only format (`System.Text.Json`) into application-defined types and validate the values; a different serializer doesn't remove the need to constrain converters and type selection. | polymorphic converters driven by payload type names | SEC-II-09 | dnet#serialization-and-xml, bf#preferred-alternatives |
| NET-05 | MUST | XML: disable unnecessary external resource resolution and follow the settings for the parser in use; defaults differ by API and framework version. | `XmlResolver = new XmlUrlResolver()`; `DtdProcessing.Parse` on untrusted input | SEC-II-05 | dnet#serialization-and-xml |
| NET-06 | MUST | Legacy ASP.NET: request validation alone doesn't prevent XSS; use context-appropriate output encoding. | `<%= %>` / `@Html.Raw` relying on `ValidateRequest` | SEC-II-08 | dnet#aspnet-mvc-and-web-forms, dnet#legacy-net-framework |
| NET-07 | MUST | (Default) `FromSql`, `FromSqlInterpolated` and `ExecuteSql` wrap interpolated values in `DbParameter`s; `FromSqlRaw`/`ExecuteSqlRaw` insert interpolated values as raw SQL, so values must be passed as `DbParameter`s. Identifiers follow SQL-04. | `ExecuteSqlRaw($"…{v}")`; `FromSqlRaw("…" + v)` | SEC-II-02 | efsql#passing-parameters, efsql#dynamic-sql-and-parameters, efsql#executing-non-querying-sql, efsql#basic-sql-queries |
| NET-08 | MUST | (Default) `XmlReaderSettings.DtdProcessing` defaults to `Prohibit`; `Parse` enables DTDs, so setting it on untrusted input fails XML-01 unless XML-02 holds. | explicit `DtdProcessing = DtdProcessing.Parse` | SEC-II-05 | dtd |
| NET-09 | MUST | `BinaryFormatter.Deserialize` is never safe with untrusted input, and a `SerializationBinder` or configuration switch can't mitigate it; `SoapFormatter`, `LosFormatter`, `NetDataContractSerializer` and `ObjectStateFormatter` are equally dangerous. | any of these on external data | SEC-II-09 | bf#binaryformatter-security-vulnerabilities, bf#dangerous-alternatives, bf#deserialization-vulnerabilities |
| NET-10 | MUST | Never use the client filename for storage; create one with `Path.GetRandomFileName`/`GetTempFileName`; HTML-encode the original name when displaying outside Razor; check for collisions. | `Path.Combine(dir, file.FileName)` | SEC-II-06 | upl#file-name-security, upl#security-considerations |
| NET-11 | MUST | (Default) Kestrel caps request bodies at 30,000,000 bytes and `FormOptions.MultipartBodyLengthLimit` at 134,217,728 bytes; removing or raising limits without bound fails FU-05/IV-04. | `MaxRequestBodySize = null`; `[DisableRequestSizeLimit]`; very large `[RequestSizeLimit]` on upload actions | SEC-II-06 | upl#kestrel-maximum-request-body-size, upl#multipart-body-length-limit, upl#request-body-size-limits-summary, upl#size-validation, upl#per-request-body-size-limits |
| NET-12 | MUST | Store uploads in a dedicated location outside the app's directory tree with execute permissions disabled. | uploads saved under the content root/`wwwroot` | SEC-II-07 | upl#security-considerations |
| NET-13 | MUST | Encode at the point of output (don't store encoded values); pass data to JS via `data-` attributes read with `textContent`, or use `JavaScriptEncoder`; use `HtmlEncoder`/`UrlEncoder` in code; no `document.write`/DOM string concatenation. | `JsonSerializer.Serialize(model)` inlined into `<script>`; `innerHTML` with server values | SEC-II-08 | axss#protect-your-application-against-xss, axss#explore-javascript-encoding-with-razor, axss#access-encoders-in-code, axss#determine-when-and-where-to-encode, axss#encode-url-parameters |
| NET-14 | MUST | (Default) Web apps must check `ModelState.IsValid`; `[ApiController]` returns 400 automatically when model state is invalid. Client-side validation doesn't replace server-side checks. | MVC/Razor Pages handlers without `ModelState.IsValid`; `SuppressModelStateInvalidFilter = true` without manual checks | SEC-II-01 | val#model-state, val#client-side-validation |
| NET-15 | SHOULD | Use `ProcessStartInfo.ArgumentList` (escaped per argument) rather than the `Arguments` string; `ProcessStartInfo` with untrusted data is a security risk. | `Arguments = "… " + input` | SEC-II-04 | arg |
