---
description: Source code creation standards for Java/Spring Boot applications in this repository.
applyTo: "src/main/**"
---

# Coding Instructions: Java (Spring Boot)

## Purpose and Scope
These instructions define how GitHub Copilot should create and maintain production source code for Java applications in this repository.

Scope restriction:
- These instructions apply to creating and maintaining application source code under `src/main/java` and resources under `src/main/resources`.
- Unit test work is governed by `unit-tests.instructions.md` and `test-resources.instructions.md`; follow those files when the task is test-related.

Hard constraints:
- Target the Java LTS version declared by the build (do not change it unless asked).
- Keep one top-level class per file.
- Never hard-code secrets, connection strings, or environment-specific values.
- Every operation that touches a database, HTTP endpoint, message broker, cache, or file system must be logged and traced, and every log entry must carry a `correlationId`.

## How This Instructions File Is Used
When a request involves creating or changing application source code, Copilot must:
1. Follow this file as the primary standard for structure, naming, design, and cross-cutting concerns.
2. Match existing conventions in the project where they do not conflict with these rules.
3. Build the project and resolve all compilation errors and warnings introduced by the change.
4. Keep changes scoped to the task; do not refactor unrelated code.

## Project Structure
Rules:
- Use the standard Maven/Gradle layout: `src/main/java`, `src/main/resources`, `src/test/java`, `src/test/resources`.
- Use a reverse-domain base package (`com.<company>.<product>`).
- Organize packages by feature first, then by technical role (package-by-feature), for example `com.pilotapi.order.api`, `com.pilotapi.order.service`, `com.pilotapi.order.repository`.
- Use multi-module builds when the application has clearly separated deployables or shared libraries.
- Keep the `@SpringBootApplication` class in the base package.
- Place configuration in `application.yml` with profile overrides (`application-{profile}.yml`); never commit secrets to these files.
- Use the build wrapper (`mvnw` / `gradlew`) committed to the repository.

Example layout:
```
src/main/java/com/pilotapi/
  PilotApiApplication.java
  order/
    api/            # @RestController, request/response DTOs, mappers
    service/        # Use cases and business logic
    domain/         # Entities, value objects, domain events
    repository/     # Spring Data repositories, persistence adapters
  shared/
    config/         # Cross-cutting @Configuration classes
    observability/  # Correlation filter, tracing/logging setup
src/main/resources/
  application.yml
  db/migration/     # Flyway or Liquibase scripts
```

## Architecture
Rules:
- Follow layered / hexagonal architecture: controllers -> services -> repositories; domain logic does not depend on web or persistence frameworks.
- Use constructor injection only; no field injection (`@Autowired` on fields). Declare injected fields `final`.
- Define interfaces (ports) for external integrations; implement them in adapter classes.
- Use Java records for immutable DTOs and value objects.
- Keep `@Transactional` boundaries at the service layer.
- Bind configuration with `@ConfigurationProperties` records and validate with `@Validated`.
- Use `Optional` for return values that may be absent; never return `null` collections.
- Handle errors centrally with `@RestControllerAdvice`; use domain-specific exceptions for expected failures.
- Apply SOLID principles; favor composition over inheritance.

## Naming Conventions
| Artifact | Convention | Example |
|---|---|---|
| Package | lowercase, no underscores | `com.pilotapi.order.service` |
| Class / Record | PascalCase noun | `OrderService`, `OrderSummary` |
| Interface | PascalCase, no `I` prefix | `OrderRepository`, `PaymentGateway` |
| Implementation | Descriptive prefix or `Impl` only if unavoidable | `JpaOrderRepository`, `StripePaymentGateway` |
| Abstract class | `Abstract` prefix | `AbstractMessageHandler` |
| Method | camelCase verb | `calculateTotal` |
| Variable / parameter | camelCase | `orderId` |
| Constant (`static final`) | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Enum type / constant | PascalCase / UPPER_SNAKE_CASE | `OrderStatus.SHIPPED` |
| Generic type parameter | Single uppercase letter or descriptive | `T`, `E`, `K`, `V` |
| Annotation | PascalCase | `@Audited` |
| Exception | Suffix `Exception` | `OrderNotFoundException` |
| Controller | Suffix `Controller` | `OrderController` |
| DTO | Suffix `Request` / `Response` | `CreateOrderRequest` |
| Configuration | Suffix `Config` / `Properties` | `KafkaConfig`, `PaymentProperties` |

Rules:
- File names match the public class name.
- Avoid abbreviations; prefer descriptive names.
- Boolean methods read as predicates (`isActive`, `hasItems`, `canShip`).

