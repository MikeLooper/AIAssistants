# Maintenance — Data Protection localized standards

**Maintainers only. Workers never load this file.** Design decisions are recorded inline (DEC-n: this skill's
localization decisions; D-n: decisions of the approved plan `docs/ai/plan-pii-secrets-checks_2026-11-24.md`).

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

| Website | Local file(s) | Elements | Cap | Note |
|---|---|---|---|---|
| cheatsheetseries.owasp.org | owasp-data-protection.md (CSD 5, UPP 2, HSP 3) | 10 | 100 | Cryptographic Storage, User Privacy Protection, HTML5 (storage and PII input hints) |
| top10.owasp.org | owasp-data-protection.md | 5 | 100 | A04:2025 "How to prevent" |
| owasp.org | owasp-data-protection.md (BOP 4, QSE 1) | 5 | 100 | API3:2023; community page on query strings |
| nvlpubs.nist.gov | nist-sp-800-122.md | 9 | 100 | SP 800-122 (2010) |
| eur-lex.europa.eu | gdpr-principles.md | 5 | 100 | Art. 5(1)(c), 5(1)(e), 25, 32(1)(a) |
| www.rfc-editor.org | rfc-2606-reserved-names.md | 1 | 100 | RFC 2606 |
| docs.sentry.io | third-party-sdks.md | 4 | 100 | One "Data Collected" page per platform |
| learn.microsoft.com | third-party-sdks.md (1) + dotnet-data-protection.md (2) | 3 | 100 | Application Insights FAQ; Data classification in .NET |
| github.com | java-data-protection.md | 2 | 100 | jackson-annotations wiki |
| www.django-rest-framework.org | python-data-protection.md | 2 | 100 | Serializers guide |
| **Total** | | **46** | | |

## Decisions

- **DEC-1 (D-1, D-2):** a separate skill and subject (`Subject: Data Protection`, step 29) instead of more checks in
  `review-security-operational` (99 elements, one of the largest packs). The subject is N/A, with no worker call, when
  the step-01 inventory finds no personal data (`personalDataFound: false`).
- **DEC-2:** check IDs use the prefix `DPR-` (the plan's draft `DP-` is already used by `review-software-quality`'s
  Design Patterns checks, and the test harness matches flaws by check ID alone).
- **DEC-3 (D-6):** engineering controls only. GDPR text is summarized as principles (Art. 5(1)(c), 5(1)(e), 25,
  32(1)(a)); lawful basis, consent, transparency, rights procedures and DPIAs are out of scope, and no finding states
  legal compliance.
- **DEC-4:** every Finding takes its check's default severity (no level-based severity), because the sources mix
  MUST/SHOULD wording, legal "shall" and descriptive guidance.
- **DEC-5:** ownership boundaries (see `SKILL.md` step 6): logs SEC-OP-03, telemetry OBS-10, `no-store` SEC-WA-08,
  credentials in URLs SEC-WA-10, input binding SEC-II-01, client-side tokens and session cookies identity-access,
  hardcoded keys SEC-OP-05. The Mass Assignment Cheat Sheet is cited only to define that boundary; no element.
- **DEC-6:** GDPR is read from gdpr-info.eu (a verbatim reproduction) because EUR-Lex refuses automated retrieval;
  citations point at the official EUR-Lex ELI URL without an article anchor, and the article is named after the
  element ID (`§` anchors).
- **DEC-7:** Sentry Python, Java and JavaScript docs describe `data_collection`/`dataCollection` options (Python SDK
  3.x); `.NET` still documents `SendDefaultPii`. The elements state only what each page says; older-SDK options
  (`send_default_pii` in Python 2.x) are not localized — a worker that meets them adds a `localized-standard-gap` note.

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Prefixes (CSD, A04,
  BOP, UPP, HSP, QSE, SP122, GDPR, RSV, TPS, DND, JVD, PYD) stay distinct from every other localized skill (A04 is
  unused elsewhere).
- Every element ID is listed by exactly one check in `../checklist.md`, and the "Check" column of its row names that check.
- Level: the source's own wording (MUST/SHOULD/REVIEW); levels are informational (DEC-4).
- **(Default)** elements state SDK, annotation or framework behaviour. Add one only with the version or page date it was
  read from. Workers may rely on no other default.
- Primary anchor first; list every absorbed anchor so coverage stays auditable. Rows ≈ 300 characters at most.
- Vendor files are split **by language** (matching `compliance-review-core/references/languages.md` ids), except
  `third-party-sdks.md`, which is gated by SDK presence instead of language. A new vendor file gets a line in
  `SKILL.md`, a row in `../sources.md` and a row in the budget table.

## Refresh procedure

1. **Cadence:**
   - OWASP cheat sheets: quarterly, or when run notes contain ≥ 3 `localized-standard-gap` or any
     `localized-standard-stale` entry for this skill.
   - Top 10 and API Security Top 10: when a new edition is published (check whether A04 or API3 is renumbered).
   - NIST SP 800-122: yearly record check (a Rev. 1 would replace the file).
   - GDPR: yearly manual check on EUR-Lex for amendments to Art. 5, 25, 32.
   - Sentry docs: quarterly (fast-moving; `dataCollection` options changed in 2026); Microsoft Learn: when `ms.date`
     changes; DRF: on each minor release; Jackson wiki: yearly.
2. **Detect drift:** `python compliance-reviewer/scripts/check_source_drift.py check review-data-protection`.
3. **Diff and propose:** follow `compliance-reviewer/REFRESH.md` steps 5–7.
4. **Verify:** `check_source_drift.py lint review-data-protection`, then `compliance_report.py packs build
   review-data-protection` and `compliance_report.py labels review-data-protection` (both must be clean). Check that
   IDs are contiguous per prefix and that every element appears in exactly one check. Run a sample review of a repo
   with personal data (e.g. `test/apis/dotNET`) with `--subjects review-data-protection` and `validate` it.

## Localization log

- **2026-11-24** — First localization (tool 2.1.0). Pins: Cryptographic Storage @ 87a1faf1 (2026-10-30), User Privacy
  Protection @ d7951be5 (2026-11-23), HTML5 Security @ 3919b1c4 (2026-10-04), A04:2025 @ d4d000ec (2025-12-24),
  API3:2023 @ ea77cba5 (2023-06-28), query-strings page @ 01e67c2f (2025-10-05), NIST SP 800-122 (April 2010), GDPR
  (OJ L 119, 4.5.2016), RFC 2606, Sentry Data Collected pages and the jackson-annotations wiki (text-hash baselines),
  Application Insights FAQ (`ms.date` 2026-05-03), Data classification in .NET (`ms.date` 2025-03-21), DRF serializers
  @ 94219574 (2026-11-10). 46 elements across DPR-01…08.

## Refresh due

- 2027-02-24 — quarterly OWASP and Sentry check.
- 2027-11-24 — yearly NIST record, GDPR (manual) and Jackson wiki check.

## Gap log

(none yet)
