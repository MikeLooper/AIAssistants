# Maintenance — Disaster Recovery localized standards

**Maintainers only. Workers never load this file.** Background and design decisions: `docs/plan_localize-review-disaster-recovery.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1).

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| learn.microsoft.com (azure/well-architected) | azure-well-architected-reliability-dr.md | 46 | 100 | 8 pinned pages |
| nvlpubs.nist.gov / csrc.nist.gov | nist-sp-800-34-contingency-planning.md | 25 | 100 | SP 800-34 Rev. 1, chapters 3–5 and the Appendix A plan structure |
| cheatsheetseries.owasp.org | owasp-secrets-backup.md | 1 | 100 | Secrets Management Cheat Sheet §2.9 (OSM-01, 2026-11-09) |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Prefixes are skill-specific (`WAFR-`, `SP34-`, `OSM-`; plan DEC-7) so they can't be confused with the cost skill's `WAF-xx` IDs or NIST SP 800-53 control IDs.
- Level: WAF elements are `REVIEW` (no normative keywords). NIST elements carry the source keyword of the summarized sentence (`SHOULD`, `MUST`) or `REVIEW`. The level never changes severity (plan DEC-8; `SKILL.md` step 8).
- Scope (WAF): `G` generic, `A` Azure-only. Keep wording cloud-neutral for `G` elements. Every `A` element needs a `G` counterpart (today: WAFR-05 → WAFR-01; WAFR-19 → WAFR-16/WAFR-28; WAFR-20 → WAFR-16; WAFR-41 → WAFR-38).
- Primary anchor (or section) first; list every absorbed anchor so coverage stays auditable.
- NIST PDF page = physical page (printed page + 14 for chapters 1–5), as used in `#page=<n>`.
- Keep rows to one line (≈ 200 characters where possible).
- Every WAFR, SP34 and OSM ID must be listed by exactly one check in `../checklist.md`, and the WAF file's `## DR-xx` section and the NIST file's Check column must agree with it.
- DR is sufficiency-only (plan DEC-4): never add an element that fails over-provisioning. That belongs to `review-cost-sustainability` COST-08.
- Don't add elements for in-region HA, zones, instance counts or probes (review-reliability AZRL-27/29/48–51), alert rules on replication lag or backup failure (review-monitoring), resilience or chaos tests (review-testing TST-13) or live-store encryption and key management (review-security-operational). See `SKILL.md` step 10.

## Refresh procedure

