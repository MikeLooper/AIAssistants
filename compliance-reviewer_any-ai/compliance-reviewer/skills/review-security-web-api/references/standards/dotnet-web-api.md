# ASP.NET Core web and API security guidance — localized summary

- Sources: learn.microsoft.com — ASP.NET Core 10.0 (`view=aspnetcore-10.0`), per-page `ms.date` below
- Localized: 2026-11-09 · Elements: learn.microsoft.com 10 (cap 100)
- Applies when language `csharp` is detected and `Microsoft.NET.Sdk.Web` or `Microsoft.AspNetCore.*` is used.
  DNW-08 … DNW-10 apply only to MVC/API controllers (formatters). HDR-16/HDR-17 (in `owasp-web-api.md`) apply only to
  .NET Framework (`web.config` `<system.web>`, `Global.asax`).
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element that is
  violated and name the DNW element in the recommendation. Where vendor guidance is weaker than an OWASP element, the
  OWASP element decides (e.g. the 30-day HSTS default fails HST-01; the 307 redirect default is not a failure).
  Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only ASP.NET Core header, HTTPS, CORS and formatting defaults a worker may rely on. The
  Kestrel `Server` header default is **not** localized: SEC-WA-07 fails for ASP.NET Core only on explicit evidence.
  NWebsec and `NetEscapades.AspNetCore.SecurityHeaders` defaults are not localized either: judge only what the files
  configure.
- Anchors: Microsoft Learn pages carry several version blocks. The 10.0 block has no suffix on `ms-ssl` and `ms-cors`,
  and suffix `-2` on `ms-fmt`.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| ms-ssl | https://learn.microsoft.com/aspnet/core/security/enforcing-ssl?view=aspnetcore-10.0 | ASP.NET Core 10.0, ms.date 2026-10-27 | Microsoft Learn — Enforce HTTPS in ASP.NET Core (10.0) |
| ms-cors | https://learn.microsoft.com/aspnet/core/security/cors?view=aspnetcore-10.0 | ASP.NET Core 10.0, ms.date 2026-05-12 | Microsoft Learn — Enable CORS in ASP.NET Core (10.0) |
| ms-fmt | https://learn.microsoft.com/aspnet/core/web-api/advanced/formatting?view=aspnetcore-10.0 | ASP.NET Core 10.0, ms.date 2026-03-22 | Microsoft Learn — Format response data in ASP.NET Core Web API (10.0) |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| DNW-01 | MUST | Web API projects either don't listen on HTTP, or close HTTP requests with 400. Don't use `RequireHttpsAttribute` on Web APIs that receive sensitive information, because clients may not obey redirects. | `[RequireHttps]` on API controllers; `http://` API endpoints in `ASPNETCORE_URLS`/Kestrel config | SEC-WA-06 | ms-ssl#api-projects, ms-ssl#http-redirect-to-https-err_invalid_redirect-on-cors-preflight-request |
| DNW-02 | MUST | **(Default)** Production web apps call `UseHttpsRedirection` (default status 307). Project templates add it unless created with `--no-https`; it isn't needed where a reverse proxy redirects. | web app pipeline without it and no proxy config | SEC-WA-06 | ms-ssl#require-https, ms-ssl#https-redirection-middleware-usehttpsredirection, ms-ssl#opt-out-of-httpshsts-on-project-creation |
| DNW-03 | MUST | **(Default)** HSTS comes from `UseHsts`, called outside Development. `max-age` defaults to 30 days unless `AddHsts` sets `MaxAge`; `IncludeSubDomains` and `Preload` are opt-in; loopback hosts are excluded. | no `UseHsts`; `UseHsts` without `AddHsts` (30 days → HST-01) | SEC-WA-02 | ms-ssl#http-strict-transport-security-hsts-protocol, ms-ssl#require-https |
| DNW-04 | SHOULD | **(Default)** API project templates don't include HSTS, because it's a browser-only instruction. The secure approach for APIs is to listen and respond over HTTPS only. | (applicability: an HTTPS-only API without HSTS passes) | SEC-WA-02 | ms-ssl#hsts-and-api-projects |
| DNW-05 | MUST | `AllowAnyOrigin` is insecure. `AllowAnyOrigin` with `AllowCredentials` is insecure and invalid, and so is bypassing that check with `SetIsOriginAllowed(_ => true)` plus `AllowCredentials`. | those calls in `AddCors` policies | SEC-WA-05 | ms-cors#set-the-allowed-origins |
| DNW-06 | SHOULD | Prefer named policies applied with `[EnableCors]` to the endpoints that need CORS (finest control). Use wildcard subdomains (`SetIsOriginAllowedToAllowWildcardSubdomains`) only for subdomains you control. | default policy via `UseCors()` covering every endpoint | SEC-WA-05 | ms-cors#enable-cors, ms-cors#set-the-allowed-origins |
| DNW-07 | MUST | Allowing cross-origin credentials (`AllowCredentials`) is a security risk: combine it only with specific trusted origins. `"*"` with credentials is invalid per the CORS specification. | `AllowCredentials()` with broad or configurable-to-any origins | SEC-WA-05 | ms-cors#credentials-in-cross-origin-requests |
| DNW-08 | MUST | **(Default)** Browser `Accept` headers are ignored by default (`RespectBrowserAcceptHeader = false`). When no formatter matches, the first one that can format the object is used; `406` is returned only with `ReturnHttpNotAcceptable = true`. | (supports RST-05: the defaults pass) | SEC-WA-09 | ms-fmt#the-accept-header-2, ms-fmt#browsers-and-content-negotiation-2 |
| DNW-09 | MUST | **(Default)** `string` results are formatted as `text/plain`, or as `text/html` when the client's `Accept` asks for it. | actions returning request-derived strings without `[Produces]` (→ RST-06) | SEC-WA-08 | ms-fmt#special-case-formatters-2 |
| DNW-10 | SHOULD | Use `[Produces]` to fix an action's response format. | — (supports RST-04) | SEC-WA-09 | ms-fmt#specify-a-format-2 |
