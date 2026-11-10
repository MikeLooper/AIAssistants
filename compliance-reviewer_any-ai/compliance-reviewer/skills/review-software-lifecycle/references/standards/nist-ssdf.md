# NIST SP 800-218 SSDF Version 1.1 — localized summary

- Source site: nist.gov · Version: SP 800-218, SSDF Version 1.1, February 2022 (final; DOI 10.6028/NIST.SP.800-218) · Rev. 1 (SSDF v1.2) initial public draft of 2025-12-17 is watched, not used
- Citation base: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf
- Localized: 2026-11-09 (from the plan's 2026-11-09 planning snapshot) · Elements: 19 (cap 100)
- Source name for `Finding.standard`: NIST SSDF 1.1
- Level: every element is `REVIEW` (the SSDF uses no normative keywords); severity is the owning check's default.
- Anchors: `ssdf#page=<physical PDF page>` (Table 1 is on PDF pages 15–28). The task ID is part of the requirement text so findings name it.
- Citation: `Finding.url` = citation base + `#page=N` (primary page first), e.g. `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf#page=16`.

| Key | Page path | Note |
|-----|-----------|------|
| ssdf | (citation base) | The PDF; anchors are `#page=N` |

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| SSDF-01 | REVIEW | (PO.3.1, PO.3.2 ex. 3) The toolchain (build, test, analysis, release) is defined as code in the repository (pipelines-as-code), not only in a UI. | always | SL-01 | ssdf#page=16 |
| SSDF-02 | REVIEW | (PW.6.2 ex. 3, PO.5.1 ex. 4) Builds run in a dedicated, controlled build environment (the CI platform) with minimal direct human access, not ad hoc on workstations. | always | SL-01 | ssdf#page=23, ssdf#page=17 |
| SSDF-03 | REVIEW | (PO.3.2 ex. 4) The technologies for reproducible builds are in place where the ecosystem supports them (deterministic compiler and packaging settings, fixed timestamps). | publishes artifacts | SL-05 | ssdf#page=16 |
| SSDF-04 | REVIEW | (PW.6.1, PW.6.2 ex. 1, 2, 7) Compiler and build-tool security and warning features are enabled in versioned build config, and warnings are treated as errors in CI builds. | compiled language in scope | SL-11 | ssdf#page=23 |
| SSDF-05 | REVIEW | (PO.3.2 ex. 5, 7) Toolchain components are kept updated, and their integrity and provenance are verified before use (pinned versions, checksum-verified downloads). | CI files in scope | SL-10 | ssdf#page=16 |
| SSDF-06 | REVIEW | (PO.4.1 ex. 3) Security-check criteria are defined (e.g. the severity threshold that blocks a merge, part of the definition of done). | security tooling in CI | SL-11 | ssdf#page=17 |
| SSDF-07 | REVIEW | (PO.4.2 ex. 1, 3) The toolchain gathers security-check results automatically and enforces the criteria as automated gates (the build fails on findings above the threshold). | security tooling in CI | SL-11 | ssdf#page=17 |
| SSDF-08 | REVIEW | (PO.3.3, PO.4.2 ex. 4) Security tools produce retained artifacts of their results (e.g. SARIF upload, reports) with restricted access. | security tooling in CI | SL-11 | ssdf#page=16, ssdf#page=17 |
| SSDF-09 | REVIEW | (PO.5.1 ex. 2, 5) Environments are separated: production deployment runs as a distinct, protected stage or environment, and non-production pipelines don't use production resources. | deploy pipeline in scope | SL-02 | ssdf#page=17 |
| SSDF-10 | REVIEW | (PS.1.1 ex. 1, 4) Code and configuration-as-code follow least privilege, and the code owner reviews changes by others (CODEOWNERS or equivalent). | forge supports CODEOWNERS | SL-04 | ssdf#page=18 |
| SSDF-11 | REVIEW | (PS.1.1 ex. 3) Commit signing is required on protected branches. | settings-as-code in scope | SL-04 | ssdf#page=18 |
| SSDF-12 | REVIEW | (PS.1.1 ex. 5, 6; PS.2.1 ex. 1, 2) Release artifacts are code-signed and/or published with cryptographic hashes so acquirers can verify integrity. | publishes artifacts | SL-05 | ssdf#page=19, ssdf#page=18 |
| SSDF-13 | REVIEW | (PS.3.1 ex. 1, 2) Release files and their integrity and provenance data are archived per release in a controlled repository (a registry or release store), not rebuilt on demand. | publishes artifacts | SL-02 | ssdf#page=19 |
| SSDF-14 | REVIEW | (PS.3.2 ex. 1, 3, 4) Provenance data is produced for every release in a standards-based format, is integrity-protected, and is updated whenever components change. | publishes artifacts | SL-05 | ssdf#page=19 |
| SSDF-15 | REVIEW | (PW.7.1, PW.7.2 ex. 1, 3) Peer code review is required for changes to protected branches. | settings-as-code in scope | SL-04 | ssdf#page=23 |
| SSDF-16 | REVIEW | (PW.7.2 ex. 4, 6) Automated static analysis checks code for vulnerabilities continuously as it's checked in, and findings are triaged. | always | SL-11 | ssdf#page=23 |
| SSDF-17 | REVIEW | (RV.1.1; RV.1.3 ex. 1) A vulnerability disclosure program is published, easy to find, and explains how to report. | always | SL-07 | ssdf#page=26, ssdf#page=25 |
| SSDF-18 | REVIEW | (RV.1.3 ex. 2, 3) The policy states who handles reports and the response process (triage, remediation, communication). | security policy exists | SL-07 | ssdf#page=26 |
| SSDF-19 | REVIEW | (RV.2.2 ex. 3) Security advisories are released for fixed vulnerabilities, describing affected versions and how to remediate (supported versions are stated). | security policy exists | SL-07 | ssdf#page=27 |
