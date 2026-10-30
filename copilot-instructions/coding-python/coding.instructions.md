---
description: Source code creation standards for Python applications in this repository.
applyTo: "src/**/*.py"
---

# Coding Instructions: Python

## Purpose and Scope
These instructions define how GitHub Copilot should create and maintain production source code for Python applications in this repository.

Scope restriction:
- These instructions apply to creating and maintaining application source code under `src/` and its supporting configuration.
- Unit test work is governed by `unit-tests.instructions.md`; follow that file when the task is test-related.

Hard constraints:
- Target the Python version declared in `pyproject.toml` (`requires-python`); do not change it unless asked.
- Add type hints to all function signatures and public attributes.
- Never hard-code secrets, connection strings, or environment-specific values.
- Every operation that touches a database, HTTP endpoint, message broker, cache, or file system must be logged and traced, and every log entry must carry a `correlation_id`.

## How This Instructions File Is Used
When a request involves creating or changing application source code, Copilot must:
1. Follow this file as the primary standard for structure, naming, design, and cross-cutting concerns.
2. Match existing conventions in the project where they do not conflict with these rules.
3. Run linting, type checking, and tests, and resolve issues introduced by the change.
4. Keep changes scoped to the task; do not refactor unrelated code.

## Project Structure
Rules:
- Use the `src` layout with a single top-level package (`src/<package_name>/`) and tests under `tests/`.
- Define project metadata, dependencies, and tool configuration in `pyproject.toml` (PEP 621).
- Organize modules by feature first, then by technical role.
- Keep the application entry point thin (`main.py` / `__main__.py`); build the app with a factory function (`create_app()`).
- Centralize configuration in a settings module using `pydantic-settings`.
- Include `py.typed` for packages consumed by others.

Example layout:
```
pyproject.toml
src/pilot_api/
  __init__.py
  main.py               # App factory, startup/shutdown
  config.py             # Settings (pydantic-settings)
  api/
    routes/             # FastAPI/Flask routers
    schemas/            # Request/response models (Pydantic)
  service/              # Use cases and business logic
  domain/               # Entities, value objects, domain errors
  repository/           # Persistence adapters (SQLAlchemy)
  integrations/         # HTTP clients, messaging adapters
  observability/        # Logging, tracing, correlation middleware
tests/
```

## Architecture
Rules:
- Follow layered / hexagonal architecture: routes -> services -> repositories; domain logic does not import web or persistence frameworks.
- Define ports with `typing.Protocol` or `abc.ABC`; implement them in adapter modules.
- Use dependency injection through constructor parameters (or FastAPI `Depends`); avoid module-level global state and singletons with hidden side effects.
- Use `dataclasses` (`frozen=True`) or Pydantic models for value objects and DTOs.
- Use `async`/`await` consistently for I/O in async frameworks; never call blocking I/O from the event loop (offload with `asyncio.to_thread` if unavoidable).
- Raise domain-specific exceptions for expected failures and translate them to responses in one central handler.
- Prefer composition over inheritance; keep functions pure where practical.
- Follow PEP 8 and PEP 20.

## Naming Conventions
| Artifact | Convention | Example |
|---|---|---|
| Package / module | lowercase_snake_case, short | `order_service.py` |
| Class | PascalCase noun | `OrderService` |
| Protocol / ABC (interface) | PascalCase, no `I` prefix | `OrderRepository`, `PaymentGateway` |
| Implementation | Descriptive prefix | `SqlAlchemyOrderRepository` |
| Function / method | snake_case verb | `calculate_total` |
| Variable / parameter | snake_case | `order_id` |
| Constant | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Enum class / member | PascalCase / UPPER_SNAKE_CASE | `OrderStatus.SHIPPED` |
| Type variable | PascalCase, short | `T`, `EntityT` |
| Exception | Suffix `Error` | `OrderNotFoundError` |
| Private member | Leading underscore | `_session` |
| Pydantic schema | Suffix `Request` / `Response` | `CreateOrderRequest` |
| Settings | Suffix `Settings` | `DatabaseSettings` |

Rules:
- Avoid abbreviations; prefer descriptive names.
- Boolean names read as predicates (`is_active`, `has_items`, `can_ship`).
- Do not shadow built-ins (`id`, `type`, `list`, `input`).

## Documentation
Rules:
- Every public module, class, function, and method must have a docstring (PEP 257) using Google style (`Args:`, `Returns:`, `Raises:`).
- Type hints are part of the documentation; do not duplicate types in docstrings.
- Comments explain *why*, not *what*; do not restate the code.
- The project includes a `README.md` describing its purpose, how to install/run it, and required environment variables.
- Record significant design decisions as Architecture Decision Records under `docs/adr/`.
- APIs publish an OpenAPI document with summaries, descriptions, and response models for every endpoint.

