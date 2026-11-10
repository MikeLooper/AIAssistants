# OWASP software supply chain guidance — localized summary

- Sources: top10.owasp.org (A03:2025) @ OWASP/Top10 d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966 (2025-12-24);
  cheatsheetseries.owasp.org — Vulnerable Dependency Management @ OWASP/CheatSheetSeries b724e32f29a1d7e1c966943f7b30e3b776d46bfe (2026-10-04),
  Software Supply Chain Security @ OWASP/CheatSheetSeries 995524d4a18e64672c80c8e13869d29ef850bd43 (2026-10-03)
- Localized: 2026-11-07 · Elements: top10.owasp.org 9 (cap 100); cheatsheetseries.owasp.org 15 (cap 100)
- Level: every element is `REVIEW` (these sections use no normative keywords); severity is the owning check's default.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Source name for `Finding.standard` |
|-----|---------------|------------------------------------|
| a03 | https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/ | OWASP Top 10:2025 A03 |
| vdm | https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html | OWASP Vulnerable Dependency Management Cheat Sheet |
| sscs | https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html | OWASP Software Supply Chain Security Cheat Sheet |

## A03:2025 Software Supply Chain Failures (OTT)

| ID | Level | Requirement (summary) | Manifest/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|--------------------------|-------|-----------|
| OTT-01 | REVIEW | Track and continuously inventory the versions of all components, including nested (transitive) dependencies. | lock file capturing the transitive graph | DEP-02 | a03#description, a03#how-to-prevent |
| OTT-02 | REVIEW | Components, runtime environments and frameworks must not be unsupported or out of date. | declared runtime/framework target | DEP-04 | a03#description |
| OTT-03 | REVIEW | Scan for vulnerabilities regularly; automate it with software composition analysis and subscribe to alerts. | Dependabot/Renovate config, NuGetAudit, scanner config | DEP-07 | a03#how-to-prevent, a03#description |
| OTT-04 | REVIEW | Centrally generate and manage an SBOM for the software. | SBOM file or SBOM-generator plugin/task | DEP-05 | a03#how-to-prevent |
| OTT-05 | REVIEW | Reduce attack surface by removing unused dependencies and unnecessary components. | test/dev-only packages in production scope; duplicate declarations | DEP-09 | a03#how-to-prevent |
| OTT-06 | REVIEW | Obtain components only from official, trusted sources over secure links; prefer signed packages. Untrusted sources must not reach production. | feed/index/repository URLs, signature-validation settings | DEP-08 | a03#how-to-prevent, a03#description |
| OTT-07 | REVIEW | Deliberately choose which version of a dependency is used, and upgrade only when there's a need. | exact or narrow versions; no `*`, `latest`, `+`, `LATEST`, `RELEASE` | DEP-01 | a03#how-to-prevent |
| OTT-08 | REVIEW | Monitor for unmaintained libraries or ones without security patches for older lines; migrate if patching isn't possible. | analyzer "deprecated"/"outdated" output | DEP-09 | a03#how-to-prevent |
| OTT-09 | REVIEW | Fix or upgrade vulnerable platforms, frameworks and dependencies in a risk-based, timely way. | analyzer vulnerability output | DEP-03 | a03#description, a03#how-to-prevent |

## OWASP Cheat Sheets (OCS)

| ID | Level | Requirement (summary) | Manifest/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|--------------------------|-------|-----------|
| OCS-01 | REVIEW | Run automated dependency analysis from the start of the project, not as a late add-on. | scanning configured in repo | DEP-07 | vdm#context |
| OCS-02 | REVIEW | Remediate a vulnerable transitive dependency through the direct dependency that pulls it in. | direct dependency of the reported package | DEP-03 | vdm#cases |
| OCS-03 | REVIEW | When a patched version exists, update to it and validate with automated tests. | analyzer "fixed in" vs declared version | DEP-03 | vdm#case-1 |
| OCS-04 | REVIEW | A risk acceptance or suppression is scoped to the specific CVE (never the whole package) and documented with its reason. | suppression/ignore files (`NuGetAuditSuppress`, `--ignore-vuln`, dependency-check suppressions, `.trivyignore`) | DEP-07 | vdm#case-2, vdm#remark-about-the-security-issue-handling-decision |
| OCS-05 | REVIEW | Suppressing an alert, or changing a version string so a tool stops matching, isn't a fix. An in-house patch is verified by a failing-then-passing test. | suppression with no fix or justification | DEP-03 | vdm#case-3, vdm#case-5 |
| OCS-06 | REVIEW | Patched or backported artifacts are published to the internal registry with a traceable version and provenance, not committed as local binaries. | `<HintPath>` to repo-local DLLs, Maven `system` scope, vendored wheels/JARs | DEP-08 | vdm#case-5 |
| OCS-07 | REVIEW | The detection tool uses several reliable vulnerability sources and supports flagging false positives. | scanner choice/config | DEP-07 | vdm#tools |
| OCS-08 | REVIEW | Prefer released, actively maintained components: no alpha/beta/pre-release versions; the project keeps its own dependencies updated. | `-alpha`/`-beta`/`-rc`/`-preview`/`-SNAPSHOT`, PEP 440 `aN`/`bN`/`rcN`/`.devN` in production scope | DEP-09 | sscs#assess-suppliers |
| OCS-09 | REVIEW | Inventory production and development dependencies, e.g. with an SBOM. | SBOM file or generator | DEP-05 | sscs#understand-and-monitor-software-dependencies |
| OCS-10 | REVIEW | Monitor dependencies for known vulnerabilities automatically (NVD, OSV, CISA KEV). | scanner/advisory automation | DEP-07 | sscs#understand-and-monitor-software-dependencies |
| OCS-11 | REVIEW | Limit dependencies to specific, previously verified versions. | exact pins / narrow ranges | DEP-01 | sscs#lockfileversion-pinning |
| OCS-12 | REVIEW | Use a lock file so builds resolve the exact, previously verified versions. | lock file present and committed | DEP-02 | sscs#lockfileversion-pinning |
| OCS-13 | REVIEW | Use a private artifact repository whose use can't be bypassed. | single feed with `<clear/>`, NuGet package source mapping, pip `index-url` only, Maven mirror `*` | DEP-08 | sscs#use-private-artifact-repository |
| OCS-14 | REVIEW | Accept only signed components and validate signatures before use. | NuGet `signatureValidationMode=require` / `trustedSigners`; pip `--require-hashes` | DEP-08 | sscs#enforce-code-signing |
| OCS-15 | REVIEW | Inventory build tools, including versions and plugins. | SDK pin (`global.json`), Maven plugin versions, Gradle plugin versions, `build-system.requires` pins | DEP-01 | sscs#inventory-build-tools |
