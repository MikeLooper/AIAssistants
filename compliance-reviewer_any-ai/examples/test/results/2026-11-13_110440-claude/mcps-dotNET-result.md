# mcps-dotNET — PASS

- Tool: claude (--tool)
- Run: `2026-11-13_1806-dotnet` — report: C:/Working/Storage/Dev/GitHub/AIAssistants/compliance-reviewer_any-ai/test/logic/results/2026-11-13_110440-claude/mcps-dotNET-report.md
- Reviewer score: 25.4 (Poor)
- Duration: 987 s, cost $5.42
- Fresh build: succeeded (dotnet build --nologo -v q, 4 s)
- Flaws found: 12/12 (100%; need 11 for 90%)
- Unexpected Error findings: 0

## Seeded flaws

| Flaw | Result | Findings |
|---|---|---|
| M1 | found | MCP-01#1 |
| M2 | found | MCP-05#1 |
| M3 | found | MCP-06#1, MCP-09#1, SEC-II-01#1 |
| M4 | found | MCP-09#1, SEC-II-04#1 |
| M5 | found | MCP-04#1, MCP-06#1, SEC-II-01#1 |
| M6 | found | MCP-10#1 |
| M7 | found | MCP-08#1, MCP-11#1, SEC-OP-05#1 |
| M8 | found | MCP-07#1, SEC-OP-01#1 |
| M9 | found | MCP-08#1, MCP-09#1, MCP-13#1, REL-01#1, SEC-II-10#1 |
| M10 | found | DEP-01#1, DEP-01#2, DEP-02#1 |
| M11 | found | DP-01#1 |
| M12 | found | TST-01#1, TST-02#1, TST-06#1, TST-07#1, TST-11#1, TST-12#1, TST-13#1 |

## Unexpected Warning/Information findings (reported only)

| Id | Check | Severity | Location | Title |
|---|---|---|---|---|
| REL-02#1 | REL-02 | Warning | test/mcps/dotNET/TodoTools.cs:110 | No retry for transient faults on the outbound import call |
| REL-06#1 | REL-06 | Warning | test/mcps/dotNET/TodoTools.cs:86 | No load shedding or rate limiting on resource-intensive tool calls |
| PERF-06#1 | PERF-06 | Warning | test/mcps/dotNET/TodoTools.cs:21 | list_todos and export_todos return the entire unbounded todo list |

Expected incidental findings (not scored): 8
