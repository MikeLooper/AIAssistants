# OWASP Secrets Management Cheat Sheet — secret-store backup and break-glass — localized summary

- Source site: cheatsheetseries.owasp.org · Pinned: OWASP/CheatSheetSeries @ d6474de095dedba6caf536fdf8926d6ae53f3cfc
  (2026-11-08; the same pin `review-security-operational` uses for its SMG elements, separate budget)
- Citation base: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- Localized: 2026-11-09 · Elements: 1 (cap 100)
- Source name for `Finding.standard`: `OWASP Secrets Management Cheat Sheet`
- Level: `SHOULD` (the section says "should"). The level never changes severity; each Finding takes DR-06's default
  (`../../SKILL.md` step 8).
- Scope: section 2.9 only. Secrets in code and secret delivery are `review-security-operational`'s (SMG-xx).
  Soft delete or purge protection on secret stores isn't in this section; it is judged only where a WAFR element
  covers recovery assets in general (WAFR-28 … WAFR-32).

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| OSM-01 | SHOULD | Secret and key stores (vault, key management service) are backed up automatically on a schedule, into encrypted, restricted and monitored storage, with tested restores; emergency break-glass credentials are backed up in a secondary secrets system and a break-glass procedure is documented and tested. | a secret or key store is defined in the IaC | DR-06 | 29-downtime-break-glass-backup-and-restore |
