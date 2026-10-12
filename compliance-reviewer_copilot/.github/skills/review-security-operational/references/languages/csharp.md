# Language Guidance — C#/.NET (Security)

Reference: OWASP .NET Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html

- Secrets via `IConfiguration` bound to environment variables, Azure Key Vault, or `dotnet user-secrets` in dev — never in `appsettings.json` committed to source control.
- `ILogger` structured logging with parameterized message templates (`_logger.LogInformation("User {UserId}", id)`), not string-concatenated PII.
- Global exception middleware (`UseExceptionHandler`) returns a generic problem response in production, detailed errors only in Development.
