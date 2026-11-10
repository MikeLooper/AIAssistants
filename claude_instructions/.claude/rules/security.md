---
paths:
  - "src/PilotApi.Shared/Api/Security/**"
  - "src/PilotApi.Shared/Helpers/SecurityHelper.cs"
  - "src/PilotApi.Shared/Configuration/SecurityConfiguration.cs"
  - "src/PilotApi.Services/Security/**"
  - "src/PilotApi.Repositories/Repositories/UserRolesRepository.cs"
---

# Security

- JWT bearer auth against Keycloak, configured by `Application.Security`.
- Roles are **not** read from token claims. `PreferredUsernameRoleClaimsTransformation` looks up the role through `UserRolesRepository` using the `preferred_username` claim.
- `HttpVerbRoleAuthorizationHandler` maps each role to its allowed HTTP verbs: ReadOnly gets GET; ReadWrite gets GET, POST and PUT; Admin gets all verbs.
- When `Security.Active` is false, `BypassOnInactiveAuthorizationMiddlewareResultHandler` lets failed requests through and adds a `Warning` header instead of returning 401/403.
- `/healthcheck` and `/about` are always anonymous.
