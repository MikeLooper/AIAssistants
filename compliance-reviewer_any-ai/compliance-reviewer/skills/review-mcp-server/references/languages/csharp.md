# C# signals — MCP Server

Lookup table for the official C# SDK (NuGet `ModelContextProtocol`; `ModelContextProtocol.AspNetCore` for HTTP;
`ModelContextProtocol.Core` for the low-level API). Signals, not elements: cite the elements in `../standards/`.

| Topic | Signals |
|---|---|
| Detection | `PackageReference Include="ModelContextProtocol*"`; `AddMcpServer()`; `[McpServerToolType]`, `[McpServerTool]`, `[McpServerResourceType]`, `[McpServerPromptType]` |
| Transport | stdio: `.WithStdioServerTransport()`; HTTP: `.WithHttpTransport()` with `app.MapMcp(...)` (then MCP-15 applies, and `review-security-web-api` judges the HTTP pipeline) |
| `stdout` writes (MCP-01) | `Console.Write`/`Console.WriteLine`/`Console.Out.*`; `Host.CreateApplicationBuilder`/`Host.CreateDefaultBuilder` keep a console logger that writes to `stdout` unless it is removed (`builder.Logging.ClearProviders()`) or configured with `AddConsole(o => o.LogToStandardErrorThreshold = LogLevel.Trace)`; Serilog `WriteTo.Console()` without `standardErrorFromLevel`; NLog `ColoredConsole`/`Console` targets without `stdErr="true"` |
| Tool definitions (MCP-04, MCP-05) | Name from `[McpServerTool(Name = "...")]` or the method name; description from `[Description]` on the method and each parameter, and `Title`; server instructions from `options.ServerInstructions`. The input schema is generated from parameter types: `JsonElement`, `JsonNode`, `object`, `Dictionary<string, object>` or `IDictionary` parameters give an untyped schema |
| Validation (MCP-06) | The SDK checks types only. Lengths, ranges, formats and allowlists need explicit checks in the method (or `[MaxLength]`/`[Range]` plus a manual `Validator` call); data annotations alone aren't enforced |
| Annotations (MCP-10) | `[McpServerTool(Destructive = true, ReadOnly = false, Idempotent = ..., OpenWorld = ...)]`; missing properties mean "not stated". Confirmation: `IMcpServer`/`McpServer` elicitation (`ElicitAsync`) or a required `confirm` parameter |
| Errors (MCP-07) | Throwing `McpException` (or a subclass) yields a protocol error with its message; other exceptions become an `IsError = true` result with a generic message. Returning `ex.ToString()`, `ex.StackTrace` or `ex.Message` of an unexpected exception leaks internals. `CallToolResult { IsError = true, Content = [...] }` is the explicit form |
| Credentials (MCP-11) | `Environment.GetEnvironmentVariable`, `IConfiguration` bound from environment or user secrets pass; `const string`/`static readonly string` tokens or keys in `appsettings.json` fail |
| Limits (MCP-13) | `HttpClient` without `Timeout` (default 100 s) or a `CancellationToken` from the tool; `Process.Start` without `WaitForExit(timeout)`; no `System.Threading.RateLimiting` limiter around tool calls |
| Audit (MCP-14) | `ILogger` in tool classes (with a console logger routed to `stderr`) or an SDK request filter that logs tool name, outcome and duration |
