# Maintenance — Cost & Sustainability localized standards

**Maintainers only. Workers never load this file.** Design decisions are recorded inline where they apply (DEC-n: this skill's localization decisions; D-n and C-n: cross-skill decisions and follow-ups); the planning documents they came from aren't kept in this repo.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1).

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| learn.microsoft.com (azure/well-architected) | azure-well-architected-cost-sustainability.md | 51 | 100 | 18 pinned pages |
| learn.greensoftware.foundation | green-software-principles.md | 4 | 100 | 4 of 6 principle pages |
| patterns.greensoftware.foundation | green-software-patterns.md | 23 | 100 | Covers 24 of 59 patterns |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Check ID COST-04 is retired (plan DEC-6) and must never be reused.
- Level is `REVIEW` for every element (no source uses normative keywords). If a source adds keywords, record the verbatim keyword and update `SKILL.md` step 6.
- Scope: `G` generic only. Keep wording cloud-neutral; name a provider's product only as an example. Don't add Azure-only (`A`) elements: generalize the source's Azure facilitation to a cloud-neutral rule or leave it unmapped (2026-11-12: WAF-51 generalized from Azure Hybrid Benefit / dev-test pricing).
- Primary anchor first; list every absorbed anchor so coverage stays auditable.
- Keep rows to one line (≈ 200 characters where possible).
- Every WAF, GSFL and GSP ID must be listed by exactly one active check in `../checklist.md`.
- Don't add elements for too little redundancy (review-reliability), missing or insufficient backup/DR (review-disaster-recovery), code-level caching, compression or async I/O (review-performance), missing logging or retention below a requirement (review-monitoring, review-observability), whether security inspection exists (security skills) or load tests (review-testing TST-12). Cost judges only excess. See `SKILL.md` step 8.

## Refresh procedure

