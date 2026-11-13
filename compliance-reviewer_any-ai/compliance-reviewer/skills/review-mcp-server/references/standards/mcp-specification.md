# Model Context Protocol specification (stdio transport and tools) — localized summary

- Source site: modelcontextprotocol.io (published from GitHub `modelcontextprotocol/modelcontextprotocol`)
- Pinned revision: **2026-07-28**. Pinned pages and commits:
  - `stdio`: `docs/specification/2026-07-28/basic/transports/stdio.mdx` @ b488c16623e5202a3961e551886044577ae0f096 (2026-07-28)
  - `tools`: `docs/specification/2026-07-28/server/tools.mdx` @ 9850cae8923b0ee3d19a4476f1010b97aa161a55 (2026-10-28)
- Citation bases (the Page column picks one):
  - `stdio` → https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio
  - `tools` → https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- Localized: 2026-11-13 · Elements: 17 (cap 100)
- Source name for `Finding.standard`: `MCP Specification 2026-07-28`
- Level is the specification's own keyword (RFC 2119). `REVIEW` marks the specification's non-normative guidance
  (the "Stateful Tools" section and the two error-reporting mechanisms), which takes the owning check's default
  severity. Anchor `(page)` means the rule sits above the page's first heading: cite the page URL with no fragment.
- Only rules a **server** implementer can meet are kept. Client- and host-side rules (consent UI, client timeouts,
  client validation of results) are left out: a reviewed MCP server can't satisfy or fail them.
- SDK-handled framing: when the server uses an official SDK transport (C# `WithStdioServerTransport`, Java
  `StdioServerTransportProvider`, Python `run("stdio")`), MCPS-02, MCPS-03 and MCPS-04 are met by the SDK unless the
  reviewed code bypasses it (writes its own frames, swallows cancellation, blocks shutdown).

| ID | Level | Page | Requirement for the server (summary) | Applies when | Anchor(s) |
|----|-------|------|--------------------------------------|--------------|-----------|
| MCPS-01 | MUST NOT; MAY | stdio | The server writes nothing to `stdout` that is not a valid MCP message. Logging of any kind (informational, debug, error) goes to `stderr` as UTF-8 text (MAY), or to a file or other sink, never to `stdout`. | stdio transport | (page) |
| MCPS-02 | MUST NOT | stdio | Each message is one JSON-RPC message per line, newline-delimited, with no embedded newlines; the server never writes JSON-RPC *requests* to `stdout`. | stdio transport with hand-written framing | (page), receiving-messages |
| MCPS-03 | SHOULD; MUST NOT | stdio | On `notifications/cancelled` the server stops work on that request as soon as practical and sends no further messages for it. | stdio transport; long-running tools | cancellation |
| MCPS-04 | SHOULD | stdio | The server exits promptly when its standard input is closed or a read returns end-of-file; it doesn't keep running detached work that blocks exit. | stdio transport | shutdown |
| MCPS-05 | MUST; MUST NOT | tools | A server exposing tools declares the `tools` capability; `tools/list` returns the tools currently available and doesn't vary per connection or as a side effect of other requests (it MAY vary by the authorization presented on the request). | tools exposed | capabilities |
| MCPS-06 | SHOULD | tools | `tools/list` returns tools in a deterministic order. | tools exposed | capabilities |
| MCPS-07 | SHOULD; SHOULD NOT | tools | Tool names are 1–128 characters, case-sensitive, use only `A-Z a-z 0-9 _ - .`, contain no spaces, commas or other special characters, and are unique within the server. | tools exposed | tool-names |
| MCPS-08 | MUST | tools | Every tool's `inputSchema` is a valid JSON Schema object (never `null`); a tool without parameters uses `{"type":"object","additionalProperties":false}` (recommended). | tools exposed | data-types |
| MCPS-09 | MUST; SHOULD | tools | When a tool declares `outputSchema`, its `structuredContent` conforms to it; a tool returning structured content also returns the serialized JSON in a text block. | tools with `outputSchema` or `structuredContent` | output-schema, structured-content |
| MCPS-10 | SHOULD NOT | tools | Sensitive parameters (passwords, API keys, tokens, personal data) aren't marked with `x-mcp-header`, because header values are visible to intermediaries. | `x-mcp-header` used | x-mcp-header |
| MCPS-11 | REVIEW | tools | State that spans calls uses an explicit handle returned by a creation tool and passed back as an argument, never implicit per-connection state. Handles are opaque; unauthenticated servers generate them with enough entropy (e.g. UUIDv4) and a bounded lifetime that the creation tool's description states; authenticated servers check the caller against the handle on every call; an expired or unknown handle returns a tool execution error that says so. | state kept across tool calls | stateful-tools |
| MCPS-12 | REVIEW | tools | Unknown tools and malformed requests are reported as JSON-RPC protocol errors; API failures, input-validation errors and business-logic errors are reported as tool results with `isError: true` and actionable text the model can use to correct the call. | tools exposed | error-handling |
| MCPS-13 | MUST | tools | The server validates all tool inputs. | tools exposed | security-considerations |
| MCPS-14 | MUST | tools | The server implements proper access controls on what its tools can reach and do. | tools exposed | security-considerations |
| MCPS-15 | MUST | tools | The server rate-limits tool invocations. | tools exposed | security-considerations |
| MCPS-16 | MUST | tools | The server sanitizes tool outputs. | tools exposed | security-considerations |
| MCPS-17 | REVIEW | tools | Tools support a human in the loop who can deny invocations: annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) describe each tool's behaviour accurately, so a host can ask for confirmation. Clients treat annotations as untrusted, so the server never relies on them as its only control. | tools exposed | user-interaction-model, data-types |
