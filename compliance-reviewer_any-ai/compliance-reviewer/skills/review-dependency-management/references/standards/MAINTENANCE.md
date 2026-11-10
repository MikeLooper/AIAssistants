# Maintenance — Dependency Management localized standards

**Maintainers only. Workers never load this file.** Design decisions are recorded inline where they apply (DEC-n: this skill's localization decisions; D-n and C-n: cross-skill decisions and follow-ups); the planning documents they came from aren't kept in this repo.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (Cost & Sustainability plan DEC-1). learn.microsoft.com is also used by `review-cost-sustainability`; the budgets are separate.

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| top10.owasp.org | owasp-supply-chain.md | 9 | 100 | A03:2025 Description + How to prevent |
| cheatsheetseries.owasp.org | owasp-supply-chain.md | 15 | 100 | Vulnerable Dependency Management; Software Supply Chain Security |
| dotnet.microsoft.com | lifecycle-dotnet.md | 6 | 100 | data from `releases-index.json` |
| learn.microsoft.com | lifecycle-dotnet.md | 5 | 100 | `lifecycle/products/microsoft-net-framework` |
| adoptium.net | lifecycle-java.md | 8 | 100 | Temurin release roadmap |
| spring.io | lifecycle-java.md | 7 | 100 | data from `api.spring.io` generations |
| devguide.python.org | lifecycle-python.md | 7 | 100 | Status of Python versions |
| github.com | lifecycle-javascript.md | 5 | 100 | `nodejs/Release` `schedule.json` (2026-11-09) |
| expressjs.com | lifecycle-javascript.md | 1 | 100 | Express 2.x/3.x end of life (2026-11-09) |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Check ID **DEP-06** is retired (plan DEC-4) and must never be reused; a future license check gets a new ID.
- Level: `REVIEW` for practice elements (OWASP uses no RFC keywords in these sections); `LIFECYCLE` for lifecycle rows (verdict from the date rule in `SKILL.md` step 5).
- Primary anchor first; list every absorbed anchor so coverage stays auditable.
- Keep rows to one line (≈ 200 characters where possible; lifecycle catch-all rows may be longer).
- Every OTT, OCS, NET, NFX, JDK, SPR, PY, NODE and EXP ID must be listed by exactly one active check in `../checklist.md` (the lifecycle IDs all belong to DEP-04).
- New release lines get **new** IDs (next free number per prefix, so IDs need not be in version order). When a line reaches end of life, mark its row `(retired)` and add the line (with its date) to the product's catch-all row (NET-05, NFX-05, JDK-08, SPR-04, SPR-07, PY-07, NODE-05).
- Pre-release rows (status "pre-release …") must say so in "Status at snapshot": `SKILL.md` routes them to DEP-09. Update the status when the line goes GA.
- Ownership: provenance, signing and CI/CD hardening: `review-software-lifecycle` SL-05/09/10; lock files: DEP-02 sole owner (TF-02 no longer judges them).
- Don't add elements for CI/CD hardening, workflow pinning, provenance or signing (review-software-lifecycle SL-05/09/10), binaries not referenced by a manifest (SL-12), unsafe use of parsers/serializers/loggers (security skills), install commands in CI (SL-10, OSC-13) or licence files (review-maintainability MAINT-10). See `SKILL.md` step 9.
- Lifecycle files are split **by language** (matching `compliance-review-core/references/languages.md` ids), not by website. A new detected language gets a new `lifecycle-<id>.md` and a line in `SKILL.md`.

## Refresh procedure

1. **Cadence:** quarterly for the lifecycle files, and within two weeks of each scheduled vendor event: .NET GA (November), Java GA (March/September), Python GA (October), Spring Boot/Framework releases (May/November). OWASP file: quarterly, or when run notes contain ≥ 3 `localized-standard-gap` or any `localized-standard-stale` entry for this skill.
2. **Detect drift:**
   - OWASP: compare the latest commit SHAs of the three pinned Markdown files (`https://api.github.com/repos/OWASP/Top10/commits?path=2025/docs/en/A03_2025-Software_Supply_Chain_Failures.md&per_page=1`, `https://api.github.com/repos/OWASP/CheatSheetSeries/commits?path=cheatsheets/<name>.md&per_page=1`) with the pinned SHAs. If they differ, diff the text and the anchor lists. Also check whether a newer OWASP Top 10 edition renumbers A03.
   - .NET: diff `releases-index.json` (`channel-version`, `support-phase`, `eol-date`) against the rows.
   - .NET Framework, Adoptium, Python devguide: re-fetch the page and diff its lifecycle table against the rows.
   - Spring: diff `https://api.spring.io/projects/<spring-boot|spring-framework>/generations` (`ossSupportEndDate`, `commercialSupportEndDate`, `initialReleaseDate`) against the rows. The spring.io pages render the table client-side; use the API.
3. **Update:** add new release lines (new IDs only), move ended lines into the catch-all row (mark the old row `(retired)`), keep each site ≤ 100 elements. Update the coverage map below, the "Localized"/retrieved dates in the file headers, `../sources.md`, and the URL list in `compliance-review-core/references/approved-sources.md` if a page moves.
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo).
   - Script-check: the checklist mapping rule above holds (every element ID in exactly one active check; DEP-06 has no elements); every listed anchor exists as an `id` on its published page; every A03 Description / How-to-prevent bullet, every H2/H3/H4 anchor of both cheat sheets and every vendor release line appears in the coverage map below — zero unaccounted.
   - Run a review against small sample repos (plan §9 step 8): `validate` passes, `21-review-dependency-management.json` has `urlsFetched: []`, 8 active checks and no DEP-06 entry, DEP-03 N/A without analyzers, expected DEP-04 findings, citations use pinned URLs and element IDs.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-dependency-management` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Refresh due (scheduled vendor events after the initial snapshot)

- **On or after 2026-11-10:** .NET 8.0 and 9.0 reach end of support. NET-03/NET-04 already carry `2026-11-10`, so the date rule fails them automatically from 2026-11-11; at the next refresh mark them `(retired)` and fold them into NET-05.
- **.NET 11 GA (expected 2026-11):** update NET-01 status from pre-release to active and add its support-end date from `releases-index.json`.
- **2026-11-30:** Spring Boot 4.2 and Spring Framework 7.1 GA. Update SPR-01/SPR-05 status from pre-release to supported.
- **2026-12-31:** Spring Boot 4.0 OSS support ends (SPR-03): fold into SPR-04 at the next refresh.
- **2027-04-22:** Node.js 27 release (NODE-01: pre-release → current); Node.js 28 alpha expected. **2027-04-30:** Node.js 22 end of life (NODE-04 → fold into NODE-05).
- **2027-01-12:** .NET Framework 4.6.2 ends (NFX-03): fold into NFX-05.

## Localization log

### 2026-11-07 — initial localization

- Snapshot taken twice on 2026-11-07: once for planning (plan DEC-7) and once at implementation (user-approved; the user chose to implement before 2026-11-10 and log the pending .NET/Spring events above instead of waiting). No differences between the two snapshots.
- Pins: `OWASP/Top10` `2025/docs/en/A03_2025-Software_Supply_Chain_Failures.md` @ `d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966` (2025-12-24); `OWASP/CheatSheetSeries` `cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.md` @ `b724e32f29a1d7e1c966943f7b30e3b776d46bfe` (2026-10-04); `cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.md` @ `995524d4a18e64672c80c8e13869d29ef850bd43` (2026-10-03).
- Lifecycle data as retrieved 2026-11-07: `releases-index.json` (latest 10.0.14, 9.0.22, 8.0.33, 11.0.0-rc.3); .NET Framework lifecycle table (end dates shown as `… 6:59:59 AM` UTC, recorded as the preceding Pacific date, e.g. 4.6.2 → 2027-01-12); Temurin roadmap (latest Java 27 jdk-27+35); Spring generations API; Python devguide versions table.
- Script verification: every element anchor exists as an `id` on its published page (`a03`: description, how-to-prevent; `vdm`: context, cases, case-1, case-2, case-3, case-5, tools, remark-about-the-security-issue-handling-decision; `sscs`: assess-suppliers, understand-and-monitor-software-dependencies, lockfileversion-pinning, inventory-build-tools, enforce-code-signing, use-private-artifact-repository; `dotnet`: lifecycle, previews, whats-covered; `netfx`: support-dates; `temurin`: release-roadmap; `pyver`: supported-versions, unsupported-versions). Checklist mapping: 57 element IDs, each in exactly one active check.
- Corrections while checking rows against the source:
  - OTT-01 also absorbs the How-to-prevent bullet "Continuously inventory the versions of … components … and their dependencies".
  - Catch-all rows now carry each ended line's date (the plan's §6 listed only some), e.g. NET-05, JDK-08, SPR-04, SPR-07, PY-07.
  - Spring citation bases are the project pages without fragment; the anchor `support` is appended like every other source. The pages render the Support tab client-side: `#support` exists as the tab link (`href="#support"`) on both pages, not as a static `id`; it was checked that way on 2026-11-07.

