# Maintenance — Software Lifecycle localized standards

**Maintainers only. Workers never load this file.** Background and design decisions:
`docs/plan_localize-review-software-lifecycle.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1). github.com is also used by `review-api-design` as a
maintenance URL; the budgets are separate. csrc.nist.gov and nvlpubs.nist.gov count as one website (nist.gov).

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| semver.org | semver.md | 11 | 100 | Semantic Versioning 2.0.0 |
| nist.gov | nist-ssdf.md | 19 | 100 | SP 800-218 SSDF v1.1 PDF (Table 1, PDF pages 15–28) |
| slsa.dev | slsa.md | 14 | 100 | v1.2: build-requirements, build-track-basics, source-requirements, distributing-provenance |
| github.com | openssf-scorecard.md | 21 | 100 | ossf/scorecard `docs/checks.md` @ v5.6.0 (9 of 20 checks) |
| learn.microsoft.com | azure-waf-safe-deployment.md | 1 | 100 | WAF OE:11 `operational-excellence/safe-deployments` (SDP-01, 2026-11-09) |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Check IDs **SL-06**
  and **SL-08** are retired (plan DEC-4) and must never be reused.
- Primary anchor first; list every absorbed anchor so coverage stays auditable.
- Every SV, SSDF, SLSA, OSC and SDP ID must be listed by exactly one active check in `../checklist.md`.
- SemVer items have no anchors of their own: cite the section anchor and name the item ("item 6") in the row.
- SSDF rows name their task IDs in the requirement text and cite the **physical** PDF page (`#page=N`), not the
  printed page number.
- Level: the source's RFC 2119 keyword (SemVer, SLSA) or `REVIEW` (SSDF, Scorecard). Levels never change severity
  (plan DEC-13).
- Keep rows to one line (≈ 200 characters where possible).
- `../lifecycle-signals.md` is a lookup table: extend it freely when a review logs an unrecognized platform, tool,
  action, setting or version scheme. No source refresh is needed for that.

## Pins and watch items

- **SSDF:** pinned to v1.1 (SP 800-218 final, Feb 2022). **Watch** SP 800-218 Rev. 1 (SSDF v1.2), initial public draft
  2025-12-17, comments closed 2026-01-30; `https://csrc.nist.gov/pubs/sp/800/218/r1/final` returned 404 on
  2026-11-09. When it is final: re-pin (plan DEC-7), re-map task IDs, re-check PDF pages, record new/renamed tasks.
- **SLSA:** pinned to v1.2 (`releases/v1.2` @ ae7fc7621500, 2026-04-14). `https://slsa.dev/spec/` redirected to
  `/spec/v1.2/` on 2026-11-09. Re-pin when the redirect target changes.
- **Scorecard:** pinned to release v5.6.0 (2026-10-12). `main` @ 2ef237f4e967 (2026-10-28) already differs in three
  places; adopt them at the next release (plan DEC-12):
  1. Immutable GitHub release tags count as pinned → OSC-11 should accept them.
  2. Merge queues satisfy "up to date before merging" → OSC-02 should accept them.
  3. Azure DevOps branch-protection notes were added → review `../lifecycle-signals.md` §3.
- **SemVer:** `https://semver.org/` serves 2.0.0. A SemVer 3.0.0 release would be a re-pin.

## Scorecard risk labels (explain the check severities, plan DEC-15)

