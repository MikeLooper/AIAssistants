# MCP Security Best Practices and Local Server Security — localized summary

- Source site: modelcontextprotocol.io (published from GitHub `modelcontextprotocol/modelcontextprotocol`)
- Pinned revision: docs for protocol revision **2026-07-28**. Pinned pages and commits:
  - `sbp`: `docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx` @ c713a5485f653cc1da8c2658510862030846d498 (2026-10-30)
  - `lss`: `docs/docs/2026-07-28/tutorials/security/local-server-security.mdx` @ e85b7ae9ee0d4c2b783f523ecf5ac34f6099102e (2026-10-05)
- Citation bases (the Page column picks one):
  - `sbp` → https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
  - `lss` → https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security
- Localized: 2026-11-13 · Elements: 13 (cap 100)
- Source name for `Finding.standard`: `MCP Security Best Practices`
- Level is the page's own keyword. `REVIEW` marks advice without a keyword (the Local Server Security guide is written
  as practical defaults); it takes the owning check's default severity.
- **Kept:** rules an MCP *server* implementer can meet in code or configuration. The local-server guide is written
  for the person who runs a server; its advice is restated as what the server's own code should do (G†), for
  example "grant the narrowest root" becomes "the server confines file access to an explicitly configured root".
- **Left out:** client-only mitigations (consent dialogs, URL-scheme validation, CSP in web clients, mix-up and
  localhost-redirect defences, CIMD trust policies) and fleet governance. A reviewed server can't satisfy them.

| ID | Level | Page | Requirement for the server (summary) | Applies when | Anchor(s) |
|----|-------|------|--------------------------------------|--------------|-----------|
| MSB-01 | MUST | sbp | An MCP proxy server that uses a static client ID with a third-party authorization server keeps per-user consent for each approved `client_id`, checks it before starting the third-party flow, and stores the decision server-side or in a signed, client-bound cookie. | MCP server acting as an OAuth proxy | confused-deputy-problem |
| MSB-02 | MUST | sbp | The proxy's consent page names the client, the scopes and the registered `redirect_uri`, has CSRF protection, can't be framed (`frame-ancestors` or `X-Frame-Options: DENY`), and consent cookies use the `__Host-` prefix, `Secure`, `HttpOnly`, `SameSite=Lax`. | MCP server acting as an OAuth proxy | confused-deputy-problem |
| MSB-03 | MUST | sbp | The proxy matches `redirect_uri` exactly against the registered value (no patterns or wildcards) and rejects a changed URI without re-registration. | MCP server acting as an OAuth proxy | confused-deputy-problem |
| MSB-04 | MUST; MUST NOT | sbp | The OAuth `state` value is cryptographically random, stored server-side only after consent, validated exactly at the callback, single-use and short-lived; no state cookie is set before consent. | MCP server running OAuth flows | confused-deputy-problem |
| MSB-05 | MUST NOT | sbp | The server accepts only tokens issued for itself (audience validated) and never passes a client's token through to a downstream API; downstream calls use the server's own credentials. | server receives or forwards access tokens | token-passthrough |
| MSB-06 | SHOULD | sbp | When the server fetches URLs it learns from metadata or other parties (OAuth discovery, client metadata documents), it requires HTTPS outside loopback development, blocks private, loopback and link-local ranges (with a vetted library, not hand-written IP parsing), validates every redirect hop, and routes such requests through an egress proxy where available. | server or its authorization server fetches discovery or metadata URLs | server-side-request-forgery-ssrf |
| MSB-07 | MUST; MUST NOT; SHOULD | sbp | A server with authorization verifies every inbound request and never treats possession of a state handle as authentication; handles are generated with a secure random generator (never sequential), expire, and are bound server-side to the authenticated user (e.g. stored as `<user_id>:<handle>`). | state handles issued | state-handle-hijacking |
| MSB-08 | SHOULD | sbp | A server meant to run locally uses the stdio transport so only its client can reach it; a local HTTP transport requires an authorization token or uses Unix domain sockets or other access-restricted IPC. | local server | local-mcp-server-compromise |
| MSB-09 | REVIEW | sbp | Scopes follow least privilege: a minimal initial scope set, step-up via precise `WWW-Authenticate` scope challenges, no wildcard or omnibus scopes (`*`, `all`, `full-access`), no full catalog in `scopes_supported`, elevation events logged, and server-side authorization beyond the scopes a token claims. | HTTP transport with OAuth | scope-minimization |
| MSB-10 | REVIEW | lss | Tool names and descriptions are instructions the model reads, so they say only what the tool does: no hidden directives, no instructions unrelated to the tool's job, nothing that steers how the agent uses other tools or servers (tool poisoning or shadowing), and definitions don't change after approval (rug pull). | tools exposed | treat-tool-definitions-as-untrusted-input, threats-this-guide-addresses |
| MSB-11 | REVIEW | lss | (G†) The server reads its credentials per server at run time (its own environment entries or the OS secret store), each narrowly scoped to the one service it needs; no long-lived secret sits in plaintext config or source, and broad personal or account-wide tokens aren't expected. | server uses credentials | isolate-credentials |
| MSB-12 | REVIEW | lss | (G†) File access is confined to a narrow root that is passed in explicitly (configuration or launch argument), never the home directory or the whole file system, and is read-only when the job only reads. A configured allowlist is a cooperative boundary: the server enforces it on every path it opens. | tools read or write files | limit-filesystem-access |
| MSB-13 | REVIEW | lss | (G†) The server talks only to a short, known list of network destinations, and needs no network at all when its job is local; it doesn't open connections to arbitrary hosts. | tools make network calls | control-network-egress |