### 2026-11-09 — JavaScript/TypeScript lifecycle (afterplanning WP-12f phase 2)

- `lifecycle-javascript.md`: Node.js lines from `https://raw.githubusercontent.com/nodejs/Release/main/schedule.json`
  (citation: the `nodejs/Release` README tables `#release-schedule`, `#end-of-life-releases`), and Express 2.x/3.x
  end of life from expressjs.com (no date given; any use fails DEP-04). Closes dependency-management C-8.

## Open items

- Follow-ups outside this skill: reviewed and closed in the cross-skill follow-up pass of 2026-11-09. Open hand-offs: none.

## `localized-standard-gap` / `localized-standard-stale` log

_No entries yet._ Record each gap or stale note reported in run notes here (date, run ID, description, action taken).

## Coverage map

Reason codes for "not localized":
- **ORG** — organizational or process practice; not observable in manifests or package config.
- **CICD** — CI/CD, build-environment or release control; likely owned by `review-software-lifecycle` / `review-security-operational` (plan §10 C-4).
- **SEC** — owned by the security skills (A02, A08, SAST, access control).
- **CTX** — context, background or reference material; no requirement.
- **PARENT** — heading whose content is in the subsections listed beneath it.
- **SEL** — not selected by plan DEC-3/DEC-4 (provenance/SLSA, licenses).
- **RT** — runtime / deployed-artifact scanning; outside the manifest scope.

