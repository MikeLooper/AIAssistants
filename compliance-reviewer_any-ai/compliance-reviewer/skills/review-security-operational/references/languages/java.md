# Detection signals — Java (Security: Operational)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only on concrete code or an explicit setting (`SKILL.md` step 4). The only Java
defaults a worker may rely on are those stated in `java-operational.md` (JVO-01, JVO-02, JVO-03, JVO-05, JVO-06), for
Spring Boot 4.x. Logback/Log4j2 pattern and masking defaults, Quarkus, Micronaut and Jakarta EE server defaults are
not localized: report explicit values only, and add a `localized-standard-gap` note for a missing setting.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `spring.web.error.include-stacktrace\|include-message` = `always` (or legacy `server.error.*`); `include-exception=true` | `application*.properties\|yml` | Error details exposed (`always` is always Error) | JVO-01, ERR-02 |
| `e.printStackTrace(response.getWriter())`; `ProblemDetail.forStatusAndDetail(…, e.getMessage())`; `e.getMessage()` in response bodies | controllers, advice, filters | Error details sent to clients | ERR-02 |
| No `<error-page>` for `java.lang.Throwable`/`Exception` in `web.xml` and no `@RestControllerAdvice`/`@ExceptionHandler(Exception.class)` | `web.xml`, advice classes | No catch-all handler | ERR-05, ERR-01 |
| `management.endpoints.web.exposure.include=*` or including `env`, `configprops`, `heapdump`, `logfile`, `threaddump` without a `SecurityFilterChain` covering `EndpointRequest` | `application*.properties\|yml`, security config | Sensitive diagnostic endpoints exposed | JVO-02 |
| `management.endpoint.env\|configprops.show-values=always` | `application*.properties\|yml` | Unsanitized config values (always Error when exposed over HTTP) | JVO-03 |
| `spring.profiles.active=dev\|local` as the packaged default; dev settings in the base `application.yml` | `application*.properties\|yml`, Dockerfile | Environments not separated | SCR-02, SCR-01 |
| `catch (Exception e) {}`, `catch (…) { return null; }` without logging | any code | Swallowed errors | A10-07, LOG-02 |
| `@ExceptionHandler` methods that build a response but never log | advice classes | Handler doesn't log | ERR-03 |
| `log.info("…" + x)`; `String.format(…)` passed to SLF4J/Log4j calls | any code | Non-constant templates | LOG-17 |
| Logback `PatternLayout`/Log4j2 text appenders receiving request data with no `%replace`/`%enc` or JSON encoder | `logback*.xml`, `log4j2*.xml` | Log injection possible | LOG-16, JVO-06 |
| Passwords, tokens, `Authorization` headers, full entities logged; `toString()` of credential-holding objects in logs | any code | Secrets or sensitive data in logs | LOG-12, LOG-13 |
| `spring.datasource.password`, `*.secret`, `*.api-key`, `*.token` with literal values | `application*.properties\|yml` | Hardcoded secrets | SMG-01 |
| Hand-rolled property decryption with the key in the same file or jar | config, `EnvironmentPostProcessor` classes | Key stored beside the secret | SMG-03, JVO-04 |
| `spring.cloud.vault.uri=http://…`; `spring.cloud.vault.ssl` verification disabled | `application*.properties\|yml`, `bootstrap*.yml` | Secrets in plaintext transit | SMG-11 |
| `logging.file.name` with `logging.logback.rollingpolicy.max-history`/`total-size-cap` or Log4j2 equivalents set unbounded; custom file appenders without policies | `application*.properties\|yml`, `logback*.xml`, `log4j2*.xml` | Unbounded log files | JVO-05, LOG-21 |
| `logging.level.root=OFF` or app packages `OFF` in production profiles | `application-prod*.properties\|yml` | Logging deactivated | LOG-19 |
| Security events written with `System.out`/`System.err` | admin, export, startup code | Not using the logging framework | LOG-11 |
| Catch blocks in `AuthorizationManager`/`AccessDecisionVoter`/filters that grant on exception | security config, filters | Fail open | A10-05 |
| Multi-step repository writes without `@Transactional` | services | No rollback for part-way writes | A10-03, SCR-03 |
| Streams, connections or locks without try-with-resources/`finally` | any code | Resources not released on exceptions | A10-06 |
