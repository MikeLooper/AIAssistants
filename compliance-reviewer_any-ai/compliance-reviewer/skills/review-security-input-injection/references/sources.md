# Sources — Security: Input & Injection (localized)

Standards are localized in `references/standards/`. Do not fetch these sources during a review, and do not use
remembered parser, framework or serializer defaults. OWASP publishes no Python-specific security cheat sheet; Python
guidance comes from the Python and Django documentation.

| Source | Pinned version | Retrieved | Elements | Local file |
|---|---|---|---|---|
| OWASP Cheat Sheets — Input Validation, Injection Prevention, SQL Injection Prevention, Query Parameterization, XML Security, File Upload, Cross Site Scripting Prevention, Deserialization (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ b9500094 / 9a91ba5a / 9a91ba5a / 9a91ba5a / 6f207d04 / 89a49d9d / 3b93fa9b / 16a0ed80 | 2026-11-08 | 58 | standards/owasp-input-injection.md |
| OWASP .NET Security Cheat Sheet, input-handling and legacy sections (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ 3cfa49de | 2026-11-08 | 6 | standards/dotnet-input.md |
| OWASP Java Security Cheat Sheet (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ f1d0311a | 2026-11-08 | 2 (site total 74 / 100) | standards/java-input.md |
| OWASP Server-Side Request Forgery Prevention Cheat Sheet (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ 0765662030093f8b9251399439580e7507148018 (2026-11-08) | 2026-11-09 | 8 | standards/owasp-input-injection.md (SSRF section) |
| OWASP Top 10:2025 A05 (top10.owasp.org) | OWASP/Top10 @ d4d000ec (2025-12-24) | 2026-11-08 | 7 / 100 | standards/owasp-input-injection.md |
| Microsoft Learn (learn.microsoft.com) — EF Core SQL queries, ASP.NET Core 10.0 uploads/XSS/validation, .NET 10 API, BinaryFormatter guide | per-page `view=` / `ms.date` | 2026-11-08 | 9 / 100 | standards/dotnet-input.md |
| Oracle Secure Coding Guidelines for Java SE (www.oracle.com) | document version 11.0 (June 2025) | 2026-11-08 | 9 / 100 | standards/java-input.md |
| Oracle JAXP Security Guide (docs.oracle.com) | Java SE 25 | 2026-11-08 | 2 / 100 | standards/java-input.md |
| Spring Data JPA Reference (docs.spring.io) | 4.1 (4.1.2) | 2026-11-08 | 2 / 100 | standards/java-input.md |
| Python documentation (docs.python.org) | 3.15 (3.15.2) | 2026-11-08 | 4 / 100 | standards/python-input.md |
| Django documentation (docs.djangoproject.com) | 6.1 | 2026-11-08 | 6 / 100 | standards/python-input.md |
| OWASP Node.js Security Cheat Sheet (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ eeaa1e47 (2026-11-05) | 2026-11-09 | 5 | standards/node-input.md |
| Express — Production Best Practices: Security (expressjs.com) | page at retrieval (Express 5.x docs) | 2026-11-09 | 1 / 100 | standards/node-input.md |

Element levels: MUST/REVIEW take the check's default severity; SHOULD one level lower (`SKILL.md` step 5).
