# Language Signals — Java (Reliability)

Local lookup table, not a standard. Use it to classify code and configuration for REL-01 … REL-08; cite the AZRL elements, never this file. If a library isn't listed and you can't classify it, add `localized-standard-gap: unrecognized library <name>` to `notes`.

## Default timeouts (AZRL-01, SKILL.md step 3)

| Client | Default timeout | AZRL-01 |
|---|---|---|
| `HttpURLConnection`; `RestTemplate` with `SimpleClientHttpRequestFactory` | connect and read: none (0) | **fail** unless set |
| `java.net.http.HttpClient` | connect: none; request: none | **fail** unless `connectTimeout` and the request `timeout` are set |
| Spring `WebClient` (Reactor Netty) | connect 30 s; response: none | **fail** unless `responseTimeout` or `.timeout()` is set |
| Apache HttpClient 5 | connect 3 min; connection-request (pool) 3 min; response: none | **fail** unless a response/socket timeout is set |
| OkHttp | connect, read and write 10 s | pass with note |
| OpenFeign (`Request.Options`) | connect 10 s, read 60 s | pass with note |
| JDBC statements | query timeout: none (0) | **fail** unless `setQueryTimeout`, `spring.jpa.properties.jakarta.persistence.query.timeout` (or `javax.…`), `spring.transaction.default-timeout` or a driver socket timeout is set |
| HikariCP | `connectionTimeout` 30 s (pool acquisition only) | doesn't cover query time |

## Signals

| Area | Pass signals | Anti-patterns / fail signals |
|---|---|---|
| Retries (REL-02) | Resilience4j `Retry` with `IntervalFunction.ofExponentialRandomBackoff`, `retryExceptions` / `ignoreExceptions`; Spring Retry `@Retryable(maxAttempts, backoff = @Backoff(multiplier, random = true))`; Spring Cloud CircuitBreaker; settings in `application.yml` | `while (true)` retry loops; `@Retryable` with the default fixed 1 s delay on many attempts; retrying on `Exception.class` including 4xx; Spring Retry around a client that already retries (AZRL-10) |
| Idempotency (REL-03) | idempotency key created before the retry; `@Retryable` only on idempotent methods; `@Transactional` boundary inside the retried method | `@Retryable` on non-idempotent POST / charge methods; retrying a single statement inside an open transaction |
| Circuit breakers (REL-04) | Resilience4j `CircuitBreaker` registered once (`CircuitBreakerRegistry`, Spring Boot config) per backend instance name; fallback method | `CircuitBreaker.ofDefaults(...)` per call; one instance name shared by unrelated backends |
| Isolation and load (REL-06) | Resilience4j `Bulkhead` / `ThreadPoolBulkhead` per backend; `RateLimiter`; Bucket4j; Spring Cloud Gateway `RequestRateLimiter` | mapping downstream `HttpClientErrorException.TooManyRequests` to 500 |
| Messaging and jobs (REL-07) | Spring Kafka `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`, `enable.auto.commit=false` with ack after processing; Spring AMQP DLX with `default-requeue-rejected=false`; Spring Batch restartable jobs; ShedLock on `@Scheduled` in multi-instance deployments; `server.shutdown=graceful` + `spring.lifecycle.timeout-per-shutdown-phase` | Kafka `enable.auto.commit=true` with side effects; requeue-on-reject with no DLX (poison loop); `@Scheduled` on several replicas without a lock; in-memory `BlockingQueue` for must-not-lose work |