## API Design
Applies when the project exposes HTTP APIs.

Rules:
- Prefer FastAPI for new APIs; use resource-oriented, plural, lowercase, kebab-case routes (`/api/v1/purchase-orders/{id}`).
- Use HTTP verbs and status codes correctly (`201 Created` with `Location` header, `204 No Content`, `404 Not Found`, `409 Conflict`).
- Return errors as RFC 9457 Problem Details (`application/problem+json`), including the `correlation_id` as an extension member.
- Version APIs explicitly (URL segment or header).
- Validate all input with Pydantic models; return field-level errors.
- Paginate collection endpoints; support filtering and sorting through query parameters.
- Support idempotency for unsafe retried operations (for example, an `Idempotency-Key` header on `POST`).
- Never expose ORM models directly; map to response schemas.
- Declare `response_model`, `status_code`, `summary`, and `responses` on every endpoint for OpenAPI generation.

### 12-Factor App Guidance
| Factor | Python Practice |
|---|---|
| I. Codebase | One repository per deployable; one build produces many deploys. |
| II. Dependencies | Declare all dependencies in `pyproject.toml` with a lock file (`uv.lock` / `poetry.lock`); always run in an isolated virtual environment. |
| III. Config | Read config from environment variables via `pydantic-settings`; secrets from a secrets manager. |
| IV. Backing services | Treat databases, queues, and caches as attached resources addressed by URL configuration. |
| V. Build, release, run | Build immutable container images; inject config at release. |
| VI. Processes | Keep services stateless; store session/state in a backing service (for example, Redis). |
| VII. Port binding | Self-host with an ASGI/WSGI server (Uvicorn/Gunicorn) bound to the `PORT` environment variable. |
| VIII. Concurrency | Scale out by adding processes/workers; run background work in separate worker processes (Celery, Arq, Dramatiq). |
| IX. Disposability | Start fast; handle `SIGTERM` with lifespan handlers and drain in-flight work before exit. |
| X. Dev/prod parity | Use the same backing services locally (Docker Compose) as in production. |
| XI. Logs | Write structured (JSON) logs to stdout; let the platform route them. |
| XII. Admin processes | Run migrations (Alembic) and one-off tasks as separate commands using the same codebase and config. |

## UI Design
Applies when the project includes a UI (Jinja2 templates, Django templates, Streamlit, or desktop UI).

Rules:
- Separate presentation from logic: views prepare context; templates contain no business logic.
- Build reusable template components/macros with clear inputs.
- Meet WCAG 2.2 AA: semantic HTML, labels for all inputs, keyboard navigation, sufficient color contrast, ARIA only when native semantics are insufficient.
- Validate input on the client for usability and on the server for security.
- Show loading, empty, and error states for every asynchronous operation.
- Externalize user-facing strings for localization (`gettext` / Babel).
- Use responsive layouts that work on mobile and desktop.
- Keep template auto-escaping and CSRF protection enabled.

## Security
Rules:
- Follow the OWASP Top 10 and OWASP ASVS.
- Authenticate with OAuth 2.0 / OpenID Connect (JWT validation for APIs); deny by default and enforce authorization in dependencies/decorators.
- Store secrets in a secrets manager; load them through settings, never commit `.env` files containing secrets.
- Use SQLAlchemy parameter binding; never build SQL with f-strings or string concatenation.
- Never use `eval`, `exec`, `pickle` on untrusted data, `yaml.load` without `SafeLoader`, or `subprocess` with `shell=True` on user input.
- Validate and encode all untrusted input and output.
- Enforce HTTPS and HSTS; set security headers (CSP, `X-Content-Type-Options`, `Referrer-Policy`).
- Configure CORS with explicit allowed origins; never combine wildcard origins with credentials.
- Apply rate limiting (for example, `slowapi` or an API gateway) to public endpoints.
- Never log secrets, tokens, passwords, or PII; mask sensitive fields.
- Use `secrets` for tokens and `argon2`/`bcrypt` for password hashing; never implement custom cryptography.
- Run security linters (`bandit`, Ruff `S` rules) in CI.
- Return generic error messages to clients; keep tracebacks out of responses.