1. **Cadence:** quarterly, or when run notes contain ≥ 3 `localized-standard-gap` entries for this skill.
2. **Detect drift:**
   - WAF: re-fetch each pinned page and compare its `ms.date` meta value with the header table of `azure-well-architected-reliability-dr.md`. A changed date means diffing that page's section text and anchor list. Also check the pillar TOC (`https://learn.microsoft.com/azure/well-architected/toc.json`) for added, removed or renamed Reliability pages and design guides (for example a new backup or DR design guide).
   - NIST: check the CSRC publication record (`https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final`) for a new revision (e.g. an SP 800-34 Rev. 2 draft or final) or a withdrawal notice. A new final revision means re-localizing from it under new pinned page numbers; existing SP34 IDs map to new rows or are retired.
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep each site ≤ 100 elements. Update the coverage map below, the page dates / PDF pages and retrieval date in each file header and in `../sources.md`, and the URL list in `compliance-review-core/references/approved-sources.md` if a page moves.
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo). Extract the PDF with `pdftotext -layout` so that form feeds separate physical pages.
   - Script-check: element IDs are contiguous; the checklist mapping rule above holds; every listed WAF anchor exists on its pinned page; every SP34 section heading appears on (or continues onto) its stated PDF page and the Level matches the source sentence; every content H2/H3/H4 anchor on the 8 WAF pages (boilerplate excluded, see below), each of the 20 `dg-dr` suggested-action rows and every numbered NIST section of chapters 1–5 and each appendix appear in the coverage map below, with zero unaccounted.
   - Run a review against small sample repos with IaC: Azure Bicep with a stated tier; non-Azure Terraform/Kubernetes with no stated tier; a repo with a database but no backup config. Expect: `validate` passes; `24-review-disaster-recovery.json` has `urlsFetched: []`; all 9 checks present; citations use pinned URLs and element IDs; Scope A skipped on non-Azure; DR-04/DR-08 N/A when no tier is stated; DR-01 fails (not N/A) on the no-backup variant.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-disaster-recovery` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-08 — initial localization

- Snapshot: planning snapshot 2026-11-07 (plan DEC-6); implementation snapshot 2026-11-08. No differences: all 8 WAF `ms.date` values match the header table; the NIST PDF is 150 pages; the CSRC record still shows "May 2010 (Updated 11/11/2010)", no newer revision and no withdrawal (its 2023-03-17 planning note only gives a contact address).
- Script verification: 115 content anchors on the 8 WAF pages, all accounted for; 20 `dg-dr` suggested-action rows, all accounted for; every element anchor exists on its pinned page; 75 NIST sections and appendices, all accounted for; 46 WAFR + 25 SP34 IDs each listed by exactly one check.
- Corrections while checking rows against the source (these take precedence over the plan's §5–§6 inventories):
  - WAFR-05: dropped "long-term retention" (not in the pinned text) and added `re-red#azure-facilitation`, the section that states PITR for PaaS data services.
  - WAFR-16: added `dg-az#synchronous-data-replication` and `dg-az#asynchronous-data-replication`, which it absorbs.
  - WAFR-22: added `dg-dr#suggested-actions-1` (row "Define manual failover runbook and criteria").
  - WAFR-35: added `dg-dr#suggested-actions-1` (row "Automate provisioning and prepare operations": CI/CD pipelines for both regions).
  - WAFR-40: added `dg-dr#suggested-actions-3` (rows "Configure secondary region at full capacity" and "Configure load distribution behavior").
  - SP34-01: §5.1.2 ("Data backups should be conducted on all systems on a regular basis") is on PDF page 58; the primary citation stays page 35 (§3.4.2).
  - SP34-11: PDF page 61 → **62** (the BIA/MTD sentence that sets the site type is at the end of §5.1.5 on page 62).
  - SP34-23: PDF page 43 → **44** (§3.5.4 starts at the foot of page 43; the per-impact exercise rules are on page 44).
  - SP34-06 keeps `MUST` ("the RTO must normally be shorter than the MTD", p. 31). SP34-02 keeps `SHOULD` ("the following questions should be considered", p. 59). SP34-18 keeps `SHOULD` for key separation, although the same paragraph says key management "must be established".
  - The plan's §7 lists did not name every anchor. The coverage map below adds the missing ones (parent headings, `dg-dr` tier subsections, `re-test#test-against-your-reliability-targets-end-to-end`, `re-test` parent and outage subsections, `dg-az` requirement subsections, `active-and-passive-regions`, and NIST §3.5.3, §4.2.3, §4.3.3, §4.5, §5.1.1) with reasons consistent with §7.

### 2026-11-09 — secret-store backup and break-glass (afterplanning WP-12e)

- OSM-01 added under DR-06 from OWASP Secrets Management Cheat Sheet §2.9 (`#29-downtime-break-glass-backup-and-restore`,
  commit d6474de095dedba6caf536fdf8926d6ae53f3cfc). Closes security-operational C-12 (DR part). Check count unchanged.
