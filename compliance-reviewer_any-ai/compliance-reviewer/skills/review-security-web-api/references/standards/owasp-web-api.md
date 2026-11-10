# OWASP web and API security guidance — localized summary

- Sources: cheatsheetseries.owasp.org @ OWASP/CheatSheetSeries (per-sheet commits below; HTML5 Security: CORS and
  offline sections only; Transport Layer Security: protocol, cipher and application sections only);
  top10.owasp.org (A02:2025 @ OWASP/Top10 d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966, 2025-12-24)
- Localized: 2026-11-09 · Elements: cheatsheetseries.owasp.org 54 (cap 100); top10.owasp.org 5 (cap 100)
- Level: `MUST` where the source says must/must not/never/do not/ensure, gives an unqualified imperative ("Remove…",
  "Use…", "Discard…"), or names a prohibited practice. `SHOULD` for recommendations (should/recommended/prefer/
  consider). Top 10 elements use `REVIEW` for "Description" weaknesses and mapped CWEs (`REVIEW` is treated like
  `MUST`). HDR-11 is **Advisory**: cited in recommendations only, never fails on its own. Severity rules are in
  `../../SKILL.md`.
- Applicability (`../../SKILL.md` step 2): HTML-serving targets are judged on every check; API-only targets skip
  SEC-WA-01, -04 and -11 (browser-rendering headers; hdr#content-security-policy-csp, rst#security-headers) and get the
  API forms of those protections through SEC-WA-08.
- Language-agnostic files (`web.config`, `nginx*.conf`, `.htaccess`, `httpd.conf`, HAProxy, `Caddyfile`, IaC) have no
  language id. Evaluate them with the elements below whenever they are in the subject's file list. Signals:
  - nginx `add_header` / Apache `Header set` without `always` count as setting the header, but the recommendation notes
    that it is missing on error responses (hdr#nginx, hdr#apache); IIS `<customHeaders>` under `<httpProtocol>`;
  - nginx `server_tokens on`, Apache `ServerTokens Full`/`ServerSignature On` (HDR-14);
  - `ssl_protocols`/`SSLProtocol` including `TLSv1`/`TLSv1.1`/`SSLv3` (TLS-01); `ssl_ciphers`/`SSLCipherSuite` with
    `NULL`, `aNULL`, `EXPORT` or `RSA` key-transport suites (TLS-02);
  - `listen 80` without `return 301 https://…` on an HTML site (TLS-03); a port-80 server block proxying an API (TLS-04);
  - `http://` `<script src>`/`<link href>` in HTML templates (TLS-05);
  - `<meta http-equiv="Content-Security-Policy">` containing `frame-ancestors` (CSP-11).
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.
- Citation preference: vendor element (DNW/JVW/PYW) → cheat-sheet element (CSP/HDR/RST/H5/HST/TLS) → A02 element
  (cite A02 only when nothing more specific fits; otherwise name it in the recommendation). For a vendor element marked
  **(Default)**, cite the OWASP element that is violated and name the vendor element in the recommendation.

| Key | Citation base | Pinned commit | Source name for `Finding.standard` |
|-----|---------------|---------------|------------------------------------|
| csp | https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html | eaa71fb4 (2026-10-04) | OWASP Content Security Policy Cheat Sheet |
| hdr | https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html | 056cc10a (2026-10-04) | OWASP HTTP Security Response Headers Cheat Sheet |
| rst | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html | 97cb8a3c (2026-10-14) | OWASP REST Security Cheat Sheet |
| h5 | https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html | 3919b1c4 (2026-10-04) | OWASP HTML5 Security Cheat Sheet |
| hsts | https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html | fa588add (2026-10-04) | OWASP HTTP Strict Transport Security Cheat Sheet |
| tls | https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html | d6474de0 (2026-11-08) | OWASP Transport Layer Security Cheat Sheet |
| a02 | https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/ | d4d000ec (2025-12-24) | OWASP Top 10:2025 A02 |

The Headers sheet repeats "Recommendation" headings; their anchors are `recommendation`, `recommendation_1` …
`recommendation_21`, in page order.

## Content Security Policy Cheat Sheet (CSP)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| CSP-01 | MUST | Deliver an enforced policy in the `Content-Security-Policy` header on every HTML response, not just the index page. Report-Only alone doesn't enforce ("fail open"). A `<meta>` policy is a fallback only when headers can't be set; it can't carry `frame-ancestors`, `sandbox` or reporting. | no CSP in middleware/server config; Report-Only only; CSP on one route | SEC-WA-01 | csp#1-content-security-policy-header, csp#2-content-security-policy-report-only-header, csp#3-content-security-policy-meta-tag |
| CSP-02 | MUST | Don't send the obsolete `X-Content-Security-Policy` or `X-WebKit-CSP` headers. | those header names in code/config | SEC-WA-11 | csp#warning |
| CSP-03 | SHOULD | Prefer a strict CSP: nonce- or hash-based `script-src` (optionally `'strict-dynamic'`) with `object-src 'none'` and `base-uri 'none'`. | allowlist-only `script-src` listing many hosts | SEC-WA-01 | csp#strict-csp, csp#strict-policy, csp#nonce-based-strict-policy, csp#hash-based-strict-policy, csp#csp-types-granularallowlist-based-or-strict |
| CSP-04 | MUST | Nonces are unique random values generated per response and rendered by the templating engine. Never use middleware that adds nonces to every `<script>` tag, and never use a fixed nonce. | constant nonce string; HTML rewriting that inserts `nonce=` | SEC-WA-01 | csp#nonce-based, csp#warning_1 |
| CSP-05 | MUST | Script sources (`script-src`, or `default-src` as the fallback) don't allow `'unsafe-inline'` or `'unsafe-eval'`. Move inline code and inline event handlers to files and `addEventListener`. | `script-src 'unsafe-inline'`/`'unsafe-eval'` | SEC-WA-01 | csp#1-restricting-inline-scripts, csp#3-restricting-unsafe-javascript, csp#refactoring-inline-code, csp#special-directive-sources |
| CSP-06 | SHOULD | Style sources avoid `'unsafe-inline'` too. | `style-src 'unsafe-inline'` | SEC-WA-01 | csp#basic-non-strict-csp-policy, csp#special-directive-sources |
| CSP-07 | SHOULD | A non-strict policy limits `default-src` to `'self'` (or `'none'` plus explicit directives) and sets `form-action`. Don't loosen it with broad sources; overly permissive policies lead to bypasses. | `default-src *`; `script-src https:`/`*`; no `form-action` | SEC-WA-01 | csp#basic-non-strict-csp-policy, csp#detailed-csp-directives, csp#2-restricting-remote-scripts, csp#4-restricting-form-submissions |
| CSP-08 | SHOULD | Set `object-src 'none'` when plugins aren't needed. Don't rely on the removed `plugin-types` or `prefetch-src` directives. | `plugin-types`/`prefetch-src` used as controls; no `object-src` and no restrictive `default-src` | SEC-WA-01 | csp#document-directives, csp#fetch-directives, csp#5-restricting-objects |
| CSP-09 | SHOULD | Report violations with `report-to` (an endpoint from `Reporting-Endpoints`), with `report-uri` kept only as a fallback. A Report-Only policy may run alongside the enforced one to test changes. | only the deprecated `report-uri` | SEC-WA-01 | csp#reporting-directives, csp#2-content-security-policy-report-only-header |
| CSP-10 | SHOULD | Use `upgrade-insecure-requests` while migrating a site from HTTP to HTTPS. | HTTPS site with legacy `http://` asset URLs and no directive | SEC-WA-06 | csp#upgrading-insecure-requests |
| CSP-11 | MUST | Restrict framing with `frame-ancestors` in a header (`'none'`, `'self'` or named trusted origins). The directive is ignored in `<meta>` and doesn't fall back to `default-src`. | `frame-ancestors *`; `frame-ancestors` only in a meta tag | SEC-WA-04 | csp#preventing-framing-attacks-clickjacking-cross-site-leaks, csp#navigation-directives, csp#defense-against-framing-attacks |

## HTTP Security Response Headers Cheat Sheet (HDR)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| HDR-01 | MUST | Pages with interactive content can't be framed by other sites. Prefer CSP `frame-ancestors`; also send `X-Frame-Options: DENY`. Redirects and JSON responses gain nothing from `X-Frame-Options`. | no frame protection on HTML responses | SEC-WA-04 | hdr#x-frame-options, hdr#recommendation |
| HDR-02 | MUST | Don't enable the browser XSS filter: omit `X-XSS-Protection` or send `X-XSS-Protection: 0`. It can create XSS in otherwise safe sites. | `X-XSS-Protection: 1` / `1; mode=block` | SEC-WA-11 | hdr#x-xss-protection, hdr#recommendation_1 |
| HDR-03 | MUST | Send `X-Content-Type-Options: nosniff` and set `Content-Type` correctly throughout the site. | no nosniff in middleware, framework or server config | SEC-WA-03 | hdr#x-content-type-options, hdr#recommendation_2 |
| HDR-04 | SHOULD | Set `Referrer-Policy` explicitly (`strict-origin-when-cross-origin` or stricter) instead of relying on browser defaults. | no Referrer-Policy; `unsafe-url`; `no-referrer-when-downgrade` | SEC-WA-11 | hdr#referrer-policy, hdr#recommendation_3 |
| HDR-05 | SHOULD | Responses declare the correct `Content-Type`; HTML responses include `charset`. This matters most when the client renders untrusted content. | `text/html` without charset; user content served without an explicit type | SEC-WA-08 | hdr#content-type, hdr#recommendation_4 |
| HDR-06 | MUST | Sensitive responses send `Cache-Control: no-store`. `private` only keeps them out of shared caches, and `no-cache` doesn't prevent storage. Don't rely on default caching, and keep sensitive responses out of application-managed caches. | sensitive endpoints without no-store; `no-cache` used as the protection | SEC-WA-08 | hdr#cache-control, hdr#recommendation_5, tls#prevent-caching-of-sensitive-data |
| HDR-07 | MUST | Send `Strict-Transport-Security` on HTTPS responses. The recommended value is `max-age=63072000; includeSubDomains`; add `preload` only when deliberately submitting to the preload list. | no HSTS in code, framework or server config | SEC-WA-02 | hdr#strict-transport-security-hsts, hdr#recommendation_7 |
| HDR-08 | MUST | Don't send `Expect-CT`; remove it from existing code. | `Expect-CT` header set | SEC-WA-11 | hdr#expect-ct, hdr#recommendation_8 |
| HDR-09 | MUST | If `Access-Control-Allow-Origin` is used, set specific origins instead of `*`. `*` is acceptable only for public resources meant for any origin. No CORS header means the Same Origin Policy applies. | `Access-Control-Allow-Origin: *` on non-public endpoints | SEC-WA-05 | hdr#access-control-allow-origin, hdr#recommendation_10 |
| HDR-10 | SHOULD | HTML documents send `Cross-Origin-Opener-Policy: same-origin`. It isn't meaningful for non-browser API clients. | no COOP on HTML responses; `unsafe-none` | SEC-WA-11 | hdr#cross-origin-opener-policy-coop, hdr#recommendation_11 |
| HDR-11 | SHOULD | `Cross-Origin-Embedder-Policy: require-corp` where cross-origin resources are prepared for it. **Advisory only; never fails on its own**, because the source warns that it blocks resources that aren't configured for it. | — (recommendation text) | SEC-WA-11 | hdr#cross-origin-embedder-policy-coep, hdr#recommendation_12 |
| HDR-12 | SHOULD | Send `Cross-Origin-Resource-Policy: same-site` to limit which origins can include a resource. | no CORP; `cross-origin` on private resources | SEC-WA-11 | hdr#cross-origin-resource-policy-corp, hdr#recommendation_13 |
| HDR-13 | SHOULD | Send `Permissions-Policy` that disables browser features the site doesn't use, or allows them only to authorized origins. | no Permissions-Policy; `*` allowlists | SEC-WA-11 | hdr#permissions-policy-formerly-feature-policy, hdr#recommendation_14 |
| HDR-14 | MUST | Remove the `Server` header or set a non-informative value. | informative `Server` value set; nginx `server_tokens on` | SEC-WA-07 | hdr#server, hdr#recommendation_15 |
| HDR-15 | MUST | Remove all `X-Powered-By` headers. | `X-Powered-By` added in code or config | SEC-WA-07 | hdr#x-powered-by, hdr#recommendation_16 |
| HDR-16 | MUST | ASP.NET (.NET Framework): disable `X-AspNet-Version` with `<httpRuntime enableVersionHeader="false" />`. | `web.config` `<system.web>` without it | SEC-WA-07 | hdr#x-aspnet-version, hdr#recommendation_17 |
| HDR-17 | MUST | ASP.NET MVC (.NET Framework): disable `X-AspNetMvc-Version` with `MvcHandler.DisableMvcResponseHeader = true`. | `Global.asax` without it | SEC-WA-07 | hdr#x-aspnetmvc-version, hdr#recommendation_18 |
| HDR-18 | MUST | Don't send `Public-Key-Pins` or `Public-Key-Pins-Report-Only`. | HPKP headers; Spring `httpPublicKeyPinning(…)` | SEC-WA-11 | hdr#public-key-pins-hpkp, hdr#recommendation_21, tls#public-key-pinning |
| HDR-19 | SHOULD | Serve user-provided files with `Content-Disposition: attachment`, `Content-Type: application/octet-stream` for unknown or binary types, and `nosniff`. | download endpoints returning uploads inline with a stored or client-supplied type | SEC-WA-08 | hdr#secure-file-download-headers |

## REST Security Cheat Sheet (RST)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| RST-01 | MUST | REST services expose only HTTPS endpoints. | `http://` listener URLs for API hosts | SEC-WA-06 | rst#https |
| RST-02 | MUST | Allowlist the HTTP methods each endpoint accepts and reject others with `405`. | handlers explicitly accepting every method; `TRACE` enabled | SEC-WA-09 | rst#restrict-http-methods |
| RST-03 | MUST | For requests with a body, require a supported `Content-Type` and reject others with `415`. Don't require one on requests without a body. | raw body parsed as JSON/XML without checking the declared type | SEC-WA-09 | rst#validate-request-content-types |
| RST-04 | SHOULD | Declare and document the content types each endpoint consumes and produces (e.g. `@Consumes`/`@Produces`), so that unintended types such as XML (an XXE vector) aren't accepted. | XML formatters enabled on a JSON-only API; no declared types | SEC-WA-09 | rst#validate-request-content-types, rst#validate-content-types |
| RST-05 | MUST | Never copy the `Accept` header into the response `Content-Type`. Pick a supported type that matches `Accept`; return `406` only when nothing matches and no default is supplied. | `Content-Type` set from `Accept` | SEC-WA-09 | rst#send-safe-response-content-types |
| RST-06 | MUST | The response `Content-Type` matches the body (e.g. `application/json`, not `application/javascript` or `text/html` for JSON). Services that return script code take extra care against header injection. | JSON written as `text/html` or `text/plain` | SEC-WA-08 | rst#send-safe-response-content-types, rst#security-headers |
| RST-07 | SHOULD | API responses that browsers may consume send `Cache-Control: no-store`. | API pipeline with no cache directive | SEC-WA-08 | rst#security-headers |
| RST-08 | SHOULD | API responses that browsers may consume send `Content-Security-Policy: frame-ancestors 'none'`, plus `X-Frame-Options: DENY` for older browsers. | no framing protection on API responses | SEC-WA-08 | rst#security-headers |
| RST-09 | SHOULD | APIs that return, or may return, HTML also send `Content-Security-Policy: default-src 'none'`, a restrictive `Permissions-Policy` and `Referrer-Policy: no-referrer`. Fails only when the files show the API returning HTML. | HTML-producing API responses without these headers | SEC-WA-08 | rst#security-headers |
| RST-10 | SHOULD | Disable CORS headers when cross-domain calls aren't expected; otherwise be as specific as possible. | global any-origin policy | SEC-WA-05 | rst#cors |
| RST-11 | MUST | Passwords, security tokens and API keys never appear in URLs, because URLs are captured in server logs. | `?apiKey=`, `?token=`, `?password=` in routes, bindings, client calls | SEC-WA-10 | rst#sensitive-information-in-http-requests |
| RST-12 | SHOULD | Send sensitive data in the body or headers for `POST`/`PUT`, and in an HTTP header for `GET`. | sensitive filters passed as GET query parameters | SEC-WA-10 | rst#sensitive-information-in-http-requests |

## HTML5 Security Cheat Sheet — CORS and offline sections (H5)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| H5-01 | MUST | Allow only selected, trusted origins in `Access-Control-Allow-Origin`. Don't use `*`, and never return the request's `Origin` without checking it against an allowlist. | origin echoed from the request; allow-all origin predicates | SEC-WA-05 | h5#cross-origin-resource-sharing |
| H5-02 | MUST | Responses with `Access-Control-Allow-Origin: *` carry no sensitive content. Set CORS headers only on URLs that need cross-domain access, not across the whole domain. | global wildcard policy covering authenticated endpoints | SEC-WA-05 | h5#cross-origin-resource-sharing |
| H5-03 | MUST | CORS isn't access control: ordinary `GET`/`POST` requests still perform access control, and the `Origin` header alone never decides access. | authorization decided by the `Origin` value | SEC-WA-05 | h5#cross-origin-resource-sharing |
| H5-04 | MUST | Discard requests received over plain HTTP that carry HTTPS origins (mixed content). | — | SEC-WA-06 | h5#cross-origin-resource-sharing |
| H5-05 | MUST | Service workers don't put sensitive responses into the Cache API, which ignores HTTP caching headers. They explicitly exclude and delete them, are registered only from the app's own origin over HTTPS, and have a restricted scope. | `cache.put`/`addAll` of authenticated API responses; broad worker scope | SEC-WA-08 | h5#offline-applications |

## HTTP Strict Transport Security Cheat Sheet (HST)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| HST-01 | SHOULD | Use a long `max-age` once HTTPS is stable; the recommended header uses two years (`63072000`). Short values (e.g. one day) are for initial rollout only. Fails below `31536000` (one year). | `max-age` below `31536000` in production config | SEC-WA-02 | hsts#examples, hdr#recommendation_7 |
| HST-02 | SHOULD | Add `includeSubDomains` when all subdomains use HTTPS. Without it, cookie attacks through subdomains stay possible. | HSTS without `includeSubDomains` | SEC-WA-02 | hsts#problems, hsts#examples |

## Transport Layer Security Cheat Sheet — protocols, ciphers, application (TLS)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| TLS-01 | MUST | Default to TLS 1.3 and allow TLS 1.2 only for compatibility. TLS 1.0/1.1 and SSLv2/v3 are disabled. | `SslProtocols.Tls`/`Tls11`; `server.ssl.enabled-protocols` with `TLSv1`/`TLSv1.1`; Python `ssl` minimum below TLS 1.2 | SEC-WA-06 | tls#only-support-strong-protocols |
| TLS-02 | MUST | Disable null, anonymous, EXPORT, RSA key-transport and static-DH cipher suites. Prefer AEAD suites (with ECDHE for TLS 1.2). | explicit cipher lists containing `NULL`, `anon`, `EXPORT`, `TLS_RSA_*` | SEC-WA-06 | tls#only-support-strong-ciphers |
| TLS-03 | SHOULD | Use TLS for all pages, not just sensitive ones. A public HTTP listener only redirects to HTTPS, backed by HSTS. | HTTP routes served without a redirect | SEC-WA-06 | tls#use-tls-for-all-pages |
| TLS-04 | SHOULD | API-only endpoints don't serve HTTP at all; where that isn't possible, they fail HTTP requests instead of redirecting. | an HTTPS redirect as an API's only HTTP protection | SEC-WA-06 | tls#use-tls-for-all-pages |
| TLS-05 | SHOULD | HTTPS pages don't load scripts, styles or other resources over plain HTTP. | `http://` `<script src>`/`<link href>` in templates | SEC-WA-06 | tls#do-not-mix-tls-and-non-tls-content |

## OWASP Top 10:2025 A02 Security Misconfiguration (A02)

Traceability elements: cite only when no more specific element fits; otherwise name the A02 ID in the recommendation.

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| A02-01 | REVIEW | The server doesn't send security headers or directives, or doesn't set them to secure values. | — | SEC-WA-11 | a02#description, a02#how-to-prevent |
| A02-02 | REVIEW | Security settings in application frameworks (e.g. Spring, ASP.NET) aren't set to secure values, or newer security features are disabled or not configured securely. | — | SEC-WA-11 | a02#description |
| A02-03 | REVIEW | Unnecessary features are enabled (ports, services, pages). | — | SEC-WA-09 | a02#description, a02#how-to-prevent |
| A02-04 | REVIEW | Permissive cross-domain policy with untrusted domains (CWE-942). | — | SEC-WA-05 | a02#list-of-mapped-cwes |
| A02-05 | REVIEW | Data transmitted without encryption (CWE-5). | — | SEC-WA-06 | a02#list-of-mapped-cwes |
