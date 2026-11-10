# Detection signals — C#/.NET (Security: Web & API)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only on concrete code or an explicit setting; a missing header follows the
evidence rule in `SKILL.md` step 3. The only ASP.NET Core defaults a worker may rely on are those stated in
`dotnet-web-api.md` (DNW-02, DNW-03, DNW-04, DNW-08, DNW-09). The Kestrel `Server` header default and NWebsec /
`NetEscapades.AspNetCore.SecurityHeaders` defaults are not localized: report explicit values only.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| No `app.UseHsts()` in the non-Development branch of a web app; `UseHsts()` without `AddHsts(o => o.MaxAge = …)` (30-day default); `IncludeSubDomains` not set | `Program.cs`, `Startup.cs` | Missing or short HSTS | DNW-03, HDR-07, HST-01, HST-02 |
| No `app.UseHttpsRedirection()` in a web app and no proxy redirect in the files | `Program.cs`, `Startup.cs`, proxy config | HTML site reachable over HTTP | DNW-02, TLS-03 |
| `[RequireHttps]` / `RequireHttpsAttribute` on API controllers | controllers, filters, `AddControllers(o => o.Filters…)` | Redirect as an API's only HTTP protection | DNW-01, TLS-04 |
| `http://` URLs in `ASPNETCORE_URLS`, Kestrel `Endpoints`, `launchSettings.json` non-Development profiles or the `Dockerfile` (`EXPOSE 80` + `ASPNETCORE_HTTP_PORTS`) | `appsettings*.json`, `launchSettings.json`, `Dockerfile`, compose | Plain-HTTP listener in production | RST-01, DNW-01 |
| `ConfigureHttpsDefaults(o => o.SslProtocols = SslProtocols.Tls \| SslProtocols.Tls11)`; `SslProtocols` set in Kestrel config | `Program.cs`, `appsettings*.json` | Legacy TLS enabled | TLS-01 |
| Explicit `CipherSuitesPolicy` listing `TLS_RSA_*`, NULL, anon or EXPORT suites | `Program.cs` | Weak ciphers | TLS-02 |
| `AddCors` policy with `AllowAnyOrigin()`; `SetIsOriginAllowed(_ => true)`; `AllowCredentials()` with broad or config-driven origins that may be `*` | `Program.cs`, `Startup.cs` | Any-origin or credentialed broad CORS | DNW-05, DNW-07, H5-01 |
| `app.UseCors()` with a default policy covering every endpoint, where only some need CORS | `Program.cs` | Global CORS scope | DNW-06, H5-02, RST-10 |
| Middleware echoing `Request.Headers.Origin` into `Access-Control-Allow-Origin`; authorization branches on `Origin` | custom middleware, filters | Reflected origin; CORS as access control | H5-01, H5-03 |
| `context.Response.Headers[...]` / `Headers.Append` for `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `Cross-Origin-*`; NWebsec / NetEscapades header policies | middleware, `Program.cs` | Headers set (check values against HDR/CSP rows) | CSP-01, CSP-05, HDR-01, HDR-03, HDR-04, HDR-10, HDR-12, HDR-13 |
| `X-XSS-Protection` set to `1`; `Expect-CT`; `Public-Key-Pins`; `X-Content-Security-Policy` | middleware, `web.config` `<customHeaders>` | Harmful or obsolete headers | HDR-02, HDR-08, HDR-18, CSP-02 |
| `X-Powered-By` added; informative `Server` value set | middleware, `web.config` `<customHeaders>` | Version-revealing headers | HDR-15, HDR-14 |
| `web.config` `<system.web><httpRuntime>` without `enableVersionHeader="false"`; `Global.asax` without `MvcHandler.DisableMvcResponseHeader = true` | `web.config`, `Global.asax` (.NET Framework only) | Version headers on | HDR-16, HDR-17 |
| Actions returning `string` built from request data without `[Produces("application/json")]` | controllers | `text/html` reflection possible | DNW-09, RST-06 |
| `RespectBrowserAcceptHeader = true` together with `StringOutputFormatter`; `Response.ContentType = Request.Headers.Accept` | `AddControllers(o => …)`, controllers | `Accept` drives `Content-Type` | DNW-08, RST-05 |
| `AddXmlSerializerFormatters()` / `AddXmlDataContractSerializerFormatters()` on a JSON-only API; body read manually without `[Consumes]` or a content-type check | `Program.cs`, controllers | Unintended formats accepted | RST-04, RST-03, DNW-10 |
| `MapMethods(pattern, new[] { "GET","POST","PUT","DELETE","PATCH","TRACE", … })` on handlers needing one method | minimal API registrations | Any-method handler | RST-02, A02-03 |
| `[FromQuery] string apiKey\|token\|password`; `Request.Query["api_key"]`; `HttpClient` calls building `?access_token=` | controllers, minimal APIs, clients | Credentials in URLs | RST-11, RST-12 |
| `File(...)`/`PhysicalFile(...)` returning uploads with the stored content type and no `fileDownloadName` | controllers | Inline download of user files | HDR-19 |
| Sensitive API responses with `[ResponseCache]` or `Cache-Control: public`/`no-cache` only | controllers, middleware | Cacheable sensitive responses | HDR-06, RST-07 |