### A03:2025 — "You are likely vulnerable if" (a03#description)

| Bullet | Covered by / reason |
|---|---|
| Don't track versions of all components incl. transitive | OTT-01 |
| Software vulnerable, unsupported or out of date (OS, server, DBMS, runtimes, libraries) | OTT-02 (runtimes/frameworks); OS/DBMS/server outside manifest scope |
| Don't scan regularly / subscribe to bulletins | OTT-03 |
| No change management / tracking of the supply chain | ORG |
| Supply chain not hardened (access control, least privilege) | CICD / SEC |
| No separation of duty | ORG / CICD |
| Components from untrusted sources reach production | OTT-06 |
| Don't fix or upgrade in a risk-based, timely fashion | OTT-09 |
| Developers don't test compatibility of updated libraries | CICD (testing owned by `review-testing`) |
| Configurations not secured (A02) | SEC |
| CI/CD weaker than the systems it builds | CICD |

### A03:2025 — How to prevent (a03#how-to-prevent)

| Bullet | Covered by / reason |
|---|---|
| Centrally generate and manage the SBOM | OTT-04 |
| Track transitive dependencies | OTT-01 |
| Reduce attack surface (remove unused dependencies, features, files) | OTT-05 |
| Continuously inventory component versions (Dependency Track/Check, retire.js) | OTT-01 |
| Continuously monitor CVE/NVD/OSV; automate with SCA; subscribe to alerts | OTT-03 |
| Only obtain components from official sources over secure links; prefer signed packages | OTT-06 |
| Deliberately choose versions; upgrade only when needed | OTT-07 |
| Monitor unmaintained libraries; migrate or virtual-patch | OTT-08 |
| Update CI/CD, IDE and developer tooling regularly | CICD |
| Staged rollouts / canary deployments | CICD |
| Change-management tracking list (CI/CD settings, repos, sandboxes, IDEs, SBOM tooling, logs, SaaS, artifact repos, registries) | ORG |
| Harden code repo, workstations, build server, artifacts, IaC | CICD / SEC |
| Ongoing plan for monitoring, triaging and applying updates | ORG |

