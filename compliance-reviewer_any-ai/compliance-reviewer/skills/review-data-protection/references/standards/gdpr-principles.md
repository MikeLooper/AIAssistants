# GDPR — data-protection principles (engineering summary) — localized summary

- Source site: eur-lex.europa.eu (official text). EUR-Lex refuses automated retrieval, so the text was read from a
  verbatim reproduction (gdpr-info.eu, Art. 5, 25 and 32) and is refreshed manually against EUR-Lex.
- Pinned version: Regulation (EU) 2016/679 (General Data Protection Regulation), OJ L 119, 4.5.2016, as in force on
  2026-11-24 (Art. 5, 25 and 32 unchanged since adoption).
- Citation base: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- Localized: 2026-11-24 · Elements: 5 (cap 100)
- Source name for `Finding.standard`: `Regulation (EU) 2016/679 (GDPR)`
- Scope: **principle summaries only**, for engineering controls that can be seen in code: Art. 5(1)(c) data
  minimisation, Art. 5(1)(e) storage limitation, Art. 25 data protection by design and by default, Art. 32(1)(a)
  pseudonymisation and encryption. Lawful basis, consent, transparency, data-subject rights procedures, DPIAs and
  accountability are not localized and are never judged. A finding never states that the target complies or doesn't
  comply with the Regulation.
- Level: `MUST` ("shall"). Levels are informational: every Finding takes its check's default severity.
- Anchor(s): the article reference (`§` = Article); the report names it after the element ID. Citation URL: citation
  base (the Regulation has no stable per-article anchor on this URL).

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|---------|
| GDPR-01 | MUST | (Art. 5(1)(c)) Data minimisation: personal data are adequate, relevant and limited to what is necessary for the purpose; for engineering, send third parties only the personal fields the call needs. | personal data sent to SDKs or external APIs | DPR-04 | §5(1)(c) |
| GDPR-02 | MUST | (Art. 5(1)(e)) Storage limitation: personal data are kept in a form that identifies people for no longer than necessary for the purpose. | personal data stored | DPR-06 | §5(1)(e) |
| GDPR-03 | MUST | (Art. 25(1)) Data protection by design: technical measures such as pseudonymisation implement the data-protection principles, such as data minimisation, in an effective manner. | pseudonymization, masking or data-copy code | DPR-07 | §25(1) |
| GDPR-04 | MUST | (Art. 25(2)) Data protection by default: by default only the personal data necessary for each specific purpose are processed (amount collected, extent of processing, storage period, accessibility), and personal data aren't made accessible to an indefinite number of people without the person's intervention. | personal data returned or published | DPR-02 | §25(2) |
| GDPR-05 | MUST | (Art. 32(1)(a)) Security of processing: appropriate technical measures, including the pseudonymisation and encryption of personal data, give a level of security appropriate to the risk. | personal data stored | DPR-01 | §32(1)(a) |
