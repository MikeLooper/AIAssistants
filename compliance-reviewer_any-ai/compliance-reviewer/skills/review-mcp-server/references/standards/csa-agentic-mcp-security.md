# CSA Agentic MCP Security Best Practices Guide (v1) — localized summary

- Source site: labs.cloudsecurityalliance.org
- Pinned document: "Agentic MCP Security Best Practices Guide", v1, white paper, status **draft**, published
  2026-03-27 (cites MCP specification 2025-11-25). Pinned by content hash in `pins.json`.
- Citation base: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/
- The page exposes no section anchors: cite the base URL with no fragment and name the section (for example
  "§3.6") in `Finding.standard` after the element ID.
- Localized: 2026-11-13 · Elements: 8 (cap 100)
- Source name for `Finding.standard`: `CSA Agentic MCP Security Best Practices`
- Level is the guide's own keyword. The guide is written mainly for organizations, clients and gateways; only
  controls that name or clearly bind the server implementer are kept, restated for the server (G†).
- **Left out:** maturity-model levels as such, message signing (§3.4, Level 3; no SDK supports it), SIEM retention
  periods, SBOM and vulnerability-remediation windows (owned by `review-dependency-management`), and gateway or
  client controls.

| ID | Level | Requirement for the server (summary) | Applies when | Anchor(s) |
|----|-------|--------------------------------------|--------------|-----------|
| CSA-01 | MUST; SHOULD | Every connection to a remote server is authenticated (OAuth 2.1, PKCE for public clients) over TLS 1.2+ with CA-issued certificates; service-to-service connections use mutual authentication. | HTTP transport | §3.1, §3.3 |
| CSA-02 | MUST; SHOULD; SHOULD NOT | (G†) The server runs with only the permissions its documented tools need, doesn't use broad administrative credentials for downstream calls, and scopes access per tool rather than per server. | always | §3.1 |
| CSA-03 | SHOULD | (G†) High-privilege operations need just-in-time re-authorization or explicit confirmation before they run. | high-privilege or destructive tools | §3.1 |
| CSA-04 | SHOULD; MUST | (G†) Tool descriptions are fixed and versioned with the server, so a host can hash or sign them at registration and detect change; the server never rewrites descriptions at run time. | tools exposed | §3.2 |
| CSA-05 | SHOULD | (G†) File-system access is denied by default, with read-only access only to the paths documented tools need; outbound network access is denied by default, with only allowlisted endpoints. | tools touch files or the network | §3.6 |
| CSA-06 | SHOULD | (G†) Each tool execution is bounded: CPU and memory quotas where the runtime allows, and a hard timeout on the work it starts (outbound calls, subprocesses). | tools run outbound calls, subprocesses or heavy work | §3.6 |
| CSA-07 | SHOULD | Every tool invocation is logged with caller or agent identity (when known), tool name, parameters with sensitive values redacted, timestamp, status and duration. | tools exposed | §3.7 |
| CSA-08 | SHOULD | (G†) Credentials are fetched at run time from a secret manager or the platform, not stored in plaintext. | server uses credentials | §3.3 |
