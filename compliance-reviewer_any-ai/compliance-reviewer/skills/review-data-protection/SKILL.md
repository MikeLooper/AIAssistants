---
name: review-data-protection
description: 'Reviews how a codebase protects personal data (PII) in code: storage encryption and minimization, over-exposure in API responses, personal data in URLs and browser storage, personal data sent to third-party SDKs, synthetic test and seed data, deletion and retention paths, masking of copied production data and data classification, against pinned OWASP (Cryptographic Storage, User Privacy Protection, HTML5 Security cheat sheets; API3:2023; Top 10:2025 A04), NIST SP 800-122, GDPR Art. 5/25/32 principle summaries, RFC 2606 and vendor guidance. Engineering controls only, never legal compliance. Use when the compliance-reviewer orchestrator delegates the Data Protection subject.'
user-invocable: false
---

# Review: Data Protection

Assesses the engineering controls a codebase uses to protect personal data, using local, pinned summaries of
OWASP, NIST, GDPR principle text, RFC 2606 and vendor guidance. The reviewer judges only what the code and
configuration show. It never judges lawful basis, consent records, privacy notices or DPIAs, and the report never
states that a target complies (or fails to comply) with GDPR, CCPA or any other law.

## Inputs

Entity and model classes, DTOs and serializers, controllers that return data, client-side storage and cookie code,
third-party SDK setup (error trackers, analytics, LLM/AI and email/SMS clients), fixtures, seed and sample data,
migrations, classification and redaction setup, and deletion, retention or data-copy code, per `compliance-inventory`.
The dispatch payload may also carry `piiCandidates` (file, line, rule, confidence; never the value) found by the
step-01 pattern pass in test, fixture, seed and sample files, and `personalDataSignals` (why the subject applies).

## Standards (local, authoritative)

- `references/standards/owasp-data-protection.md` — CSD-01…05, A04-01…05, BOP-01…04, UPP-01…02, HSP-01…03,
  QSE-01. Always load.
- `references/standards/nist-sp-800-122.md` — SP122-01…09. Always load.
- `references/standards/gdpr-principles.md` — GDPR-01…05 (principle summaries). Always load.
- `references/standards/rfc-2606-reserved-names.md` — RSV-01. Always load.
- `references/standards/third-party-sdks.md` — TPS-01…05 (Sentry per platform, Application Insights). Always load;
  each row applies only when that SDK is in the files.
- `references/standards/dotnet-data-protection.md` — DND-01…02. Load when language `csharp` is detected.
- `references/standards/java-data-protection.md` — JVD-01…02. Load when language `java` is detected.
- `references/standards/python-data-protection.md` — PYD-01…02. Load when language `python` is detected.
- Do **not** fetch any URL for this skill, and never use remembered SDK or framework defaults: a default counts only
  when a localized element states it. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, the standards files that apply (above), and
   `references/languages/<id>.md` for each detected language (detection signals only; they cite no standard).
2. Find the personal data first: entity, model and DTO fields named like the identifiers in SP122-02 (name, email,
   phone, address, date of birth, national or tax ID, passport, card or account number, IP address, biometrics),
   classification attributes, and user or customer tables in migrations. Then follow those fields to storage,
   API responses, URLs and client storage, third-party SDK calls, fixtures and deletion code.
3. **Candidates.** When the payload has `piiCandidates`, read each candidate line with ±3 lines of context, even when
   the file isn't in your own list. Decide whether the value is real-looking personal data or clearly synthetic
   (reserved domains per RSV-01, published test card numbers, obviously fake values). Real-looking values fail
   DPR-05 with `confidence: high` for a Luhn-valid card number or a checksum-valid IBAN that the context confirms,
   `medium` otherwise. When `piiCandidatesTotal` is larger than the list, add
   `pii-candidates-truncated: <total>` to `notes`.
4. For each check DPR-01…DPR-08, evaluate the elements it lists against the subject's files. Mark a check N/A with a
   reason when no element applies (e.g. DPR-03 when there is no URL, client storage or cookie code; DPR-07 when there
   are no data-copy scripts; DPR-04 when no third-party SDK or outbound personal-data call is in the files).
5. Evidence rules: fail an element only on concrete code or configuration in the files (see the evidence notes in
   `checklist.md`). A missing control counts only where the files show the personal data it should protect. Don't
   fail on speculation, and use confidence `medium` unless the evidence is unambiguous.
6. **Ownership** (Boundaries). These stay with their own subjects; don't report them here:
   - personal data or secrets in logs and error reports: `review-security-operational` SEC-OP-03;
   - personal data in telemetry attributes and baggage: `review-observability` OBS-10;
   - `Cache-Control: no-store` on sensitive responses: `review-security-web-api` SEC-WA-08;
   - credentials (passwords, tokens, API keys) in URLs: `review-security-web-api` SEC-WA-10;
   - mass assignment and over-posting on input: `review-security-input-injection` SEC-II-01;
   - tokens in `localStorage`/`sessionStorage`, session cookies, password hashing: `review-security-identity-access`;
   - TLS and HSTS in transit: `review-security-web-api`; hardcoded keys and secrets: SEC-OP-05.

   DPR-02 owns over-exposure on output (responses and serializers). DPR-03 owns personal data other than credentials
   in URLs, query strings and client storage. Store-level encryption in IaC is judged under DPR-01 only when the
   payload says `advanced: true` and IaC files are in your list; otherwise judge field- and application-level
   controls only.
7. Severity: every Finding takes its check's default severity from `checklist.md`. When several elements fail on the
   same evidence, write one finding.
8. Citations: set `element` to the failed element's ID (e.g. `BOP-03`); the report script derives `standard` and
   `url`. Prefer a vendor element (DND/JVD/PYD/TPS), then an OWASP element, then NIST, then GDPR. Cite a GDPR element
   only when nothing more specific fits, and word the finding as an engineering gap ("personal data is returned
   that the endpoint doesn't need"), never as a legal conclusion.
9. **Redaction.** Evidence excerpts never contain the personal data or secret itself: replace the value with
   `<redacted:kind>` (e.g. `"cardNumber": "<redacted:card-number>"`), keeping the field name and the line numbers.
10. If the reference date (date part of `startedAt`) is more than 9 months after a standards file's "Localized"
    date, add `localized-standard-stale: <file> localized <date>` to `notes`.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