### A03:2025 — other anchors

| Anchor | Covered by / reason |
|---|---|
| a03#a032025-software-supply-chain-failures | PARENT |
| a03#background | CTX |
| a03#score-table | CTX |
| a03#example-attack-scenarios | CTX |
| a03#references | CTX |
| a03#list-of-mapped-cwes | CTX |

### Vulnerable Dependency Management Cheat Sheet (vdm) — every H1–H4 anchor

| Anchor | Covered by / reason |
|---|---|
| vdm#vulnerable-dependency-management-cheat-sheet | PARENT |
| vdm#introduction | CTX |
| vdm#context | OCS-01 |
| vdm#remark-about-the-detection | ORG (disclosure types) |
| vdm#1-responsible-disclosure | ORG |
| vdm#2-full-disclosure | ORG |
| vdm#remark-about-the-security-issue-handling-decision | OCS-04 (documented risk acceptance; the CRO/CISO decision itself is ORG) |
| vdm#cases | OCS-02 |
| vdm#case-1 | OCS-03 |
| vdm#context_1, vdm#ideal-condition-of-application-of-the-approach, vdm#approach | OCS-03 (subsections of case-1) |
| vdm#case-2 | OCS-04 |
| vdm#context_2, vdm#ideal-condition-of-application-of-the-approach_1, vdm#approach_1 | OCS-04 (scoped suppression); workaround/wrapper code is application code → ORG |
| vdm#case-3 | OCS-05 |
| vdm#context_3, vdm#ideal-condition-of-application-of-the-approach_2, vdm#approach_2 | OCS-05 |
| vdm#case-4 | ORG (pentest / full-disclosure handling) |
| vdm#context_4, vdm#ideal-condition-of-application-of-the-approach_3, vdm#approach_3 | ORG |
| vdm#case-5 | OCS-06 (also absorbed by OCS-05) |
| vdm#context_5, vdm#ideal-condition-of-application-of-the-approach_4, vdm#approach_4 | OCS-06 |
| vdm#tools | OCS-07 |
| vdm#remediation-and-maintained-backports | ORG (vendor selection) |
| vdm#references | CTX |

### Software Supply Chain Security Cheat Sheet (sscs) — every H1–H4 anchor

| Anchor | Covered by / reason |
|---|---|
| sscs#software-supply-chain-security | PARENT |
| sscs#introduction | CTX |
| sscs#overview-of-threat-landscape | CTX |
| sscs#mitigations-and-security-best-practices | PARENT |
| sscs#general | PARENT |
| sscs#implement-strong-access-control | SEC |
| sscs#logging-and-monitoring | SEC / CICD |
| sscs#leverage-security-automation | CICD |
| sscs#mitigating-source-code-threats | PARENT |
| sscs#peer-reviews | CICD (owned by `review-software-lifecycle`) |
| sscs#secure-config-of-version-control-systems | CICD |
| sscs#secure-development-platform | CICD / SEC |
| sscs#mitigating-dependency-threats | PARENT |
| sscs#assess-suppliers | OCS-08 (license-usage bullet → SEL, DEP-06 retired) |
| sscs#understand-and-monitor-software-dependencies | OCS-09, OCS-10 |
| sscs#sast | SEC |
| sscs#lockfileversion-pinning | OCS-11, OCS-12 |
| sscs#build-threats | PARENT |
| sscs#inventory-build-tools | OCS-15 |
| sscs#harden-build-tools | CICD |
| sscs#enforce-code-signing | OCS-14 |
| sscs#use-private-artifact-repository | OCS-13 |
| sscs#use-source-control-for-build-scripts-and-config | CICD |
| sscs#verify-provenanceensure-sufficient-metadata-is-generated | SEL (provenance/SLSA, DEC-3) |
| sscs#ephemeral-isolated-builds | CICD |
| sscs#limit-use-of-parameters | CICD |
| sscs#deployment-and-runtime-threats | PARENT |
| sscs#scan-final-build-binary | RT |
| sscs#monitor-deployed-software-for-vulnerabilities | RT |
| sscs#references | CTX |

