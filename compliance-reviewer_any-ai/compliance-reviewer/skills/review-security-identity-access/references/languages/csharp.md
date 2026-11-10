# Detection signals — C#/.NET (Security: Identity & Access)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). ASP elements apply only when ASP.NET Core or legacy ASP.NET is in use. Microsoft defaults are not
localized: report only **explicit** values for `TokenValidationParameters` and cookie options; a missing setting gets
a `localized-standard-gap` note, not a finding.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `AddAuthorization` without `FallbackPolicy`; private endpoints relying on opt-in `[Authorize]`; `UseStaticFiles` before `UseAuthorization` for private files | `Program.cs`, `Startup.cs` | No deny-by-default | ASP-09, ATZ-02 |
| Admin/privileged actions with plain `[Authorize]` (no `Roles`/`Policy`); `RequireAuthorization()` with no policy on admin routes | controllers, minimal-API route maps | Missing function-level authorization | ASP-10, ATZ-03 |
| Handler loads an entity by route/query id and returns or changes it without `IAuthorizationService.AuthorizeAsync` or an owner/tenant filter | controllers, services, repositories | IDOR | ASP-11, ATZ-04 |
| `AddJwtBearer` with `ValidateIssuer`, `ValidateAudience`, `ValidateLifetime` or `ValidateIssuerSigningKey = false`; `RequireSignedTokens = false`; `SignatureValidator` returning the token unchecked | `Program.cs`, auth setup | JWT validation disabled | JWT-01, JWT-04, JWT-05, JWT-06 |
| `ValidAlgorithms` absent while both a symmetric key and asymmetric keys are configured; `IssuerSigningKeyResolver` fetching `jku`/`x5u` | auth setup | Algorithm/key confusion | JWT-02, JWT-03 |
| Short or literal `SymmetricSecurityKey(Encoding.UTF8.GetBytes("…"))` | auth setup, token service | Weak HMAC secret | JWT-08 |
| `RequireHttpsMetadata = false`; `http://` `Authority`, `MetadataAddress` or `CallbackPath` host | auth setup, `appsettings*.json` | Credentials/tokens over plain HTTP | OAU-11, ATN-09 |
| `ConfigureApplicationCookie`/`CookieAuthenticationOptions`: `Cookie.SecurePolicy = SameAsRequest`/`None`, `Cookie.HttpOnly = false`, `SameSite = None` | auth setup | Insecure auth cookie | ASP-06 |
| Very long `ExpireTimeSpan` with `SlidingExpiration = true` and no absolute cap | auth setup | No absolute timeout | ASP-07, SES-14 |
| Password or role change without `UpdateSecurityStampAsync`; `SecurityStampValidatorOptions` validation disabled | account/admin services | Sessions survive privilege change | ASP-08 |
| `PasswordSignInAsync(..., lockoutOnFailure: false)`; `Lockout.AllowedForNewUsers = false` | login handler, `IdentityOptions` | No lockout | ASP-02 |
| Distinct "user not found" / "wrong password" / "email already registered" messages | login, register, forgot-password handlers | Account enumeration | ASP-03, ATN-10 |
| `IdentityOptions.Password.RequireDigit/RequireUppercase/RequireLowercase/RequireNonAlphanumeric = true`; low `RequiredLength` | `IdentityOptions` | Composition rules / short minimum | ASP-05, ATN-02, ATN-04 |
| `KeyDerivation.Pbkdf2` for password storage; low `PasswordHasherOptions.IterationCount`; `MD5`, `SHA1`, `SHA256.HashData` on password fields | user services, custom hashers | Weak password storage | ASP-04, PWS-01, PWS-05 |
| Custom password/session/user tables and middleware alongside no Identity or IdP | data layer, middleware | Home-grown auth | ASP-01, SES-01 |
| `[IgnoreAntiforgeryToken]`; no `AutoValidateAntiforgeryToken`/`[ValidateAntiForgeryToken]` on cookie-authenticated POST/PUT/DELETE | MVC filters, controllers, Razor Pages | Missing CSRF defense | ASP-13, SES-07 |
| `Redirect(returnUrl)` without `Url.IsLocalUrl`/`LocalRedirect` | account controllers | Open redirect | ASP-12, OAU-01 |
| `web.config` `<forms cookieless="UseUri"/"AutoDetect" requireSSL="false">`; `<sessionState cookieless="true">` | `web.config` | Legacy Forms auth weaknesses | ASP-14, SES-03 |
