# Python (FastAPI or Flask)

## Recognizing the layers

The layers are usually packages: `domain/`, `repository/` (or `repositories/`, `persistence/`, `data/`), `service/` (or `services/`), and `api/` (`routes/`, `routers/`, `controllers/`). Treat each package as the "project" for that layer. Imports must point inward: `api` imports `service`, `service` imports `domain` and `repository`; `domain` imports neither web nor persistence frameworks.

## Files and names

Python interfaces take no `I` prefix, so the `typing.Protocol` (or `abc.ABC`, if the codebase uses those) gets the plain name and the class gets a descriptive prefix. Both still contain the domain name, and the classes end in the required suffix. Follow an existing scheme if the codebase has one.

| Artifact | Default name | Module |
|---|---|---|
| DTO | `<Domain>Dto` (Pydantic model, or `@dataclass(frozen=True)` if the codebase uses dataclasses) | `domain/<domain>_dto.py` |
| Entity | `<Domain>Entity` (SQLAlchemy model with `__tablename__ = "<table>"`) | `repository/<domain>_entity.py` |
| Repository interface | `<Domain>Repository` (`Protocol`) | `repository/<domain>_repository.py` |
| Repository class | `SqlAlchemy<Domain>Repository` | same module, or `sqlalchemy_<domain>_repository.py` |
| Service interface | `<Domain>Service` (`Protocol`) | `service/<domain>_service.py` |
| Service class | `Default<Domain>Service` | same module, or `default_<domain>_service.py` |
| Controller | router module `api/routes/<domain>_routes.py` or the existing router named in question D | `api/` |

Use type hints everywhere, and `async def` if the existing repositories and routes are async.

## Data access by technology

**SQLAlchemy ORM**: inherit the entity from the existing declarative `Base`; take the `Session`/`AsyncSession` in the repository constructor the way existing repositories do.

**SQLAlchemy Core / DB-API** (raw SQL): keep the table name in a module constant `TABLE_NAME = "<table>"`, and use bound parameters (`text("... WHERE id = :id")`, `%s` placeholders) only. Never format values into SQL strings.

## Registration

Python has no single standard DI container, so follow what the codebase uses:

- **A container library** (`dependency-injector`, `injector`, `punq`, `lagom`): add the providers to the repository-layer container/module and the service-layer container/module, and have the service one include the repository one.
- **None**: create one function per layer and chain them.

```python
# repository/registration.py
def register_repositories(registry: Registry) -> None:
    registry.register(SupplierRepository, SqlAlchemySupplierRepository)

# service/registration.py
def register_services(registry: Registry) -> None:
    register_repositories(registry)          # Service registration calls Repository registration
    registry.register(SupplierService, DefaultSupplierService)

# main.py
register_services(registry)                  # Presentation calls Service registration
```

If the codebase only wires dependencies with FastAPI `Depends` provider functions, add `get_<domain>_repository` and `get_<domain>_service` provider functions in the repository and service layers instead, have the service provider depend on the repository provider, and have the routes depend on the service provider. Say which pattern you used in the summary.

## Service and mapping

`Default<Domain>Service.__init__` takes the `<Domain>Repository`. It holds `to_entity(dto) -> <Domain>Entity` and `to_dto(entity) -> <Domain>Dto` as `@staticmethod`s.

## Controller

Add an `APIRouter` (or Flask `Blueprint`) with the routes and status codes in [actions.md](../actions.md), inject `<Domain>Service` via the registration mechanism above, and include the router in the app the way existing routers are included.

## Unit tests

These are the standard best practices for this stack. A `unit-tests.instructions.md` file in the repository takes precedence over them (see [testing.md](../testing.md)).

Tests live in `tests/` (mirroring the package layout, for example `tests/service/test_<domain>_service.py`) and use `pytest`, unless the codebase uses `unittest`. Follow the existing fixtures in `conftest.py`.

- Repository: a SQLAlchemy engine on `sqlite://` (in-memory), with `Base.metadata.create_all(engine)` in a fixture and a fresh session per test. Use `sqlite+aiosqlite://` for an async codebase (the `aiosqlite` package, named in the plan if it is not already a dependency).
- Service and mapping: a hand-written fake class that satisfies the `<Domain>Repository` protocol, or `unittest.mock.Mock(spec=...)` if the existing tests use mocks.
- Controller: FastAPI `TestClient` with `app.dependency_overrides` replacing the service provider with a fake; for Flask, `app.test_client()` with the fake registered the way the app wires dependencies. Add `httpx` to the dev dependencies if FastAPI's `TestClient` needs it and it is missing.
- Registration: call the service registration function (or the provider functions) and assert the repository and service are registered or returned.

Use `pytest-asyncio` (or `anyio`) for async tests if the codebase already does.

## Bruno base URL

Use the address from the app's README or run configuration as `baseUrl` (for example `http://localhost:8000` for `uvicorn`, `http://localhost:5000` for `flask run`).

## Verify

Run the project's type checker and linter if configured (`mypy`, `ruff`), import the app module (`python -c "import <package>.main"`), then run `pytest`. Report the results.
