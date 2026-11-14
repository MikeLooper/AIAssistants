---
name: review-mcp-server
description: 'Reviews Model Context Protocol (MCP) server code: the stdio transport contract, tool definitions and descriptions (tool poisoning), input validation, tool errors, output safety, least privilege, destructive-action confirmation, credentials, state handles, limits, audit logging and, for HTTP transports, remote transport security. Localized from the MCP specification (revision 2026-07-28), the MCP security guides, modelcontextprotocol.info and the CSA agentic MCP guide. Use when the compliance-reviewer orchestrator delegates the MCP Server subject. Marked N/A when no MCP server is found.'
user-invocable: false
---

# Review: MCP Server

Checks code that implements a Model Context Protocol server (tools, resources, prompts) in C#, Java or Python against
local, version-pinned summaries of the MCP specification and MCP security guidance. MCP tools are not HTTP API
routes: `review-api-design` doesn't judge them, and for a stdio-only server there is no HTTP surface at all.

## Inputs

The MCP server's entry point and host/transport setup, tool (and resource/prompt) definition files, server
`instructions`, logging configuration, MCP client configuration samples (`.mcp.json`, `mcp.json`, `server.json`) and
the dependency manifest that names the MCP SDK, per `compliance-inventory` (`mcpServers` in `01-inventory.json`). If
the inventory found no MCP server, mark the whole subject N/A with a `notes` explanation; don't fabricate findings.

## Standards (local, authoritative)

- `references/standards/mcp-specification.md` — MCPS-01…MCPS-17. Always load.
- `references/standards/mcp-security-best-practices.md` — MSB-01…MSB-13. Always load.
- `references/standards/mcp-server-best-practices.md` — MBP-01…MBP-10. Always load.
- `references/standards/csa-agentic-mcp-security.md` — CSA-01…CSA-08. Always load.
- `references/standards/thenewstack-mcp-practices.md` — TNS-01…TNS-03. Always load.
- `references/languages/<id>.md` for each detected language (`csharp`, `java`, `python`): SDK signals for the
  transport, `stdout` writes, tool registration, schemas, annotations and errors.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, the standards files and the language files that apply.
2. Identify each MCP server in the file list: its SDK, its transports (stdio, Streamable HTTP, SSE) and its tools,
   resources and prompts. Record them in `notes` (e.g. `mcp: python mcp 2.x, stdio, 7 tools`).
3. Transport scoping: MCP-01 and MCP-02 apply only to stdio servers; MCP-15 applies only when an HTTP transport is
   configured (otherwise N/A, "stdio transport only"). MCP-03 applies to every server.
4. For each check MCP-01…MCP-16, evaluate only the elements it lists whose "Applies when" condition holds; if none
   apply, mark the check N/A with that reason (e.g. MCP-12 when no tool keeps state across calls). Follow the
   evidence notes in `checklist.md`. Evaluate every tool, not a sample: a check fails if any tool fails it, and the
   finding names the tool. An official SDK transport satisfies the framing, cancellation and shutdown parts of
   MCPS-02…MCPS-04 unless the reviewed code bypasses or blocks it.
5. Severity: each Finding takes the failed element's level — MUST/MUST NOT/REQUIRED/SHALL → Error; SHOULD/SHOULD
   NOT/RECOMMENDED → Warning; MAY/OPTIONAL → Information; REVIEW → the check's default. For a merged element with
   mixed levels, use the level of the part that failed. `checkResults.severityIfFailed` is always the check's
   default severity from `checklist.md`.
6. Citations: `standard` = "<source name> — <element ID>" (source name from the standards file header; for CSA and
   The New Stack add the section or item, e.g. "CSA Agentic MCP Security Best Practices — CSA-05 (§3.6)");
   `url` = the citation base for the element's page + "#" + its primary anchor (first anchor listed), or the base
   alone when the anchor is `(page)`, a section number or an item number. `urlsFetched` stays empty.
7. Boundaries: **owned here** — the stdio `stdout` contract, MCP tool schemas and descriptions, `isError`
   semantics, exposure of over-broad tools, MCP annotations and confirmation, handle design, per-invocation
   audit logging and MCP remote-transport rules. **Report also, but don't replace:** injection mechanics in tool
   handlers (path traversal, OS command injection, SSRF, SQL: `review-security-input-injection` SEC-II-01/02/04/10;
   MCP-09 judges only that the tool exposes more than its job needs); hard-coded secrets (`review-security-operational`
   SEC-OP-05 and `review-twelve-factor` TF-03; MCP-11 also fails them); stack traces returned to the client
   (SEC-OP-01; MCP-07 also fails them). **Don't fail here for:** secrets or injection in log *messages*
   (SEC-OP-03/04), log structure, tracing or metrics (`review-observability`), dependency pinning, SBOMs or
   vulnerable SDK versions (`review-dependency-management`), missing tests (`review-testing`), thread safety of
   shared state (`review-reliability`/`review-twelve-factor` TF-06), or code structure (`review-software-quality`).
8. Note strengths where tools are narrowly scoped, schemas are tight, destructive tools ask for confirmation,
   diagnostics go to `stderr`, or credentials come from per-server environment entries.

## Output

Labels: copy `subject`/`subSubject` from `references/checklist.md` (the `Subject:` line and the check's `Sub-subject`
column); never invent or combine labels. Findings, strengths and check results per `compliance-review-core`'s
`finding-schema.md`.
