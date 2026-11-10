# Spring web and API security guidance — localized summary

- Sources: docs.spring.io — Spring Security Reference 7.1 (7.1.2, current GA on api.spring.io on 2026-11-09; the
  `/7.1/` paths redirect to the unversioned current pages listed below) and Spring Framework Reference 7.0 (7.0.10)
- Localized: 2026-11-09 · Elements: docs.spring.io 11 (cap 100; Spring Security and Spring Framework share the host budget)
- Applies when language `java` is detected. JVW-01 … JVW-09 apply when `spring-security-web` (or
  `spring-boot-starter-security`) is a dependency; JVW-10/JVW-11 when Spring MVC (`spring-webmvc`) is used. Spring
  WebFlux, Quarkus, Jakarta EE and other frameworks are **not** localized: judge explicit values only, and add
  `localized-standard-gap: <framework> default for <header> not localized` to `notes` for a missing header.
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element that is
  violated and name the JVW element in the recommendation. Where vendor guidance is weaker than an OWASP element, the
  OWASP element decides. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only Spring header, HTTPS and CORS defaults a worker may rely on. Spring Boot
  `server.server-header` and `server.ssl.*` defaults are not localized: judge explicit values only.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| ss-hdr | https://docs.spring.io/spring-security/reference/features/exploits/headers.html | Spring Security 7.1.2 | Spring Security Reference — Security HTTP Response Headers (7.1) |
| ss-shdr | https://docs.spring.io/spring-security/reference/servlet/exploits/headers.html | Spring Security 7.1.2 | Spring Security Reference — Servlet Security Headers (7.1) |
| ss-http | https://docs.spring.io/spring-security/reference/servlet/exploits/http.html | Spring Security 7.1.2 | Spring Security Reference — Servlet HTTP Requests (7.1) |
| ss-cors | https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html | Spring Security 7.1.2 | Spring Security Reference — CORS (7.1) |
| sf-cors | https://docs.spring.io/spring-framework/reference/web/webmvc-cors.html | Spring Framework 7.0.10 | Spring Framework Reference — Web MVC CORS (7.0) |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| JVW-01 | MUST | **(Default)** Spring Security sends `X-Content-Type-Options: nosniff` by default. `contentTypeOptions(c -> c.disable())`, `headers(h -> h.disable())`, or `defaultsDisabled()` without re-adding it, removes it. | those calls in a `SecurityFilterChain` | SEC-WA-03 | ss-hdr#headers-content-type-options, ss-shdr#servlet-headers-content-type-options, ss-shdr#servlet-headers-default |
| JVW-02 | MUST | **(Default)** Spring Security sends `X-Frame-Options: DENY` by default. | `frameOptions(f -> f.disable())`; per-path disabling | SEC-WA-04 | ss-hdr#headers-frame-options, ss-shdr#servlet-headers-frame-options |
| JVW-03 | MUST | **(Default)** Spring Security adds HSTS on HTTPS responses only, as `max-age=31536000 ; includeSubDomains` (defaults list; the HSTS section's example also shows `preload` — unresolved, see MAINTENANCE.md). | `hsts(h -> h.disable())` | SEC-WA-02 | ss-hdr#headers-hsts, ss-hdr#headers-default, ss-shdr#servlet-headers-hsts |
| JVW-04 | SHOULD | **(Default)** Spring Security sends `Cache-Control: no-cache, no-store, max-age=0, must-revalidate`, `Pragma: no-cache` and `Expires: 0` by default, and backs off when the application sets its own cache headers. | `cacheControl(c -> c.disable())` on authenticated content | SEC-WA-08 | ss-hdr#headers-cache-control, ss-shdr#servlet-headers-cache-control |
| JVW-05 | MUST | **(Default)** Spring Security sends `X-XSS-Protection: 0` by default. | `xssProtection(…)` set to enabled/block mode | SEC-WA-11 | ss-hdr#headers-xss-protection, ss-shdr#servlet-headers-xss-protection |
| JVW-06 | MUST | **(Default)** Spring Security doesn't add `Content-Security-Policy` by default; configure it with `contentSecurityPolicy(…)`. | HTML-serving app with no CSP configuration | SEC-WA-01 | ss-shdr#servlet-headers-csp, ss-hdr#headers-csp |
| JVW-07 | MUST | **(Default)** Spring Security doesn't add `Referrer-Policy`, `Permissions-Policy` (or `Feature-Policy`) or `Clear-Site-Data` by default. | — | SEC-WA-11 | ss-shdr#servlet-headers-referrer, ss-shdr#servlet-headers-permissions, ss-shdr#servlet-headers-clear-site-data |
| JVW-08 | SHOULD | Redirect HTTP to HTTPS with `redirectToHttps(withDefaults())` (or `requires-channel="https"`) unless the front end does it. | — (supports TLS-03) | SEC-WA-06 | ss-http#servlet-http-redirect |
| JVW-09 | SHOULD | Integrate CORS with Spring Security through a `UrlBasedCorsConfigurationSource` bean or `.cors(…)`, so that it runs before authentication. `.cors(c -> c.disable())` removes CORS support, not browser protection. | — | SEC-WA-05 | ss-cors#cors-configuration-source, ss-cors#cors-spring-mvc-integration, ss-cors#cors-preflight-request-handler |
| JVW-10 | MUST | **(Default)** A bare `@CrossOrigin`, or a global `addCorsMappings` registration, allows **all origins**, all headers and the mapped methods. Credentials are off and `maxAge` is 30 minutes by default. | `@CrossOrigin` without `origins`; `addMapping("/**")` without `allowedOrigins` | SEC-WA-05 | sf-cors#mvc-cors-controller, sf-cors#mvc-cors-global |
| JVW-11 | MUST | With `allowCredentials(true)`, `"*"` isn't permitted in `allowedOrigins`. `allowedOriginPatterns` matches a dynamic set of origins; keep it to a finite, trusted set, because credentials establish a high level of trust. | `allowCredentials(true)` with `allowedOriginPatterns("*")` | SEC-WA-05 | sf-cors#mvc-cors-credentialed-requests, sf-cors#mvc-cors-controller |
