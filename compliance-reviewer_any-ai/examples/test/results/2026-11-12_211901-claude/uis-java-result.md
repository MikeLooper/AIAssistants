# uis-java — FAIL

- Tool: claude (--tool)
- Run: `2026-11-13_0422-java-ui` — report: C:/Working/Storage/Dev/GitHub/AIAssistants/compliance-reviewer_any-ai/test/logic/results/2026-11-12_211901-claude/uis-java-report.md
- Reviewer score: 36.65 (Poor)
- Duration: 902 s, cost $5.32
- Fresh build: succeeded (mvn -B -q clean package -DskipTests, 4 s)
- Flaws found: 9/12 (75%; need 11 for 90%)
- Unexpected Error findings: 0

## Seeded flaws

| Flaw | Result | Findings |
|---|---|---|
| U1 | found | SEC-II-08#1 |
| U2 | **missed** | expected SEC-IA-05 in src/main/java/com/example/todoui/TodoController.java, src/main/resources/templates/index.html, pom.xml |
| U3 | found | SEC-OP-05#1, TF-03#1 |
| U4 | found | SEC-IA-01#1, SEC-IA-02#1, SEC-IA-07#1, SEC-IA-09#1 |
| U5 | found | SEC-II-01#1, SEC-II-01#2, SEC-II-01#3 |
| U6 | found | SEC-OP-01#1, SEC-OP-07#1 |
| U7 | found | DP-01#1 |
| U8 | found | SEC-OP-02#1, SQ-06#1 |
| U9 | found | OBS-01#1, SEC-OP-04#1, TF-11#1 |
| U10 | **missed** | expected SQ-08 in src/main/java/com/example/todoui/TodoController.java |
| U11 | **missed** | expected SEC-WA-01, SEC-WA-03, SEC-WA-04, SEC-WA-11 in (whole app) |
| U12 | found | TST-01#1, TST-02#1, TST-06#1, TST-07#1, TST-11#1, TST-12#1 |

## Unexpected Warning/Information findings (reported only)

| Id | Check | Severity | Location | Title |
|---|---|---|---|---|
| PERF-05#1 | PERF-05 | Information | src/main/java/com/example/todoui/TodoController.java:52 | Linear scan over the in-memory todo list to find an item by id |

Expected incidental findings (not scored): 7