1. **Cadence:** quarterly, or when run notes contain ≥ 3 `localized-standard-gap` entries for this skill.
2. **Detect drift:**
   - WAF: re-fetch each pinned page and compare its `ms.date` meta value with the header table of `azure-well-architected-cost-sustainability.md`. A changed date means diffing that page's section text and anchor list. Also check the pillar TOC (`https://learn.microsoft.com/azure/well-architected/toc.json`) for added or removed Cost Optimization or sustainability pages. (The 2026-06-25 sustainability restructure is the kind of change this catches.)
   - GSF: compare the latest commit SHAs of `Green-Software-Foundation/learn` and `Green-Software-Foundation/patterns` (`https://api.github.com/repos/Green-Software-Foundation/<repo>/commits?per_page=1`) with the pinned SHAs. If they differ, diff the pattern list (`https://patterns.greensoftware.foundation/sitemap.xml`) and the principle-page anchors.
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep each site ≤ 100 elements. Update the coverage map below, the page dates/SHAs and retrieval date in each file header and in `../sources.md`, and the URL list in `compliance-review-core/references/approved-sources.md` if a page moves.
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo).
   - Script-check: element IDs are contiguous; the checklist mapping rule above holds; every listed anchor exists on its pinned page (GSP: every page path exists and has a `solution` anchor); every content H2/H3 anchor on the 18 WAF pages, each of the 135 sustainability recommendation rows, every H2/H3 anchor on the 6 GSF principle pages, and all 59 patterns appear in the coverage map below — zero unaccounted.
   - Run a review against small sample repos with IaC (one Azure Bicep, one non-Azure Terraform/Kubernetes): `validate` passes, `26-review-cost-sustainability.json` has `urlsFetched: []`, all 9 active checks present and no COST-04 entry, citations use pinned URLs and element IDs, WAF-51 skipped on the non-Azure sample.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-cost-sustainability` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-07 — initial localization

- Snapshot (taken twice on 2026-11-07: once for planning, once at implementation; no differences): 18 WAF pages with the `ms.date` values in the header table; `Green-Software-Foundation/learn` @ `dbe70f6e4e2640485b320dfd85ae5f368d2e1e88` (2026-05-21); `Green-Software-Foundation/patterns` @ `36ccf754849bce89af87fb5222f7bce069cd2ffd` (2026-09-10); pattern list from `sitemap.xml` (59 patterns).
- Script verification: 129 content H2/H3 anchors on the 18 WAF pages (boilerplate excluded, see coverage map) → all accounted for; 135 sustainability recommendation rows → all accounted for; every element anchor exists on its pinned page; 6 GSF principle pages → all anchors accounted for; 59 patterns → 24 localized in 23 elements, 35 not localized with reasons; every GSP page has a `solution` anchor.
- Corrections while checking rows against the source:
  - Added `su-rel#factor-in-sustainability-into-platform-choices` to WAF-02, WAF-11 and WAF-40, because that section's rows 3, 7 and 9 are absorbed by them.
  - GSP citation URLs have no trailing slash (matching the site's `sitemap.xml`); GSFL pages redirect to a trailing-slash form, so GSFL citations use `<page>/#<anchor>`.
  - The plan's §7 lists did not name every anchor. The coverage map below adds the missing ones (parent headings, cost-model and environment analysis activities, `co-env#consider-endpoint-emulation`, `co-data#optimize-data-segmentation`, `co-data#optimize-security-and-compliance`, `co-code` data-access/design subsections, `co-scale#evaluate-scale-out-versus-scale-up`, `co-consol#offload-responsibilities-to-external-teams`) with reasons consistent with §7.

## Open items

- Follow-ups outside this skill: reviewed and closed in the cross-skill follow-up pass of 2026-11-09. Open hand-offs: none.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Coverage map

### WAF — section anchors (18 pages)

Excluded as boilerplate on every page: `ms--in-this-article`, `ms--feedback`, `ms--additional-resources-mobile-heading`, `azure-facilitation` (Azure tool pointers, no review rule), `related-links`, `related-guidance`, `next-steps`, `cost-optimization-checklist`.

Reason codes for "not localized":
- **ORG** — organizational practice or analysis activity; not observable in a repo.
- **BILL** — billing-tool reporting, purchasing or commitment decision; not visible in IaC.
- **PERF** — application-code efficiency; owned by `review-performance` (plan §10 C-3).
- **REL** — reliability behaviour: `review-reliability`; load and resilience tests: `review-testing` TST-12/13.
- **SEC** — security control; owned by the security skills.
- **APP** — application-layer or CI/CD behaviour removed with COST-04 (plan §7.4).
- **PARENT** — heading whose content is in the H3 subsections listed beneath it.
- **INDEX** — index of other pages; traced through the CO column.

| Anchor | Covered by / reason |
|---|---|
| co-check#checklist | INDEX (CO:01…CO:14 traced in the CO column; CO:01, CO:13 → ORG) |
| co-model#conduct-workload-assessment | ORG (outcome reviewed via WAF-28) |
| co-model#estimate-workload-costs | ORG (outcome reviewed via WAF-28) |
| co-model#develop-the-cost-model | WAF-28 |
| co-model#align-estimates-to-cost-drivers | ORG (part of building the model; outcome WAF-28) |
| co-model#associate-costs-with-business-metrics | ORG (outcome WAF-28 / WAF-29) |
| co-model#publish-the-cost-model | WAF-28 |
| co-model#set-a-budget | WAF-28 |
| co-model#use-the-cost-model | ORG |
| co-model#maintain-the-cost-model | ORG |
| co-costdata#collect-cost-data | BILL |
| co-costdata#group-and-categorize-cost-data | WAF-21, WAF-23 |
| co-costdata#generate-cost-reports | BILL |
| co-costdata#assign-resource-owners | WAF-22 |
| co-costdata#review-cost-data | BILL |
| co-costdata#review-architectural-choices | BILL |
| co-costdata#automate-cost-alerts | WAF-24, WAF-25 |
| co-guard#use-governance-policies | WAF-12, WAF-21, WAF-23, WAF-26 |
| co-guard#configure-access-controls | SEC |
| co-guard#use-release-gates | WAF-27 |
| co-guard#configure-cost-alerts | WAF-24, WAF-25 |
| co-guard#use-iac | WAF-17, WAF-27 |
| co-guard#organizational-alignment | ORG |
| co-rates#uncover-workload-spending-patterns | BILL |
| co-rates#determine-the-right-billing-model | WAF-50 |
| co-rates#understand-the-consumption-based-billing-model | WAF-50 (analysis under the parent; only the outcome is reviewable) |
| co-rates#understand-the-commitment-based-billing-model | WAF-50 (same) |
| co-rates#discuss-options-with-the-workload-team | ORG |
| co-rates#determine-component-permanence | WAF-50 (same) |
| co-rates#determine-usage-consistency | WAF-50 (same) |
| co-rates#select-the-right-commitment-based-plan | BILL |
| co-rates#evaluate-and-commit-to-available-discounts | WAF-51 (Azure dev/test pricing); other discounts BILL |
| co-rates#decide-whether-to-build-or-buy-a-solution | BILL |
| co-rates#optimize-licensing-costs | WAF-51 |
| co-billing#determine-billing-factors | ORG (analysis; outcome WAF-50) |
| co-billing#determine-billing-increments | ORG (analysis; outcome WAF-50) |
| co-billing#map-usage-to-billing-increments | ORG (analysis; outcome WAF-50) |
| co-billing#consider-building-a-proof-of-concept-poc | ORG |
| co-billing#align-usage-to-maximize-resource-value | WAF-50 |
| co-comp#optimize-application-features | ORG (product value review with stakeholders) |
| co-comp#evaluate-application-feature-value | ORG |
| co-comp#evaluate-application-feature-cost | ORG |
| co-comp#review-application-feature-value-with-stakeholders | ORG |
| co-comp#determine-the-future-of-the-feature | ORG |
| co-comp#optimize-workload-resources | WAF-01, WAF-09, WAF-19, WAF-38 |
| co-comp#optimize-platform-features | WAF-03, WAF-04, WAF-05 |
| co-comp#be-methodical-in-optimization-efforts | WAF-21 |
| co-env#assess-environment-value | ORG |
| co-env#determine-environment-costs | ORG |
| co-env#optimize-the-production-environment | WAF-04, WAF-08 |
| co-env#optimize-disaster-recovery-environments | WAF-38 |
| co-env#optimize-preproduction-environments | PARENT |
| co-env#evaluate-preproduction-environments | WAF-18 |
| co-env#apply-governance | WAF-12, WAF-14, WAF-15, WAF-20, WAF-26 |
| co-env#balance-similarity-with-production | WAF-15, WAF-16 |
| co-env#optimize-development-environments | WAF-16, WAF-18, WAF-19, WAF-20 |
| co-env#consider-endpoint-emulation | PERF/APP (local emulators in developer workflow; not IaC-visible) |
| co-flow#create-an-inventory-of-flows | ORG |
| co-flow#prioritize-flows | WAF-07 |
| co-flow#optimize-independent-flows | WAF-07, WAF-49 |
| co-flow#separate-dissimilar-flows | WAF-07 |
| co-flow#combine-similar-flows | WAF-47 |
| co-flow#monitor-flows-continuously | ORG |
| co-data#take-an-inventory-of-data | ORG |
| co-data#prioritize-data | ORG |
| co-data#optimize-data-management | PARENT |
| co-data#optimize-data-lifecycle-management | WAF-30, WAF-31 |
| co-data#optimize-data-segmentation | PERF (data partitioning/indexing in the data layer) |
| co-data#minimize-data-transfer | WAF-39 |
| co-data#optimize-security-and-compliance | SEC (data classification/encryption choices) |
| co-data#optimize-data-volume | WAF-31, WAF-34, WAF-35 |
| co-data#optimize-data-replication | WAF-37 |
| co-data#optimize-backups | WAF-36 |
| co-data#optimize-file-formats | WAF-34 |
| co-data#optimize-storage-solutions | WAF-32, WAF-33, WAF-46 |
| co-code#instrument-your-code | PERF |
| co-code#optimize-hot-paths | WAF-33 (logging volume only); rest PERF |
| co-code#evaluate-the-use-of-concurrency | PERF |
| co-code#use-the-right-sdks | PERF |
| co-code#choose-the-right-operating-system | PERF (OS choice for code; non-prod OS parity is in WAF-15) |
| co-code#optimize-network-traffic | PARENT |
| co-code#optimize-network-protocols | WAF-42 |
| co-code#minimize-network-overhead | WAF-42 (compression); chattiness APP |
| co-code#optimize-data-access | PARENT |
| co-code#use-caching-mechanisms | WAF-41 (CDN/edge config only); code caching PERF |
| co-code#optimize-database-traffic | PERF |
| co-code#organize-data | PERF |
| co-code#optimize-solution-design | PARENT |
| co-code#use-design-patterns | PERF |
| co-code#change-configurations | PERF (runtime configuration tuning) |
| co-code#refactor-architecture | PERF (architecture refactoring; not a compliance finding) |
| co-code#modify-resource-sizes | WAF-01 |
| co-scale#evaluate-scale-out-versus-scale-up | ORG (design analysis; outcome WAF-01, WAF-09) |
| co-scale#optimize-autoscaling | WAF-10, WAF-11 |
| co-scale#use-event-based-scaling | WAF-13 |
| co-scale#optimize-demand-and-supply | PARENT |
| co-scale#offload-demand | WAF-41 |
| co-scale#reduce-demand | WAF-13 (scale-to-zero); throttling/demand patterns APP |
| co-scale#control-supply | WAF-12 |
| co-consol#consolidate-resources | WAF-47 |
| co-consol#consolidate-responsibilities | PARENT |
| co-consol#use-external-centralized-resources | WAF-48 |
| co-consol#offload-responsibilities-to-external-teams | ORG |
| su-co#make-cost-visible-and-actionable | rows below |
| su-co#reduce-structural-waste-in-the-application-layer | rows below |
| su-co#reduce-idle-and-baseline-platform-waste | rows below |
| su-co#use-geography-and-timing-deliberately | rows below |
| su-co#limit-delivery-path-amplification | rows below |
| su-co#control-storage-growth-over-time | rows below |
| su-co#keep-engineering-workflows-proportionate | rows below |
| su-pe#improve-application-efficiency | rows below |
| su-pe#optimize-compute-resources | rows below |
| su-pe#reduce-network-traversal | rows below |
| su-pe#reduce-storage-footprint | rows below |
| su-pe#balance-with-scalability-needs | rows below |
| su-pe#drive-efficiency-in-deployments | rows below |
| su-pe#use-modern-technology | rows below |
| su-rel#prevent-failure-amplification | rows below |
| su-rel#design-resiliency-intentionally | rows below |
| su-rel#stabilize-demand-to-reduce-waste | rows below |
| su-rel#factor-in-sustainability-into-platform-choices | rows below |
| su-rel#run-tests-that-provide-meaningful-resiliency-validation | rows below |
| su-sec#prevent-malicious-activity-from-driving-unnecessary-resource-consumption | rows below |
| su-sec#security-hardening-improves-sustainability-by-reducing-workload-footprint | rows below |
| su-sec#reduce-security-data-collection-and-processing-overhead | rows below |
| su-sec#improve-centralized-network-security-efficiency | rows below |
| su-oe#monitor-and-measure-sustainability | rows below |
| su-oe#use-policy-to-drive-behavior-to-support-sustainability | rows below |
| su-oe#build-culture-around-sustainability | rows below |

Not localized (plan §7.1, conceptual pages): `sustainability/overview`, `sustainability/sustainability-design-methodology`, `cost-optimization/principles`, `/tradeoffs`, `/maturity-model`, `/design-patterns`, `create-culture-financial-responsibility` (CO:01), `optimize-personnel-time` (CO:13).

### WAF — sustainability recommendation rows (135)

Key: `<page key>#<section anchor>/r<n>`, where n is the row's position in that section's recommendation table (1-based, header excluded). Reason codes as above.

| Row | Recommendation (abridged) | Covered by / reason |
|---|---|---|
| su-co#make-cost-visible-and-actionable/r1 | Track cost at feature/workload level | WAF-21 |
| su-co#make-cost-visible-and-actionable/r2 | Cost signals as input to sustainability measurement | WAF-29 |
| su-co#make-cost-visible-and-actionable/r3 | Explicit efficiency baselines | WAF-29 |
| su-co#make-cost-visible-and-actionable/r4 | Observability spend in optimization scope | WAF-33 |
| su-co#make-cost-visible-and-actionable/r5 | Cost accountability at workload level | WAF-22 |
| su-co#make-cost-visible-and-actionable/r6 | Challenge local optimizations that shift cost | ORG |
| su-co#reduce-structural-waste-in-the-application-layer/r1 | Reduce API chattiness, payload size, repeat calls | APP |
| su-co#reduce-structural-waste-in-the-application-layer/r2 | Algorithm and execution-path improvements | PERF |
| su-co#reduce-structural-waste-in-the-application-layer/r3 | Cache repeated/expensive responses | PERF |
| su-co#reduce-structural-waste-in-the-application-layer/r4 | Caution with abstraction in hot paths | PERF |
| su-co#reduce-structural-waste-in-the-application-layer/r5 | Monolith vs microservices on real needs | ORG (architecture decision; not a cost finding from IaC) |
| su-co#reduce-structural-waste-in-the-application-layer/r6 | SSR vs CSR footprint | APP (front-end; plan §7.3 front-end group) |
| su-co#reduce-structural-waste-in-the-application-layer/r7 | Remove cross-service data duplication | WAF-35 |
| su-co#reduce-idle-and-baseline-platform-waste/r1 | Autoscale against observed demand | WAF-09 |
| su-co#reduce-idle-and-baseline-platform-waste/r2 | Shut down/downsize non-prod | WAF-14 |
| su-co#reduce-idle-and-baseline-platform-waste/r3 | Remove orphaned/zombie resources | WAF-19 |
| su-co#reduce-idle-and-baseline-platform-waste/r4 | Match tiers and reservations to usage | WAF-02, WAF-50 |
| su-co#reduce-idle-and-baseline-platform-waste/r5 | Favor containers, PaaS, serverless | WAF-46 |
| su-co#reduce-idle-and-baseline-platform-waste/r6 | Spot VMs only where interruption is acceptable | WAF-49 |
| su-co#reduce-idle-and-baseline-platform-waste/r7 | CI/CD caching, reuse, incremental builds | APP |
| su-co#use-geography-and-timing-deliberately/r1 | Consider lower-carbon regions | WAF-43 |
| su-co#use-geography-and-timing-deliberately/r2 | Schedule batch in lower-carbon/cost periods | WAF-44 |
| su-co#use-geography-and-timing-deliberately/r3 | Place workloads closer to users when justified | WAF-40 |
| su-co#use-geography-and-timing-deliberately/r4 | Avoid unneeded cross-region routing/replication | WAF-39 |
| su-co#use-geography-and-timing-deliberately/r5 | Reassess regional choices over time | ORG (periodic review) |
| su-co#limit-delivery-path-amplification/r1 | CDNs for repeated content | WAF-41 |
| su-co#limit-delivery-path-amplification/r2 | Compress payloads, choose transfer formats | WAF-42 |
| su-co#limit-delivery-path-amplification/r3 | Reduce cross-service chaining and fan-out | APP |
| su-co#limit-delivery-path-amplification/r4 | Keep traffic within regional boundaries | WAF-39 |
| su-co#limit-delivery-path-amplification/r5 | Place workloads near users | WAF-40 |
| su-co#limit-delivery-path-amplification/r6 | Centralize repeated media processing | APP (application media pipeline) |
| su-co#control-storage-growth-over-time/r1 | Match storage tiers to access | WAF-30 |
| su-co#control-storage-growth-over-time/r2 | Remove stale/redundant data on purpose | WAF-31 |
| su-co#control-storage-growth-over-time/r3 | Control logging and telemetry growth | WAF-32, WAF-33 |
| su-co#control-storage-growth-over-time/r4 | Avoid duplicating datasets | WAF-35 |
| su-co#control-storage-growth-over-time/r5 | Backup retention vs recovery requirements | WAF-36 |
| su-co#control-storage-growth-over-time/r6 | Compress stored data | WAF-34 |
| su-co#keep-engineering-workflows-proportionate/r1 | Scale CI/CD resources dynamically | APP |
| su-co#keep-engineering-workflows-proportionate/r2 | Cache build artifacts | APP |
| su-co#keep-engineering-workflows-proportionate/r3 | Test changed components only | APP |
| su-co#keep-engineering-workflows-proportionate/r4 | Incremental builds | APP |
| su-co#keep-engineering-workflows-proportionate/r5 | Remove redundant pipeline stages | APP |
| su-co#keep-engineering-workflows-proportionate/r6 | Avoid always-on full-suite testing | APP |
| su-pe#improve-application-efficiency/r1 | Optimize API communication patterns | APP |
| su-pe#improve-application-efficiency/r2 | Request throttling and response caching (APIM) | APP (throttling) / PERF (caching) |
| su-pe#improve-application-efficiency/r3 | Monitor and optimize high-volume endpoints | APP |
| su-pe#improve-application-efficiency/r4 | Choose SSR/CSR rendering | APP (front-end) |
| su-pe#improve-application-efficiency/r5 | Caching to avoid repeated rendering | PERF |
| su-pe#improve-application-efficiency/r6 | Lightweight UIs | APP (front-end) |
| su-pe#improve-application-efficiency/r7 | Right-sized media, system fonts | APP (front-end) |
| su-pe#improve-application-efficiency/r8 | Navigation, findability, eco/dark mode | APP (front-end) |
| su-pe#optimize-compute-resources/r1 | Profile workloads for concurrency/utilization | PERF (runtime profiling) |
| su-pe#optimize-compute-resources/r2 | Evaluate specialized compute (GPU) | Not localized (specialized/AI compute; plan §7.3 AI follow-up) |
| su-pe#optimize-compute-resources/r3 | CPU/memory baselines and pipeline quality gates | WAF-29 |
| su-pe#reduce-network-traversal/r1 | CDNs, caching, compression | WAF-41, WAF-42 |
| su-pe#reduce-network-traversal/r2 | Deploy close to users; dependent resources in one region | WAF-40, WAF-39 |
| su-pe#reduce-network-traversal/r3 | Tune cache retention/expiration | WAF-41 |
| su-pe#reduce-storage-footprint/r1 | Storage compression, query optimization | WAF-34 (query optimization PERF) |
| su-pe#reduce-storage-footprint/r2 | Access tiers and lifecycle policies | WAF-30, WAF-31 |
| su-pe#reduce-storage-footprint/r3 | Review backup, recovery point and log retention | WAF-32, WAF-36 |
| su-pe#balance-with-scalability-needs/r1 | Tier decisions match demand | WAF-02, WAF-01 |
| su-pe#balance-with-scalability-needs/r2 | Prefer dynamic scaling | WAF-09 |
| su-pe#balance-with-scalability-needs/r3 | Avoid unneeded higher tiers | WAF-02 |
| su-pe#drive-efficiency-in-deployments/r1 | CI/CD caching of build outputs | APP |
| su-pe#drive-efficiency-in-deployments/r2 | Local caching on self-hosted agents | APP |
| su-pe#use-modern-technology/r1 | Modernize to serverless/PaaS | WAF-46 |
| su-pe#use-modern-technology/r2 | Keep platforms and OS updated | WAF-05 |
| su-rel#prevent-failure-amplification/r1 | Circuit breakers | REL |
| su-rel#prevent-failure-amplification/r2 | Throttling under overload | REL |
| su-rel#prevent-failure-amplification/r3 | Graceful degradation | REL |
| su-rel#prevent-failure-amplification/r4 | Early failure detection | REL (monitoring) |
| su-rel#prevent-failure-amplification/r5 | Isolate dependency failures | REL |
| su-rel#design-resiliency-intentionally/r1 | Align resiliency to continuity requirements | WAF-37 |
| su-rel#design-resiliency-intentionally/r2 | Is multi-region truly required | WAF-37 |
| su-rel#design-resiliency-intentionally/r3 | Monolith vs microservice tradeoffs | ORG (architecture decision) |
| su-rel#design-resiliency-intentionally/r4 | Right-size failover environments | WAF-38 |
| su-rel#design-resiliency-intentionally/r5 | Review backup, replication, retention | WAF-36 |
| su-rel#stabilize-demand-to-reduce-waste/r1 | Asynchronous processing for bursts | APP |
| su-rel#stabilize-demand-to-reduce-waste/r2 | Buffering and queue-based load leveling | APP |
| su-rel#stabilize-demand-to-reduce-waste/r3 | Batch non-urgent operations | APP |
| su-rel#stabilize-demand-to-reduce-waste/r4 | Tune autoscaling to avoid aggressive reactions | WAF-11 |
| su-rel#factor-in-sustainability-into-platform-choices/r1 | Managed PaaS and serverless | WAF-46 |
| su-rel#factor-in-sustainability-into-platform-choices/r2 | Keep platforms, runtimes updated | WAF-05 |
| su-rel#factor-in-sustainability-into-platform-choices/r3 | Match tiers and scaling models to demand | WAF-02 |
| su-rel#factor-in-sustainability-into-platform-choices/r4 | Remove zombie/orphaned/inactive resources | WAF-19 |
| su-rel#factor-in-sustainability-into-platform-choices/r5 | Shut down non-prod when unused | WAF-14 |
| su-rel#factor-in-sustainability-into-platform-choices/r6 | Avoid dedicated infrastructure | WAF-06 |
| su-rel#factor-in-sustainability-into-platform-choices/r7 | Tune autoscaling to avoid churn | WAF-11 |
| su-rel#factor-in-sustainability-into-platform-choices/r8 | Spot only for interrupt-tolerant work | WAF-49 |
| su-rel#factor-in-sustainability-into-platform-choices/r9 | Regions close to users | WAF-40 |
| su-rel#factor-in-sustainability-into-platform-choices/r10 | Weigh carbon, latency, resiliency for regions | WAF-43 |
| su-rel#run-tests-that-provide-meaningful-resiliency-validation/r1 | Load testing and chaos engineering | REL |
| su-rel#run-tests-that-provide-meaningful-resiliency-validation/r2 | Chaos to find energy-inefficient paths | REL |
| su-rel#run-tests-that-provide-meaningful-resiliency-validation/r3 | Define expected behaviour under constraint | REL |
| su-rel#run-tests-that-provide-meaningful-resiliency-validation/r4 | "Eco version" benchmark | APP (demand shaping; plan §7.4) |
| su-rel#run-tests-that-provide-meaningful-resiliency-validation/r5 | Weigh cost of chaos/load tests | REL |
| su-rel#run-tests-that-provide-meaningful-resiliency-validation/r6 | Schedule and scope chaos intentionally | REL |
| su-sec#prevent-malicious-activity-from-driving-unnecessary-resource-consumption/r1 | Block malicious traffic at edge | SEC |
| su-sec#prevent-malicious-activity-from-driving-unnecessary-resource-consumption/r2 | Rate limiting and throttling | SEC (also plan §7.4) |
| su-sec#prevent-malicious-activity-from-driving-unnecessary-resource-consumption/r3 | Identity-based access control | SEC |
| su-sec#prevent-malicious-activity-from-driving-unnecessary-resource-consumption/r4 | Filter traffic early | SEC |
| su-sec#prevent-malicious-activity-from-driving-unnecessary-resource-consumption/r5 | Avoid excessive overlapping security layers | SEC |
| su-sec#security-hardening-improves-sustainability-by-reducing-workload-footprint/r1 | Harden networking | SEC |
| su-sec#security-hardening-improves-sustainability-by-reducing-workload-footprint/r2 | Harden identity and access | SEC |
| su-sec#security-hardening-improves-sustainability-by-reducing-workload-footprint/r3 | Harden resource configuration | SEC |
| su-sec#security-hardening-improves-sustainability-by-reducing-workload-footprint/r4 | Harden application and code | SEC |
| su-sec#security-hardening-improves-sustainability-by-reducing-workload-footprint/r5 | Harden operational access paths | SEC |
| su-sec#reduce-security-data-collection-and-processing-overhead/r1 | Filter logs before SIEM ingestion | WAF-33 |
| su-sec#reduce-security-data-collection-and-processing-overhead/r2 | Collect only required security signals | WAF-33 |
| su-sec#reduce-security-data-collection-and-processing-overhead/r3 | Data collection rules for telemetry intake | WAF-33 |
| su-sec#reduce-security-data-collection-and-processing-overhead/r4 | Forward filtered/aggregated signals | WAF-33 |
| su-sec#reduce-security-data-collection-and-processing-overhead/r5 | Purpose-built monitoring pipelines | WAF-33 |
| su-sec#improve-centralized-network-security-efficiency/r1 | Controls close to the traffic source | WAF-45 |
| su-sec#improve-centralized-network-security-efficiency/r2 | Avoid hub-and-spoke for uninspected traffic | WAF-45 |
| su-sec#improve-centralized-network-security-efficiency/r3 | Cloud-native local enforcement | WAF-45 |
| su-sec#improve-centralized-network-security-efficiency/r4 | Minimize inspection-only hops | WAF-45 |
| su-oe#monitor-and-measure-sustainability/r1 | Carbon emissions baseline | WAF-29 |
| su-oe#monitor-and-measure-sustainability/r2 | Use emissions monitoring tools | BILL (tooling outside the repo) |
| su-oe#monitor-and-measure-sustainability/r3 | Carbon reduction targets | WAF-29 |
| su-oe#monitor-and-measure-sustainability/r4 | Measurable metric such as SCI | WAF-29 (and GSFL-04) |
| su-oe#monitor-and-measure-sustainability/r5 | Record impact of sustainability changes | ORG |
| su-oe#use-policy-to-drive-behavior-to-support-sustainability/r1 | Follow organizational governance | ORG |
| su-oe#use-policy-to-drive-behavior-to-support-sustainability/r2 | Reuse cost governance policies | WAF-26 |
| su-oe#use-policy-to-drive-behavior-to-support-sustainability/r3 | Built-in policy for efficient configuration | WAF-26 |
| su-oe#use-policy-to-drive-behavior-to-support-sustainability/r4 | Dedicated sustainability policy initiative | WAF-26 |
| su-oe#use-policy-to-drive-behavior-to-support-sustainability/r5 | Data lifecycle policies and collection rules | WAF-31, WAF-33 |
| su-oe#use-policy-to-drive-behavior-to-support-sustainability/r6 | Review policy compliance regularly | ORG |
| su-oe#build-culture-around-sustainability/r1 | Sustainability community / CoE | ORG |
| su-oe#build-culture-around-sustainability/r2 | Ongoing training | ORG |
| su-oe#build-culture-around-sustainability/r3 | Communicate policies and targets | ORG |
| su-oe#build-culture-around-sustainability/r4 | Central guidance repository | ORG |
| su-oe#build-culture-around-sustainability/r5 | Knowledge-sharing sessions | ORG |
| su-oe#build-culture-around-sustainability/r6 | Sustainability metrics in governance/KPIs | ORG |
| su-oe#build-culture-around-sustainability/r7 | Recognize and reward teams | ORG |
| su-oe#build-culture-around-sustainability/r8 | Promote carbon-aware design | ORG |

### GSF principles — section anchors (6 pages)

Every page also has `introduction`, `key-concepts` (where present), `summary` and `quiz`: concept or quiz text, not localized.

| Anchor | Covered by / reason |
|---|---|
| carbon-awareness#carbon-intensity | Concept (background for GSFL-01) |
| carbon-awareness#variability-of-carbon-intensity | Concept (background for GSFL-01) |
| carbon-awareness#dispatchability--curtailment | Concept |
| carbon-awareness#marginal-carbon-intensity | Concept |
| carbon-awareness#energy-markets | Concept |
| carbon-awareness#how-to-be-more-carbon-aware | PARENT |
| carbon-awareness#demand-shifting | GSFL-01 |
| carbon-awareness#demand-shaping | Not localized (application feature degradation; plan §7.4) |
| energy-efficiency#fossil-fuels-and-high-carbon-sources-of-energy | Concept |
| energy-efficiency#low-carbon-sources-of-energy | Concept |
| energy-efficiency#energy-measurement | Concept |
| energy-efficiency#how-to-improve-energy-efficiency | PARENT |
| energy-efficiency#power-usage-effectiveness | Not localized (data-centre property; no repo signal) |
| energy-efficiency#energy-proportionality | GSFL-02 |
| hardware-efficiency#embodied-carbon | GSFL-03 |
| hardware-efficiency#amortization | Concept |
| hardware-efficiency#how-to-improve-hardware-efficiency | PARENT |
| hardware-efficiency#extending-the-lifespan-of-hardware | Not localized (end-user device lifespan; no repo signal) |
| hardware-efficiency#increasing-device-utilization | GSFL-03 |
| measurement#the-ghg-protocol | Concept |
| measurement#what-scope-does-my-application-fall-into | Concept |
| measurement#is-it-possible-to-calculate-a-total-for-software-carbon-emissions | Concept |
| measurement#do-totals-tell-the-whole-story | Concept (background for GSFL-04) |
| measurement#software-carbon-intensity-specification | PARENT |
| measurement#the-sci-equation | GSFL-04 |
| measurement#how-to-calculate-your-sci-score | GSFL-04 |
| carbon-efficiency (all anchors: global-warming-vs-climate-change, climate-vs-weather, greenhouse-gases-and-the-greenhouse-effect, carbon-and-co2eq, monitoring-climate-change) | Not localized (concepts; plan §7.2) |
| climate-commitments (all anchors: carbon-reduction-methodologies, abatement--carbon-elimination, offsets, compensating--carbon-avoidance, neutralizing--carbon-removal, climate-commitments-1, carbon-neutral, net-zero, 100-renewable, 247-hourly-matching) | Not localized (organizational commitments; plan §7.2) |

### GSF patterns (59)

| Pattern page path | Covered by / reason |
|---|---|
| architecture/system-topology/choose-region-closest-to-users | GSP-18 |
| architecture/system-topology/containerize-your-workload-where-applicable | GSP-22 |
| architecture/system-topology/efficient-hardware-ai-workloads | AI (follow-up candidate) |
| architecture/system-topology/implement-stateless-design | GSP-08 |
| architecture/system-topology/on-demand-execution-ai-agent-workloads | AI (follow-up candidate) |
| architecture/system-topology/queue-non-urgent-requests | APP (plan §7.4) |
| architecture/system-topology/run-ai-models-edge | AI (follow-up candidate) |
| architecture/system-topology/scale-logical-components-independently | GSP-07 |
| architecture/system-topology/serverless-model-development | AI (follow-up candidate) |
| architecture/technology-selection/evaluate-other-cpu-architectures | GSP-03 |
| architecture/technology-selection/use-serverless | GSP-23 |
| design/system-first-typography-user-needs | FRONT-END (follow-up candidate) |
| development/data-handling/avoid-tracking-unnecessary-data | FRONT-END (follow-up candidate) |
| development/data-handling/cache-static-data | GSP-19 |
| development/data-handling/compress-stored-data | GSP-16 |
| development/data-handling/compress-transmitted-data | GSP-20 |
| development/data-handling/optimize-data-storage-ai-training | AI (follow-up candidate) |
| development/data-handling/reduce-transmitted-data | APP (plan §7.4) |
| development/evaluate-whether-to-use-TLS-termination | SEC (may conflict with transport-security guidance; never score here) |
| development/media-and-code-efficiency/defer-offscreen-images | FRONT-END |
| development/media-and-code-efficiency/deprecate-gifs | FRONT-END |
| development/media-and-code-efficiency/properly-sized-images | FRONT-END |
| development/media-and-code-efficiency/remove-unused-css | FRONT-END |
| development/media-and-code-efficiency/serve-images-in-modern-formats | FRONT-END |
| development/media-and-code-efficiency/use-compiled-languages | Not localized (language choice; not actionable as a finding) |
| development/minimizing-deployed-environments | GSP-11 |
| development/optimize-agent-orchestration-reduce-model-calls | AI (follow-up candidate) |
| development/pre-trained-transfer-learning | AI (follow-up candidate) |
| development/right-sized-energy-efficient-ai-models | AI (follow-up candidate) |
| development/select-efficient-ml-frameworks-inference-runtimes | AI (follow-up candidate) |
| development/use-async-instead-of-sync | PERF (owned by `review-performance`, PERF-02) |
| development/web-performance/avoid-chaining-critical-requests | FRONT-END |
| development/web-performance/avoid-excessive-dom-size | FRONT-END |
| development/web-performance/enable-text-compression | GSP-20 |
| development/web-performance/keep-request-counts-low | FRONT-END |
| development/web-performance/minimize-main-thread-work | FRONT-END |
| development/web-performance/use-server-side-rendering | FRONT-END |
| operations/capacity-management/match-utilization-requirements-of-vm | GSP-01 |
| operations/capacity-management/match-utilization-requirements-with-pre-configured-server | GSP-02 |
| operations/capacity-management/optimize-avg-cpu-utilization | GSP-04 |
| operations/capacity-management/optimize-peak-cpu-utilization | Not localized (needs runtime profiling data) |
| operations/capacity-management/scale-down-kubernetes-workloads | GSP-10 |
| operations/capacity-management/scale-down-unused-applications | GSP-09 |
| operations/capacity-management/scale-infrastructure-with-user-load | GSP-05 |
| operations/capacity-management/scale-kubernetes-workloads-based-on-events | GSP-06 |
| operations/capacity-management/use-circuit-breaker | REL (owned by `review-reliability`, REL-04) |
| operations/carbon-aware-ai-scheduling | AI (follow-up candidate) |
| operations/optimize-edge-ai-power-performance | AI (follow-up candidate) |
| operations/resource-lifecycle/delete-unused-storage-resources | GSP-13 |
| operations/resource-lifecycle/optimise-storage-resource-utilisation | GSP-15 |
| operations/resource-lifecycle/remove-unused-assets | GSP-12 |
| operations/resource-lifecycle/set-retention-policy-on-storage-resources | GSP-14 |
| operations/scan-for-vulnerabilities | SEC |
| operations/time-shift-kubernetes-cron-jobs | GSP-21 |
| operations/use-cloud-native-network-security-tools-and-controls | SEC |
| operations/use-ddos-protection | SEC |
| requirements/encrypt-what-is-necessary | SEC (may conflict with encryption guidance; never score here) |
| requirements/match-slo | GSP-17 |
| requirements/shed-lower-priority-traffic | APP (plan §7.4) |

Totals: 24 localized (GSP-01…GSP-23; GSP-20 covers two pages), 11 AI, 12 FRONT-END, 5 SEC, 1 REL, 1 PERF, 2 other not localized, 3 APP = 59.