## Documentation
Rules:
- Every public class, interface, and public/protected method must have Javadoc (`@param`, `@return`, `@throws` as applicable).
- Add `package-info.java` describing each feature package.
- Comments explain *why*, not *what*; do not restate the code.
- The project includes a `README.md` describing its purpose, how to build/run it, and required configuration properties.
- Record significant design decisions as Architecture Decision Records under `docs/adr/`.
- APIs publish an OpenAPI document (springdoc-openapi) with summaries, descriptions, and response schemas for every endpoint.

## API Design
Applies when the project exposes HTTP APIs.

Rules:
- Use `@RestController` with resource-oriented, plural, lowercase, kebab-case routes (`/api/v1/purchase-orders/{id}`).
- Use HTTP verbs and status codes correctly (`201 Created` with `Location` header, `204 No Content`, `404 Not Found`, `409 Conflict`).
- Return errors as RFC 9457 Problem Details (`ProblemDetail`, `spring.mvc.problemdetails.enabled=true`), including the `correlationId` as a property.
- Version APIs explicitly (URL segment or header).
- Validate input with Jakarta Bean Validation (`@Valid`, `@NotNull`, `@Size`) and return field-level errors.
- Paginate collection endpoints (`Pageable`); support filtering and sorting through query parameters.
- Support idempotency for unsafe retried operations (for example, an `Idempotency-Key` header on `POST`).
- Never expose JPA entities directly; map to DTOs (MapStruct or explicit mappers).
- Document every endpoint with springdoc-openapi annotations.

### 12-Factor App Guidance
| Factor | Java / Spring Boot Practice |
|---|---|
| I. Codebase | One repository per deployable; one build produces many deploys. |
| II. Dependencies | Declare all dependencies in `pom.xml` / `build.gradle`; use the committed build wrapper. |
| III. Config | Externalize config through environment variables and Spring profiles; secrets from Vault / cloud secret managers (Spring Cloud). |
| IV. Backing services | Treat databases, queues, and caches as attached resources addressed by configuration. |
| V. Build, release, run | Build immutable container images (Buildpacks or Jib); inject config at release. |
| VI. Processes | Keep services stateless; store session/state in a backing service (Spring Session + Redis). |
| VII. Port binding | Use the embedded server; bind to `server.port` from the `PORT`/`SERVER_PORT` environment variable. |
| VIII. Concurrency | Scale out by adding processes; use virtual threads or worker processes for concurrent work. |
| IX. Disposability | Start fast; enable `server.shutdown=graceful` and set `spring.lifecycle.timeout-per-shutdown-phase`. |
| X. Dev/prod parity | Use the same backing services locally (Docker Compose / Testcontainers) as in production. |
| XI. Logs | Write structured (JSON) logs to stdout; let the platform route them. |
| XII. Admin processes | Run migrations (Flyway/Liquibase) and one-off tasks as separate commands using the same codebase and config. |

## UI Design
Applies when the project includes a UI (Thymeleaf, Vaadin, JavaFX, or a server-rendered front end).

Rules:
- Separate presentation from logic: controllers prepare view models; templates contain no business logic.
- Build reusable fragments/components with clear inputs.
- Meet WCAG 2.2 AA: semantic HTML, labels for all inputs, keyboard navigation, sufficient color contrast, ARIA only when native semantics are insufficient.
- Validate input on the client for usability and on the server for security.
- Show loading, empty, and error states for every asynchronous operation.
- Externalize user-facing strings in `messages.properties` for localization.
- Use responsive layouts that work on mobile and desktop.
- Keep CSRF protection enabled for form posts.

## Security
Rules:
- Follow the OWASP Top 10 and OWASP ASVS.
- Use Spring Security with OAuth 2.0 / OpenID Connect (resource server with JWT for APIs); deny by default and authorize with method security (`@PreAuthorize`).
- Store secrets in a secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault).
- Use Spring Data / JPA parameter binding or `PreparedStatement`; never build SQL or JPQL by string concatenation.
- Validate and encode all untrusted input and output; rely on template auto-escaping.
- Enforce HTTPS and HSTS; set security headers (CSP, `X-Content-Type-Options`, `Referrer-Policy`).
- Configure CORS with explicit allowed origins; never combine wildcard origins with credentials.
- Apply rate limiting (Bucket4j / Resilience4j RateLimiter / API gateway) to public endpoints.
- Never log secrets, tokens, passwords, or PII; mask sensitive fields.
- Hash passwords with `BCryptPasswordEncoder` / Argon2; never implement custom cryptography.
- Restrict Actuator endpoints: expose only `health` and `info` publicly; secure the rest.
- Return generic error messages to clients; keep stack traces out of responses.