### Lifecycle — every vendor release line

| Source | Release line(s) | Row |
|---|---|---|
| releases-index.json | 11.0 | NET-01 |
| releases-index.json | 10.0 | NET-02 |
| releases-index.json | 9.0 | NET-03 |
| releases-index.json | 8.0 | NET-04 |
| releases-index.json | 7.0, 6.0, 5.0, 3.1, 3.0, 2.2, 2.1, 2.0, 1.1, 1.0 | NET-05 |
| dotnet#whats-covered | ASP.NET Core / EF Core / Microsoft.Extensions packages | NET-06 |
| netfx#support-dates | 4.8.1, 4.8 | NFX-01 |
| netfx#support-dates | 4.7.2, 4.7.1, 4.7 | NFX-02 |
| netfx#support-dates | 4.6.2 | NFX-03 |
| netfx#support-dates | 3.5 SP1 | NFX-04 |
| netfx#support-dates | 4.6.1, 4.6, 4.5.2, 4.5.1, 4.5, 4.0, 3.0, 2.0 | NFX-05 |
| temurin#release-roadmap | 27 | JDK-01 |
| temurin#release-roadmap | 25 | JDK-02 |
| temurin#release-roadmap | 21 | JDK-03 |
| temurin#release-roadmap | 17 | JDK-04 |
| temurin#release-roadmap | 11 | JDK-05 |
| temurin#release-roadmap | 8 | JDK-06 |
| temurin#release-roadmap | 26 | JDK-07 |
| temurin#release-roadmap | 24, 23, 22, 20, 19, 18, 16 | JDK-08 |
| api.spring.io spring-boot | 4.2.x | SPR-01 |
| api.spring.io spring-boot | 4.1.x | SPR-02 |
| api.spring.io spring-boot | 4.0.x | SPR-03 |
| api.spring.io spring-boot | 3.5.x, 3.4.x, 3.3.x, 3.2.x, 3.1.x, 3.0.x, 2.7.x, 2.6.x, 2.5.x, 2.4.x, 2.3.x, 2.2.x, 2.1.x, 2.0.x, 1.5.x | SPR-04 |
| api.spring.io spring-framework | 7.1.x | SPR-05 |
| api.spring.io spring-framework | 7.0.x | SPR-06 |
| api.spring.io spring-framework | 6.2.x, 6.1.x, 6.0.x, 5.3.x, 5.2.x, 5.1.x, 5.0.x, 4.3.x | SPR-07 |
| pyver#supported-versions | main (3.16) | PY-01 |
| pyver#supported-versions | 3.15 | PY-02 |
| pyver#supported-versions | 3.14 | PY-03 |
| pyver#supported-versions | 3.13 | PY-04 |
| pyver#supported-versions | 3.12 | PY-05 |
| pyver#supported-versions | 3.11 | PY-06 |
| pyver#unsupported-versions | 3.10, 3.9, 3.8, 3.7, 3.6, 3.5, 3.4, 3.3, 3.2, 3.1, 3.0, 2.7, 2.6 | PY-07 |

### Not localized (lifecycle)

| Item | Reason / follow-up |
|---|---|
| Oracle Java SE Support Roadmap | DEC-5: Temurin is the baseline. Follow-up option: Oracle dates as a note when a target documents an Oracle subscription. |
| Django, Flask, FastAPI | Not selected (DEC-5). Follow-up option: Django (≈ 6 elements, djangoproject.com). |
| Node.js, Go, Ruby, … | Not a detected language in `languages.md`. |
| Container base images, OS, databases | Outside the manifest file list. |
| CVE/NVD/OSV/GitHub Advisory data | DEC-2: approved analyzers only. |
| SPDX License List | DEC-4: DEP-06 retired; a future license check needs a new ID. |
