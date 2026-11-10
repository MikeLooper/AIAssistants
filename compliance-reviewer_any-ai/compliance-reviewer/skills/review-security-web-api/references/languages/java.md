# Detection signals — Java (Security: Web & API)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only on concrete code or an explicit setting; a missing header follows the
evidence rule in `SKILL.md` step 3. The only Spring defaults a worker may rely on are those stated in
`java-web-api.md` (JVW-01 … JVW-07, JVW-10). Spring Boot `server.server-header`/`server.ssl.*` defaults, WebFlux and
other frameworks are not localized: report explicit values only.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `headers(h -> h.disable())`; `headers(h -> h.defaultsDisabled())` without re-adding `contentTypeOptions` | `SecurityFilterChain` beans, `WebSecurityConfig` | Default headers removed | JVW-01, HDR-03 |
| `contentTypeOptions(c -> c.disable())` | `SecurityFilterChain` | nosniff removed | JVW-01, HDR-03 |
| `frameOptions(f -> f.disable())`; `frameOptions(f -> f.sameOrigin())` only on some paths with others disabled | `SecurityFilterChain` | Framing allowed | JVW-02, HDR-01, CSP-11 |
| `hsts(h -> h.disable())`; `maxAgeInSeconds(...)` below `31536000`; `includeSubDomains(false)` | `SecurityFilterChain` | HSTS off or weak | JVW-03, HDR-07, HST-01, HST-02 |
| `cacheControl(c -> c.disable())` on authenticated content | `SecurityFilterChain` | Sensitive responses cacheable | JVW-04, HDR-06 |
| `xssProtection(x -> x.headerValue(ENABLED_MODE_BLOCK))` or other enabled mode | `SecurityFilterChain` | XSS filter enabled | JVW-05, HDR-02 |
| No `contentSecurityPolicy(...)` on an HTML-serving app; policy with `'unsafe-inline'`/`'unsafe-eval'` in `script-src` | `SecurityFilterChain`, filters | CSP missing or weak | JVW-06, CSP-01, CSP-05 |
| No `referrerPolicy(...)` / `permissionsPolicy(...)` / COOP on an HTML-serving app | `SecurityFilterChain` | Browser policy headers missing | JVW-07, HDR-04, HDR-10, HDR-13 |
| `httpPublicKeyPinning(...)`; `Expect-CT` set via `StaticHeadersWriter` | `SecurityFilterChain` | Harmful headers | HDR-18, HDR-08 |
| No `redirectToHttps(...)` / `requires-channel="https"` and no proxy redirect on an HTML site | `SecurityFilterChain`, XML config, proxy config | HTTP not redirected | JVW-08, TLS-03 |
| `server.ssl.enabled-protocols` including `TLSv1`/`TLSv1.1`; `server.ssl.ciphers` with `TLS_RSA_*`/NULL/EXPORT suites | `application*.properties`, `application*.yml` | Legacy TLS or weak ciphers | TLS-01, TLS-02 |
| `server.port` HTTP-only for a public API with no TLS and no TLS-terminating proxy in the files; `http://` base URLs in production profiles | `application*.properties`/`.yml`, `Dockerfile` | Plain-HTTP API | RST-01, TLS-04 |
| `@CrossOrigin` without `origins`; `registry.addMapping("/**")` without `allowedOrigins` | controllers, `WebMvcConfigurer` | All origins allowed | JVW-10, H5-02, RST-10 |
| `allowedOrigins("*")`; `allowCredentials(true)` with `allowedOriginPatterns("*")` or broad patterns | `WebMvcConfigurer`, `CorsConfigurationSource` beans | Any-origin or credentialed broad CORS | JVW-11, H5-01, HDR-09 |
| `cors(c -> c.disable())` while MVC CORS is configured; `CorsConfiguration` built outside the security chain | `SecurityFilterChain` | CORS not integrated with Spring Security | JVW-09 |
| Filters echoing `request.getHeader("Origin")` into `Access-Control-Allow-Origin`; authorization on `Origin` | filters, interceptors | Reflected origin; CORS as access control | H5-01, H5-03 |
| `response.setHeader("X-Powered-By", ...)`; informative `Server` values set in code | filters, controllers | Version-revealing headers | HDR-15, HDR-14 |
| `@RequestMapping` with `method = { all RequestMethod values }`; `TRACE` enabled (`setDispatchTraceRequest(true)`) | controllers, servlet config | Any-method handler | RST-02, A02-03 |
| `@RequestParam("apiKey"\|"token"\|"password")`; `RestTemplate`/`WebClient` URLs with `?access_token=` | controllers, clients | Credentials in URLs | RST-11, RST-12 |
| `produces = "text/html"` on JSON endpoints | controllers | Wrong response type | RST-06 |
| No `consumes`/`produces` while XML message converters (`jackson-dataformat-xml`) are on the classpath of a JSON-only API | controllers, `pom.xml`/`build.gradle` | Unintended formats accepted | RST-04, RST-03 |
| `response.setContentType(request.getHeader("Accept"))` | controllers, filters | `Accept` drives `Content-Type` | RST-05 |
| Download endpoints returning uploads with `Content-Disposition: inline` or the stored/client-supplied type | controllers | Inline download of user files | HDR-19 |
