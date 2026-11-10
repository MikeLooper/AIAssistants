# Checklist — Security: Web & API

Subject: Security

Each check is evaluated through the elements it lists; every element belongs to exactly one check. Element
definitions, anchors and citation bases are in `standards/`. Severity rules (SHOULD elements one level lower; HDR-11
advisory) are in `../SKILL.md`. **Applies to:** `HTML` = HTML-serving targets only; `API` = targets with API endpoints
or file downloads; `all` = every target with HTTP endpoints (`../SKILL.md` step 2).

| id | Sub-subject | Check | Default severity | Applies to | Elements | Source |
|----|-------------|-------|------------------|------------|----------|--------|
| SEC-WA-01 | Web & API | HTML responses carry an enforced Content-Security-Policy header, preferably strict (nonces/hashes), with no `unsafe-inline`/`unsafe-eval` for scripts | Warning | HTML | CSP-01, CSP-03 … CSP-09, JVW-06, PYW-06, MDN-01, NDW-04 | CSP, JVW, PYW, MDN, NDW |
| SEC-WA-02 | Web & API | `Strict-Transport-Security` is sent on HTTPS responses with a long `max-age` and `includeSubDomains` | Warning | HTML, API serving HTTP | HDR-07, HST-01, HST-02, DNW-03, DNW-04, JVW-03, PYW-02 | HDR, HST, DNW, JVW, PYW |
| SEC-WA-03 | Web & API | `X-Content-Type-Options: nosniff` is sent on all responses | Warning | all | HDR-03, JVW-01, PYW-01 | HDR, JVW, PYW |
| SEC-WA-04 | Web & API | Pages can't be framed by untrusted sites (`frame-ancestors`, with `X-Frame-Options` for older browsers) | Warning | HTML | HDR-01, CSP-11, JVW-02, PYW-05 | HDR, CSP, JVW, PYW |
| SEC-WA-05 | Web & API | CORS is off unless needed, scoped to specific trusted origins on the endpoints that need it, never any-origin or reflected origin with credentials, and never used as access control | Error | all | HDR-09, RST-10, H5-01, H5-02, H5-03, DNW-05, DNW-06, DNW-07, JVW-09, JVW-10, JVW-11, PYW-09, A02-04 | HDR, RST, H5, DNW, JVW, PYW, A02 |
| SEC-WA-06 | Web & API | All endpoints use HTTPS with TLS 1.2+ and strong ciphers; HTML sites redirect HTTP to HTTPS, APIs refuse HTTP; no mixed content | Error | all | RST-01, TLS-01 … TLS-05, CSP-10, H5-04, DNW-01, DNW-02, JVW-08, PYW-03, PYW-04, A02-05, NDW-03 | RST, TLS, CSP, H5, DNW, JVW, PYW, A02, NDW |
| SEC-WA-07 | Web & API | Response headers don't reveal server or framework versions (`Server`, `X-Powered-By`, `X-AspNet-Version`, `X-AspNetMvc-Version`) | Warning | all | HDR-14 … HDR-17, NDW-02 | HDR, NDW |
| SEC-WA-08 | Web & API | API responses and file downloads carry safe headers: correct `Content-Type`, `no-store` on sensitive responses, `frame-ancestors 'none'`, attachment download headers, and no sensitive data in Cache API storage | Warning | API | HDR-05, HDR-06, HDR-19, RST-06 … RST-09, H5-05, DNW-09, JVW-04, NDW-05 | HDR, RST, H5, DNW, JVW, NDW |
| SEC-WA-09 | Web & API | Endpoints accept only allowlisted HTTP methods and declared content types (405/415), never copy `Accept` into `Content-Type`, and expose no unnecessary methods or formats | Warning | API | RST-02 … RST-05, DNW-08, DNW-10, A02-03 | RST, DNW, A02 |
| SEC-WA-10 | Web & API | Passwords, tokens and API keys aren't sent in URLs; sensitive request data travels in headers or bodies | Warning | API | RST-11, RST-12 | RST |
| SEC-WA-11 | Web & API | HTML responses set browser policy headers (Referrer-Policy, Permissions-Policy, COOP, CORP) and send no obsolete or harmful headers (`X-XSS-Protection: 1`, `Expect-CT`, HPKP, `X-Content-Security-Policy`) | Warning | HTML | CSP-02, HDR-02, HDR-04, HDR-08, HDR-10 … HDR-13, HDR-18, JVW-05, JVW-07, PYW-07, PYW-08, A02-01, A02-02, NDW-01 | CSP, HDR, JVW, PYW, A02, NDW |