## Observability
Rules:
- Instrument with OpenTelemetry (OpenTelemetry Java agent or the OpenTelemetry Spring Boot starter) for traces, metrics, and logs; export via OTLP.
- Set `service.name`, `service.version`, and `deployment.environment` resource attributes.
- Ensure instrumentation covers every component:
  - HTTP server: Spring MVC / WebFlux instrumentation.
  - HTTP client: `RestClient` / `WebClient` instrumentation.
  - Database: JDBC / Hibernate / R2DBC instrumentation.
  - Messaging: Kafka / RabbitMQ / JMS instrumentation with context propagation through message headers.
  - Cache: Redis (Lettuce/Jedis) instrumentation.
- Use SLF4J with structured logging (`logging.structured.format.console=ecs` or Logstash encoder); use parameterized messages, never string concatenation.
- Log each action against a database, HTTP endpoint, message broker, cache, or external component with: operation name, target, outcome, and duration.
- Create custom spans (`@WithSpan` or the `Tracer` API) for significant business operations and Micrometer/OpenTelemetry meters for business metrics.

### CorrelationId
Rules:
- Every log entry must include a `correlationId`.
- A servlet filter (or WebFlux `WebFilter`) reads `X-Correlation-Id` from the inbound request, or generates one if absent, and returns it in the response header.
- Put the `correlationId` in the SLF4J `MDC` and as a span attribute/baggage so it flows across HTTP calls and messages; clear the `MDC` in a `finally` block.
- Propagate `X-Correlation-Id` on all outbound HTTP calls (via a `ClientHttpRequestInterceptor` / `ExchangeFilterFunction`) and as a header on all published messages.
- Consumers restore the `correlationId` into the `MDC` from message headers before processing.
- When using virtual threads or async executors, propagate `MDC` context with a `TaskDecorator` / Micrometer context propagation.

Example:
```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class CorrelationIdFilter extends OncePerRequestFilter {

    private static final String HEADER_NAME = "X-Correlation-Id";
    private static final String MDC_KEY = "correlationId";

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String correlationId = Optional.ofNullable(request.getHeader(HEADER_NAME))
                .filter(value -> !value.isBlank())
                .orElseGet(() -> UUID.randomUUID().toString());

        MDC.put(MDC_KEY, correlationId);
        Span.current().setAttribute("correlation.id", correlationId);
        response.setHeader(HEADER_NAME, correlationId);
        try {
            chain.doFilter(request, response);
        } finally {
            MDC.remove(MDC_KEY);
        }
    }
}
```

## Scalability, Reliability, and Maintainability
Rules:
- Design services to be stateless and horizontally scalable.
- Reuse configured `RestClient` / `WebClient` beans; set connection and read timeouts on every client.
- Apply resilience with Resilience4j: timeouts, retries with exponential backoff and jitter, circuit breakers, and bulkheads.
- Make message consumers idempotent; use the transactional outbox pattern for reliable event publishing.
- Expose Actuator health groups (`liveness`, `readiness`) covering every backing service.
- Implement graceful shutdown.
- Keep methods small and cohesive; keep cyclomatic complexity low.
- Enforce style and static analysis (Checkstyle or Spotless, SpotBugs, Error Prone, or SonarQube) in the build.
- Manage schema with Flyway or Liquibase; migrations must be backward compatible for rolling deployments.

## Dependency Management
Rules:
- Use the Spring Boot BOM (`spring-boot-starter-parent` or `platform(...)`) to align versions; avoid overriding managed versions without reason.
- Declare versions centrally (`<dependencyManagement>` / Gradle version catalog `libs.versions.toml`).
- Prefer Spring Boot starters and the JDK standard library before adding third-party libraries.
- Add a dependency only when it provides clear value; justify new dependencies in the pull request.
- Use Gradle dependency locking or the Maven Enforcer plugin for reproducible builds.
- Scan for vulnerabilities (OWASP Dependency-Check, Dependabot, Snyk) and keep dependencies current.
- Verify licenses are compatible with the project.
- Resolve artifacts only from trusted repositories.

## Performance
Rules:
- Avoid N+1 queries: use fetch joins, `@EntityGraph`, or DTO projections; default associations to `LAZY`.
- Use read-only transactions (`@Transactional(readOnly = true)`) for queries.
- Paginate and stream large result sets.
- Tune connection pools (HikariCP) to match database capacity.
- Cache read-heavy data with Spring Cache (Caffeine/Redis) and explicit expiration.
- Use virtual threads (`spring.threads.virtual.enabled=true`) for blocking I/O workloads where supported.
- Minimize object creation in hot paths; use `StringBuilder` for loops; prefer primitive collections when profiling shows benefit.
- Close resources with try-with-resources.
- Measure before optimizing: use JMH and profilers (JFR, async-profiler); track latency with OpenTelemetry metrics.

## Validation Workflow
Before completing a code change, Copilot must:
1. Run `./mvnw verify` or `./gradlew build` with zero errors and no new warnings.
2. Confirm existing tests pass.
3. Confirm new public members are documented and new I/O paths are logged, traced, and carry the `correlationId`.
