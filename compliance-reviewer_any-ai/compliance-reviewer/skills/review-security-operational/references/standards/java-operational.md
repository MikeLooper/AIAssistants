# Java / Spring Boot operational security guidance — localized summary

- Sources: docs.spring.io — Spring Boot reference, 4.1 (4.1.2 current GA at localization, api.spring.io). The
  `/spring-boot/4.1/…` paths redirect to the unversioned current pages, so the version is recorded here and in
  `../sources.md`. Selected sections only.
- Localized: 2026-11-08 · Elements: 6 — docs.spring.io 6 (cap 100)
- Applies when language `java` is detected and `spring-boot-starter*` is a dependency; JVO-02 and JVO-03 only when
  `spring-boot-starter-actuator` is present. ERR-05 (in `owasp-operational.md`) applies to any servlet or Spring MVC app.
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element it supports
  and name the JVO element in the recommendation. Where vendor guidance is weaker than an OWASP element, the OWASP
  element decides: the servlet page says the default `/error` JSON includes "the exception message", while the
  properties appendix says `spring.web.error.include-message` defaults to `never`; JVO-01 records the property default
  and ERR-02 decides. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only Java defaults a worker may rely on. Logback/Log4j2 pattern and masking defaults,
  Quarkus, Micronaut, Jakarta EE servers and Spring Boot versions before 4.0 are **not** localized: report only
  explicit insecure settings there (legacy `server.error.*` values set to `always` count as explicit), and add a
  `localized-standard-gap` note for a missing setting.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| sb-web | https://docs.spring.io/spring-boot/reference/web/servlet.html | Spring Boot 4.1 | Spring Boot 4.1 reference — Servlet Web Applications |
| sb-act | https://docs.spring.io/spring-boot/reference/actuator/endpoints.html | Spring Boot 4.1 | Spring Boot 4.1 reference — Actuator Endpoints |
| sb-props | https://docs.spring.io/spring-boot/appendix/application-properties/index.html | Spring Boot 4.1 | Spring Boot 4.1 reference — Common Application Properties |
| sb-cfg | https://docs.spring.io/spring-boot/reference/features/external-config.html | Spring Boot 4.1 | Spring Boot 4.1 reference — Externalized Configuration |
| sb-log | https://docs.spring.io/spring-boot/reference/features/logging.html | Spring Boot 4.1 | Spring Boot 4.1 reference — Logging |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| JVO-01 | MUST | **(Default)** Boot's `/error` handling: `spring.web.error.include-stacktrace` and `include-message` default to `never`, `include-exception` to `false`, `include-binding-errors` to `never`. Setting them to `always` (or on a request parameter) exposes details. | `spring.web.error.include-stacktrace=always`; legacy `server.error.*` equivalents | SEC-OP-01 | sb-props#application-properties.web.spring.web.error.include-stacktrace, sb-web#web.servlet.spring-mvc.error-handling |
| JVO-02 | MUST | **(Default)** Only `health` is exposed over HTTP and JMX by default. Before widening `management.endpoints.web.exposure.include`, ensure exposed endpoints hold no sensitive data or are secured; with Spring Security and no custom `SecurityFilterChain`, endpoints other than `health` are secured automatically. | `exposure.include=*` with no security; `heapdump`, `env`, `logfile` exposed | SEC-OP-07 | sb-act#actuator.endpoints.exposing, sb-act#actuator.endpoints.security |
| JVO-03 | MUST | **(Default)** `/env`, `/configprops` and `/quartz` values are fully sanitized by default (`show-values: never`); `always` shows them to all users; `when-authorized` shows them to any authenticated user unless roles are set. | `management.endpoint.env.show-values=always` | SEC-OP-07 | sb-act#actuator.endpoints.sanitization, sb-props#application-properties.actuator.management.endpoint.env.show-values |
| JVO-04 | SHOULD | Prefer mounted configuration trees (`configtree:`) over environment variables for secrets; Boot has no built-in property encryption, so use a secret store (e.g. Spring Cloud Vault) for credentials. | home-grown property "encryption" with a key in the same config | SEC-OP-06 | sb-cfg#features.external-config.files.configtree, sb-cfg#features.external-config.encrypting |
| JVO-05 | MUST | **(Default)** Boot logs only to the console by default; file logging needs `logging.file.name`/`path`. Logback and Log4j2 rotation is tuned with `logging.logback.rollingpolicy.*` / `logging.log4j2.rollingpolicy.*` (`max-history` defaults to 7); other logging systems need their own rotation. | file logging with rotation removed or uncapped; other file appenders without rotation | SEC-OP-09 | sb-log#features.logging.file-output, sb-log#features.logging.file-rotation |
| JVO-06 | MUST | **(Default)** Structured JSON logging (ECS, GELF, Logstash) is built in via `logging.structured.format.console`/`file`; the default output is plain text. | user input in default text logs without CR/LF handling | SEC-OP-04 | sb-log#features.logging.structured |