- The plan's "soft delete/purge protection" clause isn't in §2.9 (the sheet doesn't mention it), so OSM-01 leaves it
  out; soft delete of recovery assets in general stays under WAFR-28 … WAFR-32.

## Open items

- Plan §10 follow-ups (changes outside this skill): reviewed and closed by `docs/plan_localize-afterplanning-changes.md` on 2026-11-09 (see its Appendix A). Open hand-offs: none.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Shared pages

`re-check`, `re-prin` and `re-red` are also pinned by `review-reliability`. When either skill refreshes them, record the new metadata in both `MAINTENANCE.md` files. The cross-region sections of `re-red` are mapped here; the in-region sections are reliability's.

## Coverage map

Reason codes for "not localized":
- **REL**: in-region high availability (the `re-red` intra-region rows: `review-reliability` AZRL-27/29/48/51) and SLO composition (`review-reliability`); resilience and chaos testing: `review-testing` TST-13.
- **MON**: health modelling and target visualization. Owned by `review-monitoring` / `review-observability`.
- **COST**: cost proportionality. Owned by `review-cost-sustainability` (COST-07/COST-08, plan DEC-4).
- **PRIN**: pillar-wide principle; not DR-specific (only `#design-for-recovery` is localized).
- **ORG**: organizational practice; not visible in a workload repo.
- **FAC**: physical-facility control; owned by the cloud provider in cloud workloads.
- **PLAT**: on-premises platform technique (tape, RAID, leased lines, mainframe); the cloud-relevant ideas are in SP34-01, SP34-19, SP34-21.
- **TPL**: template or sample material.
- **SUPERSEDED**: refers to SP 800-53 Rev. 3, since replaced by Rev. 5.
- **BG**: background, definitions, examples or tool pointers.
- **PARENT**: parent heading whose substance is in its subsections (mapped separately).

### WAF — section anchors (8 pages)

Excluded as boilerplate on every page: `ms--in-this-article`, `ms--feedback`, `ms--additional-resources-mobile-heading`, `next-steps`, `related-links`, `reliability-checklist`.

**re-check** (1 anchors)

| Anchor | Mapped to |
|---|---|
| `checklist` | WAFR-12 |

**re-prin** (5 anchors)

| Anchor | Mapped to |
|---|---|
| `design-for-business-requirements` | not localized: PRIN |
| `design-for-resilience` | not localized: PRIN |
| `design-for-recovery` | WAFR-01, WAFR-29, WAFR-30 |
| `design-for-operations` | not localized: PRIN |
| `keep-it-simple` | not localized: PRIN |

**re-met** (15 anchors)

| Anchor | Mapped to |
|---|---|
| `set-availability-objectives` | not localized: REL |
| `consider-common-slos-and-influencing-factors` | not localized: REL |
| `determine-the-slo-scope` | not localized: REL |
| `define-composite-slo-targets` | not localized: REL |
| `assess-the-impact-of-microsoft-slas` | not localized: REL |
| `implement-multiregion-targets` | not localized: REL (multi-region SLO composition; DR posture is WAFR-15) |
| `define-recovery-metrics` | WAFR-12, WAFR-13 |
| `monitor-and-visualize-the-targets` | not localized: MON |
| `azure-facilitation` | not localized: BG (Azure tool pointers) |
| `example` | not localized: BG |
| `components` | not localized: BG |
| `calculate-a-composite-slo` | not localized: BG |
| `determine-the-overall-composite-slo-result` | not localized: BG |
| `set-the-workload-sla` | not localized: BG |
| `set-the-correctness-slo` | not localized: BG |

**re-red** (11 anchors)

| Anchor | Mapped to |
|---|---|
| `prefer-serverless-and-fully-managed-services-to-reduce-operational-burden` | not localized: REL |
| `build-redundancy-into-your-workload-with-multiple-component-instances` | not localized: REL |
| `use-the-deployment-stamps-pattern-to-streamline-your-redundancy-approach` | not localized: REL |
| `achieve-zero-downtime-through-active-active-redundancy` | not localized: REL (active-active posture is judged via the tier table, WAFR-15) |
| `use-an-active-passive-architecture-design-as-a-cost-effective-dr-approach` | WAFR-15, WAFR-38 |
| `distribute-workloads-across-proximate-independent-infrastructure` | not localized: REL |
| `strengthen-fault-tolerance-with-geo-distant-deployments` | WAFR-17 |
| `azure-facilitation` | WAFR-05, WAFR-20 |
| `dns-specific-azure-facilitation` | not localized: REL |
| `apply-delete-protection-to-preserve-redundancy` | WAFR-31 |
| `example` | not localized: BG |

**re-test** (17 anchors)

| Anchor | Mapped to |
|---|---|
| `define-reliability-testing-scope-based-on-service-types` | not localized: REL |
| `test-against-your-reliability-targets-end-to-end` | not localized: REL (flow-level recovery timing is reflected by WAFR-10 and WAFR-45) |
| `build-reliability-scenarios-from-critical-flows-and-failure-modes` | not localized: REL |
| `validate-your-fault-tolerance-and-recovery-mechanisms` | not localized: PARENT (subsections backup-and-restore and incidents-and-disaster-recovery-dr are localized; the rest REL) |
| `backup-and-restore` | WAFR-07, WAFR-08, WAFR-09, WAFR-10 |
| `transient-faults` | not localized: REL |
| `load-and-scaling-response` | not localized: REL |
| `dependency-failures` | not localized: REL |
| `self-preservation-and-recovery` | not localized: REL |
| `incidents-and-disaster-recovery-dr` | WAFR-40, WAFR-44, WAFR-45 |
| `test-and-assess-your-plan-with-tabletop-exercises` | WAFR-43 |
| `take-advantage-of-planned-and-unplanned-outages` | not localized: REL |
| `planned-maintenance` | not localized: REL |
| `unplanned-outage` | not localized: REL |
| `combine-different-types-of-tests` | not localized: REL |
| `use-fault-injection-and-chaos-engineering` | not localized: REL |
| `azure-facilitation` | not localized: BG (Azure tool pointers) |

**re-dr** (11 anchors)

| Anchor | Mapped to |
|---|---|
| `prioritize-by-business-impact` | WAFR-11, WAFR-12 |
| `define-disaster-thresholds` | WAFR-22 |
| `establish-communication-protocols` | WAFR-21, WAFR-26 |
| `design-recovery-aware-architecture` | WAFR-04, WAFR-16 |
| `prepare-infrastructure-and-recovery-procedures` | WAFR-14, WAFR-23, WAFR-24, WAFR-25, WAFR-34 |
| `implement-robust-backup-strategies` | WAFR-01, WAFR-03, WAFR-06, WAFR-28, WAFR-37 |
| `practice-with-regular-drills` | WAFR-43, WAFR-44, WAFR-45 |
| `keep-plans-current-and-actionable` | WAFR-46 |
| `ensure-accessibility-during-outages` | WAFR-27, WAFR-32, WAFR-35 |
| `automate-recovery-procedures-safely` | WAFR-33, WAFR-35, WAFR-36 |
| `azure-facilitation` | WAFR-05, WAFR-41 |

**dg-dr** (23 anchors)

| Anchor | Mapped to |
|---|---|
| `terminology` | not localized: BG |
| `what-is-disaster-recovery` | not localized: BG |
| `select-your-criticality-tier` | WAFR-11, WAFR-15 |
| `tier-0-mission-critical` | WAFR-15 (via parent `select-your-criticality-tier`; source of the SKILL.md tier table) |
| `tier-1-business-critical` | WAFR-15 (via parent `select-your-criticality-tier`; source of the SKILL.md tier table) |
| `tier-2-business-operational` | WAFR-15 (via parent `select-your-criticality-tier`; source of the SKILL.md tier table) |
| `tier-3-administrative` | WAFR-15 (via parent `select-your-criticality-tier`; source of the SKILL.md tier table) |
| `classify-your-workload` | WAFR-11, WAFR-46 |
| `watch-out-for-these-friction-points` | WAFR-14, WAFR-22, WAFR-24 |
| `optimize-your-recovery-costs` | not localized: COST |
| `document-your-dr-plan` | not localized: PARENT (introduces dr-communication-plan, dr-runbook, dr-escalation-plan; its activation narrative is WAFR-22) |
| `dr-communication-plan` | WAFR-22, WAFR-26 |
| `dr-runbook` | WAFR-21, WAFR-23, WAFR-24, WAFR-25, WAFR-27 |
| `dr-escalation-plan` | WAFR-26 |
| `test-regularly-and-improve-the-plan` | WAFR-09, WAFR-43, WAFR-45 |
| `recovery-strategy-for-backup-and-restore` | WAFR-01 |
| `suggested-actions` | WAFR-02, WAFR-03, WAFR-05, WAFR-06, WAFR-28 |
| `recovery-strategy-for-active-passive-cold-standby` | not localized: PARENT (intro to suggested-actions-1; posture via the tier table, WAFR-15) |
| `suggested-actions-1` | WAFR-07, WAFR-08, WAFR-10, WAFR-16, WAFR-18, WAFR-19, WAFR-20, WAFR-22, WAFR-33, WAFR-34, WAFR-35, WAFR-38, WAFR-40, WAFR-41, WAFR-42 |
| `recovery-strategy-for-active-passive-warm-standby` | not localized: PARENT (intro to suggested-actions-2; posture via the tier table, WAFR-15) |
| `suggested-actions-2` | WAFR-38, WAFR-39, WAFR-40 |
| `recovery-strategy-for-active-active-deployments` | not localized: PARENT (intro to suggested-actions-3; posture via the tier table, WAFR-15) |
| `suggested-actions-3` | WAFR-38, WAFR-40 |

**dg-az** (32 anchors)

| Anchor | Mapped to |
|---|---|
| `terminology` | not localized: BG |
| `understand-how-regions-and-availability-zones-are-organized-in-azure` | not localized: BG |
| `understand-shared-responsibilities` | not localized: BG |
| `identify-key-business-and-workload-requirements` | not localized: PARENT (requirement inputs; only data-residency is localized, WAFR-18) |
| `risk-tolerance` | not localized: REL |
| `reliability-requirements` | not localized: REL (recovery targets themselves are WAFR-11 and WAFR-12) |
| `service-level-objectives` | not localized: REL |
| `data-residency` | WAFR-18 |
| `user-location` | not localized: REL |
| `budget` | not localized: COST |
| `complexity` | not localized: REL |
| `example-scenario` | not localized: BG |
| `deployment-approach-1-locally-redundant-deployments` | not localized: REL (zone-level choice; its backup-across-regions subsection is localized) |
| `locally-redundant-deployments-with-backup-across-regions` | WAFR-02, WAFR-33, WAFR-35 |
| `deployment-approach-2-zonal-pinned-deployments` | not localized: REL (zone-level choice) |
| `deployment-approach-3-zone-redundant-deployments` | not localized: REL (zone-level choice; its backup-across-regions subsection is localized) |
| `zone-redundant-deployments-with-backup-across-regions` | WAFR-28 |
| `deployment-approach-4-multi-region-deployments` | WAFR-17 |
| `active-and-passive-regions` | not localized: PARENT (intro to data-replication and region-architectures; posture via the tier table, WAFR-15) |
| `data-replication` | WAFR-16 |
| `asynchronous-data-replication` | WAFR-16 |
| `synchronous-data-replication` | WAFR-16 |
| `region-architectures` | WAFR-19 |
| `combine-multi-zone-and-multi-region-approaches` | WAFR-15 |
| `how-azure-services-support-deployment-approaches` | not localized: BG |
| `use-case-examples` | not localized: BG |
| `line-of-business-application-for-an-enterprise` | not localized: BG |
| `internal-application` | not localized: BG |
| `legacy-application-migration` | not localized: BG |
| `healthcare-application` | not localized: BG |
| `banking-system` | not localized: BG |
| `software-as-a-service` | not localized: BG |

### WAF — `dg-dr` suggested-action rows (20)

Table rows have no anchors; they are keyed by table and row number.

| Table | # | Row (Action) | Mapped to |
|---|---|---|---|
| suggested-actions (backup and restore) | 1 | Configure backup policies and retention | WAFR-02, WAFR-03, WAFR-05, WAFR-28 |
| suggested-actions | 2 | Implement cost-effective storage tiers | not localized: COST |
| suggested-actions | 3 | Document restore procedures | WAFR-06 |
| suggested-actions | 4 | Monitor backup costs and compliance | WAFR-03 (retention compliance); cost parts not localized: COST |
| suggested-actions | 5 | Maintain and audit backup systems | not localized: ORG (quarterly audits, retiring systems); its RPO/RTO review step is reflected by WAFR-46 |
| suggested-actions-1 (cold standby) | 1 | Set up primary and secondary regions | WAFR-33, WAFR-34 |
| suggested-actions-1 | 2 | Set up cross-region data replication | WAFR-16, WAFR-19, WAFR-20, WAFR-42 |
| suggested-actions-1 | 3 | Secure DR environment and maintain compliance | WAFR-18, WAFR-34; audit-trail continuity not localized: MON |
| suggested-actions-1 | 4 | Automate provisioning and prepare operations | WAFR-33, WAFR-35, WAFR-40 |
| suggested-actions-1 | 5 | Monitor readiness and health | WAFR-42 |
| suggested-actions-1 | 6 | Configure load balancer with manual failover | WAFR-38, WAFR-41 |
| suggested-actions-1 | 7 | Define manual failover runbook and criteria | WAFR-22 |
| suggested-actions-1 | 8 | Test restore processes regularly | WAFR-07, WAFR-08, WAFR-10 |
| suggested-actions-2 (warm standby) | 1 | Configure secondary region at partial scale | WAFR-40 |
| suggested-actions-2 | 2 | Enable auto-scaling in secondary region | WAFR-40 |
| suggested-actions-2 | 3 | Configure automated failover procedures | WAFR-39 |
| suggested-actions-2 | 4 | Configure load balancer with auto failover | WAFR-38 |
| suggested-actions-3 (active-active) | 1 | Configure secondary region at full capacity | WAFR-40 |
| suggested-actions-3 | 2 | Configure load balancer to distribute traffic across active instances | WAFR-38 |
| suggested-actions-3 | 3 | Configure load distribution behavior | WAFR-40 (capacity under peer-region failure); network-partition behaviour not localized: REL |

### NIST SP 800-34 Rev. 1 — sections (chapters 1–5 and appendices)

| Section | Mapped to |
|---|---|
| §1 | not localized: BG |
| §1.1 | not localized: BG |
| §1.2 | not localized: BG |
| §1.3 | not localized: BG |
| §1.4 | not localized: BG |
| §2 | not localized: BG |
| §2.1 | not localized: BG |
| §2.2 | not localized: BG (federal plan taxonomy) |
| §2.2.1 | not localized: BG |
| §2.2.2 | not localized: BG |
| §2.2.3 | not localized: BG |
| §2.2.4 | not localized: BG |
| §2.2.5 | not localized: BG |
| §2.2.6 | not localized: BG |
| §2.2.7 | not localized: BG |
| §2.2.8 | not localized: BG |
| §3 | not localized: PARENT |
| §3.1 | not localized: ORG (policy statement) |
| §3.2 | SP34-05 |
| §3.2.1 | SP34-05, SP34-06 |
| §3.2.2 | SP34-07 |
| §3.2.3 | SP34-07 |
| §3.3 | not localized: FAC (preventive physical controls) |
| §3.4 | not localized: PARENT |
| §3.4.1 | SP34-09 |
| §3.4.2 | SP34-01, SP34-03, SP34-19 |
| §3.4.3 | SP34-10 |
| §3.4.4 | not localized: FAC (equipment replacement) |
| §3.4.5 | not localized: COST |
| §3.4.6 | not localized: ORG (organizational roles; plan-level roles are SP34-15) |
| §3.5 | SP34-22, SP34-24 |
| §3.5.1 | SP34-22 |
| §3.5.2 | not localized: ORG (training) |
| §3.5.3 | SP34-23 (exercise types) |
| §3.5.4 | SP34-23 |
| §3.6 | SP34-17, SP34-25 |
| Ch. 4 intro | SP34-12 |
| §4.1 | SP34-08, SP34-12, SP34-15 |
| §4.2 | not localized: PARENT |
| §4.2.1 | SP34-13 |
| §4.2.2 | SP34-13 |
| §4.2.3 | not localized: ORG (outage assessment performed during an event) |
| §4.3 | not localized: PARENT |
| §4.3.1 | SP34-14 |
| §4.3.2 | SP34-14 |
| §4.3.3 | SP34-14 (escalation steps) |
| §4.4 | SP34-04, SP34-16 |
| §4.5 | not localized: TPL (plan appendix contents) |
| §5 | not localized: PARENT |
| §5.1 | not localized: PARENT |
| §5.1.1 | not localized: BG (BIA restated for technical planning; covered by SP34-05, SP34-09, SP34-11) |
| §5.1.2 | SP34-01, SP34-02, SP34-18 |
| §5.1.3 | SP34-20 |
| §5.1.4 | not localized: SUPERSEDED (SP 800-53 Rev. 3 controls; follow-up candidate: SP 800-53 Rev. 5 CP family as its own source) |
| §5.1.5 | SP34-03, SP34-11, SP34-19 |
| §5.1.6 | SP34-21 |
| §5.2 | not localized: PLAT |
| §5.2.1 | not localized: PLAT |
| §5.2.2 | not localized: PLAT |
| §5.3 | not localized: PLAT |
| §5.3.1 | not localized: PLAT |
| §5.3.2 | not localized: PLAT |
| §5.4 | not localized: PLAT |
| §5.4.1 | not localized: PLAT |
| §5.4.2 | not localized: PLAT |
| §5.5 | not localized: PLAT |
| App. A | not localized: TPL (only the plan structure is used, SP34-12 to SP34-16) |
| App. B | not localized: TPL (BIA template) |
| App. C | not localized: BG (FAQ) |
| App. D | not localized: ORG (personnel) |
| App. E | not localized: SUPERSEDED (SP 800-53 Rev. 3 CP controls) |
| App. F | not localized: BG (SDLC) |
| App. G | not localized: BG (glossary) |
| App. H | not localized: BG (acronyms) |
| App. I | not localized: BG (resources) |
