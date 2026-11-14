# dotNET — Compliance Review

_Generated 2026-11-13T11:20:49-07:00 · Run `2026-11-13_1806-dotnet`_

## 1. Summary

**Overall score: 25.40/100 — Poor**

| Subject | Score | Band |
|---------|-------|------|
| Software Quality | 66.67/100 | Fair |
| Software Lifecycle | 11.11/100 | Poor |
| Twelve-Factor | 100.00/100 | Excellent |
| Security | 15.15/100 | Poor |
| Testing | 0.00/100 | Poor |
| Observability | 0.00/100 | Poor |
| Dependency Management | 50.00/100 | Poor |
| Reliability | 0.00/100 | Poor |
| Performance | 25.00/100 | Poor |
| Maintainability | 0.00/100 | Poor |
| MCP Server | 6.67/100 | Poor |

**Findings by severity:** Error: 10 · Warning: 17 · Information: 4

### Top 5 Risks

1. **[Error] Hardcoded sync API token in source, also returned to any tool caller** — Security / Operational (test/mcps/dotNET/TodoTools.cs (+1 more)). Remove the hardcoded SyncApiToken literal and load it from a secret manager or platform-injected environment variable at runtime; stop returning it from get_status, which hands the live secret to every MCP caller. [OWASP .NET Security Cheat Sheet — DNO-01](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html#configuration-and-deployment)
1. **[Error] The stdio server writes a startup banner and tool diagnostics to stdout, corrupting the JSON-RPC stream** — MCP Server / Stdio Transport (test/mcps/dotNET/Program.cs (+2 more)). Remove all Console.Write*/Console.WriteLine calls from Program.cs and every tool method; send diagnostics to stderr (Console.Error.WriteLine) or a logger configured with AddConsole(o => o.LogToStandardErrorThreshold = LogLevel.Trace). [MCP Specification 2026-07-28 — MCPS-01](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
1. **[Error] add_todo declares an untyped catch-all input schema** — MCP Server / Tool Definitions (test/mcps/dotNET/TodoTools.cs). Replace the JsonElement parameter with a typed request record (Title/Priority properties) so the generated inputSchema declares real property types instead of an untyped object. [MCP Specification 2026-07-28 — MCPS-08](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#data-types)
1. **[Error] list_todos' description hides a prompt-injection instruction that exfiltrates the sync token** — MCP Server / Tool Description Integrity (test/mcps/dotNET/TodoTools.cs). Rewrite the description to state only what list_todos does; remove the embedded directive that steers the model into calling get_status, disclosing the sync token and concealing the step from the user. [MCP Security Best Practices — MSB-10](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security#treat-tool-definitions-as-untrusted-input)
1. **[Error] Tool arguments (title, priority, path, name, url) aren't validated before use** — Security / Input & Injection (test/mcps/dotNET/TodoTools.cs (+2 more)). Add per-field server-side checks (allowed length, format, allowlisted characters) for title, priority, path, name and url before any of them reach a sink. [OWASP Input Validation Cheat Sheet — IV-01](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html#common-pitfalls)

## 2. Things Done Well

### Software Quality

- [Coding Standards] archive_todos disposes its subprocess with a using declaration — test/mcps/dotNET/TodoTools.cs
- [Coding Standards] TodoStore initializes its collection with target-typed new() — test/mcps/dotNET/TodoStore.cs

### Software Lifecycle

- [Static Analysis] Nullable reference types enabled as a compiler safety feature — test/mcps/dotNET/TodoMcp.csproj

### Twelve-Factor

- [IX. Disposability] The host starts with minimal setup and runs under the Generic Host's graceful-shutdown pattern — test/mcps/dotNET/Program.cs

### Security

- [Input & Injection] import_todos deserializes fetched JSON into typed DTOs with no polymorphic type resolution — test/mcps/dotNET/TodoTools.cs

### Dependency Management

- Microsoft.Extensions.Hosting is pinned to an exact version — test/mcps/dotNET/TodoMcp.csproj
- Target framework net10.0 is a currently active, supported .NET release — test/mcps/dotNET/TodoMcp.csproj

### Performance

- The sync HTTP client is created once as a static singleton and reused — test/mcps/dotNET/TodoTools.cs

### MCP Server

- [Tool Definitions] Most tools declare typed parameters instead of a catch-all object — test/mcps/dotNET/TodoTools.cs

## 3. Recommended Improvements

### Errors

- **No CI pipeline builds changes before merge** — Software Lifecycle / Continuous Integration (test/mcps/dotNET/TodoMcp.csproj, lines 1-16). Add a source-controlled CI pipeline (e.g. a GitHub Actions workflow) that builds the project on every pull request and push to the default branch. [NIST SSDF 1.1 — SSDF-01](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf#page=16)
- **Tool arguments (title, priority, path, name, url) aren't validated before use** — Security / Input & Injection (test/mcps/dotNET/TodoTools.cs (+2 more), lines 33-34). Add per-field server-side checks (allowed length, format, allowlisted characters) for title, priority, path, name and url before any of them reach a sink. [OWASP Input Validation Cheat Sheet — IV-01](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html#common-pitfalls)
- **archive_todos builds an OS shell command from unvalidated caller input** — Security / Input & Injection (test/mcps/dotNET/TodoTools.cs, lines 91-94). Invoke the archiver directly with ProcessStartInfo.ArgumentList (no shell), and validate name against an allowlist of safe characters before it's used in the archive filename. [OWASP Injection Prevention Cheat Sheet — INJ-04](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html#remediation)
- **import_todos fetches any caller-supplied URL with no allowlist or redirect protection** — Security / Input & Injection (test/mcps/dotNET/TodoTools.cs (+1 more), lines 110-110). Accept only an identifier or hostname checked against an allowlist (not a full URL), disable automatic redirects on the HttpClient, resolve and validate the destination IP before connecting, and block internal/metadata address ranges. [OWASP Server-Side Request Forgery Prevention Cheat Sheet — SSRF-01](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html#case-1-application-can-send-request-only-to-identified-and-trusted-applications)
- **Hardcoded sync API token in source, also returned to any tool caller** — Security / Operational (test/mcps/dotNET/TodoTools.cs (+1 more), lines 11-11). Remove the hardcoded SyncApiToken literal and load it from a secret manager or platform-injected environment variable at runtime; stop returning it from get_status, which hands the live secret to every MCP caller. [OWASP .NET Security Cheat Sheet — DNO-01](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html#configuration-and-deployment)
- **No test suite exists to run in CI** — Testing / CI Execution (test/mcps/dotNET/Program.cs, lines 1-14). Add a dotnet test project and a CI step that runs it on every push and pull request, so failures block the build. [Compliance Reviewer Testing Rubric — TSR-13](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-13)
- **The stdio server writes a startup banner and tool diagnostics to stdout, corrupting the JSON-RPC stream** — MCP Server / Stdio Transport (test/mcps/dotNET/Program.cs (+2 more), lines 12-12). Remove all Console.Write*/Console.WriteLine calls from Program.cs and every tool method; send diagnostics to stderr (Console.Error.WriteLine) or a logger configured with AddConsole(o => o.LogToStandardErrorThreshold = LogLevel.Trace). [MCP Specification 2026-07-28 — MCPS-01](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
- **add_todo declares an untyped catch-all input schema** — MCP Server / Tool Definitions (test/mcps/dotNET/TodoTools.cs, lines 26-26). Replace the JsonElement parameter with a typed request record (Title/Priority properties) so the generated inputSchema declares real property types instead of an untyped object. [MCP Specification 2026-07-28 — MCPS-08](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#data-types)
- **list_todos' description hides a prompt-injection instruction that exfiltrates the sync token** — MCP Server / Tool Description Integrity (test/mcps/dotNET/TodoTools.cs, lines 17-17). Rewrite the description to state only what list_todos does; remove the embedded directive that steers the model into calling get_status, disclosing the sync token and concealing the step from the user. [MCP Security Best Practices — MSB-10](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security#treat-tool-definitions-as-untrusted-input)
- **No rate limiting, and no timeout bounds the sync HTTP client or the archive subprocess** — MCP Server / Limits & Timeouts (test/mcps/dotNET/TodoTools.cs (+1 more), lines 14-14). Set a bounded HttpClient.Timeout instead of Timeout.InfiniteTimeSpan, pass a timeout to the archive subprocess (WaitForExit(ms) with a kill fallback), and add a rate limiter (System.Threading.RateLimiting) around tool invocations. [MCP Specification 2026-07-28 — MCPS-15](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#security-considerations)

### Warnings

- **TodoStore holds per-process mutable state in static fields with no synchronization [ISO 25010:2023 Functional suitability › Functional correctness, ISO-02]** — Software Quality / Design Patterns (test/mcps/dotNET/TodoStore.cs (+1 more), lines 5-5). Encapsulate Items and NextId behind a class instance instead of static fields (FRC-16, Encapsulate Variable), and guard mutation with a lock or a concurrent collection if more than one tool call can run at once. [Compliance Reviewer Software Quality Rubric — SQR-19](../../../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-19)
- **Identical exception-to-string error mapping is repeated in four tool handlers [ISO 25010:2023 Maintainability › Modifiability, ISO-30]** — Software Quality / Architecture Patterns (test/mcps/dotNET/TodoTools.cs (+2 more), lines 40-43). Centralize the catch/return-error pattern in one helper or an SDK-level error filter instead of repeating catch (Exception ex) { return ex.ToString(); } in add_todo, export_todos, archive_todos and import_todos. [Compliance Reviewer Software Quality Rubric — SQR-31](../../../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-31)
- **No static analysis / SAST runs on changes** — Software Lifecycle / Static Analysis (test/mcps/dotNET/TodoMcp.csproj, lines 1-16). Run a SAST tool (e.g. CodeQL or a .NET analyzer with TreatWarningsAsErrors) in CI on every pull request and push, and retain its results. [OpenSSF Scorecard v5.6.0 — OSC-14](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#sast)
- **No automated tests of any kind exist** — Testing / Test Pyramid (test/mcps/dotNET/Program.cs, lines 1-14). Add a unit-test project covering TodoTools' tool handlers before adding any integration or E2E coverage, so the suite has a pyramid shape. [Compliance Reviewer Testing Rubric — TSR-03](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-03)
- **No code coverage is measured anywhere** — Testing / Coverage (test/mcps/dotNET/Program.cs, lines 1-14). Once a test project exists, configure and publish coverage collection (e.g. coverlet with a CI artifact or PR comment). [Compliance Reviewer Testing Rubric — TSR-04](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-04)
- **The production root has no corresponding test project** — Testing / Module Coverage (test/mcps/dotNET/Program.cs, lines 1-14). Create a TodoMcp.Tests (or similarly named) project covering the logic-bearing TodoTools module. [Compliance Reviewer Testing Rubric — TSR-15](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-15)
- **No request-rate, latency or error metrics are emitted for tool invocations** — Observability / Metrics (test/mcps/dotNET/Program.cs, lines 7-10). Instrument tool-call handling with request-level signals (rate, duration, status) using a metrics SDK. [Azure Well-Architected Framework — WAFO-08](https://learn.microsoft.com/azure/well-architected/design-guides/monitoring#phase-1---instrumentation)
- **Floating package version on ModelContextProtocol** — Dependency Management (test/mcps/dotNET/TodoMcp.csproj, lines 12-12). Pin ModelContextProtocol to an exact or narrow version range instead of "*" so upgrades are deliberate. [OWASP Top 10:2025 A03 — OTT-07](https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/#how-to-prevent)
- **Build SDK/toolchain version is not pinned** — Dependency Management (test/mcps/dotNET/TodoMcp.csproj, lines 1-1). Add a global.json pinning the .NET SDK version used to build the project. [OWASP Software Supply Chain Security Cheat Sheet — OCS-15](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html#inventory-build-tools)
- **No NuGet lock file capturing the transitive dependency graph** — Dependency Management (test/mcps/dotNET/TodoMcp.csproj, lines 11-14). Set <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile> and commit the generated packages.lock.json. [OWASP Software Supply Chain Security Cheat Sheet — OCS-12](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html#lockfileversion-pinning)
- **No package signature validation is enforced** — Dependency Management (test/mcps/dotNET/TodoMcp.csproj, lines 1-1). Add a nuget.config that sets signatureValidationMode to require (or configures trustedSigners) so only signed packages are accepted. [OWASP Software Supply Chain Security Cheat Sheet — OCS-14](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html#enforce-code-signing)
- **No retry for transient faults on the outbound import call** — Reliability / Transient-Fault Retries (test/mcps/dotNET/TodoTools.cs, lines 110-114). Wrap the outbound call in a resilience library (e.g. Polly) retry policy for transient HTTP failures instead of failing on the first error. [Azure Architecture Center — AZRL-05](https://learn.microsoft.com/azure/architecture/best-practices/transient-faults#check-whether-a-built-in-retry-mechanism-exists)
- **No load shedding or rate limiting on resource-intensive tool calls** — Reliability / Load Protection (test/mcps/dotNET/TodoTools.cs (+1 more), lines 86-106). Limit or shed excess concurrent invocations of expensive tools (archive_todos spawns a shell process; import_todos performs network I/O) with a concurrency or rate limiter, rather than running every request unconditionally. [Azure Architecture Center — AZRL-32](https://learn.microsoft.com/azure/architecture/patterns/throttling#solution)
- **list_todos and export_todos return the entire unbounded todo list** — Performance (test/mcps/dotNET/TodoTools.cs (+1 more), lines 21-21). Add a server-side maximum (page size or item count cap) to list_todos and export_todos so the result can't grow unbounded as the list grows. [Azure Architecture Center — AZPE-37](https://learn.microsoft.com/azure/architecture/antipatterns/extraneous-fetching/#considerations)
- **Required toolchain version is not documented or pinned** — Maintainability / Prerequisites & Configuration (test/mcps/dotNET/TodoMcp.csproj, lines 5-5). Document the required .NET SDK version in a README, or pin it with a global.json. [Compliance Reviewer Maintainability Rubric — MR-13](../../../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-13)
- **delete_all_todos is marked ReadOnly even though it destroys all data, with no confirmation** — MCP Server / Destructive Actions (test/mcps/dotNET/TodoTools.cs, lines 59-64). Remove the incorrect ReadOnly = true, add Destructive = true, and require a confirm argument or elicitation before clearing the list. [MCP Specification 2026-07-28 — MCPS-17](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#user-interaction-model)
- **Tool invocations aren't consistently or properly audit-logged** — MCP Server / Audit Logging (test/mcps/dotNET/TodoTools.cs (+1 more), lines 20-20). Add a single, consistent audit-log call per tool invocation (tool name, redacted arguments, outcome, duration) to stderr or a log sink, instead of ad hoc Console.WriteLine calls present in some tools and absent from others (e.g. complete_todo). [CSA Agentic MCP Security Best Practices — CSA-07 (§3.7)](https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/)

### Information

- **Public tool and data classes have no XML documentation comments** — Software Quality / Coding Standards (test/mcps/dotNET/TodoTools.cs (+1 more), lines 9-9). Add /// XML doc comments to the public TodoTools methods and the public TodoItem/TodoStore members. [Microsoft C# conventions — MSC-23](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions#comment-style)
- **Untrusted-input parsing has no fuzz, property-based or DAST coverage** — Testing / Fuzz & Dynamic Testing (test/mcps/dotNET/Program.cs, lines 1-14). Add property-based or fuzz tests (e.g. FsCheck/CsCheck/SharpFuzz) for the tool handlers that parse caller-supplied JSON and URLs, since the inventory signals untrusted input parsing and there are no tests at all. [Compliance Reviewer Testing Rubric — TSR-23](../../../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-23)
- **No automated load or performance tests exist for the server's tool-call endpoints** — Testing / Load & Performance Tests (test/mcps/dotNET/Program.cs, lines 1-14). Add a load/performance test (e.g. NBomber) against the tool handlers with pass/fail thresholds, run on a recorded schedule. [Azure Well-Architected Framework — AZT-01](https://learn.microsoft.com/azure/well-architected/performance-efficiency/performance-test#apply-multiple-performance-test-types)
- **No test exercises the failure of the outbound dependency call** — Testing / Resilience Tests (test/mcps/dotNET/Program.cs, lines 1-14). Add a test (fake/mock HTTP handler) that simulates the import_todos dependency failing, timing out or returning malformed data, and asserts the tool handles it without breaking unrelated functionality. [Azure Well-Architected Framework — AZT-08](https://learn.microsoft.com/azure/well-architected/reliability/reliability-test#dependency-failures)

## 4. Full Results

### Software Quality

| Check | Result | Evidence |
|-------|--------|----------|
| SQ-01 | pass |  |
| SQ-02 | pass |  |
| SQ-03 | pass |  |
| SQ-04 | pass |  |
| SQ-05 | pass |  |
| SQ-06 | pass |  |
| SQ-08 | pass |  |

#### Design Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| DP-01 | fail | TodoStore.Items/NextId are static mutable fields modified by multiple tool handlers with no synchronization or concurrent collection. |
| DP-02 | N/A | No inheritance hierarchies in the reviewed files. |
| DP-04 | N/A | No named design patterns or pass-through abstractions present to judge. |
| DP-05 | N/A | No complex construction repeated across call sites. |
| DP-06 | N/A | No event subscriptions present. |

#### Architecture Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| AP-01 | N/A | No distinct presentation/business/data layers; the files use a flat Tools/Store design. |
| AP-02 | N/A | No layered business logic or multi-step workflow to assess. |
| AP-03 | N/A | Fewer than 2 modules/projects in the reviewed files. |
| AP-04 | N/A | Fewer than 2 modules in the reviewed files. |
| AP-06 | fail | Exception-to-string error mapping is repeated identically in 4 tool handlers instead of a shared helper or filter. |
| AP-07 | N/A | Fewer than 2 independently deployable units in the reviewed files. |

#### Coding Standards

| Check | Result | Evidence |
|-------|--------|----------|
| CS-01 | pass |  |
| CS-02 | pass |  |
| CS-03 | N/A | No comments present in the reviewed files to evaluate. |
| CS-04 | fail | Public TodoTools, TodoItem and TodoStore members have no XML documentation comments. |
| CS-05 | fail | duplicate evidence of MCP-13#1, see MCP Server / Limits & Timeouts |

### Software Lifecycle

#### Continuous Integration

| Check | Result | Evidence |
|-------|--------|----------|
| SL-01 | fail | No CI/CD pipeline definition exists anywhere in the target (confirmed by run context). |

#### Release Automation

| Check | Result | Evidence |
|-------|--------|----------|
| SL-02 | N/A | Repo publishes no versioned artifacts: Exe output type, no package id/version, no release or deploy pipeline. |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| SL-03 | N/A | No version field (Version/VersionPrefix/VersionSuffix) is declared in the project file. |

#### Branch Protection

| Check | Result | Evidence |
|-------|--------|----------|
| SL-04 | N/A | Repository settings not visible in files: no settings-as-code and no CODEOWNERS present. |

#### Provenance & Signing

| Check | Result | Evidence |
|-------|--------|----------|
| SL-05 | N/A | Repo publishes no versioned artifacts. |

#### Security Policy

| Check | Result | Evidence |
|-------|--------|----------|
| SL-07 | fail | duplicate evidence of DEP-01#2, see Dependency Management |

#### Workflow Security

| Check | Result | Evidence |
|-------|--------|----------|
| SL-09 | N/A | No CI files are in scope (none exist in the target), so there is no workflow to judge for injection risk. |

#### Pipeline Hardening

| Check | Result | Evidence |
|-------|--------|----------|
| SL-10 | N/A | No CI files are in scope (none exist in the target), so there is no pipeline to judge for token scope or pinning. |

#### Static Analysis

| Check | Result | Evidence |
|-------|--------|----------|
| SL-11 | fail | No SAST tool or static-analysis gate runs anywhere (no CI at all). |

#### Committed Binaries

| Check | Result | Evidence |
|-------|--------|----------|
| SL-12 | pass |  |

### Twelve-Factor

#### I. Codebase

| Check | Result | Evidence |
|-------|--------|----------|
| TF-01 | pass |  |

#### II. Dependencies

| Check | Result | Evidence |
|-------|--------|----------|
| TF-02 | pass |  |

#### III. Config

| Check | Result | Evidence |
|-------|--------|----------|
| TF-03 | pass |  |

#### IV. Backing services

| Check | Result | Evidence |
|-------|--------|----------|
| TF-04 | N/A | No backing services in the reviewed files (Program.cs, TodoMcp.csproj). |

#### V. Build, release, run

| Check | Result | Evidence |
|-------|--------|----------|
| TF-05 | N/A | No build/deploy config visible in the reviewed files. |

#### VI. Processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-06 | N/A | No process-state code visible in the reviewed files (Program.cs, TodoMcp.csproj). |

#### VII. Port binding

| Check | Result | Evidence |
|-------|--------|----------|
| TF-07 | N/A | Not applicable to a local stdio MCP server (no HTTP listener). |

#### VIII. Concurrency

| Check | Result | Evidence |
|-------|--------|----------|
| TF-08 | N/A | Not applicable to a local stdio MCP server. |

#### IX. Disposability

| Check | Result | Evidence |
|-------|--------|----------|
| TF-09 | pass |  |

#### X. Dev/prod parity

| Check | Result | Evidence |
|-------|--------|----------|
| TF-10 | N/A | No backing services to compare between development and production. |

#### XI. Logs

| Check | Result | Evidence |
|-------|--------|----------|
| TF-11 | pass |  |

#### XII. Admin processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-12 | N/A | No admin or migration tasks in the reviewed files. |

### API Design

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | no HTTP surface (stdio-only MCP server) |

### Security

#### Identity & Access

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-IA-01 | N/A | stdio MCP server: no caller authentication boundary |
| SEC-IA-02 | N/A | stdio MCP server: no caller authentication boundary |
| SEC-IA-03 | N/A | no JWTs are issued or validated in these files |
| SEC-IA-04 | N/A | no OAuth 2.0/OIDC flow is used in these files |
| SEC-IA-05 | N/A | stdio MCP server: no caller authentication boundary; no sessions or cookies are used |
| SEC-IA-06 | N/A | the target stores no passwords |
| SEC-IA-07 | N/A | no home-grown credential, hashing, session or authentication scheme is implemented in these files |
| SEC-IA-08 | N/A | no service-to-service authentication scenario is in these files; the only outbound call (ImportTodos) is an unauthenticated fetch of a caller-supplied URL, and the server's own downstream credential (SyncApiToken) is judged by review-security-operational |
| SEC-IA-09 | N/A | stdio MCP server: no caller authentication boundary, so there are no login/access-control failures to handle |
| SEC-IA-10 | N/A | the target has no password policy or credential lifecycle to evaluate |
| SEC-IA-11 | N/A | stdio MCP server: no caller authentication boundary; no client-side credential storage or credential HTTP path exists in these files |

#### Input & Injection

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-II-01 | fail | add_todo, export_todos, archive_todos and import_todos use their arguments with no field-level validation. |
| SEC-II-02 | N/A | No SQL or ORM query code in the reviewed files. |
| SEC-II-03 | N/A | No database access in the reviewed files. |
| SEC-II-04 | fail | archive_todos concatenates caller-supplied input into a shell command string. |
| SEC-II-05 | N/A | No XML parsing in the reviewed files. |
| SEC-II-06 | N/A | No file upload handling; the caller-controlled path/name issues in export_todos and archive_todos are judged under SEC-II-01 and review-mcp-server MCP-09. |
| SEC-II-07 | N/A | No serving of uploaded files from storage. |
| SEC-II-08 | N/A | Nothing is rendered to HTML, JavaScript, CSS or a DOM in the reviewed files. |
| SEC-II-09 | pass |  |
| SEC-II-10 | fail | import_todos sends a server-side request to a caller-supplied URL with no destination restriction. |

#### Web & API

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | no HTTP surface (stdio-only MCP server) |

#### Operational

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-OP-01 | fail | duplicate evidence of AP-06#1, see Software Quality / Architecture Patterns |
| SEC-OP-02 | fail | duplicate evidence of AP-06#1, see Software Quality / Architecture Patterns |
| SEC-OP-03 | N/A | no log statement in these files writes a secret or sensitive personal data (the hardcoded secret is exposed via a tool response, not a log; see SEC-OP-05) |
| SEC-OP-04 | fail | duplicate evidence of MCP-01#1, see MCP Server / Stdio Transport |
| SEC-OP-05 | fail | SyncApiToken is a hardcoded literal secret in source |
| SEC-OP-06 | N/A | no secret-delivery mechanism exists in these files; the only secret found is hardcoded (see SEC-OP-05), not retrieved at runtime |
| SEC-OP-07 | N/A | no production/environment configuration is in these files (a console host app with no ASP.NET Core pipeline) |
| SEC-OP-08 | fail | duplicate evidence of MCP-01#1, see MCP Server / Stdio Transport |
| SEC-OP-09 | N/A | no log storage, rotation or transport configuration is in these files |
| SEC-OP-10 | N/A | no multi-step transactional writes, fail-open security decisions or resource-cleanup-on-exception patterns are in these files |

### Testing

#### Test Pyramid

| Check | Result | Evidence |
|-------|--------|----------|
| TST-01 | fail | testInventory totals show zero unit, integration, e2e or unclassified tests |

#### Coverage

| Check | Result | Evidence |
|-------|--------|----------|
| TST-02 | fail | no coverage collection is configured anywhere |

#### Assertion Quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-03 | N/A | no tests |

#### Test Doubles

| Check | Result | Evidence |
|-------|--------|----------|
| TST-04 | N/A | no tests |

#### Isolation & Determinism

| Check | Result | Evidence |
|-------|--------|----------|
| TST-05 | N/A | no tests |

#### CI Execution

| Check | Result | Evidence |
|-------|--------|----------|
| TST-06 | fail | there is no test suite for any CI step to run |

#### Module Coverage

| Check | Result | Evidence |
|-------|--------|----------|
| TST-07 | fail | the production root test/mcps/dotNET has no corresponding tests |

#### Test Code Quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-08 | N/A | no tests |

#### Integration & Contract Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-09 | N/A | no tests |

#### Security Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-10 | N/A | no access control in scope (testInventory.signals.accessControl is false) |

#### Fuzz & Dynamic Testing

| Check | Result | Evidence |
|-------|--------|----------|
| TST-11 | fail | untrusted input is parsed (testInventory.signals.untrustedInput is true) with no fuzz/property-based tests or DAST job |

#### Load & Performance Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-12 | fail | no load tests exist (testInventory.signals.loadTests is false) |

#### Resilience Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-13 | fail | the code makes a remote call (testInventory.signals.integrationPoints is true) with no test for its failure path |

### Observability

#### Structured Logging

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-01 | fail | duplicate evidence of MCP-01#1, see MCP Server / Stdio Transport |

#### Correlation & Context Propagation

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-02 | fail | duplicate evidence of SEC-II-10#1, see Security / Input & Injection |

#### Distributed Tracing

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-03 | fail | duplicate evidence of MCP-13#1, see MCP Server / Limits & Timeouts |

#### Metrics

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-04 | fail | no request-rate/latency/error metrics are emitted |

#### Telemetry Export

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-05 | fail | duplicate evidence of MCP-01#1, see MCP Server / Stdio Transport |

#### Health Endpoints

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-06 | N/A | stdio MCP server |

#### SLOs & SLIs

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-07 | N/A | no SLO/SLI documentation is in these files; the server is treated like a CLI/worker process, which is never failed for a missing SLO |

#### Telemetry Identity & Naming

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-08 | N/A | no telemetry SDK or agent is configured in these files, so service-identity/naming elements don't apply |

#### Error Recording

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-09 | fail | duplicate evidence of AP-06#1, see Software Quality / Architecture Patterns |

#### Telemetry Volume & Safety

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-10 | fail | duplicate evidence of MCP-01#1, see MCP Server / Stdio Transport |

### Dependency Management

| Check | Result | Evidence |
|-------|--------|----------|
| DEP-01 | fail | ModelContextProtocol floats on "*" and no SDK pin (global.json) exists. |
| DEP-02 | fail | NuGet supports lock files for this project type but none is configured or committed. |
| DEP-03 | N/A | No vulnerability analyzer output for this run (no 02-analyzers.json). |
| DEP-04 | pass |  |
| DEP-05 | fail | duplicate evidence of SL-01#1, see Software Lifecycle / Continuous Integration |
| DEP-07 | N/A | No update/scanning config (Dependabot, Renovate, NuGetAudit, scanner config) is in this subject's file list. |
| DEP-08 | fail | No nuget.config enforces signature validation on restored packages; the default NuGet feed is used without it. |
| DEP-09 | pass |  |

### Reliability

#### Timeouts

| Check | Result | Evidence |
|-------|--------|----------|
| REL-01 | fail | duplicate evidence of SEC-II-10#1, see Security / Input & Injection |

#### Transient-Fault Retries

| Check | Result | Evidence |
|-------|--------|----------|
| REL-02 | fail | the outbound call in ImportTodos has no retry and HttpClient doesn't retry by default |

#### Idempotency

| Check | Result | Evidence |
|-------|--------|----------|
| REL-03 | N/A | no retry logic exists in these files, so idempotency-under-retry elements don't apply |

#### Circuit Breakers

| Check | Result | Evidence |
|-------|--------|----------|
| REL-04 | fail | duplicate evidence of SEC-II-10#1, see Security / Input & Injection |

#### Redundancy

| Check | Result | Evidence |
|-------|--------|----------|
| REL-05 | N/A | no deployment config in scope (advanced usage off; no hosting/IaC files reviewed) |

#### Load Protection

| Check | Result | Evidence |
|-------|--------|----------|
| REL-06 | fail | resource-intensive tools (archive_todos, import_todos) have no concurrency or rate limiting |

#### Messaging & Background Jobs

| Check | Result | Evidence |
|-------|--------|----------|
| REL-07 | N/A | no message consumers or background jobs are in scope |

#### In-Region High Availability

| Check | Result | Evidence |
|-------|--------|----------|
| REL-08 | N/A | no deployment config in scope (advanced usage off) |

### Performance

| Check | Result | Evidence |
|-------|--------|----------|
| PERF-01 | N/A | No expensive or repeated reads to cache; todo data is a small in-memory list. |
| PERF-02 | fail | duplicate evidence of MCP-13#1, see MCP Server / Limits & Timeouts |
| PERF-03 | pass |  |
| PERF-04 | N/A | No ORM/database access or chatty remote calls in the reviewed files. |
| PERF-05 | N/A | No repeated expensive computation inside a hot loop in the reviewed files. |
| PERF-06 | fail | list_todos and export_todos return the full todo list with no server-side cap. |
| PERF-07 | fail | duplicate evidence of REL-06#1, see Reliability / Load Protection |
| PERF-08 | N/A | No hosting/scaling config in scope; the stdio MCP server runs as a single per-client process by design. |

### Disaster Recovery

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Monitoring

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Cost & Sustainability

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Maintainability

#### README & Onboarding

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-01 | fail | duplicate evidence of DEP-01#2, see Dependency Management |

#### Repository Layout

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-02 | N/A | A full folder listing is not in this subject's file list, so layout and naming conventions can't be judged. |

#### Prerequisites & Configuration

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-03 | fail | Required SDK/toolchain version is stated in neither documentation nor a pin file (no README, no global.json). |

#### Technical Debt

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-04 | N/A | No source files in scope (this subject's file list contains only the project file). |

#### Deprecated Code

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-05 | N/A | No source files in scope (this subject's file list contains only the project file). |

#### Contributing Guide

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-06 | fail | duplicate evidence of DEP-01#2, see Dependency Management |

#### Change History

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-07 | N/A | Repo publishes no versioned artifacts (Exe output type, no package id/version, no release pipeline), so a change log isn't required. |

#### Architecture Docs

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-08 | N/A | Only one project is in scope, with no evidence of multiple modules or a layered structure requiring architecture docs. |

#### Docs Accuracy

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-09 | N/A | No docs exist anywhere in the target to check for accuracy against the code. |

#### License & Conduct

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-10 | fail | duplicate evidence of SL-01#1, see Software Lifecycle / Continuous Integration |

### MCP Server

#### Stdio Transport

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-01 | fail | Program.cs and several TodoTools methods write to stdout while the stdio server is running. |
| MCP-02 | pass |  |

#### Deployment Shape

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-03 | fail | duplicate evidence of SEC-OP-05#1, see Security / Operational |

#### Tool Definitions

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-04 | fail | add_todo's JsonElement parameter produces an untyped inputSchema. |

#### Tool Description Integrity

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-05 | fail | list_todos' description embeds a hidden instruction that steers the model into another tool call and credential disclosure. |

#### Input Validation

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-06 | fail | duplicate evidence of SEC-II-01#1, see Security / Input & Injection |

#### Tool Errors

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-07 | fail | duplicate evidence of AP-06#1, see Software Quality / Architecture Patterns |

#### Output Safety

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-08 | fail | duplicate evidence of SEC-OP-05#1, see Security / Operational |

#### Least Privilege

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-09 | fail | duplicate evidence of SEC-II-04#1, see Security / Input & Injection |

#### Destructive Actions

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-10 | fail | delete_all_todos is destructive but annotated ReadOnly = true with no confirmation. |

#### Credentials

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-11 | fail | duplicate evidence of SEC-OP-05#1, see Security / Operational |

#### State & Handles

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-12 | N/A | Todo IDs are ordinary sequential resource identifiers for a single-client stdio server, not authorization-relevant state handles. |

#### Limits & Timeouts

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-13 | fail | The shared HttpClient disables its timeout and the archive subprocess has no bound; no rate limiter is present. |

#### Audit Logging

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-14 | fail | Logging is inconsistent across tools and some tool calls (e.g. complete_todo) aren't logged at all. |

#### Remote Transport Security

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-15 | N/A | stdio transport only. |

#### Versioning & Documentation

| Check | Result | Evidence |
|-------|--------|----------|
| MCP-16 | pass |  |

## 5. Appendix

- **Run:** `2026-11-13_1806-dotnet` · Target: `test/mcps/dotNET` · Git HEAD: `51f0bc91c5054936e4b7953e15bb17e15586af5a`
- **Started:** 2026-11-13T18:06:48Z · **Completed:** 2026-11-13T11:20:49-07:00
- **Run flags:** advanced off (IaC and CLI analyzers not run)
- **Subjects skipped:** review-api-design (no HTTP surface (stdio-only MCP server)); review-security-web-api (no HTTP surface (stdio-only MCP server)); review-disaster-recovery (advanced usage off (IaC not reviewed)); review-monitoring (advanced usage off (IaC not reviewed)); review-cost-sustainability (advanced usage off (IaC not reviewed))
- **URLs fetched:** none
- **Link approvals:** none