| Scorecard check | Risk | Lifecycle check (default severity) |
|---|---|---|
| Dangerous-Workflow | Critical | SL-09 (Error) |
| Branch-Protection | High | SL-04 (Warning) |
| Token-Permissions | High | SL-10 (Warning) |
| Signed-Releases | High | SL-05 (Information) |
| Binary-Artifacts | High | SL-12 (Information: a file review can't tell committed from local files) |
| Pinned-Dependencies | Medium | SL-10 (Warning) |
| SAST | Medium | SL-11 (Warning) |
| Security-Policy | Medium | SL-07 (Information) |
| Packaging | Medium | SL-02 (Warning) |
| CI-Tests | Low | SL-01 (Error, from SSDF/SLSA) |

## Refresh procedure

1. **Cadence:** every six months. Refresh earlier on any trigger below, or when run notes contain ≥ 3
   `localized-standard-gap` entries for this skill.
2. **Drift checks:**
   - SSDF: check `https://csrc.nist.gov/pubs/sp/800/218/final` for a supersession notice and whether `…/r1/final`
     exists.
   - SLSA: check where `https://slsa.dev/spec/` redirects. If newer than v1.2, diff the four localized pages between
     release branches (`https://api.github.com/repos/slsa-framework/slsa/commits`) and update anchors and levels.
   - Scorecard: check `https://api.github.com/repos/ossf/scorecard/releases/latest`. For a new tag, diff
     `docs/checks.md` against v5.6.0; adopt the `main` differences above and any new or renamed check.
   - SemVer: confirm `https://semver.org/` still serves 2.0.0 (`https://api.github.com/repos/semver/semver/commits`).
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep each website ≤ 100 elements.
   Update the coverage map, the header pins and dates, `../sources.md`, and the URL list in
   `compliance-review-core/references/approved-sources.md` if a page moves.
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo).
   - Script-check: every element ID is in exactly one active check of `../checklist.md`; every listed anchor exists
     on its pinned page; every SSDF row names a task on the cited PDF page; every SemVer item/FAQ anchor, SSDF task
     ID, SLSA requirement anchor and Scorecard check appears in the coverage map below — zero unaccounted.
   - Run a review against small sample repos (plan §11 step 8): `validate` passes, `11-review-software-lifecycle.json`
     has `urlsFetched: []`, 10 active checks and no SL-06/SL-08 entries, citations use pinned URLs and element IDs.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-software-lifecycle` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-09 — initial localization

- Written from the **planning snapshot** of 2026-11-09 (plan DEC-3). The implementation re-snapshot (plan §11 step 1)
  was **not** taken: on 2026-11-09 the user chose to implement from the plan as-is, without further fetches. Pins,
  anchors and PDF pages are exactly those recorded in plan §5–§8; the verifications in "Open items" are outstanding.
- Plan decisions: DEC-2 … DEC-9 confirmed by the user on 2026-11-09 during planning; the SL-08 retirement (DEC-4)
  was re-confirmed at implementation. DEC-10 … DEC-16 are planning defaults.
- Defects fixed: the old nist.gov landing page for SP 800-218 (under `www.nist.gov/itl/executive-order-14028-…`)
  returned HTTP 404 on 2026-11-09 and is no longer cited anywhere in the skill; SLSA v1.0 `requirements` citations
  replaced by v1.2 pages (`/spec/` → `/spec/v1.2/` redirect).
- Checklist mapping checked by script on 2026-11-09: 65 element IDs (11 SV, 19 SSDF, 14 SLSA, 21 OSC), each in exactly
  one active check.
- Plan §11 step 8 (sample-repo review runs) was skipped by user decision on 2026-11-09 and remains open.

### 2026-11-09 — staged rollouts (afterplanning WP-12c)

- SDP-01 added under SL-02 (check count unchanged) from WAF OE:11 `operational-excellence/safe-deployments`
  (`ms.date` 2026-02-11, `git_commit_id` a3fa10710fd98dabc8074a51d946c25b95c1a8bb, fetched 2026-11-09). User chose OE:11
  over the A03:2025 text pinned by dependency-management. Closes dependency-management C-4 and lifecycle C-4 (staged
  rollout part). Anchors from the page's heading text (Learn slugs); confirm against HTML ids on the first refresh.
- Not localized from OE:11: bake time in hours/days, health-model halting, emergency SDP protocols, safe decommissioning
  and blameless postmortems (ORG; not visible as pass/fail in a repo); branching strategy (OWN-MAINT); feature-flag
  service choice (TOOL).

## Open items

- Plan §10 follow-ups (changes outside this skill): reviewed and closed by `docs/plan_localize-afterplanning-changes.md` on 2026-11-09 (see its Appendix A). Open hand-offs: none.
1. Re-take the snapshot (plan §11 step 1) and verify: SemVer anchors; SSDF physical PDF pages per task; SLSA v1.2
   anchors at `releases/v1.2`; Scorecard anchors at v5.6.0 (and whether a newer release exists).
2. Script-check the coverage map below against the published heading/anchor lists (it was built from the plan, not
   from a heading dump). In particular enumerate the 7 SSDF v1.1 "moved" placeholders by ID, and the full SLSA
   requirement-anchor list of the four localized pages.
3. Check each name in `../lifecycle-signals.md` once against current vendor documentation (plan §11 step 4).
4. Run the plan §11 step 8 sample-repo reviews.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Coverage map

**Status: built from the plan's 2026-11-09 planning snapshot (plan §5–§9); not yet script-checked** (see "Open
items").

Reason codes for "not localized":
- **ORG** — organizational or process practice; not visible in a repository.
- **OWN-<subject>** — owned by another subject skill (TST testing, DEP dependency management, MAINT maintainability,
  SEC security skills, ARCH architecture/software quality).
- **GIT** — needs Git history, forge activity or forge APIs (forbidden).
- **VENDOR** — requirement on a build-platform or SCS vendor, not the producer.
- **CTX** — background, explanation or cross-reference; no requirement.
- **FU** — follow-up candidate (plan §9).

### semver.org

| Item / anchor | Covered by / reason |
|---|---|
| Item 1 (declare public API) | SV-02 |
| Item 2 (X.Y.Z form, numeric increase) | SV-01, SV-06 |
| Item 3 (released versions immutable) | SV-03 |
| Items 4, 5 (0.y.z, 1.0.0 defines public API) | SV-04 |
| Items 6–8 (patch/minor/major semantics, resets) | SV-05, SV-06 |
| Item 9 (pre-release) | SV-07 |
| Item 10 (build metadata) | SV-08 |
| Item 11 (precedence) | CTX (tool comparison rule; syntax covered by SV-07/SV-08) |
| BNF grammar | SV-01 (secondary anchor); also summarized by SV-07/SV-08 |
| FAQ: 0.y.z revisions in initial development | SV-04 |
| FAQ: how do I know when to release 1.0.0 | SV-04 |
| FAQ: documenting the entire public API is too much work | SV-02 |
| FAQ: accidentally released a breaking change as a minor version | SV-10 |
| FAQ: how should I handle deprecating functionality | SV-09 |
| FAQ: is "v1.2.3" a semantic version | SV-11 |
| FAQ: rapid development and fast iteration | CTX |
| FAQ: won't I end up at 42.0.0 | CTX |
| FAQ: updating my own dependencies without changing the public API | CTX |
| FAQ: inadvertently altering the public API | CTX (judgement on intent; not observable) |
| FAQ: size limit on the version string | CTX |
| FAQ: suggested regular expression | CTX (summarized by SV-01/SV-07/SV-08) |
| About, License | CTX |

### nist.gov — SSDF v1.1 tasks (42 active)

| Task | Covered by / reason |
|---|---|
| PO.1.1, PO.1.2, PO.1.3 | ORG (security requirements) |
| PO.2.1, PO.2.2, PO.2.3 | ORG (roles, training, management commitment) |
| PO.3.1 | SSDF-01 |
| PO.3.2 | SSDF-01 (ex. 3), SSDF-03 (ex. 4), SSDF-05 (ex. 5, 7) |
| PO.3.3 | SSDF-08 |
| PO.4.1 | SSDF-06 |
| PO.4.2 | SSDF-07 (ex. 1, 3), SSDF-08 (ex. 4) |
| PO.5.1 | SSDF-02 (ex. 4), SSDF-09 (ex. 2, 5) |
| PO.5.2 | ORG (developer endpoint hardening) |
| PS.1.1 | SSDF-10 (ex. 1, 4), SSDF-11 (ex. 3), SSDF-12 (ex. 5, 6) |
| PS.2.1 | SSDF-12 |
| PS.3.1 | SSDF-13 |
| PS.3.2 | SSDF-14 |
| PW.1.1, PW.1.2, PW.1.3 | OWN-ARCH / OWN-SEC (secure design) |
| PW.2.1 | OWN-ARCH / OWN-SEC (design review) |
| PW.4.1, PW.4.2, PW.4.4 | OWN-DEP (third-party components) |
| PW.5.1 | OWN-SEC / OWN-ARCH (secure coding) |
| PW.6.1 | SSDF-04 |
| PW.6.2 | SSDF-04 (ex. 1, 2, 7), SSDF-02 (ex. 3) |
| PW.7.1 | SSDF-15 |
| PW.7.2 | SSDF-15 (ex. 1, 3), SSDF-16 (ex. 4, 6) |
| PW.8.1, PW.8.2 | OWN-TST (STS-08 … STS-12; plan C-3) |
| PW.9.1, PW.9.2 | OWN-SEC (secure defaults) |
| RV.1.1 | SSDF-17 |
| RV.1.2 | ORG (vulnerability analysis) |
| RV.1.3 | SSDF-17 (ex. 1), SSDF-18 (ex. 2, 3) |
| RV.2.1 | ORG |
| RV.2.2 | SSDF-19 (ex. 3); other examples ORG |
| RV.3.1, RV.3.2, RV.3.3, RV.3.4 | ORG (root-cause analysis) |
| 7 "moved" placeholders (e.g. PW.3 and its tasks, moved to PW.4) | CTX — enumerate by ID at the first script check (Open item 2) |
| Task references (BSIMM, EO 14028, …) | CTX |

### slsa.dev — v1.2 pages

| Page / anchor | Covered by / reason |
|---|---|
| br#choose-an-appropriate-build-platform, br#hosted | SLSA-01 |
| br#follow-a-consistent-build-process | SLSA-02 |
| br#provenance-exists | SLSA-03 |
| br#provenance-authentic | SLSA-04 |
| br#provenance-unforgeable, br#isolated | SLSA-05 |
| br#distribute-provenance | SLSA-06 |
| br#security-best-practices | SLSA-08 |
| br — other build-platform requirements (provenance generation internals, isolation mechanics) | VENDOR |
| btb#build-l1-provenance-exists | SLSA-03 |
| btb#build-l2-hosted-build-platform | SLSA-01, SLSA-04 |
| btb#build-l3-hardened-builds | SLSA-05 |
| btb — L0 and introductory sections | CTX |
| sr#level-1-version-controlled, sr#choose-scs | SLSA-09 |
| sr#access-and-history, sr#identity-management | SLSA-10, SLSA-12 |
| sr#history | SLSA-11 |
| sr#technical-controls, sr#level-3-continuous-technical-controls | SLSA-13 |
| sr#two-party-review, sr#level-4-two-party-review | SLSA-14 |
| sr — repository/revision IDs, human-readable diffs, Source VSA, source provenance attestations, continuity, safe expunging | VENDOR |
| dp#where-attestations-are-published | SLSA-06 |
| dp#relationship-between-releases-and-attestations, dp#immutability-of-attestations | SLSA-07 |
| dp — other sections | CTX |
| `verifying-artifacts` (page not localized) | FU (≈ 3 elements; possible overlap with DEP-08, plan C-4) |
| `threats`, `attestation-model`, `terminology`, `principles`, `faq`, `future-directions` | CTX |

### github.com — Scorecard v5.6.0 checks (20)

| Check (anchor) | Covered by / reason |
|---|---|
| Binary-Artifacts (`binary-artifacts`) | OSC-21 |
| Branch-Protection (`branch-protection`) | OSC-01 … OSC-05 (admin-token notes: CTX) |
| CI-Tests (`ci-tests`) | OSC-06 (whether tests run: OWN-TST, TST-06) |
| CII-Best-Practices (`cii-best-practices`) | GIT (external badge) |
| Code-Review (`code-review`) | GIT (commit history); required-review settings via OSC-02/OSC-05 |
| Contributors (`contributors`) | GIT |
| Dangerous-Workflow (`dangerous-workflow`) | OSC-07, OSC-08 |
| Dependency-Update-Tool (`dependency-update-tool`) | OWN-DEP (DEP-07; SL-06 retired) |
| Fuzzing (`fuzzing`) | OWN-TST / FU (plan C-3) |
| License (`license`) | FU (no subject owns it; plan C-5) |
| Maintained (`maintained`) | GIT |
| Packaging (`packaging`) | OSC-20 |
| Pinned-Dependencies (`pinned-dependencies`) | OSC-11, OSC-12, OSC-13 (application manifests and lock files: OWN-DEP, DEP-01/02) |
| SAST (`sast`) | OSC-14 |
| SBOM (`sbom`) | OWN-DEP (DEP-05) |
| Security-Policy (`security-policy`) | OSC-15, OSC-16, OSC-17 |
| Signed-Releases (`signed-releases`) | OSC-18, OSC-19 (scoring mechanics: CTX) |
| Token-Permissions (`token-permissions`) | OSC-09, OSC-10 |
| Vulnerabilities (`vulnerabilities`) | OWN-DEP (DEP-03, analyzer-only) |
| Webhooks (`webhooks`) | GIT (forge settings) |