Totals: 54 OWASP cheat-sheet + 5 Top 10 + 10 DNW + 11 JVW + 9 PYW = 89 elements across 11 checks.

Applicability: an HTML-serving target is judged on all 11 checks (SEC-WA-08 … -10 only if it also has API endpoints or
file downloads). For an API-only target, mark SEC-WA-01, -04 and -11 N/A with the reason "API-only: browser-rendering
headers not applicable (hdr#content-security-policy-csp, rst#security-headers)". A target with no HTTP endpoints in
its files makes the subject N/A.

## Evidence notes

- **Header set or missing.** A response header counts as set when application code or configuration sets it, a
  localized (Default) element says the framework sends it and the files don't disable it, or a web-server, proxy or
  IaC file in the subject's list sets it (nginx `add_header` / Apache `Header set` without `always` count, but the
  recommendation notes the header is missing on error responses). If none holds: for ASP.NET Core, Spring Security
  and Django fail the element at confidence `medium`, with the recommendation "if a reverse proxy or CDN outside the
  repository adds this header, record that in the repository"; for any other framework judge explicit insecure values
  only, and add `localized-standard-gap: <framework> default for <header> not localized` to `notes`.
- **SEC-WA-01:** fail when an HTML-serving target has no enforced CSP (CSP-01), or when the policy allows
  `'unsafe-inline'`/`'unsafe-eval'` for scripts (CSP-05). CSP is defense in depth: never report a missing CSP as an
  XSS vulnerability (`review-security-input-injection` owns XSS).
- **SEC-WA-02:** `max-age` below `31536000` fails HST-01 (SHOULD); the recommendation names `63072000`. A missing
  `includeSubDomains` fails HST-02 (SHOULD). `preload` without evidence of an intended preload submission goes in the
  recommendation only. An API-only target that serves HTTPS only passes without the header (DNW-04); it fails only if
  the API also serves HTTP.
- **SEC-WA-05:** fail on wildcard or reflected origins on non-public endpoints, any-origin with credentials,
  `Origin`-based authorization, and bare `@CrossOrigin`/global mappings without `allowedOrigins`. Origins read from
  configuration pass unless the configured value is `*` or empty-means-all. No CORS configuration at all is a pass
  (HDR-09: the Same Origin Policy applies).
- **SEC-WA-06:** fail on HTTP listeners in production configuration (launch profiles under Development don't count),
  API endpoints whose only HTTP protection is a redirect (TLS-04, DNW-01), explicit TLS 1.0/1.1/SSL or weak cipher
  settings, and `http://` subresources in HTML templates. Server-side TLS settings outside the repository aren't
  judged. ASP.NET Core's default 307 redirect is not a failure.
- **SEC-WA-07:** fail on code or config that **adds** or explicitly keeps version-revealing headers (`X-Powered-By`,
  `X-AspNet-Version`, `X-AspNetMvc-Version`, informative `Server`), and on .NET Framework `web.config`/`Global.asax`
  missing the HDR-16/HDR-17 settings. The Kestrel `Server` default is not localized: ASP.NET Core fails only on
  explicit evidence. Error-body content is not judged here (`review-security-operational` SEC-OP-01).
- **SEC-WA-08:** judge only API responses and file downloads. `Cache-Control` for responses carrying session IDs or
  authentication data belongs to `review-security-identity-access`; here it covers all other sensitive API responses
  (HDR-06) and the general API recommendation (RST-07).
- **SEC-WA-09:** fail on explicit any-method handlers or TRACE enabled (RST-02), bodies parsed without a content-type
  check (RST-03), `Accept` copied into `Content-Type` (RST-05), and XML formatters enabled on JSON-only APIs (RST-04).
  Framework method-mapping defaults aren't localized, so only explicit code counts.
- **SEC-WA-10:** fail when routes, model binding or client calls in the files put passwords, tokens or API keys in a
  URL path or query string (`?api_key=`, `[FromQuery] string apiKey`, `request.GET["token"]`,
  `@RequestParam("password")`). Session IDs in URLs and OAuth implicit-grant tokens belong to identity-access.
- **SEC-WA-11:** HTML-serving targets only. Harmful values (`X-XSS-Protection: 1…`, `Expect-CT`, HPKP, obsolete CSP
  header names, `Referrer-Policy: unsafe-url`) fail at MUST level. A missing Referrer-Policy, Permissions-Policy, COOP
  or CORP is a SHOULD failure (Information). HDR-11 (COEP) is advisory only.
