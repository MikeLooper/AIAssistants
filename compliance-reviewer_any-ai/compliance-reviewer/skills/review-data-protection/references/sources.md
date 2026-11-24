# Sources — Data Protection (localized)

Standards are localized in `references/standards/`. Do not fetch these sources during a review, and do not use
remembered SDK, serializer or framework defaults.

| Source | Pinned version | Retrieved | Elements | Local file |
|---|---|---|---|---|
| OWASP Cheat Sheets — Cryptographic Storage, User Privacy Protection, HTML5 Security (storage and PII input hints only) (cheatsheetseries.owasp.org) | OWASP/CheatSheetSeries @ 87a1faf1 / d7951be5 / 3919b1c4 | 2026-11-24 | 10 / 100 | standards/owasp-data-protection.md |
| OWASP Top 10:2025 A04 Cryptographic Failures, "How to prevent" (top10.owasp.org) | OWASP/Top10 @ d4d000ec | 2026-11-24 | 5 / 100 | standards/owasp-data-protection.md |
| OWASP API Security Top 10:2023 API3; OWASP community page "Information exposure through query strings in URL" (owasp.org) | OWASP/API-Security @ ea77cba5; OWASP/www-community @ 01e67c2f | 2026-11-24 | 5 / 100 | standards/owasp-data-protection.md |
| NIST SP 800-122 (nvlpubs.nist.gov) | April 2010 (final; no newer revision) | 2026-11-24 | 9 / 100 | standards/nist-sp-800-122.md |
| Regulation (EU) 2016/679 (GDPR) Art. 5(1)(c), 5(1)(e), 25, 32(1)(a), principle summaries (eur-lex.europa.eu; read via a verbatim reproduction, see MAINTENANCE.md) | OJ L 119, 4.5.2016 | 2026-11-24 | 5 / 100 | standards/gdpr-principles.md |
| RFC 2606 Reserved Top Level DNS Names (www.rfc-editor.org) | June 1999 (BCP 32) | 2026-11-24 | 1 / 100 | standards/rfc-2606-reserved-names.md |
| Sentry "Data Collected" pages for .NET, Java, Python (SDK 3.x), JavaScript (docs.sentry.io) | page text at retrieval (text hashes in `pins.json`) | 2026-11-24 | 4 / 100 | standards/third-party-sdks.md |
| Microsoft Learn — Application Insights FAQ; Data classification in .NET (learn.microsoft.com) | per-page `ms.date` (2026-05-03; 2025-03-21) | 2026-11-24 | 3 / 100 | standards/third-party-sdks.md, standards/dotnet-data-protection.md |
| FasterXML jackson-annotations wiki — Jackson Annotations (github.com) | page text at retrieval (text hash in `pins.json`) | 2026-11-24 | 2 / 100 | standards/java-data-protection.md |
| Django REST framework API Guide — Serializers (www.django-rest-framework.org) | encode/django-rest-framework @ 94219574 | 2026-11-24 | 2 / 100 | standards/python-data-protection.md |

Not localized: the OWASP Mass Assignment Cheat Sheet (input binding is owned by `review-security-input-injection`
SEC-II-01; the plan names it for ownership only), GDPR articles on lawful basis, consent, data-subject rights and
DPIAs (out of scope: the reviewer judges engineering controls only), and .NET data redaction (logging redaction is
judged by `review-security-operational`).

Every Finding takes its check's default severity (`SKILL.md` step 7).
