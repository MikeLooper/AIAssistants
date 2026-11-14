# 15 Best Practices for Building MCP Servers in Production (The New Stack) — partial localized summary

- Source site: thenewstack.io
- Pinned article: "15 Best Practices for Building MCP Servers in Production", published 2025-09-15.
- Citation base: https://thenewstack.io/15-best-practices-for-building-mcp-servers-in-production/
- The article has no stable section anchors: cite the base URL with no fragment and name the item number (for
  example "item 15") in `Finding.standard` after the element ID.
- Localized: 2026-11-13 · Elements: 3 (cap 100) · **Partial:** the site refused automated retrieval (HTTP 403) when
  this file was written, so only the three items whose text could be confirmed are kept. Every other topic the
  article covers is already covered by the specification and the three other sources. `MAINTENANCE.md` records the
  manual follow-up.
- Source name for `Finding.standard`: `The New Stack — MCP Servers in Production`
- Level: every element is `REVIEW` (the article uses no normative keywords); it takes the owning check's default
  severity.

| ID | Level | Requirement for the server (summary) | Applies when | Anchor(s) |
|----|-------|--------------------------------------|--------------|-----------|
| TNS-01 | REVIEW | Each server is a bounded context: one coherent domain with a small set of purpose-built tools, not a general-purpose gateway to the host. | always | item 1 |
| TNS-02 | REVIEW | The server versions its surface area and advertises its capabilities accurately (server name and version, declared capabilities that match what it implements). | always | item 8 |
| TNS-03 | REVIEW | Actions that change state or spend money require confirmation, for example through elicitation or a dry-run mode that previews the change before it runs; the risks are documented. | state-changing or spending tools | item 15 |
