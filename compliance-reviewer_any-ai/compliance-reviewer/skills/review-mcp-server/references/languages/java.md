# Java signals — MCP Server

Lookup table for the official Java SDK (Maven `io.modelcontextprotocol.sdk:mcp` / `mcp-core`, JSON module
`mcp-json-jackson2`/`mcp-json-jackson3`) and Spring AI's MCP server starters. Signals, not elements: cite the
elements in `../standards/`.

| Topic | Signals |
|---|---|
| Detection | `io.modelcontextprotocol.sdk` dependencies; `McpServer.sync(...)`/`McpServer.async(...)`; Spring AI `spring-ai-starter-mcp-server*`, `@McpTool`, `@Tool`, `MethodToolCallbackProvider` |
| Transport | stdio: `new StdioServerTransportProvider(mapper)`; Spring AI `spring.ai.mcp.server.stdio=true`. HTTP: `HttpServletStreamableServerTransportProvider`, `WebMvc*`/`WebFlux*ServerTransportProvider`, `spring-ai-starter-mcp-server-webmvc`/`-webflux` (then MCP-15 applies) |
| `stdout` writes (MCP-01) | `System.out.print*`, `System.out.printf`; Logback `ConsoleAppender` without `<target>System.err</target>` (Spring Boot's default console logging writes to `stdout`); a Spring Boot banner (`spring.main.banner-mode` not `off`) or console log pattern left on for a stdio server; `slf4j-simple` defaults to `stderr` (passes). `e.printStackTrace()` writes to `stderr` (passes MCP-01, but see MCP-07 and SEC-OP-02) |
| Tool definitions (MCP-04, MCP-05) | `McpSchema.Tool.builder().name(..).description(..).inputSchema(mapper, json)`; an `inputSchema` of `{"type":"object"}` with no `properties`, or one that doesn't list the arguments the handler reads, is untyped; server instructions from `.instructions(...)`. Spring AI: `@McpTool(description=...)`, `@McpToolParam` |
| Validation (MCP-06) | Handlers read `request.arguments()` (a `Map<String, Object>`): casts and `toString()` without null, type, length or range checks fail |
| Annotations (MCP-10) | `McpSchema.ToolAnnotations.builder().readOnlyHint(..).destructiveHint(..).idempotentHint(..).openWorldHint(..)`; Spring AI `@McpTool(annotations = @McpTool.McpAnnotations(...))` |
| Errors (MCP-07) | `CallToolResult.builder().isError(true).addTextContent(...)`; text built from `e.toString()`, `e.getMessage()` of an unexpected exception or a `StringWriter` stack trace leaks internals; an error returned without `isError(true)` is reported as success |
| Credentials (MCP-11) | `System.getenv(...)` or Spring `@Value("${...}")` bound from the environment pass; `static final String` tokens or keys in `application.properties` fail |
| Limits (MCP-13) | `HttpClient.newHttpClient()` without `connectTimeout` and per-request `.timeout(...)`; `ProcessBuilder.start()` without `waitFor(timeout, unit)`; no rate limiter (Resilience4j `RateLimiter`, Bucket4j) around tool calls |
| Audit (MCP-14) | SLF4J logger in handlers with a `stderr` appender, logging tool name, outcome and duration |
