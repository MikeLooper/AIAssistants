# Detection signals — C#/.NET (Security: Operational)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only on concrete code or an explicit setting (`SKILL.md` step 4). The only .NET
defaults a worker may rely on are those stated in `dotnet-operational.md` (DNO-06, DNO-07, DNO-10, DNO-11, DNO-12,
DNO-14). Serilog, NLog and log4net defaults are not localized: report explicit values only, and add a
`localized-standard-gap` note for a missing setting.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `app.UseDeveloperExceptionPage()` outside `if (app.Environment.IsDevelopment())` | `Program.cs`, `Startup.cs` | Developer page outside Development (always Error) | DNO-06, ERR-04 |
| `ASPNETCORE_ENVIRONMENT`/`DOTNET_ENVIRONMENT` = `Development` | Dockerfile, compose, Kubernetes manifests, App Service settings, pipeline YAML | Production running as Development | DNO-03, DNO-07 |
| `<customErrors mode="Off">` | `web.config` | Detailed errors for remote users | ERR-04 |
| No `UseExceptionHandler` in the non-Development branch; `UseExceptionHandler()` with no path, lambda or `AddProblemDetails()` | `Program.cs`, `Startup.cs` | No global generic handler | DNO-04, DNO-08, ERR-01 |
| `AddExceptionHandler<T>()` without `UseExceptionHandler()` | `Program.cs` | Registered handler never runs | DNO-08 |
| `IExceptionHandlerFeature.Error.Message`/`.StackTrace`, `ex.ToString()` written to the response or `ProblemDetails.Detail` | handlers, middleware, filters, controllers | Error details sent to clients | DNO-09, ERR-02 |
| `TryHandleAsync` returning `true` without a logger call; `SuppressDiagnosticsCallback` returning `true` broadly | `IExceptionHandler` classes, `Program.cs` | Handled exceptions not logged (.NET 10 default) | DNO-10 |
| Empty `catch { }`, `catch (Exception) { return null; }` without logging | any code | Swallowed errors | A10-07, LOG-02 |
| `.NET Framework` `WebApiConfig` without `IExceptionLogger` and `IExceptionHandler` replaced | `App_Start/WebApiConfig.cs` | No global Web API handler | ERR-06 |
| `_logger.Log*($"…{x}…")` or `"…" + x` templates; CA2254 suppressed | any code, `.editorconfig`, `GlobalSuppressions.cs` | Non-constant templates | DNO-16, LOG-17 |
| `AddHttpLogging(o => o.LoggingFields = HttpLoggingFields.All \| RequestBody …)`; `RequestHeaders.Add("Authorization"\|"Cookie")` | `Program.cs` | Sensitive headers/bodies in HTTP logs | DNO-14 |
| Passwords, tokens, `ConnectionString`, `Authorization` values, whole request/user objects passed to logger calls | any code | Secrets or sensitive data in logs | LOG-12, LOG-13 |
| `[DataClassification]`/sensitive attributes present but no `AddRedaction` | models, `Program.cs` | Sensitive fields logged without redaction | DNO-15 |
| `Password=`, `AccountKey=`, `ClientSecret`, `ApiKey` with real values | `appsettings*.json`, `web.config` `connectionStrings`, code | Hardcoded secrets | DNO-01, SMG-01 |
| `AddUserSecrets` outside Development; Secret Manager or `secrets.json` referenced for production | `Program.cs`, deployment docs/scripts | Development-only store in production | DNO-02, DNO-12 |
| Secret-store or cloud credentials in config: `ClientSecretCredential`/client secrets (Azure Key Vault), `AWSAccessKeyId`/`aws_secret_access_key` or `BasicAWSCredentials` (AWS Secrets Manager), Vault tokens/AppRole secret IDs (HashiCorp Vault) | `Program.cs`, `appsettings*.json` | Secret-zero in config instead of a workload identity | DNO-13 |
| `PersistKeysTo*` (e.g. `PersistKeysToFileSystem`, `PersistKeysToDbContext`, `PersistKeysToStackExchangeRedis`, `PersistKeysToAzureBlobStorage`, `PersistKeysToAWSSystemsManager`) without `ProtectKeysWith*` | `Program.cs` | Unprotected Data Protection keys | DNO-05 |
| `http://` secret-store URLs (Key Vault, Secrets Manager, Vault, …); certificate validation disabled for them | config, `Program.cs` | Secrets in plaintext transit | SMG-11 |
| Serilog/NLog file sinks under `wwwroot`; no `fileSizeLimitBytes`/`rollingInterval`/`retainedFileCountLimit`/archive limits (explicit values only) | `appsettings*.json` `Serilog`, `nlog.config` | Web-accessible or unbounded log files | LOG-22, LOG-21 |
| Minimum level `None`/`Off` for the app or security categories in production config | `appsettings.Production.json` `Logging`, `Serilog` | Logging deactivated | LOG-19 |
| Security events written with `Console.WriteLine`/`Debug.WriteLine` | admin, export, startup code | Not using the logging framework | LOG-11 |
| User-admin, role-change, export or import endpoints with no logger call | controllers, minimal-API endpoints | Higher-risk functions not logged | LOG-04 |
| Catch blocks in authorization handlers or policy code that `return true`/`context.Succeed` on exception | `IAuthorizationHandler`, filters | Fail open | A10-05 |
| Several `SaveChanges`/repository writes without `BeginTransaction`/a single unit of work | services, repositories | No rollback for part-way writes | A10-03, SCR-03 |
| `Stream`/`SqlConnection`/`SemaphoreSlim` without `using`/`finally` | any code | Resources not released on exceptions | A10-06 |