## Observability
Rules:
- Instrument with OpenTelemetry (`opentelemetry-sdk`, `opentelemetry-distro`) for traces, metrics, and logs; export via OTLP.
- Set `service.name`, `service.version`, and `deployment.environment` resource attributes.
- Enable instrumentation for every component:
  - HTTP server: `opentelemetry-instrumentation-fastapi` / `-flask` / `-django`.
  - HTTP client: `opentelemetry-instrumentation-httpx` / `-requests`.
  - Database: `opentelemetry-instrumentation-sqlalchemy` / `-psycopg` / `-asyncpg`.
  - Messaging: `opentelemetry-instrumentation-kafka-python` / `-aio-pika` / `-celery` with context propagation through message headers.
  - Cache: `opentelemetry-instrumentation-redis`.
- Use the standard `logging` module (or `structlog`) with JSON output; obtain loggers with `logging.getLogger(__name__)`; never use `print` for diagnostics.
- Use lazy formatting (`logger.info("Order %s created", order_id)`) or structured key/value fields; never f-strings in log calls.
- Log each action against a database, HTTP endpoint, message broker, cache, or external component with: operation name, target, outcome, and duration.
- Create custom spans (`tracer.start_as_current_span`) for significant business operations and meters for business metrics.

### CorrelationId
Rules:
- Every log entry must include a `correlation_id`.
- Middleware reads `X-Correlation-Id` from the inbound request, or generates one if absent, and returns it in the response header.
- Store the `correlation_id` in a `contextvars.ContextVar` and inject it into every log record with a `logging.Filter` (or `structlog` contextvars); add it as a span attribute/baggage.
- Propagate `X-Correlation-Id` on all outbound HTTP calls (via an `httpx` event hook or client wrapper) and as a header on all published messages.
- Consumers restore the `correlation_id` from message headers before processing.

Example:
```python
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="-")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Reads or creates the request correlation ID and binds it to logs and traces."""

    header_name = "X-Correlation-Id"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        correlation_id = request.headers.get(self.header_name) or str(uuid.uuid4())
        token = correlation_id_var.set(correlation_id)
        trace.get_current_span().set_attribute("correlation.id", correlation_id)
        try:
            response = await call_next(request)
        finally:
            correlation_id_var.reset(token)
        response.headers[self.header_name] = correlation_id
        return response


class CorrelationIdFilter(logging.Filter):
    """Adds the current correlation ID to every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_var.get()
        return True
```

## Scalability, Reliability, and Maintainability
Rules:
- Design services to be stateless and horizontally scalable.
- Reuse long-lived HTTP clients (`httpx.AsyncClient`) and database engines; create them at startup and close them at shutdown.
- Set explicit timeouts on every network call.
- Apply retries with exponential backoff and jitter (`tenacity`) and circuit breakers for unreliable dependencies.
- Make message consumers idempotent; use the transactional outbox pattern for reliable event publishing.
- Expose health endpoints (`/health/live`, `/health/ready`) covering every backing service.
- Implement graceful shutdown in lifespan handlers.
- Keep functions small and cohesive; keep cyclomatic complexity low.
- Enforce formatting and linting with Ruff and type checking with mypy (strict) or Pyright in CI.
- Manage schema with Alembic; migrations must be backward compatible for rolling deployments.

## Dependency Management
Rules:
- Declare dependencies in `pyproject.toml`; separate runtime and development dependencies (dependency groups / optional extras).
- Use a lock file (`uv.lock` or `poetry.lock`) committed to the repository for reproducible installs.
- Prefer the standard library before adding third-party packages.
- Add a dependency only when it provides clear value; justify new dependencies in the pull request.
- Use compatible version ranges in libraries and locked exact versions in applications.
- Scan for vulnerabilities (`pip-audit`, Dependabot) and keep dependencies current.
- Verify licenses are compatible with the project.
- Install only from trusted indexes.

## Performance
Rules:
- Use async I/O for I/O-bound services; use process pools for CPU-bound work.
- Avoid N+1 queries: use `selectinload` / `joinedload`; select only needed columns.
- Paginate and stream large result sets (generators, async iterators, server-side cursors).
- Tune database connection pools to match database capacity.
- Cache read-heavy data (`functools.lru_cache` for pure functions, Redis for shared data) with explicit expiration.
- Prefer built-ins, comprehensions, and generators over manual loops; use `collections` and `itertools` where appropriate.
- Use context managers (`with` / `async with`) to release resources.
- Measure before optimizing: use `cProfile`, `py-spy`, or `pytest-benchmark`; track latency with OpenTelemetry metrics.

## Validation Workflow
Before completing a code change, Copilot must:
1. Run `ruff check`, `ruff format --check`, and `mypy` (or Pyright) with no new issues.
2. Run `pytest` and confirm existing tests pass.
3. Confirm new public members are documented and new I/O paths are logged, traced, and carry the `correlation_id`.
