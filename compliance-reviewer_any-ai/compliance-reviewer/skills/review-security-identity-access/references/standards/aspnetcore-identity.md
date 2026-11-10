# ASP.NET Core / ASP.NET identity guidance — localized summary

- Source: cheatsheetseries.owasp.org — OWASP .NET Security Cheat Sheet (identity sections only)
  @ OWASP/CheatSheetSeries 3cfa49de48236c667ddf1d0f9dc79e13e672b56d (2026-10-18)
- Localized: 2026-11-08 · Elements: 14 (counted with the 80 in `owasp-identity-access.md`: cheatsheetseries.owasp.org 94, cap 100)
- Applies when ASP.NET Core (`Microsoft.AspNetCore.*`) or legacy ASP.NET (`System.Web`, ASP-14) is in use.
  Microsoft Learn defaults (e.g. `TokenValidationParameters`, cookie defaults) are **not** localized: report only
  explicit insecure settings for those, and add a `localized-standard-gap` note for a missing setting.
- Framework elements apply only when that framework is in use; otherwise they don't apply.
- Level: a framework element takes the level of the OWASP element it implements (e.g. a cookie-flag setting implements
  SES-04/SES-05), or `SHOULD` when the vendor only recommends. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only framework defaults a worker may rely on. Never use remembered defaults.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Source name for `Finding.standard` |
|-----|---------------|------------------------------------|
| dnet | https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html | OWASP .NET Security Cheat Sheet |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| ASP-01 | MUST | Use ASP.NET Core Identity or a supported IdP integration; don't build password recovery or session management from scratch. | custom user/password/session tables and middleware | SEC-IA-07 | dnet#authentication-and-authorization |
| ASP-02 | SHOULD | Enable lockout: `LockoutEnabled`, `IdentityOptions.Lockout`, and `lockoutOnFailure: true` on `PasswordSignInAsync`. | `lockoutOnFailure: false`; lockout disabled | SEC-IA-09 | dnet#account-protection |
| ASP-03 | SHOULD | Login, registration and recovery give consistent responses and timing (no account disclosure); protect registration and recovery as well as login. | distinct messages; recovery without throttling | SEC-IA-09 | dnet#account-protection |
| ASP-04 | MUST | Store passwords with Identity's `PasswordHasher<TUser>`, not direct `KeyDerivation.Pbkdf2`; set `PasswordHasherOptions.IterationCount` to meet PWS-05. | `KeyDerivation.Pbkdf2` for storage; low `IterationCount` | SEC-IA-06 | dnet#passwords |
| ASP-05 | SHOULD | Set `RequiredLength` per ATN-02; disable `RequireDigit`/`RequireLowercase`/`RequireUppercase`/`RequireNonAlphanumeric`; add breached-password screening. | composition rules on; short `RequiredLength` | SEC-IA-10 | dnet#passwords |
| ASP-06 | MUST | Application cookie: `Cookie.HttpOnly = true`, `Cookie.SecurePolicy = CookieSecurePolicy.Always`, `Cookie.SameSite` chosen explicitly. | `SecurePolicy.SameAsRequest`/`None`; `HttpOnly = false` | SEC-IA-05 | dnet#authentication-cookies |
| ASP-07 | SHOULD | Set an appropriate `ExpireTimeSpan`; `SlidingExpiration` isn't an absolute limit. | very long `ExpireTimeSpan` with sliding expiration and no absolute cap | SEC-IA-05 | dnet#authentication-cookies |
| ASP-08 | SHOULD | Update the security stamp on security-sensitive changes (`UpdateSecurityStampAsync`); keep stamp validation enabled. | password/role change without stamp update; validator disabled | SEC-IA-05 | dnet#authentication-cookies |
| ASP-09 | SHOULD | Use a fallback policy requiring authentication and mark public endpoints `[AllowAnonymous]`; static files served before the authorization middleware aren't covered. | no `FallbackPolicy`; `UseStaticFiles` before auth for private files | SEC-IA-01 | dnet#authorization |
| ASP-10 | MUST | Privileged operations require a role or named policy (`[Authorize(Policy=…)]`, `RequireAuthorization("…")`); named policies include the authentication requirement. | admin actions with plain `[Authorize]` only | SEC-IA-02 | dnet#authorization |
| ASP-11 | MUST | Object-specific permissions use `IAuthorizationService.AuthorizeAsync(user, resource, requirement)` before returning or changing the object. | resource returned by id with only `[Authorize]` | SEC-IA-02 | dnet#authorization |
| ASP-12 | MUST | Return URLs use `LocalRedirect`/`Url.IsLocalUrl`; external destinations come from a server-side allowlist. | `Redirect(returnUrl)` unchecked | SEC-IA-04 | dnet#redirects |
| ASP-13 | MUST | Antiforgery validation for state-changing requests when credentials are sent automatically (cookies, Windows/Basic/Digest): global `AutoValidateAntiforgeryToken` in MVC, MVC `[ValidateAntiForgeryToken]` and `ViewStateUserKey` on legacy; never `IgnoreAntiforgeryToken` just to make a request pass. | missing antiforgery on cookie-auth POST; `IgnoreAntiforgeryToken` | SEC-IA-05 | dnet#cross-site-request-forgery, dnet#aspnet-mvc-and-web-forms |
| ASP-14 | MUST | Legacy Forms auth: `cookieless="UseCookies"`, `requireSSL="true"` and an appropriate `timeout`. | `cookieless="UseUri"`/`AutoDetect`; `requireSSL="false"` | SEC-IA-05 | dnet#forms-authentication |
