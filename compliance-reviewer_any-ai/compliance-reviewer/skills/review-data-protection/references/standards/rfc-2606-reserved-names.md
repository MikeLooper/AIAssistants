# RFC 2606 — Reserved Top Level DNS Names — localized summary

- Source site: www.rfc-editor.org
- Pinned version: RFC 2606 (BCP 32), June 1999. RFCs don't change; a successor would be a new RFC that updates or
  obsoletes it (none as of 2026-11-24).
- Citation base: https://www.rfc-editor.org/rfc/rfc2606.html
- Localized: 2026-11-24 · Elements: 1 (cap 100)
- Source name for `Finding.standard`: `RFC 2606`
- Level: `SHOULD` (the RFC "recommends" the reserved names). Levels are informational: every Finding takes its
  check's default severity.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor.

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| RSV-01 | SHOULD | Test and documentation data uses reserved names that can never belong to real people or organizations: the `.test`, `.example`, `.invalid` and `.localhost` TLDs and the `example.com`, `example.net` and `example.org` second-level domains (e.g. email addresses `jane@example.com`). | fixtures, seed or sample data with email addresses or host names | DPR-05 | section-2, section-3 |
