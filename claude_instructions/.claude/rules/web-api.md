---
paths:
  - "src/PilotApi.Web/**"
  - "src/PilotApi.Domain/**"
  - "src/PilotApi.Shared/OpenApi/**"
  - "shared/PilotSharedSource/**"
---

# Controllers, DTOs and the OpenAPI contract

- Versioned controllers live in `Controllers/V1` and derive from `SimpleControllerBase`. It declares the common request headers (`X-Api-Version`, `X-Caller-Name`, `X-Correlation-Id`) as `[FromHeader]` properties. `SystemController` (`/healthcheck`, `/about`) is anonymous and declares the same headers itself.
- Controllers translate `RetrieveResponse<T>` into status codes: `IsError` sets a `Warning` response header and returns 400, a null `Result` returns 204, and an add returns 201 via `CreatedAtAction`.
- `Program.cs` stays thin. It calls `ApplicationRegistration()` (Services DI), then `ApiWebApplicationBuilder()` / `ApiWebApplication()` (Shared).
- The generated OpenAPI document must match `shared/PilotSharedSource/OpenAPI/PilotApi_v1.yaml`, and `OpenApiIntegrationTests` fails otherwise. Signature, route, header or DTO changes need the spec updated in the submodule (a separate repo) or must conform to it. XML doc comments feed the document through `ManualXmlComments*Transformer`.
- JSON number handling is strict for both MVC and the OpenAPI generator (`ApiExtensions`).
