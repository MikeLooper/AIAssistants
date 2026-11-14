# java — Compliance Review

_Generated 2026-11-12T21:33:58-07:00 · Run `2026-11-13_0422-java-ui`_

## 1. Summary

**Overall score: 36.65/100 — Poor**

| Subject | Score | Band |
|---------|-------|------|
| Software Quality | 63.16/100 | Fair |
| Software Lifecycle | 27.27/100 | Poor |
| Twelve-Factor | 56.25/100 | Poor |
| Security | 28.95/100 | Poor |
| Testing | 0.00/100 | Poor |
| Observability | 0.00/100 | Poor |
| Dependency Management | 91.67/100 | Excellent |
| Performance | 0.00/100 | Poor |
| Maintainability | 33.33/100 | Poor |

**Findings by severity:** Error: 11 · Warning: 9 · Information: 7

### Top 5 Risks

1. **[Error] Admin credential committed as a literal config value** — Twelve-Factor / III. Config (src/main/resources/application.properties). Move admin.password out of the committed properties file; supply it only via an environment variable, mounted secret or secret manager at deploy time (TFR-07). [The Twelve-Factor App (12factor.net) — TFA-13](https://12factor.net/config)
1. **[Error] Todo title is rendered unescaped via Thymeleaf th:utext** — Security / Input & Injection (src/main/resources/templates/index.html (+1 more)). Render item.title with the auto-escaping th:text attribute instead of th:utext; the title field comes directly from an unvalidated request parameter (TodoController.add), so rendering it unescaped allows stored XSS. [OWASP Cross Site Scripting Prevention Cheat Sheet — XSS-02](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#framework-security)
1. **[Error] Production error responses always include stack trace and exception message** — Security / Operational (src/main/resources/application.properties). Remove these overrides (or gate them to a development profile) so Boot's never default applies in production, keeping stack traces and messages out of client error responses (OWASP ERR-02). [Spring Boot 4.1 reference — Common Application Properties — JVO-01](https://docs.spring.io/spring-boot/appendix/application-properties/index.html#application-properties.web.spring.web.error.include-stacktrace)
1. **[Error] No CI pipeline builds changes before merge** — Software Lifecycle / Continuous Integration (pom.xml). Add a CI workflow (e.g. a GitHub Actions file under .github/workflows/) that builds and tests the project on every pull request, using a build definition kept in the repository; no such pipeline-as-code exists anywhere in the project. [NIST SSDF 1.1 — SSDF-01](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf#page=16)
1. **[Error] No deny-by-default authorization mechanism protects any endpoint** — Security / Identity & Access (src/main/java/com/example/todoui/TodoUiApplication.java (+1 more)). Add Spring Security (or an equivalent filter/interceptor) with a deny-by-default rule, so every endpoint — including /admin/clear — is protected by a global policy instead of relying on an ad hoc request parameter. [OWASP Authorization Cheat Sheet — ATZ-02](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#deny-by-default)

## 2. Things Done Well

### Software Quality

- [Coding Standards] TodoItem fields and accessors use clear, intention-revealing names — src/main/java/com/example/todoui/TodoItem.java
- TodoUiApplication is a minimal, idiomatic Spring Boot entry point with no mixed concerns — src/main/java/com/example/todoui/TodoUiApplication.java

### Twelve-Factor

- [II. Dependencies] Dependencies declared through a Maven manifest with a managed parent version — pom.xml
- [VII. Port binding] Self-contained service binds its own port from configuration — src/main/resources/application.properties

### Security

- [Input & Injection] Todo priority is rendered through Thymeleaf's auto-escaping th:text — src/main/resources/templates/index.html
- [Operational] Security-relevant admin action is logged through SLF4J, not console output — src/main/java/com/example/todoui/TodoController.java

### Observability

- [Telemetry Identity & Naming] Service name is set explicitly via spring.application.name — src/main/resources/application.properties

### Dependency Management

- Spring Boot parent and Java version are pinned to exact versions with no floating ranges — pom.xml

### Maintainability

- [Prerequisites & Configuration] Required Java runtime version is pinned in the project file — pom.xml

## 3. Recommended Improvements

### Errors

- **No CI pipeline builds changes before merge** — Software Lifecycle / Continuous Integration (pom.xml, lines 1-5). Add a CI workflow (e.g. a GitHub Actions file under .github/workflows/) that builds and tests the project on every pull request, using a build definition kept in the repository; no such pipeline-as-code exists anywhere in the project. [NIST SSDF 1.1 — SSDF-01](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf#page=16)
- **Admin credential committed as a literal config value** — Twelve-Factor / III. Config (src/main/resources/application.properties, lines 6-6). Move admin.password out of the committed properties file; supply it only via an environment variable, mounted secret or secret manager at deploy time (TFR-07). [The Twelve-Factor App (12factor.net) — TFA-13](https://12factor.net/config)
- **No deny-by-default authorization mechanism protects any endpoint** — Security / Identity & Access (src/main/java/com/example/todoui/TodoUiApplication.java (+1 more), lines 6-11). Add Spring Security (or an equivalent filter/interceptor) with a deny-by-default rule, so every endpoint — including /admin/clear — is protected by a global policy instead of relying on an ad hoc request parameter. [OWASP Authorization Cheat Sheet — ATZ-02](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#deny-by-default)
- **Authorization check is implemented ad hoc in one handler, not through a shared mechanism** — Security / Identity & Access (src/main/java/com/example/todoui/TodoController.java, lines 64-70). Replace the inline password check with a shared, reusable authorization mechanism enforced the same way for every sensitive endpoint (T10-02). [OWASP Authorization Cheat Sheet — ATZ-03](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#validate-the-permissions-on-every-request)
- **Home-grown authentication check using a non-constant-time comparison** — Security / Identity & Access (src/main/java/com/example/todoui/TodoController.java, lines 66-66). Use a vetted authentication mechanism (Spring Security) instead of a hand-rolled String.equals comparison (T10-13). [OWASP Authentication Cheat Sheet — ATN-07](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#compare-password-hashes-using-safe-functions)
- **Title and priority request parameters lack server-side validation rules** — Security / Input & Injection (src/main/java/com/example/todoui/TodoController.java, lines 34-36). Bind the request to a DTO with Bean Validation constraints (@NotBlank/@Size on title, @Min/@Max on priority) and @Valid, rejecting the request when validation fails. [OWASP Input Validation Cheat Sheet — IV-02](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html#input-validation-strategies)
- **Unvalidated returnUrl parameter is used to build a redirect (open redirect)** — Security / Input & Injection (src/main/java/com/example/todoui/TodoController.java (+1 more), lines 28-30). Validate returnUrl against a fixed allowlist of known internal relative paths before using it in a redirect; ignore or reject any value that doesn't match. [OWASP Input Validation Cheat Sheet — IV-03](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html#allowlist-vs-denylist)
- **Invalid priority input is silently ignored instead of rejecting the request** — Security / Input & Injection (src/main/java/com/example/todoui/TodoController.java, lines 40-43). Reject the request (e.g. HTTP 400) when priority fails to parse, instead of silently continuing with a default value. [OWASP Input Validation Cheat Sheet — IV-07](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html#validate-structured-data)
- **Todo title is rendered unescaped via Thymeleaf th:utext** — Security / Input & Injection (src/main/resources/templates/index.html (+1 more), lines 19-19). Render item.title with the auto-escaping th:text attribute instead of th:utext; the title field comes directly from an unvalidated request parameter (TodoController.add), so rendering it unescaped allows stored XSS. [OWASP Cross Site Scripting Prevention Cheat Sheet — XSS-02](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#framework-security)
- **Production error responses always include stack trace and exception message** — Security / Operational (src/main/resources/application.properties, lines 3-4). Remove these overrides (or gate them to a development profile) so Boot's never default applies in production, keeping stack traces and messages out of client error responses (OWASP ERR-02). [Spring Boot 4.1 reference — Common Application Properties — JVO-01](https://docs.spring.io/spring-boot/appendix/application-properties/index.html#application-properties.web.spring.web.error.include-stacktrace)
- **No automated tests exist for CI to run or gate on** — Testing / CI Execution (src/main/java/com/example/todoui, lines 1-1). Add a test suite and a CI step (e.g. mvn verify) that runs it on every push and pull request, and that fails the build on a failing test. [Compliance Reviewer Testing Rubric — TSR-13](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-13)

### Warnings

- **No static analysis or compiler security gating configured** — Software Lifecycle / Static Analysis (pom.xml, lines 34-41). Add a SAST tool (e.g. CodeQL, Semgrep, or SpotBugs/FindSecBugs with failOnError) that runs in CI on every change, with warnings-as-errors enabled in the Maven build; no analyzer plugin or CI exists today. [OpenSSF Scorecard v5.6.0 — OSC-14](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#sast)
- **Application writes its own log file instead of stdout** — Twelve-Factor / XI. Logs (src/main/resources/application.properties, lines 5-5). Remove logging.file.name and let the process write its event stream to stdout/stderr, leaving collection and routing to the execution environment (TFR-19). [The Twelve-Factor App (12factor.net) — TFA-49](https://12factor.net/logs)
- **No throttling or lockout on repeated admin-password attempts** — Security / Identity & Access (src/main/java/com/example/todoui/TodoController.java, lines 64-70). Add throttling or lockout after repeated failed attempts against /admin/clear, and log each failed attempt (ATN-14). [OWASP Authentication Cheat Sheet — ATN-12](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#login-throttling)
- **User-supplied title is concatenated into the log template** — Security / Operational (src/main/java/com/example/todoui/TodoController.java, lines 45-45). Use a parameterized call (logger.info("Added todo: {}", title)) and keep the template constant so untrusted input can't forge or corrupt log entries (LOG-16). [OWASP Logging Cheat Sheet — LOG-17](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#log-injection-in-java)
- **No environment separation: debug-level error detail is always on** — Security / Operational (src/main/resources/application.properties, lines 1-6). Split configuration per environment (e.g. an application-prod.properties or profile) so development-only settings like include-stacktrace=always never ship to production (SCR-01). [OWASP Secure Code Review Cheat Sheet — SCR-02](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html#configuration-deployment)
- **No automated tests exist, so the suite has no pyramid shape at all** — Testing / Test Pyramid (src/main/java/com/example/todoui, lines 1-1). Create a test source set (e.g. src/test/java) with JUnit 5 unit tests mirroring com.example.todoui (TodoItem, TodoController), then add a thin layer of MockMvc-based controller tests to build a proper pyramid. [Compliance Reviewer Testing Rubric — TSR-03](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-03)
- **No coverage collection is configured anywhere in the repository** — Testing / Coverage (src/main/java/com/example/todoui, lines 1-1). Add a coverage tool (e.g. JaCoCo) to the Maven build once tests exist, and publish the report (CI artifact, PR comment or a documented local command) to find untested code. [Compliance Reviewer Testing Rubric — TSR-04](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-04)
- **The todoui production module has zero corresponding tests** — Testing / Module Coverage (src/main/java/com/example/todoui, lines 1-1). Add unit tests for TodoItem and controller-level tests (e.g. @WebMvcTest/MockMvc) for TodoController, and an acceptance-level test exercising the main list/add/complete journeys through the rendered Thymeleaf views. [Compliance Reviewer Testing Rubric — TSR-15](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-15)
- **No README exists for the app** — Maintainability / README & Onboarding (pom.xml, lines 14-17). Add a root README.md stating the app's purpose and documenting setup, build/run (e.g. `mvn spring-boot:run`) and test commands. [Compliance Reviewer Maintainability Rubric — MR-01](../../../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-01)

### Information

- **No SECURITY.md security policy in the repository** — Software Lifecycle / Security Policy (pom.xml, lines 1-2). Add a SECURITY.md (root, .github/ or docs/) giving a private reporting channel (email or URL), the triage/handling process, and supported-version/advisory information. [OpenSSF Scorecard v5.6.0 — OSC-15](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#security-policy)
- **Code parsing untrusted input has no fuzz, property-based or DAST testing** — Testing / Fuzz & Dynamic Testing (src/main/java/com/example/todoui, lines 1-1). Add fuzz or property-based tests (e.g. Jazzer, jqwik) for the form/request parameter parsing in TodoController, or add a DAST job (e.g. OWASP ZAP baseline scan) to the pipeline. [Compliance Reviewer Testing Rubric — TSR-23](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-23)
- **No automated load or performance tests exist for the web app** — Testing / Load & Performance Tests (src/main/java/com/example/todoui, lines 1-1). Add automated load tests for the todo app's critical request flows (list, add, complete), scripted with realistic data and usage patterns, run in CI or on a recorded schedule. [Azure Well-Architected Framework — AZT-01](https://learn.microsoft.com/azure/well-architected/performance-efficiency/performance-test#apply-multiple-performance-test-types)
- **Service version is not set in telemetry identity** — Observability / Telemetry Identity & Naming (src/main/resources/application.properties, lines 1-1). Set service.version (e.g. via otel.resource.attributes or build-info) to the deployed artifact version instead of leaving it unset. [OpenTelemetry — OTO-32](https://opentelemetry.io/docs/specs/semconv/registry/attributes/service/#service-attributes)
- **Linear scan over the in-memory todo list to find an item by id** — Performance (src/main/java/com/example/todoui/TodoController.java, lines 52-58). Store todos in a Map<Integer, TodoItem> keyed by id (or a ConcurrentHashMap given the shared-state issue noted under Software Quality DP-01) for O(1) lookup instead of an O(n) scan on every complete request. [Azure Well-Architected Framework — AZPE-31](https://learn.microsoft.com/azure/well-architected/performance-efficiency/optimize-code-infrastructure#optimize-code-logic)
- **No contributing guide exists** — Maintainability / Contributing Guide (pom.xml, lines 14-17). Add a CONTRIBUTING.md (or a README section) explaining the branching/PR workflow and any pre-submit checks (build, tests). [Compliance Reviewer Maintainability Rubric — MR-24](../../../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-24)
- **No license is stated for the app** — Maintainability / License & Conduct (pom.xml, lines 1-42). Add a LICENSE/LICENSE.md file at the root, or add a <licenses> element naming the license in pom.xml. [Compliance Reviewer Maintainability Rubric — MR-37](../../../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-37)

## 4. Full Results

### Software Quality

| Check | Result | Evidence |
|-------|--------|----------|
| SQ-01 | pass |  |
| SQ-02 | pass |  |
| SQ-03 | pass |  |
| SQ-04 | pass |  |
| SQ-05 | pass |  |
| SQ-06 | fail | duplicate evidence of SEC-II-01#3, see Security / Input & Injection |
| SQ-08 | pass |  |

#### Design Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| DP-01 | fail | duplicate evidence of SEC-II-01#3, see Security / Input & Injection |
| DP-02 | N/A | No inheritance hierarchies present in the reviewed files. |
| DP-04 | N/A | No design patterns or abstractions present to assess. |
| DP-05 | N/A | No complex, multi-step construction present. |
| DP-06 | N/A | No event subscriptions present. |

#### Architecture Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| AP-01 | N/A | App has no separate business/data layer to bypass; trivial single-layer design. |
| AP-02 | N/A | No layered architecture or multi-step workflow present to evaluate. |
| AP-03 | N/A | Fewer than 2 modules; no dependency cycles to assess. |
| AP-04 | N/A | Single-package app; no modules to assess cohesion/coupling between. |
| AP-06 | N/A | Fewer than 3 handlers share repeated cross-cutting logic to assess. |
| AP-07 | N/A | Fewer than 2 independently deployable units are in the files. |

#### Coding Standards

| Check | Result | Evidence |
|-------|--------|----------|
| CS-01 | pass |  |
| CS-02 | pass |  |
| CS-03 | N/A | No explanatory comments present to evaluate. |
| CS-04 | fail | duplicate evidence of SEC-IA-01#1, see Security / Identity & Access |
| CS-05 | fail | duplicate evidence of SEC-IA-01#1, see Security / Identity & Access |

### Software Lifecycle

#### Continuous Integration

| Check | Result | Evidence |
|-------|--------|----------|
| SL-01 | fail | No pipeline-as-code (GitHub Actions, Azure Pipelines, GitLab CI, Jenkinsfile) exists anywhere in the repository. |

#### Release Automation

| Check | Result | Evidence |
|-------|--------|----------|
| SL-02 | N/A | Repo publishes no versioned artifacts (no release/deploy pipeline or versioned API in scope). |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| SL-03 | pass |  |

#### Branch Protection

| Check | Result | Evidence |
|-------|--------|----------|
| SL-04 | N/A | Repository settings not visible in files (no settings-as-code, CODEOWNERS or forge signals present). |

#### Provenance & Signing

| Check | Result | Evidence |
|-------|--------|----------|
| SL-05 | N/A | Repo publishes no versioned artifacts. |

#### Security Policy

| Check | Result | Evidence |
|-------|--------|----------|
| SL-07 | fail | No SECURITY.md exists anywhere in the repository. |

#### Workflow Security

| Check | Result | Evidence |
|-------|--------|----------|
| SL-09 | N/A | No CI workflow files in scope. |

#### Pipeline Hardening

| Check | Result | Evidence |
|-------|--------|----------|
| SL-10 | N/A | No CI/build files in scope. |

#### Static Analysis

| Check | Result | Evidence |
|-------|--------|----------|
| SL-11 | fail | No SAST tool or compiler warnings-as-errors configuration exists, and there is no CI to run one. |

#### Committed Binaries

| Check | Result | Evidence |
|-------|--------|----------|
| SL-12 | pass |  |

### Twelve-Factor

#### I. Codebase

| Check | Result | Evidence |
|-------|--------|----------|
| TF-01 | pass |  |

#### II. Dependencies

| Check | Result | Evidence |
|-------|--------|----------|
| TF-02 | pass |  |

#### III. Config

| Check | Result | Evidence |
|-------|--------|----------|
| TF-03 | fail | admin.password is a literal deploy-varying credential committed in application.properties. |

#### IV. Backing services

| Check | Result | Evidence |
|-------|--------|----------|
| TF-04 | N/A | no backing services used (in-memory storage only) |

#### V. Build, release, run

| Check | Result | Evidence |
|-------|--------|----------|
| TF-05 | N/A | deployment/release pipeline files not in the subject's file list |

#### VI. Processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-06 | N/A | process-state and session-handling code not in the subject's file list |

#### VII. Port binding

| Check | Result | Evidence |
|-------|--------|----------|
| TF-07 | pass |  |

#### VIII. Concurrency

| Check | Result | Evidence |
|-------|--------|----------|
| TF-08 | pass |  |

#### IX. Disposability

| Check | Result | Evidence |
|-------|--------|----------|
| TF-09 | N/A | startup/shutdown and container entrypoint files not in the subject's file list |

#### X. Dev/prod parity

| Check | Result | Evidence |
|-------|--------|----------|
| TF-10 | N/A | development and production backing-service configurations not both visible |

#### XI. Logs

| Check | Result | Evidence |
|-------|--------|----------|
| TF-11 | fail | logging.file.name routes the event stream to a file instead of stdout. |

#### XII. Admin processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-12 | N/A | no admin or migration task definitions in the subject's file list |

### API Design

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | no API found: this is a server-rendered Spring MVC/Thymeleaf UI with no REST controllers or OpenAPI/Swagger spec |

### Security

#### Identity & Access

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-IA-01 | fail | No filter/interceptor enforces a deny-by-default rule anywhere in the files. |
| SEC-IA-02 | fail | The only authorization check is an inline comparison in one handler. |
| SEC-IA-03 | N/A | no JWTs issued or validated in the files |
| SEC-IA-04 | N/A | no OAuth 2.0/OIDC flow in the files |
| SEC-IA-05 | N/A | no session or cookie-based authentication in the files |
| SEC-IA-06 | fail | duplicate evidence of TF-03#1, see Twelve-Factor / III. Config |
| SEC-IA-07 | fail | Authentication is a hand-rolled String.equals check instead of a vetted mechanism. |
| SEC-IA-08 | N/A | no service-to-service calls or multiple privilege tiers in the files |
| SEC-IA-09 | fail | No throttle, lockout or failure logging is configured for the admin-password check. |
| SEC-IA-10 | fail | duplicate evidence of TF-03#1, see Twelve-Factor / III. Config |
| SEC-IA-11 | N/A | no OAuth tokens, client-side storage, or determinable TLS configuration for the credential path in the files |

#### Input & Injection

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-II-01 | fail | title, priority and returnUrl parameters are bound and used without server-side validation rules. |
| SEC-II-02 | N/A | No SQL or ORM query code in the files. |
| SEC-II-03 | N/A | No database access code in the files. |
| SEC-II-04 | N/A | No OS command or other interpreter invocation in the files. |
| SEC-II-05 | N/A | No XML parsing in the files. |
| SEC-II-06 | N/A | No file upload handling in the files. |
| SEC-II-07 | N/A | No file upload handling in the files. |
| SEC-II-08 | fail | item.title is rendered unescaped via th:utext in two places. |
| SEC-II-09 | N/A | No deserialization of untrusted data beyond plain request parameters in the files. |
| SEC-II-10 | N/A | No outbound server-side request derived from untrusted input in the files. |

#### Web & API

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-WA-01 | pass |  |
| SEC-WA-02 | pass |  |
| SEC-WA-03 | pass |  |
| SEC-WA-04 | pass |  |
| SEC-WA-05 | pass |  |
| SEC-WA-06 | N/A | no TLS settings or environment-separated production configuration in the files |
| SEC-WA-07 | pass |  |
| SEC-WA-08 | N/A | HTML-serving target with no JSON/XML API endpoints or file downloads in the files |
| SEC-WA-09 | N/A | HTML-serving target with no JSON/XML API endpoints or file downloads in the files |
| SEC-WA-10 | N/A | HTML-serving target with no JSON/XML API endpoints or file downloads in the files |
| SEC-WA-11 | pass |  |

#### Operational

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-OP-01 | fail | Boot's /error handling exposes stack traces and messages unconditionally. |
| SEC-OP-02 | fail | duplicate evidence of SEC-II-01#3, see Security / Input & Injection |
| SEC-OP-03 | pass |  |
| SEC-OP-04 | fail | Untrusted todo title is concatenated into a log template rather than passed as a parameter. |
| SEC-OP-05 | fail | duplicate evidence of TF-03#1, see Twelve-Factor / III. Config |
| SEC-OP-06 | N/A | no secret manager, container or orchestrator delivery mechanism in the subject's files to judge |
| SEC-OP-07 | fail | A single properties file ships development-level error detail with no production override. |
| SEC-OP-08 | fail | duplicate evidence of SEC-IA-02#1, see Security / Identity & Access |
| SEC-OP-09 | fail | duplicate evidence of TF-11#1, see Twelve-Factor / XI. Logs |
| SEC-OP-10 | N/A | no multi-step transactions or resource-handling code (streams/connections/locks) in the subject's files |

### Testing

#### Test Pyramid

| Check | Result | Evidence |
|-------|--------|----------|
| TST-01 | fail | No automated tests of any kind exist in the repository, so there is no pyramid to assess. |

#### Coverage

| Check | Result | Evidence |
|-------|--------|----------|
| TST-02 | fail | No coverage tool, CI step or documented command measures or reports coverage anywhere in the repository. |

#### Assertion Quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-03 | N/A | no tests |

#### Test Doubles

| Check | Result | Evidence |
|-------|--------|----------|
| TST-04 | N/A | no tests |

#### Isolation & Determinism

| Check | Result | Evidence |
|-------|--------|----------|
| TST-05 | N/A | no tests |

#### CI Execution

| Check | Result | Evidence |
|-------|--------|----------|
| TST-06 | fail | No automated tests exist, so no CI step can run or gate the build on them. |

#### Module Coverage

| Check | Result | Evidence |
|-------|--------|----------|
| TST-07 | fail | The known production root src/main/java/com/example/todoui (logic-bearing) has no corresponding tests at all. |

#### Test Code Quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-08 | N/A | no tests |

#### Integration & Contract Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-09 | N/A | no tests |

#### Security Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-10 | N/A | testInventory.signals.accessControl is false; no access control in scope to test. |

#### Fuzz & Dynamic Testing

| Check | Result | Evidence |
|-------|--------|----------|
| TST-11 | fail | testInventory.signals.untrustedInput is true, but no fuzz/property-based tests or DAST job exist. |

#### Load & Performance Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-12 | fail | The reviewed module is a deployable web app (todoui) with request endpoints and no load or performance tests at all (testInventory.signals.loadTests is false). |

#### Resilience Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-13 | N/A | testInventory.signals.integrationPoints is false; no remote-call dependency in scope to test for resilience. |

### Observability

#### Structured Logging

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-01 | fail | duplicate evidence of SEC-OP-07#1, see Security / Operational |

#### Correlation & Context Propagation

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-02 | N/A | single-process app with no calls to other services, databases or brokers in the subject's files |

#### Distributed Tracing

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-03 | N/A | no remote calls, messaging or custom span code in the subject's files |

#### Metrics

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-04 | N/A | no metrics or actuator/micrometer configuration in the subject's files |

#### Telemetry Export

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-05 | fail | duplicate evidence of TF-11#1, see Twelve-Factor / XI. Logs |

#### Health Endpoints

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-06 | fail | duplicate evidence of SEC-OP-07#1, see Security / Operational |

#### SLOs & SLIs

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-07 | fail | duplicate evidence of SEC-OP-07#1, see Security / Operational |

#### Telemetry Identity & Naming

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-08 | fail | service.version is not set, even though service.name is. |

#### Error Recording

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-09 | N/A | no tracing or exception-logging code in the subject's files |

#### Telemetry Volume & Safety

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-10 | N/A | no telemetry SDK, sampling or baggage configuration in the subject's files |

### Dependency Management

| Check | Result | Evidence |
|-------|--------|----------|
| DEP-01 | pass |  |
| DEP-02 | N/A | Maven-only target; Maven has no native lock file. |
| DEP-03 | N/A | No vulnerability analyzer output for this run. |
| DEP-04 | pass |  |
| DEP-05 | fail | duplicate evidence of SL-11#1, see Software Lifecycle / Static Analysis |
| DEP-07 | N/A | No dependency-update or vulnerability-scanning configuration in the file list. |
| DEP-08 | pass |  |
| DEP-09 | pass |  |

### Reliability

#### Timeouts

| Check | Result | Evidence |
|-------|--------|----------|
| REL-01 | N/A | This file is only the Spring Boot application entry point (main method); it contains no remote calls (HTTP/gRPC/DB/cache/broker). |

#### Transient-Fault Retries

| Check | Result | Evidence |
|-------|--------|----------|
| REL-02 | N/A | No remote calls or retry logic exist in this file. |

#### Idempotency

| Check | Result | Evidence |
|-------|--------|----------|
| REL-03 | N/A | No retried or multi-step operations exist in this file. |

#### Circuit Breakers

| Check | Result | Evidence |
|-------|--------|----------|
| REL-04 | N/A | No synchronous remote-dependency calls exist in this file. |

#### Redundancy

| Check | Result | Evidence |
|-------|--------|----------|
| REL-05 | N/A | No deployment config in scope; this file only starts the Spring application. |

#### Load Protection

| Check | Result | Evidence |
|-------|--------|----------|
| REL-06 | N/A | No dependency calls, bulkheads, load-shedding or rate-limiting code exist in this file. |

#### Messaging & Background Jobs

| Check | Result | Evidence |
|-------|--------|----------|
| REL-07 | N/A | No message consumers or background jobs in scope. |

#### In-Region High Availability

| Check | Result | Evidence |
|-------|--------|----------|
| REL-08 | N/A | Not a deployable service; no hosting, IaC or Kubernetes config is in scope for this file. |

### Performance

| Check | Result | Evidence |
|-------|--------|----------|
| PERF-01 | N/A | No expensive or repeated remote/data-store reads present to cache. |
| PERF-02 | N/A | Thread-per-request Spring MVC stack with no async APIs, blocking-on-async calls or concurrent fan-out present. |
| PERF-03 | N/A | No shareable HTTP/DB/cache clients or expensive objects instantiated in the files. |
| PERF-04 | N/A | No data-access or remote I/O code in the files. |
| PERF-05 | fail | complete() does a linear scan over the unbounded in-memory items list on every request. |
| PERF-06 | N/A | No data-store query code in the files. |
| PERF-07 | N/A | No long-running or resource-intensive work present to offload. |
| PERF-08 | N/A | No hosting/scaling config, static assets or processing pipelines in scope. |

### Disaster Recovery

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Monitoring

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Cost & Sustainability

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Maintainability

#### README & Onboarding

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-01 | fail | No README exists anywhere in this app (pom.xml is the only in-scope file); purpose, setup, build/run and test instructions are undocumented. |

#### Repository Layout

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-02 | N/A | Folder listing is not in this subject's file list (only pom.xml was given), so layout and module boundaries can't be judged. |

#### Prerequisites & Configuration

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-03 | pass |  |

#### Technical Debt

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-04 | N/A | No source files in scope: pom.xml is a build manifest, not reviewed source code. |

#### Deprecated Code

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-05 | N/A | No source files in scope: pom.xml is a build manifest, not reviewed source code. |

#### Contributing Guide

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-06 | fail | No CONTRIBUTING guide or README section exists anywhere in this app. |

#### Change History

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-07 | N/A | No versioned, publishable artifact is evident: pom.xml declares a 0.0.1-SNAPSHOT build version for a runnable app, not a released package, pipeline or versioned API. |

#### Architecture Docs

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-08 | N/A | Single-module Spring Boot app with no documented multi-module or layered structure in scope requiring an architecture overview. |

#### Docs Accuracy

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-09 | N/A | No docs are in scope naming commands, env vars, versions or links to check for staleness. |

#### License & Conduct

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-10 | fail | No LICENSE file and no <licenses> element exist in pom.xml, the only in-scope file. |

## 5. Appendix

- **Run:** `2026-11-13_0422-java-ui` · Target: `test/uis/java` · Git HEAD: `1e32a558426c76db3e23e432405a93bcc4371384`
- **Started:** 2026-11-13T04:22:01Z · **Completed:** 2026-11-12T21:33:58-07:00
- **Run flags:** advanced off (IaC and CLI analyzers not run)
- **Subjects skipped:** review-disaster-recovery (advanced usage off (IaC not reviewed)); review-monitoring (advanced usage off (IaC not reviewed)); review-cost-sustainability (advanced usage off (IaC not reviewed))
- **URLs fetched:** none
- **Link approvals:** none
