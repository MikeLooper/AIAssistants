# Sources — Security: Operational (localized)

Standards are localized in `references/standards/`. Do not fetch these sources during a review, and do not use
remembered error-page, logging or secret-store defaults.

| Source | Pinned version | Retrieved | Elements | Local file |
|---|---|---|---|---|
| OWASP Cheat Sheets — Error Handling, Logging, Secrets Management, Secure Code Review (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ 796eed7d / f1d0311a / d6474de0 / a11444a5 | 2026-11-08 | 47 | standards/owasp-operational.md |
| OWASP REST Security Cheat Sheet, `#management-endpoints` only (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ 97cb8a3c (2026-10-14) | 2026-11-09 | 1 | standards/owasp-operational.md (ORS section) |
| OWASP .NET Security Cheat Sheet, configuration/deployment and data-protection sections (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ 3cfa49de | 2026-11-08 | 5 (site total 53 / 100) | standards/dotnet-operational.md |
| OWASP Top 10:2025 A09, A10 (top10.owasp.org) | OWASP/Top10 @ d4d000ec / 494be56d | 2026-11-08 | 15 / 100 | standards/owasp-operational.md |
| Microsoft Learn (learn.microsoft.com) — ASP.NET Core 10.0 error handling, environments, app secrets, Key Vault, HTTP logging; .NET logging and data redaction | per-page `ms.date` / `view=aspnetcore-10.0` | 2026-11-08 | 11 / 100 | standards/dotnet-operational.md |
| Spring Boot Reference (docs.spring.io) | 4.1 (4.1.2) | 2026-11-08 | 6 / 100 | standards/java-operational.md |
| Django documentation (docs.djangoproject.com) | 6.1 | 2026-11-08 | 5 / 100 | standards/python-operational.md |
| Python documentation (docs.python.org) | 3.15 (3.15.2) | 2026-11-08 | 4 / 100 | standards/python-operational.md |
| OWASP Node.js Security Cheat Sheet (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ eeaa1e47 (2026-11-05) | 2026-11-09 | 5 | standards/node-operational.md |
| Express — Production Best Practices: Security (expressjs.com) | page at retrieval (Express 5.x docs) | 2026-11-09 | 1 / 100 | standards/node-operational.md |

Not used: the OWASP Java Security Cheat Sheet (no error-handling, logging or secrets content). OWASP has no Python
security cheat sheet; Python guidance comes from the Django and Python documentation.

Element levels: MUST/REVIEW take the check's default severity; SHOULD one level lower (`SKILL.md` step 6).
