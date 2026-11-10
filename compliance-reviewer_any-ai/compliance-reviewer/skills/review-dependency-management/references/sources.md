# Sources — Dependency Management (localized)

Standards are localized in `references/standards/`. Do not fetch these sources during a review, and do not
use remembered CVE, end-of-life or license facts. Vulnerabilities come only from `02-analyzers.json`.

| Source | Pinned version | Retrieved | Elements | Local file |
|---|---|---|---|---|
| OWASP Top 10:2025 A03 (top10.owasp.org) | OWASP/Top10 @ d4d000ec (2025-12-24) | 2026-11-07 | 9 / 100 | standards/owasp-supply-chain.md |
| OWASP Cheat Sheets — Vulnerable Dependency Mgmt, Software Supply Chain Security (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ b724e32f (2026-10-04) / 995524d4 (2026-10-03) | 2026-11-07 | 15 / 100 | standards/owasp-supply-chain.md |
| Microsoft .NET Support Policy (dotnet.microsoft.com) | releases-index.json at retrieval | 2026-11-07 | 6 / 100 | standards/lifecycle-dotnet.md |
| Microsoft .NET Framework Lifecycle (learn.microsoft.com) | page at retrieval | 2026-11-07 | 5 / 100 | standards/lifecycle-dotnet.md |
| Eclipse Temurin Support (adoptium.net) | page at retrieval | 2026-11-07 | 8 / 100 | standards/lifecycle-java.md |
| Spring Support Policy (spring.io) | api.spring.io generations at retrieval | 2026-11-07 | 7 / 100 | standards/lifecycle-java.md |
| Python versions (devguide.python.org) | page at retrieval | 2026-11-07 | 7 / 100 | standards/lifecycle-python.md |
| Node.js release schedule (github.com, `nodejs/Release` `schedule.json`) | main branch at retrieval | 2026-11-09 | 5 / 100 | standards/lifecycle-javascript.md |
| Express security best practices (expressjs.com) | page at retrieval (Express 5.x docs) | 2026-11-09 | 1 / 100 | standards/lifecycle-javascript.md |

Practice elements are REVIEW level (severity = the check's default); lifecycle elements use the date rule; DEP-03
severity follows the analyzer-reported severity (see SKILL.md steps 4, 5 and 7).
