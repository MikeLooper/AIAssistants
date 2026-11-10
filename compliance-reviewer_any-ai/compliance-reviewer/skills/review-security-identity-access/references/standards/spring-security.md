# Spring Security identity guidance — localized summary

- Source: docs.spring.io — Spring Security Reference **7.1** (pages report `data-version` 7.1.2, the current GA at
  snapshot; 7.2.0-RC1 was a pre-release, 7.2 GA due 2026-11-30)
- Localized: 2026-11-08 · Elements: docs.spring.io 13 (cap 100)
- Applies when `spring-security-*`, `spring-boot-starter-security` or `spring-boot-starter-oauth2-*` is a dependency.
  Spring Boot `server.servlet.session.cookie.*` defaults are **not** localized (gap note per `SKILL.md`).
- Framework elements apply only when that framework is in use; otherwise they don't apply.
- Level: a framework element takes the level of the OWASP element it implements (e.g. a cookie-flag setting implements
  SES-04/SES-05), or `SHOULD` when the vendor only recommends. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only framework defaults a worker may rely on. Never use remembered defaults.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Source name for `Finding.standard` |
|-----|---------------|------------------------------------|
| ahr | https://docs.spring.io/spring-security/reference/7.1/servlet/authorization/authorize-http-requests.html | Spring Security Reference 7.1 |
| ms | https://docs.spring.io/spring-security/reference/7.1/servlet/authorization/method-security.html | Spring Security Reference 7.1 |
| sm | https://docs.spring.io/spring-security/reference/7.1/servlet/authentication/session-management.html | Spring Security Reference 7.1 |
| lo | https://docs.spring.io/spring-security/reference/7.1/servlet/authentication/logout.html | Spring Security Reference 7.1 |
| csrf | https://docs.spring.io/spring-security/reference/7.1/servlet/exploits/csrf.html | Spring Security Reference 7.1 |
| pw | https://docs.spring.io/spring-security/reference/7.1/features/authentication/password-storage.html | Spring Security Reference 7.1 |
| rsj | https://docs.spring.io/spring-security/reference/7.1/servlet/oauth2/resource-server/jwt.html | Spring Security Reference 7.1 |
| ocg | https://docs.spring.io/spring-security/reference/7.1/servlet/oauth2/client/authorization-grants.html | Spring Security Reference 7.1 |
| olc | https://docs.spring.io/spring-security/reference/7.1/servlet/oauth2/login/core.html | Spring Security Reference 7.1 |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| SPS-01 | MUST | `authorizeHttpRequests` ends with a catch-all (`anyRequest().denyAll()` or `.authenticated()`) so rules form an allow list ("denying by default is a healthy security practice"). | no `anyRequest()` rule; `anyRequest().permitAll()` | SEC-IA-01 | ahr#authorize-requests, ahr#match-by-httpmethod |
| SPS-02 | SHOULD | Use `permitAll()` for public/static resources instead of `web.ignoring()` (which drops them from the filter chain). | `WebSecurityCustomizer` ignoring paths | SEC-IA-01 | ahr#favor-permitall |
| SPS-03 | MUST | Method security annotations are enforced only once enabled: `@PreAuthorize`/`@PostAuthorize` need `@EnableMethodSecurity`; `@Secured` also needs `securedEnabled = true`, `@RolesAllowed` needs `jsr250Enabled = true`. | annotations without `@EnableMethodSecurity` or the matching attribute | SEC-IA-02 | ms#method-security-architecture, ms#use-secured, ms#use-jsr250 |
| SPS-04 | SHOULD | Fine-grained/object decisions use method security with parameters or return values (`@PreAuthorize("… #id …")`, `@PostAuthorize`, `@AuthorizeReturnObject`). | only coarse URL rules for per-object access | SEC-IA-02 | ms#request-vs-method, ms#use-postauthorize, ms#authorize-object |
| SPS-05 | SHOULD | Prefer granting authorities over complex SpEL expressions for authorization logic. | long inline SpEL with string concatenation | SEC-IA-02 | ms#favor-granting-authorities |
| SPS-06 | MUST | Keep session fixation protection (default `changeSessionId`; `newSession`/`migrateSession` allowed); never `sessionFixation().none()`. | `sessionFixation(f -> f.none())` | SEC-IA-05 | sm#ns-session-fixation, sm#_configuring_session_fixation_protection |
| SPS-07 | SHOULD | Logout via POST with CSRF token; default handlers invalidate the HTTP session and clear the security context; `Clear-Site-Data` can clear client storage. | custom GET logout that skips invalidation; `invalidateHttpSession(false)` | SEC-IA-05 | lo#logout-java-configuration, lo#clear-all-site-data |
| SPS-08 | MUST | CSRF protection is on by default; disable it only for backends that serve no browser traffic, and prefer ignoring specific endpoints over global disable. | `csrf(c -> c.disable())` with form/session login | SEC-IA-05 | csrf#disable-csrf, csrf#csrf-integration-mobile |
| SPS-09 | MUST | Encode passwords with `DelegatingPasswordEncoder` (`PasswordEncoderFactories`) or an adaptive encoder (bcrypt, Argon2, scrypt, PBKDF2); never `NoOpPasswordEncoder` or `User.withDefaultPasswordEncoder()` in production. | `NoOpPasswordEncoder`, `{noop}`, `withDefaultPasswordEncoder`, `StandardPasswordEncoder`/MD5/SHA encoders | SEC-IA-06 | pw#authentication-password-storage-dpe, pw#authentication-password-storage-dep-getting-started |
| SPS-10 | SHOULD | Check passwords against known compromises (`CompromisedPasswordChecker`, e.g. HaveIBeenPwned) on registration and change. | registration/change without compromised check | SEC-IA-10 | pw#authentication-compromised-password-check |
| SPS-11 | MUST | Resource server: `issuer-uri`/`jwk-set-uri` configured (validates signature, `iss`, `exp`, `nbf` by default); `audiences` configured, because `aud` isn't validated otherwise. | no `audiences` property or `AudienceValidator` | SEC-IA-03 | rsj#_runtime_expectations, rsj#_supplying_audiences, rsj#oauth2resourceserver-jwt-validation |
| SPS-12 | SHOULD | Restrict trusted algorithms explicitly (default RS256 only; `jwsAlgorithm(…)`); a single symmetric key only when issuer and audience are the same party. | broad algorithm lists; shared `SecretKey` across services | SEC-IA-03 | rsj#oauth2resourceserver-jwt-decoder-algorithm, rsj#oauth2resourceserver-jwt-decoder-secret-key |
| SPS-13 | SHOULD | OAuth2 client/login uses authorization code; PKCE for public clients and, by default, confidential clients (`requireProofKey`); registered redirect URI template. | `requireProofKey(false)` without provider reason; non-code grants for users | SEC-IA-04 | ocg#oauth2-client-authorization-code, olc#oauth2login-sample-redirect-uri |
