# Checklist — MCP Server

Subject: MCP Server

Each check is evaluated only against the elements it lists, in the local files under `standards/`; every element
belongs to exactly one check. A Finding's severity comes from the failed element's level (see `../SKILL.md`);
`severityIfFailed` is always the check's default severity below.

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|------------------|----------|--------|
| MCP-01 | Stdio Transport | A stdio server writes only MCP messages to `stdout`: no `print`/`Console.WriteLine`/`System.out` output, banners or console loggers on `stdout`; logs and diagnostics go to `stderr` or another sink | Error | MCPS-01, MCPS-02 | mcp-specification.md |
| MCP-02 | Stdio Transport | The server honours cancellation and exits promptly when `stdin` closes | Warning | MCPS-03, MCPS-04 | mcp-specification.md |
| MCP-03 | Deployment Shape | The transport fits the deployment: a local single-user server uses stdio with credentials from its environment; a local HTTP server binds to loopback, validates `Origin` and requires a token or restricted IPC | Warning | MSB-08, MBP-01 | mcp-security-best-practices.md, mcp-server-best-practices.md |
| MCP-04 | Tool Definitions | Tools have valid, unique names, a typed `inputSchema` object (no `null`, no untyped catch-all objects), structured results that match any `outputSchema`, and a `tools/list` that is static per connection and deterministic | Warning | MCPS-05…09, MBP-06 | mcp-specification.md, mcp-server-best-practices.md |
| MCP-05 | Tool Description Integrity | Tool names, titles, descriptions and server instructions describe only what each tool does: no hidden directives, requests for unrelated data, steering of other tools or servers, or text that changes at run time | Error | MSB-10, CSA-04, MBP-09 | mcp-security-best-practices.md, csa-agentic-mcp-security.md, mcp-server-best-practices.md |
| MCP-06 | Input Validation | Every tool validates its arguments server-side (type, length, range, format, allowlists) before using them, not only through the advertised schema | Error | MCPS-13, MBP-04 | mcp-specification.md, mcp-server-best-practices.md |
| MCP-07 | Tool Errors | Validation and business failures are returned as `isError` results with actionable text; unknown tools and malformed requests are protocol errors; no stack traces or internal details reach the model | Warning | MCPS-12, MBP-07 | mcp-specification.md, mcp-server-best-practices.md |
| MCP-08 | Output Safety | Tool outputs are sanitized: no secrets, credentials or internal configuration in results, and content from untrusted sources is bounded and marked as data | Error | MCPS-16 | mcp-specification.md |
| MCP-09 | Least Privilege | The server is a bounded context with least privilege: no general-purpose shell, eval, SQL, any-file or any-URL tools; file access confined to a configured root; network limited to known destinations | Error | MCPS-14, MSB-12, MSB-13, CSA-02, CSA-05, TNS-01 | mcp-specification.md, mcp-security-best-practices.md, csa-agentic-mcp-security.md, thenewstack-mcp-practices.md |
| MCP-10 | Destructive Actions | Destructive, state-changing or spending tools carry accurate annotations and require explicit confirmation (a confirm argument, elicitation or a dry run) | Warning | MCPS-17, CSA-03, TNS-03 | mcp-specification.md, csa-agentic-mcp-security.md, thenewstack-mcp-practices.md |
| MCP-11 | Credentials | Credentials come from the environment or a secret store at run time, are scoped to one service, are never hard-coded, returned in results, put in `x-mcp-header` or passed through to downstream APIs | Error | MSB-05, MSB-11, MCPS-10, MBP-08, CSA-08 | mcp-security-best-practices.md, mcp-specification.md, mcp-server-best-practices.md, csa-agentic-mcp-security.md |
| MCP-12 | State & Handles | Tools don't rely on connection or process state; state across calls uses opaque, random, expiring handles bound to the caller | Warning | MCPS-11, MSB-07, MBP-02 | mcp-specification.md, mcp-security-best-practices.md, mcp-server-best-practices.md |
| MCP-13 | Limits & Timeouts | Tool invocations are rate-limited, and the work a tool starts (outbound calls, subprocesses, large reads) has timeouts and size bounds | Warning | MCPS-15, CSA-06 | mcp-specification.md, csa-agentic-mcp-security.md |
| MCP-14 | Audit Logging | Each tool invocation is logged (tool, redacted arguments, outcome, duration) to `stderr` or a log sink | Warning | CSA-07 | csa-agentic-mcp-security.md |
| MCP-15 | Remote Transport Security | HTTP transports only: `Origin` and protocol-header validation, OAuth resource-server token and audience checks, no token passthrough, minimal scopes, and proxy consent, `state` and `redirect_uri` protections | Error | MBP-03, MBP-05, MSB-01…04, MSB-06, MSB-09, CSA-01 | mcp-server-best-practices.md, mcp-security-best-practices.md, csa-agentic-mcp-security.md |
| MCP-16 | Versioning & Documentation | The server declares its name, version and accurate capabilities, and documents its deployment shape, transport and authorization model | Information | MBP-10, TNS-02 | mcp-server-best-practices.md, thenewstack-mcp-practices.md |

Totals: 17 MCPS + 13 MSB + 10 MBP + 8 CSA + 3 TNS = 51 elements across 16 checks.

## Evidence notes

- **MCP-01:** fail on any code path reachable while the stdio server runs that writes to `stdout`: `print(...)`
  without `file=sys.stderr`, `sys.stdout.write`, a `logging` handler on `sys.stdout`, `Console.Write*`/`Console.Out`,
  a .NET console logger without `LogToStandardErrorThreshold = LogLevel.Trace`, `System.out.print*`, a Logback
  `ConsoleAppender` without `<target>System.err</target>`, or a Spring Boot banner or console log pattern left on.
  The language files list the patterns. Writes in a separate CLI entry point that never starts the server pass.
- **MCP-05:** quote the offending description text in the excerpt. A description that tells the model to read
  credentials, call another tool first, hide actions from the user or ignore earlier instructions fails with
  confidence High.
- **MCP-06 vs MCP-04:** an untyped catch-all argument (`dict`, `Dictionary<string, object>`, `JsonElement`,
  `{"type":"object"}` with no properties) fails MCP-04 (schema); using its contents without checks fails MCP-06.
- **MCP-09:** judge the exposed capability, not the injection mechanics: a tool that writes or reads any
  caller-supplied path, runs a caller-influenced shell command or fetches any caller-supplied URL fails here.
  The injection itself is also reported by `review-security-input-injection` (SEC-II-01, SEC-II-04, SEC-II-10).
- **MCP-10:** a destructive tool with no annotations, with `readOnlyHint: true` or with `destructiveHint: false`
  fails, and so does one that runs without a confirmation argument, elicitation or dry-run path.
- **MCP-15:** N/A ("stdio transport only") unless an HTTP transport is configured.
