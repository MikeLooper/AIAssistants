# MCP Server Best Practices — Transport, Security and Tool Design (modelcontextprotocol.info) — localized summary

- Source site: modelcontextprotocol.info
- Pinned page: `docs/best-practices/` (written for protocol revision 2026-07-28, experiments on Python SDK 2.3.0;
  the page shows no publication or last-updated date). Pinned by content hash in `pins.json`.
- Citation base: https://modelcontextprotocol.info/docs/best-practices/
- Localized: 2026-11-13 · Elements: 10 (cap 100)
- Source name for `Finding.standard`: `MCP Server Best Practices`
- Level is the page's own keyword; `REVIEW` marks its unkeyworded guidance, which takes the owning check's default
  severity. Where a row repeats a specification rule, the specification (`mcp-specification.md`) is cited first.
- **Left out:** the HTTP probe script and its rows (section 6) and testing advice: tests are judged by
  `review-testing`; failure-mode tips (section 5) are folded into the rows they explain.

| ID | Level | Requirement for the server (summary) | Applies when | Anchor(s) |
|----|-------|--------------------------------------|--------------|-----------|
| MBP-01 | SHOULD NOT; REVIEW | The deployment shape matches the transport: a single user on the same machine uses stdio and reads credentials from the environment (stdio servers don't implement the HTTP authorization spec); a local HTTP server binds to `127.0.0.1`, validates `Origin` and requires a token or restricted IPC; a shared server uses Streamable HTTP as an OAuth 2.1 resource server. | always | 1-pick-the-deployment-shape-first |
| MBP-02 | MUST NOT; SHOULD | The server doesn't rely on earlier requests on the same connection or on the process lifetime: cross-request state lives behind opaque, random, expiring handles bound to the user and stored under a user-scoped key, not keyed on connection, process or `Mcp-Session-Id`. | state kept across requests | 2-make-the-server-stateless-on-purpose |
| MBP-03 | MUST | A remote server implements `server/discover`, validates `Origin` (403 when invalid), rejects missing or mismatched `Mcp-Method`/`Mcp-Name`/`MCP-Protocol-Version` headers (400, `-32020`) and unsupported versions (400, `-32022` with the supported list), and answers unknown methods with 404/`-32601`. | Streamable HTTP transport | 3-the-rules-a-remote-server-must-pass, which-requests-carry-which-headers |
| MBP-04 | MUST | Tool inputs are validated, access control is enforced, invocations are rate-limited and outputs are sanitized (restates MCPS-13 … MCPS-16; cite those first). | tools exposed | 3-the-rules-a-remote-server-must-pass |
| MBP-05 | MUST; MUST NOT; SHOULD | A protected server serves Protected Resource Metadata with at least one `authorization_servers` entry, validates access tokens and their audience (401 when invalid, expired or wrong-audience), never accepts or passes through tokens issued for another resource, and answers insufficient scope with one 403 `insufficient_scope` challenge listing every scope needed. | HTTP transport with authorization | 3-the-rules-a-remote-server-must-pass, 5-failure-modes-and-recovery |
| MBP-06 | MUST; SHOULD | Tool definitions follow the tool rules: valid names, a non-null `inputSchema` (`additionalProperties: false` for parameterless tools), conforming structured results plus a JSON text block, and a `tools/list` that doesn't vary per connection and is sorted deterministically. | tools exposed | 4-define-tools-so-the-model-can-recover |
| MBP-07 | REVIEW | Validation and business-rule failures are returned as `isError: true` results that name the field that was wrong and the values that are valid, not as protocol errors or vague text, so the model doesn't repeat the bad call. | tools exposed | 4-define-tools-so-the-model-can-recover, 5-failure-modes-and-recovery |
| MBP-08 | SHOULD NOT; REVIEW | Secrets and personal data aren't marked with `x-mcp-header`, and annotations aren't relied on as a security control: the server enforces its own checks whatever the annotations say. | tools exposed | 4-define-tools-so-the-model-can-recover |
| MBP-09 | REVIEW | Guidance that spans tools goes in the server `instructions`, not in one tool's description. | more than one tool | 4-define-tools-so-the-model-can-recover |
| MBP-10 | REVIEW | The deployment-shape decision and its rationale are recorded (README or design notes), with the transport, the authorization model and where state lives. | always | 7-before-you-ship |
