# Maintenance — Monitoring localized standards

**Maintainers only. Workers never load this file.** Design decisions are recorded inline where they apply (DEC-n: this skill's localization decisions; D-n and C-n: cross-skill decisions and follow-ups); the planning documents they came from aren't kept in this repo.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1).

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| learn.microsoft.com (azure/well-architected) | azure-well-architected-monitoring.md | 44 | 100 | 6 content pages + 2 checklist pages (traceability) |
| sre.google | google-sre-monitoring-alerting.md | 28 | 100 | 4 chapters (SRE book ch. 6, 10; Workbook ch. 4, 5) |

`../monitoring-iac-signals.md` is a local lookup table, not a source summary. It isn't counted against any budget and isn't refreshed from these sources.

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Prefixes are skill-specific (`WAFM-`, `SREM-`; plan DEC-6) so they can't be confused with the cost skill's `WAF-xx`, the DR skill's `WAFR-xx`, or a future reliability localization of the SRE books.
- Level: WAF elements are `REVIEW` (no normative keywords). SRE elements are `SHOULD` only when the summarized sentence says "should" or "(strongly) recommend/advise"; otherwise `REVIEW`. The level never changes severity (plan DEC-8; `SKILL.md` step 8).
- Scope (WAF): `G` generic, `A` Azure-only. Keep wording tool-neutral for `G` elements. Every `A` element needs a `G` counterpart (today: WAFM-31 → WAFM-30; WAFM-34 → WAFM-33; WAFM-44 → WAFM-43).
- SRE rows must be summaries in our own words. The chapters are CC BY-NC-ND 4.0: never paste passages, tables or rule examples.
- Primary anchor first; list every absorbed anchor so coverage stays auditable. sre.google anchors with generated suffixes (`-g0sEi4`) are used exactly as published.
- Keep rows to one line (≈ 200 characters where possible).
- Every WAFM and SREM ID must be listed by exactly one check in `../checklist.md`, and each standards file's `## MON-xx` section must agree with it.
- Retention elements (WAFM-36, SREM-26) are sufficiency-only: never add an element that fails over-retention or telemetry cost. That belongs to `review-cost-sustainability`.
- Don't add elements for code instrumentation, health-endpoint existence or SLO documentation. Those belong to `review-observability` (OBS-01 … OBS-07; plan DEC-9). Also don't add elements for load-balancer routing or restart probes (review-reliability AZRL-49/50), recovery posture (review-disaster-recovery), telemetry cost or over-retention (review-cost-sustainability), sensitive data in log content (review-security-operational) or application tests (review-testing). See `SKILL.md` step 10.

## Refresh procedure

1. **Cadence:** quarterly, or when run notes contain ≥ 3 `localized-standard-gap` entries for this skill.
2. **Detect drift:**
   - WAF: re-fetch each pinned page (locale `en-us`), follow redirects, and compare the final URL and the `ms.date` meta value with the header table of `azure-well-architected-monitoring.md`. A changed date means diffing that page's section text and anchor list. A new redirect means updating the page path here, in the standards file and in `approved-sources.md`. Also check the pillar TOC (`https://learn.microsoft.com/azure/well-architected/toc.json`) for added, removed or renamed monitoring, observability or health-modeling pages.
   - SRE: the chapters are published book text and rarely change. Re-fetch each chapter, list its `id` attributes (note that some headings are written `id ="…"` with a space), and diff them against the coverage map. Check both tables of contents (`https://sre.google/sre-book/table-of-contents/`, `https://sre.google/workbook/table-of-contents/`) for a new monitoring or alerting chapter or a new edition.
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep each site ≤ 100 elements. Update the coverage map below, the page dates and retrieval date in each file header and in `../sources.md`, and the URL list in `compliance-review-core/references/approved-sources.md` if a page moves.
4. **IaC signals file:** when a review logs a `localized-standard-gap` for an unrecognized monitoring resource type, add it to `../monitoring-iac-signals.md`. No source refresh is needed for that.
5. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo).
   - Script-check: element IDs are contiguous; the checklist mapping rule above holds; every listed anchor exists on its pinned page; every content heading anchor on the pinned pages (boilerplate excluded, see below), each `dg-mon` antipattern-table row and every SRE section anchor listed below appear in the coverage map, with zero unaccounted.
   - Run a review against small sample repos with IaC: Azure Bicep with metric alerts, action groups and a workbook; Kubernetes with `PrometheusRule` + Alertmanager + Grafana JSON and a stated SLO; Terraform with resources but no monitoring-as-code. Expect: `validate` passes; `25-review-monitoring.json` has `urlsFetched: []`; all 6 checks present; citations use pinned URLs and element IDs; Scope A skipped on non-Azure; SREM-13 skipped without a stated SLO; the third variant fails MON-01 (low confidence) and MON-02, with MON-03 … MON-05 N/A.
6. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-monitoring` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-08 — initial localization

- Snapshot: planning snapshot and implementation snapshot both 2026-11-08 (plan DEC-5). No differences: all 7 WAF `ms.date` values match the header table and the final URLs match the pinned paths; the 4 SRE chapter pages are byte-identical between the two snapshots.
- Redirects recorded: `reliability/monitoring-alerting-strategy` → `reliability/monitoring`; `performance-efficiency/collect-performance-data` → `performance-efficiency/monitoring`; `cross-cutting-guides/health-modeling` serves `design-guides/health-modeling`.
- Script verification: 130 element anchors, all present on their pinned pages; 68 IDs (40 WAFM + 28 SREM), each listed by exactly one check; coverage map below accounts for all 160 content heading / section anchors on the 7 WAF pages and 4 SRE chapters (zero unaccounted), plus the 10 `dg-mon` antipattern rows.
- Corrections while checking rows against the source (these take precedence over the plan's §5–§6 inventories):
  - WAFM-08: added "locks and resource pressure" (both in the re-mon data-layer sentence).
  - WAFM-12: dropped "parameterized" (not in the source); the row now says the config is kept current by automation.
  - WAFM-19: reworded to the source's "production data drives monitoring and alerts"; added `dg-hm#continuous-validation`, which says non-production test results must not change production health.
  - WAFM-22: "reference a runbook" → "tie into operational runbooks" (dg-hm#set-actionable-alerts).
  - WAFM-38: added `dg-mon#telemetry-performance-and-reliability-considerations` (queueing with at-least-once delivery), which it absorbs.
  - WAFM-39: "don't depend on one region's monitoring store" → the source's "autonomous storage" for business-critical workloads.
  - Levels changed after checking each SRE sentence (severity is unaffected, plan DEC-8): SREM-01 and SREM-03 → `REVIEW` (no "should"); SREM-10 → `REVIEW`; SREM-05 ("you should also monitor"), SREM-09 ("strongly advise against"), SREM-17 ("should be simple"), SREM-22 ("we recommend … monitor the version") and SREM-28 ("we recommend keeping … loosely coupled") → `SHOULD`.
- `../monitoring-iac-signals.md`: resource type names were checked against maintainer knowledge of the providers, not by fetching provider documentation (fetching was approved for the standards sources only). Unverified entries were left out (e.g. an Azure-native SLO resource). Re-check names on the first quarterly refresh.

### 2026-11-09 — security-event alerting (afterplanning WP-10, decision D-2)

- Monitoring owns security-event alert rules and SIEM routing (cross-skill decision D-2;
  closes monitoring C-4 security part and security-operational C-7). Pinned WAF SE:10
  `security/monitor-threats` (ms.date 2024-02-13, `git_commit_id` bb2e40b7f88c35b52263e5303880b7911f726d4a, retrieved
  2026-11-09; page key `se-mon`).
- New elements WAFM-41, WAFM-42 (MON-01) and WAFM-43, WAFM-44 (MON-04, WAFM-44 Azure-only). The check count stays at 6;
  MON-01 and MON-04 gained elements (minor scope change, README note).
- Anchors were taken from the page's heading text (Learn heading slugs); confirm against the HTML `id` values on the
  first refresh.
- se-mon coverage: `capture-data-to-keep-a-trail-of-activities` and `application-user-flows` (security-event *logging*:
  `review-security-operational`); `identity-and-access-monitoring` (WAFM-41; logging part: security-operational);
  `network-monitoring` (WAFM-42; flow-log routing: WAFM-30/MON-06); `capture-system-changes` (WAFM-42; build telemetry:
  ORG; "include the validation of logging and alerting" in test plans: SREM-08); `store-aggregate-and-analyze-data`
  (WAFM-43; storage tiers: COST); `centralized-threat-detection-with-correlated-logs` (WAFM-43); `detect-abuse`
  (WAFM-41; hardening and vulnerability scanning: SEC / `review-software-lifecycle`); `azure-facilitation` (WAFM-44;
  retention note: WAFM-36); `networking`, `identity`, `azure-pipelines` (TOOL / SEC).

## Open items

- Follow-ups outside this skill: reviewed and closed in the cross-skill follow-up pass of 2026-11-09. Open hand-offs: none.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Coverage map

Reason codes for "not localized":
- **OBS**: code instrumentation (structured logs, correlation IDs, tracing, emitted metrics). Owned by `review-observability`.
- **SLO**: defining SLOs, SLIs, KPIs or reliability targets. Owned by `review-observability` (OBS-07).
- **DR**: recovery signals (failover readiness, backup success, replication lag). Owned by `review-disaster-recovery` (WAFR-42).
- **SEC**: sensitive data in logs and security-event *logging*: `review-security-operational`. Security-event alert rules and SIEM routing are owned here (WAFM-41 … WAFM-44, decision D-2, 2026-11-09).
- **COST**: telemetry cost, sampling for cost, archive tiers. Owned by `review-cost-sustainability`.
- **PERF**: performance data collection and boundaries: not localized; instrumentation owned by `review-observability` (decided when Performance was localized, 2026-11-08).
- **TEST**: load and resilience (chaos, fault-injection) tests: `review-testing` (TST-12/TST-13).
- **ARCH**: architecture or technology choice that isn't verifiable as a pass/fail check from IaC.
- WAF sections split with `review-observability` (e.g. `dg-hm#use-health-probes`): health-endpoint implementation is WAFO (observability); probes that raise alerts are WAFM-32 here.
- **ORG**: organizational practice or recurring process; not visible in a repo.
- **TOOL**: optional tooling advice (AI/AIOps, dynamic thresholds, product overviews).
- **BG**: background, definitions, history, examples or case studies.
- **PARENT**: page title or parent heading whose substance is in its subsections (mapped separately).

### WAF — section anchors (7 pages)

Excluded as boilerplate on every page: `ms--in-this-article`, `ms--feedback`, `ms--additional-resources-mobile-heading`, `next-step`, `next-steps`, `related-links`, `operational-excellence-checklist`, `reliability-checklist`, `performance-efficiency-checklist`.

**oe-check** (2 anchors)
- `design-review-checklist-for-operational-excellence` → PARENT
- `checklist` → WAFM-11 (OE:07 row, traceability; other OE rows are owned by other skills or are ORG)

**re-check** (2 anchors)
- `design-review-checklist-for-reliability` → PARENT
- `checklist` → RE:10 row, traceability only (no element cites it); other rows owned by `review-reliability` / `review-disaster-recovery`

**oe-obs** (13 anchors)
- `architecture-strategies-for-designing-a-monitoring-system` → PARENT
- `align-telemetry-with-health-and-kpi-models` → SLO
- `emit-telemetry-from-workload-components` → OBS
- `collect-telemetry-across-the-workload` → ARCH (push vs pull)
- `standardize-data-consolidation` → WAFM-30, WAFM-39
- `tailor-storage-and-retention-for-usage-patterns` → WAFM-36, WAFM-37, WAFM-40 (polyglot persistence: ARCH)
- `correlate-data-for-end-to-end-insights` → OBS
- `analyze-and-visualize-to-support-actionable-decisions` → WAFM-23, WAFM-26 (AI notes: TOOL)
- `define-alerts-around-meaningful-operational-conditions` → WAFM-14, WAFM-16, WAFM-18, WAFM-19, WAFM-20, WAFM-21, WAFM-22, WAFM-33 (AI notes: TOOL)
- `design-scalable-durable-telemetry-pipelines` → WAFM-38
- `use-observability-to-support-continuous-improvement` → WAFM-13 (feedback loop: ORG)
- `watch-out-for-antipatterns` → BG (pointer to dg-mon antipatterns, mapped below)
- `azure-facilitation` → TOOL (dynamic thresholds, product list)

**re-mon** (14 anchors)
- `architecture-strategies-for-monitoring-workload-reliability` → PARENT
- `monitor-workload-functionality` → WAFM-06
- `monitor-user-experience` → WAFM-02
- `track-availability-targets` → WAFM-27 (target definition: SLO)
- `track-recoverability-targets` → WAFM-36 (retention note; recovery metrics: DR)
- `make-alerts-actionable-with-a-health-model` → WAFM-04, WAFM-15
- `monitor-all-layers-of-the-system` → WAFM-01, WAFM-08, WAFM-32, WAFM-35 (sync vs async logging: OBS)
- `monitor-administrative-dashboards-and-status-apis` → WAFM-29
- `define-and-monitor-stamp-capacity` → WAFM-03
- `monitor-load-distribution-across-redundant-instances` → WAFM-09
- `detect-failure-modes` → WAFM-07 (DDoS / malicious activity: SEC)
- `be-informed-about-platform-reliability-status` → WAFM-33, WAFM-34
- `azure-facilitation` → WAFM-34 (rest: TOOL)
- `example` → BG

**dg-mon** (20 anchors)
- `how-to-build-a-monitoring-system-for-azure-workloads` → PARENT
- `terminology` → BG
- `phase-1---instrumentation` → OBS
- `best-practices-for-instrumentation` → OBS
- `example-instrumentation` → BG
- `phase-2---telemetry-data-collection-and-storage` → PARENT
- `telemetry-data-storage-decision` → ARCH
- `telemetry-performance-and-reliability-considerations` → WAFM-38
- `telemetry-data-lifecycle-management` → WAFM-36 (down-sampling and archive tiers: COST)
- `telemetry-data-security` → WAFM-37 (encryption and PII scrubbing: SEC)
- `phase-3---correlation-aggregation-analysis` → WAFM-01, WAFM-03
- `correlation` → OBS
- `supporting-hot-warm-and-cold-analysis` → ARCH
- `best-practices-for-alerts` → WAFM-14, WAFM-16, WAFM-17, WAFM-18, WAFM-20, WAFM-21, WAFM-22
- `example-correlation-aggregation-analysis` → BG
- `phase-4---visualization` → PARENT
- `best-practices-for-visualization` → WAFM-23, WAFM-24, WAFM-25, WAFM-26
- `example-visualization` → BG
- `monitoring-antipatterns-and-how-to-avoid-them` → rows below
- `azure-facilitation` → TOOL

**dg-mon antipattern rows** (10 rows; keyed by row name)
- Logging too little, or too much → OBS
- Missing correlation across services → OBS
- Ignoring business context → WAFM-24, WAFM-17
- Unconfigured or mismanaged telemetry → WAFM-30, WAFM-36
- Poor data governance → WAFM-36, WAFM-37 (PII masking: SEC)
- Ignoring monitoring costs → COST
- Inconsistent and fragmented telemetry → OBS
- Poorly designed dashboards → WAFM-24, WAFM-25
- Alert fatigue → WAFM-16, WAFM-17, WAFM-21 (dynamic thresholds, pruning: TOOL / ORG)
- No trend analysis or forecasting → WAFM-27

**dg-hm** (25 anchors)
- `health-modeling-for-workloads` → PARENT
- `terminology` → BG
- `what-is-health-health-modeling-and-a-health-model` → BG
- `health-model-schema` → BG
- `build-a-health-model` → PARENT
- `evaluate-your-workload-design` → ARCH
- `contextualize-using-business-requirements` → SLO
- `map-to-reliability-metrics` → SLO
- `identify-health-signals` → WAFM-05, WAFM-14
- `use-platform-metrics-and-logs` → WAFM-30, WAFM-31
- `add-application-logs` → WAFM-31 (workspace note; logging practice: OBS)
- `implement-distributed-tracing` → OBS
- `use-health-probes` → WAFM-32 (endpoint implementation: OBS)
- `adopt-structural-and-functional-monitoring-techniques` → WAFM-32
- `model-the-design` → WAFM-09 (propagation rules: ARCH)
- `set-actionable-alerts` → WAFM-18, WAFM-21, WAFM-22
- `visualize-the-model` → WAFM-23, WAFM-28
- `adopt-your-health-model` → PARENT
- `applicability-to-various-roles` → ORG
- `continuous-validation` → WAFM-19 (non-production results kept out of production health; load/chaos testing: TEST)
- `organizational-health` → ORG
- `health-trends-and-ai-for-it-operations` → TOOL
- `maintain-your-health-model` → WAFM-11, WAFM-12 (30-day health-data retention: COST)
- `azure-facilitation` → TOOL
- `implement-with-azure-monitor-health-models` → TOOL

**pe-mon** (14 anchors)
- `architecture-strategies-for-monitoring-workload-performance` → PARENT
- `use-percentile-based-metrics` → WAFM-02
- `define-your-performance-improvement-boundaries` → PERF
- `segment-signals-by-environment-and-purpose` → WAFM-19, WAFM-40 (business vs performance streams: OBS)
- `create-scoped-and-actionable-performance-alerts` → WAFM-02, WAFM-04, WAFM-07, WAFM-15, WAFM-16
- `monitor-elasticity` → WAFM-10
- `track-performance-over-time` → WAFM-27 (baselines and deployment annotations; refining SLOs: SLO)
- `collect-application-performance-data` → PERF
- `collect-resource-performance-data` → PERF
- `collect-database-and-storage-data` → PERF
- `collect-operating-system-performance-data` → PERF
- `generate-synthetic-data-when-necessary` → PERF
- `azure-facilitation` → TOOL
- `examples` → BG

### SRE — section anchors (4 chapters)

Excluded on every page: site chrome ids (`curtain`, `burger-menu`, `content`, icon ids), footnote ids (`*fn*`, `*-marker`), MathJax ids and figure/table ids not listed below.

**mds** (`sre-book/monitoring-distributed-systems/`)
- `chapter_monitoring` → PARENT
- `definitions-2ksZhN` → BG (definition-list ids `monitoring`, `white-box-monitoring`, `black-box-monitoring`, `dashboard`, `alert`, `root-cause`, `node-and-machine`, `push`: BG)
- `why-monitor-pWsBTZ` → BG (`building-dashboards` → SREM-21; `alerting`, `analyzing-long-term-trends`, `comparing-over-time-or-experiment-groups`, `conducting-ad-hoc-retrospective-analysis-ie-debugging`: BG)
- `setting-reasonable-expectations-for-monitoring-o8svcM` → SREM-04, SREM-17
- `symptoms-versus-causes-g0sEi4` → SREM-10 (`table_monitoring_symptoms`: BG)
- `black-box-versus-white-box-q8sJuw` → SREM-25
- `xref_monitoring_golden-signals` → SREM-01 (`latency` → SREM-02; `traffic` → SREM-01; `errors` → SREM-02; `saturation` → SREM-03)
- `worrying-about-your-tail-or-instrumentation-and-performance-Yms9Ck` → SREM-15
- `choosing-an-appropriate-resolution-for-measurements-vJsBsE` → SREM-27
- `as-simple-as-possible-no-simpler-lqskHx` → SREM-17 (pruning unused signals: ORG)
- `tying-these-principles-together-nqsJfw` → SREM-10, SREM-11, SREM-20
- `monitoring-for-the-long-term-NbsNS8` → ORG
- `bigtable-sre-a-tale-of-over-alerting-dbsXtjSM` → BG
- `gmail-predictable-scriptable-responses-from-humans-BVs1h4SD` → SREM-11
- `the-long-run-MQsWTMS7` → ORG
- `conclusion-8ksvFj` → SREM-10, SREM-18

**pa** (`sre-book/practical-alerting/`)
- `practical-alerting-from-time-series-data` → PARENT
- `the-rise-of-borgmon` → BG (`time-series-monitoring-outside-of-google`: BG)
- `instrumentation-of-applications` → OBS (`exporting-variables`: OBS)
- `collection-of-exported-data` → BG
- `storage-in-the-time-series-arena` → BG
- `labels-and-vectors` → BG
- `rule-evaluation` → BG (`note`, `tip`, `note-1`: BG)
- `alerting` → SREM-12, SREM-16, SREM-18, SREM-19
- `sharding-the-monitoring-topology` → BG
- `black-box-monitoring` → SREM-25
- `maintaining-the-configuration` → SREM-07, SREM-08
- `ten-years-on` → BG

**wb-mon** (`workbook/monitoring/`)
- `monitoring` → PARENT
- `desirable-features-of-a-monitoring-strategy` → PARENT
- `speed` → SREM-27
- `calculations` → SREM-15, SREM-26
- `interfaces` → SREM-24
- `alerts` → SREM-18, SREM-19
- `sources-of-monitoring-data` → OBS
- `examples` → OBS
- `move-information-from-logs-to-metrics` → OBS
- `improve-both-logs-and-metrics` → OBS
- `keep-logs-as-the-data-source` → SREM-16 (logs vs metrics choice: OBS)
- `managing_your_monitoring_system` → SREM-28
- `treat-your-configuration-as-code` → SREM-06
- `encourage-consistency` → SREM-07
- `prefer-loose-coupling` → SREM-28
- `metrics-with-purpose` → SREM-21
- `intended-changes` → SREM-16, SREM-22 (exporting flags/versions as metrics: OBS)
- `dependencies` → SREM-05
- `saturation` → SREM-03
- `status-of-served-traffic` → SREM-23
- `implementing-purposeful-metrics` → SREM-15
- `testing-alerting-logic` → SREM-08
- `conclusion` → BG

**wb-slo** (`workbook/alerting-on-slos/`)
- `alerting-on-slos` → PARENT
- `alerting-considerations` → SREM-14
- `ways-to-alert-on-significant-events` → PARENT
- `1-target-error-rate-slo-threshold` → BG (stepping stone to SREM-13; `note`: BG)
- `2-increased-alert-window` → BG (stepping stone)
- `3-incrementing-alert-duration` → SREM-12
- `4-alert-on-burn-rate` → BG (stepping stone)
- `5-multiple-burn-rate-alerts` → SREM-13
- `6-multiwindow-multi-burn-rate-alerts` → SREM-13
- `low-traffic-services-and-error-budget-alerting` → SREM-14
- `generating-artificial-traffic` → SREM-14
- `combining-services` → SREM-14
- `making-service-and-infrastructure-changes` → ARCH (client retries, fallback paths: `review-reliability`)
- `lowering-the-slo-or-increasing-the-window` → SREM-14 (lowering the SLO: SLO)
- `extreme-availability-goals` → ARCH (`review-reliability`)
- `alerting_at_scale` → SREM-09
- `conclusion` → BG
