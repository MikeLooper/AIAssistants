# Maintenance — MCP Server localized standards

**Maintainers only. Workers never load this file.**

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| modelcontextprotocol.io | mcp-specification.md, mcp-security-best-practices.md | 17 + 13 = 30 | 100 | Two files, one website: the cap counts both |
| modelcontextprotocol.info | mcp-server-best-practices.md | 10 | 100 | — |
| labs.cloudsecurityalliance.org | csa-agentic-mcp-security.md | 8 | 100 | Source is a v1 **draft**; re-check for a final version |
| thenewstack.io | thenewstack-mcp-practices.md | 3 | 100 | **Partial** (DEC-2) |

## Decisions

- **DEC-1 (2026-11-13): one new subject, shared pipeline.** MCP servers are reviewed by a new subject,
  `review-mcp-server` (step 28), not by `review-api-design`: MCP tools are JSON-RPC operations described by JSON
  Schema, not HTTP resources, and the stdio transport has no HTTP surface. Every other subject still reviews an MCP
  server as ordinary code. The inventory records `mcpServers` and `httpSurfaceFound`; with no HTTP surface,
  `review-api-design` and `review-security-web-api` are N/A for the run.
- **DEC-2 (2026-11-13): The New Stack is partial.** thenewstack.io returned HTTP 403 to automated retrieval, and the
  page wasn't fetched by other means. Only items 1, 8 and 15, whose text was confirmed from search-result excerpts,
  were localized. Everything else the article covers is already covered by the specification and the other three
  sources. Complete the file by hand (pins.json `thenewstack-article`); keep IDs TNS-01…03 and add new ones after them.
- **DEC-3 (2026-11-13): server-side rules only.** Client, host and fleet-governance rules (consent dialogs, URL-scheme
  checks, client timeouts and validation, mix-up defences, CIMD trust policies, install-time provenance) are left
  out because a reviewed server can't meet or fail them. Advice written for the operator of a local server
  (Local Server Security) is restated as what the server's own code should do and marked `(G†)`.
- **DEC-4 (2026-11-13): HTTP transport kept but untested.** MCP-15 and the HTTP rows (MBP-03, MBP-05, MSB-01…04,
  MSB-06, MSB-09, CSA-01) are localized so an HTTP server isn't silently passed, but the test apps under
  `test/mcps/` cover stdio only. Add an HTTP test app before relying on MCP-15 results.

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID.
- Level is the source's own keyword, verbatim (or `REVIEW` for unkeyworded guidance). Merged elements list each level.
- Primary anchor first. CSA and The New Stack have no anchors: record the section or item number instead.
- Every active element must be listed by exactly one check in `../checklist.md`.
- Don't add elements for injection mechanics (`review-security-input-injection`), secrets or injection in log
  messages (`review-security-operational`), log structure or telemetry (`review-observability`), dependency pinning
  or SBOMs (`review-dependency-management`) or tests (`review-testing`). See `SKILL.md` step 7.

## Refresh procedure

1. **Cadence:** quarterly; also when a new MCP specification revision is published, when an official SDK major
   version changes how transports, tools or annotations are declared (update `../languages/*.md`), or when run notes
   contain ≥ 3 `localized-standard-gap` entries for this skill.
2. **Detect drift:** `python compliance-reviewer/scripts/check_source_drift.py check review-mcp-server`
   (GitHub commits for the four modelcontextprotocol.io pages, text hashes for modelcontextprotocol.info and CSA;
   record the first text-hash baselines with `--record-baselines`). Process the two `manual` checks by hand.
3. **Update:** edit or add elements (new IDs only), keep each website ≤ 100 elements, update the pins and retrieval
   dates in each file header, in `../sources.md` and in `pins.json`. If a pinned URL changes, update
   `compliance-review-core/references/approved-sources.md` too.
4. **Verify:** `python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py labels review-mcp-server`,
   `check_source_drift.py lint review-mcp-server`, then run the MCP validation tests
   (`python test/logic/test_all.py --only mcps-dotNET,mcps-java,mcps-python`).
