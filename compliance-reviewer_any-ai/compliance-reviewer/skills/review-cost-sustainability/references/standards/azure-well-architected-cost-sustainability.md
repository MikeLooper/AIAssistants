# Azure Well-Architected Framework — Cost Optimization & Sustainability — localized summary

- Source site: learn.microsoft.com (azure/well-architected)
- Pinned pages: see the page table below (path + `ms.date` at retrieval)
- Citation base: https://learn.microsoft.com/azure/well-architected/
- Localized: 2026-11-07 · Generalized: 2026-11-12 · Elements: 51 (cap 100)
- Source name for `Finding.standard`: `Azure Well-Architected Framework`
- Level: every element is `REVIEW` (the source uses no normative keywords); severity is the owning check's default.
- Scope column: G = generic (any cloud / Kubernetes). Every element is Scope G; the only Azure-only element (WAF-51) was generalized on 2026-11-12. Azure product names appear only as examples.
- CO column: the WAF Cost Optimization checklist code the element implements (traceability only).
- Anchor(s): `<page key>#<section anchor>`, primary first. Recommendation-table rows have no anchors of their own, so the anchor is the section that holds the row.
- Citation URL: citation base + page path + `#` + primary anchor, with no locale segment.

| Key | Page path | ms.date |
|-----|-----------|---------|
| co-check | cost-optimization/checklist | 2023-11-15 |
| co-model | cost-optimization/cost-model | 2023-11-15 |
| co-costdata | cost-optimization/collect-review-cost-data | 2026-05-20 |
| co-guard | cost-optimization/set-spending-guardrails | 2026-08-31 |
| co-rates | cost-optimization/get-best-rates | 2023-11-15 |
| co-billing | cost-optimization/align-usage-to-billing-increments | 2023-11-15 |
| co-comp | cost-optimization/optimize-component-costs | 2023-11-15 |
| co-env | cost-optimization/optimize-environment-costs | 2023-11-15 |
| co-flow | cost-optimization/optimize-flow-costs | 2023-11-15 |
| co-data | cost-optimization/optimize-data-costs | 2023-11-15 |
| co-code | cost-optimization/optimize-code-costs | 2023-11-15 |
| co-scale | cost-optimization/optimize-scaling-costs | 2023-11-15 |
| co-consol | cost-optimization/consolidation | 2023-11-15 |
| su-co | sustainability/sustainability-cost-optimization-recommendations | 2026-06-25 |
| su-pe | sustainability/sustainability-performance-efficiency-recommendations | 2026-06-25 |
| su-rel | sustainability/sustainability-reliability-recommendations | 2026-06-25 |
| su-sec | sustainability/sustainability-security-recommendations | 2026-06-25 |
| su-oe | sustainability/sustainability-operational-excellence-recommendations | 2026-06-25 |

## COST-01 — Right-sizing and tier selection

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-01 | REVIEW | G | Size compute (instance count, vCPU/memory, SKU) to measured or stated demand. A large fixed SKU needs a recorded justification. | compute in IaC | CO:07 | co-comp#optimize-workload-resources, su-pe#balance-with-scalability-needs, co-code#modify-resource-sizes |
| WAF-02 | REVIEW | G | Pick service tiers for features actually used. A higher tier chosen only for unused features is waste. | PaaS tiers | CO:07 | su-pe#balance-with-scalability-needs, su-co#reduce-idle-and-baseline-platform-waste, su-rel#factor-in-sustainability-into-platform-choices |
| WAF-03 | REVIEW | G | Disable paid platform features and add-ons that aren't used. | PaaS options | CO:07 | co-comp#optimize-platform-features |
| WAF-04 | REVIEW | G | Availability and performance settings (zone redundancy, replica count, premium storage, SLA tier) match stated requirements, no more. | compute, storage | CO:07 | co-comp#optimize-platform-features, co-env#optimize-the-production-environment |
| WAF-05 | REVIEW | G | Use current SKU/service generations and keep platforms, runtimes and OS images current. | compute | CO:07 | co-comp#optimize-platform-features, su-pe#use-modern-technology, su-rel#factor-in-sustainability-into-platform-choices |
| WAF-06 | REVIEW | G | Avoid dedicated or isolated infrastructure (dedicated hosts, isolated tiers) unless requirements justify it. | compute | CO:07 | su-rel#factor-in-sustainability-into-platform-choices |
| WAF-07 | REVIEW | G | Size and tier each flow by its priority. Low-priority flows get cheaper tiers, and dissimilar flows aren't forced onto one oversized resource. | multiple components | CO:09 | co-flow#optimize-independent-flows, co-flow#separate-dissimilar-flows, co-flow#prioritize-flows |
| WAF-08 | REVIEW | G | Capacity per region follows the share of users each region serves. Low-traffic regions don't mirror the main region's capacity. | multi-region | CO:08 | co-env#optimize-the-production-environment |

## COST-02 — Autoscaling

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-09 | REVIEW | G | Autoscale variable-load components against observed demand instead of running a fixed, peak-sized deployment. | scalable compute | CO:12 | su-co#reduce-idle-and-baseline-platform-waste, co-comp#optimize-workload-resources, su-pe#balance-with-scalability-needs |
| WAF-10 | REVIEW | G | Rules scale in as well as out: scale out at the last responsible moment and scale in as soon as practical. | autoscaler | CO:12 | co-scale#optimize-autoscaling |
| WAF-11 | REVIEW | G | Scale on workload-relevant metrics (sustained CPU, queue length, traffic), with a cooldown or stabilization window so short spikes don't cause churn. | autoscaler | CO:12 | co-scale#optimize-autoscaling, su-rel#stabilize-demand-to-reduce-waste, su-rel#factor-in-sustainability-into-platform-choices |
| WAF-12 | REVIEW | G | Every autoscaler has a tested maximum, and non-prod maximums are lower than production. | autoscaler | CO:04 | co-guard#use-governance-policies, co-env#apply-governance, co-scale#control-supply |
| WAF-13 | REVIEW | G | Queue and event workers scale on event count or queue depth (e.g. KEDA), down to zero where possible. | queue/event workers | CO:12 | co-scale#use-event-based-scaling, co-scale#reduce-demand |

## COST-03 — Environments and idle resources

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-14 | REVIEW | G | Non-prod environments shut down, scale to zero or run on a schedule outside working hours. | non-prod env | CO:08 | co-env#apply-governance, su-co#reduce-idle-and-baseline-platform-waste, su-rel#factor-in-sustainability-into-platform-choices |
| WAF-15 | REVIEW | G | Non-prod uses lower tiers, fewer instances and lower scaling limits through per-environment parameters, while keeping the same services, OS and CPU architecture as production. | non-prod env | CO:08 | co-env#apply-governance, co-env#balance-similarity-with-production |
| WAF-16 | REVIEW | G | Non-prod isn't an exact replica of production: no geo-replication, zone redundancy or premium options unless a test needs them. | non-prod env | CO:08 | co-env#balance-similarity-with-production, co-env#optimize-development-environments |
| WAF-17 | REVIEW | G | Short-lived dev, test and preview environments are created on demand and destroyed after use. | non-prod env | CO:04 | co-guard#use-iac |
| WAF-18 | REVIEW | G | Keep preproduction environments few. Combine environments whose functions don't overlap. | non-prod env | CO:08 | co-env#evaluate-preproduction-environments, co-env#optimize-development-environments |
| WAF-19 | REVIEW | G | No orphaned or unused resources (unattached disks/IPs, empty plans, leftover proof-of-concept resources). Lifecycle tooling removes child resources with their parent. | any IaC | CO:07 | co-comp#optimize-workload-resources, su-co#reduce-idle-and-baseline-platform-waste, co-env#optimize-development-environments, su-rel#factor-in-sustainability-into-platform-choices |
| WAF-20 | REVIEW | G | Non-prod has shorter log/data retention and less frequent backups than production. | non-prod env | CO:08 | co-env#apply-governance, co-env#optimize-development-environments |

## COST-05 — Cost allocation metadata

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-21 | REVIEW | G | Apply consistent cost metadata (tags/labels for workload, environment, cost center or feature) to every resource, e.g. from a shared tag map. | any IaC | CO:03 | co-costdata#group-and-categorize-cost-data, co-guard#use-governance-policies, co-comp#be-methodical-in-optimization-efforts, su-co#make-cost-visible-and-actionable |
| WAF-22 | REVIEW | G | Every resource has an identifiable owner (owner tag, or ownership documented for the resource group or stack). | any IaC | CO:03 | co-costdata#assign-resource-owners, su-co#make-cost-visible-and-actionable |
| WAF-23 | REVIEW | G | Tagging is enforced or inherited automatically (policy, tag inheritance, provider default tags), not left to convention. | policy/provider config | CO:04 | co-guard#use-governance-policies, co-costdata#group-and-categorize-cost-data, su-oe#use-policy-to-drive-behavior-to-support-sustainability |

## COST-06 — Spending guardrails and targets

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-24 | REVIEW | G | Budgets with actual-cost and forecast-cost alerts at defined thresholds exist, preferably defined as code. | any IaC | CO:03, CO:04 | co-guard#configure-cost-alerts, co-costdata#automate-cost-alerts |
| WAF-25 | REVIEW | G | Cost anomaly alerts are configured. | any IaC | CO:03 | co-guard#configure-cost-alerts, co-costdata#automate-cost-alerts |
| WAF-26 | REVIEW | G | Policies restrict allowed resource types, SKUs and regions, at least for non-prod. | policy IaC | CO:04 | co-guard#use-governance-policies, co-env#apply-governance, su-oe#use-policy-to-drive-behavior-to-support-sustainability |
| WAF-27 | REVIEW | G | IaC pipelines estimate cost before deploying and gate releases on it. | pipeline files | CO:04 | co-guard#use-iac, co-guard#use-release-gates |
| WAF-28 | REVIEW | G | A cost estimate (cost model) and budget for the workload is documented in the repo. | docs | CO:02 | co-model#develop-the-cost-model, co-model#set-a-budget, co-model#publish-the-cost-model |
| WAF-29 | REVIEW | G | Efficiency or carbon baselines and targets are defined (e.g. cost per transaction, carbon score, CPU/memory baselines used as pipeline quality gates). | docs, pipeline files | CO:03 | su-co#make-cost-visible-and-actionable, su-oe#monitor-and-measure-sustainability, su-pe#optimize-compute-resources |

## COST-07 — Data lifecycle, retention and telemetry volume

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-30 | REVIEW | G | Storage access tiers match how often the data is read (hot / cool / cold / archive). | storage | CO:10 | co-data#optimize-data-lifecycle-management, su-co#control-storage-growth-over-time, su-pe#reduce-storage-footprint |
| WAF-31 | REVIEW | G | Lifecycle rules move data to cheaper tiers and delete it at the end of its retention period. | storage | CO:10 | co-data#optimize-data-lifecycle-management, co-data#optimize-data-volume, su-oe#use-policy-to-drive-behavior-to-support-sustainability |
| WAF-32 | REVIEW | G | Log and telemetry stores have an explicit, bounded retention period. | log workspaces, diagnostics | CO:10 | su-co#control-storage-growth-over-time, su-pe#reduce-storage-footprint, co-data#optimize-storage-solutions |
| WAF-33 | REVIEW | G | Telemetry volume is controlled: sampling, ingestion filters/transformations, only needed signals, and no verbose production log level by default. | log/telemetry config | CO:10 | su-co#make-cost-visible-and-actionable, su-sec#reduce-security-data-collection-and-processing-overhead, co-code#optimize-hot-paths, co-data#optimize-storage-solutions |
| WAF-34 | REVIEW | G | Compress stored data and use efficient formats (e.g. columnar for analytics) where the tradeoff is favorable. | storage, data pipelines | CO:10 | co-data#optimize-data-volume, co-data#optimize-file-formats, su-co#control-storage-growth-over-time |
| WAF-35 | REVIEW | G | Don't duplicate datasets across services or stores without a clear reason. | multiple data stores | CO:10 | su-co#control-storage-growth-over-time, su-co#reduce-structural-waste-in-the-application-layer, co-data#optimize-data-volume |

## COST-08 — Proportionate backup and redundancy

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-36 | REVIEW | G | Backup retention, frequency and type (incremental where possible) match stated business or compliance needs. Long-term backups go to cheaper tiers. | backup config | CO:10 | co-data#optimize-backups, su-co#control-storage-growth-over-time, su-rel#design-resiliency-intentionally |
| WAF-37 | REVIEW | G | Replication and redundancy (local / zone / geo, multi-region) match how critical the data or system is. Multi-region only where required. | storage, multi-region | CO:10 | co-data#optimize-data-replication, su-rel#design-resiliency-intentionally |
| WAF-38 | REVIEW | G | A DR environment is sized to its RTO/RPO (cold, warm, or redeploy via IaC) instead of mirroring peak production. | DR IaC | CO:08 | co-env#optimize-disaster-recovery-environments, co-comp#optimize-workload-resources, su-rel#design-resiliency-intentionally |

## COST-09 — Placement, data transfer and timing

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-39 | REVIEW | G | Keep dependent resources in the same region. Avoid cross-region routing or replication that no workload need justifies. | multi-resource | CO:10 | su-co#use-geography-and-timing-deliberately, su-co#limit-delivery-path-amplification, su-pe#reduce-network-traversal, co-data#minimize-data-transfer |
| WAF-40 | REVIEW | G | Place workloads near users when the traffic pattern justifies it. | region choice | CO:10 | su-co#use-geography-and-timing-deliberately, su-pe#reduce-network-traversal, su-rel#factor-in-sustainability-into-platform-choices |
| WAF-41 | REVIEW | G | Serve frequently requested static content from a CDN, edge cache or static hosting, with tuned cache TTLs. | static content | CO:12 | su-co#limit-delivery-path-amplification, su-pe#reduce-network-traversal, co-scale#offload-demand, co-code#use-caching-mechanisms |
| WAF-42 | REVIEW | G | Compress payloads in transit (gateway, CDN or app compression; compact serialization). | HTTP endpoints | CO:11 | su-co#limit-delivery-path-amplification, co-code#optimize-network-protocols, co-code#minimize-network-overhead |
| WAF-43 | REVIEW | G | Weigh carbon intensity alongside cost, latency and resiliency when choosing regions. | region choice | — | su-co#use-geography-and-timing-deliberately, su-rel#factor-in-sustainability-into-platform-choices |
| WAF-44 | REVIEW | G | Schedule flexible batch jobs in lower-carbon or lower-cost windows, not on fixed convenience schedules. | batch/cron schedules | — | su-co#use-geography-and-timing-deliberately |
| WAF-45 | REVIEW | G | Don't route traffic through central inspection hubs or extra hops it doesn't need. | network IaC | — | su-sec#improve-centralized-network-security-efficiency |

## COST-10 — Platform choice, consolidation and pricing model

| ID | Level | Scope | Requirement (summary) | Applies when | CO | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAF-46 | REVIEW | G | Prefer PaaS, serverless or containers to self-managed VMs where they fit the workload. | compute, databases | CO:07 | su-co#reduce-idle-and-baseline-platform-waste, su-rel#factor-in-sustainability-into-platform-choices, su-pe#use-modern-technology, co-data#optimize-storage-solutions |
| WAF-47 | REVIEW | G | Consolidate compatible components onto shared hosting (plans, clusters, database pools, gateways) to raise density, while respecting isolation needs. | multiple components | CO:14 | co-consol#consolidate-resources, co-flow#combine-similar-flows |
| WAF-48 | REVIEW | G | Reuse central shared services (log workspace, firewall, gateway) instead of deploying duplicates per workload. | platform IaC | CO:14 | co-consol#use-external-centralized-resources |
| WAF-49 | REVIEW | G | Use spot or preemptible capacity only for work that tolerates interruption, and handle eviction. | compute | CO:05 | su-co#reduce-idle-and-baseline-platform-waste, su-rel#factor-in-sustainability-into-platform-choices, co-flow#optimize-independent-flows |
| WAF-50 | REVIEW | G | Billing model fits usage: consumption pricing for ephemeral or variable use, commitments only for steady permanent components, and usage aligned with billing increments. | compute | CO:05, CO:06 | co-rates#determine-the-right-billing-model, co-billing#align-usage-to-maximize-resource-value, su-co#reduce-idle-and-baseline-platform-waste |
| WAF-51 | REVIEW | G | Apply the licensing benefits and non-production pricing the provider offers where licenses and environments allow (bring-your-own-license, dev/test pricing; e.g. Azure Hybrid Benefit `licenseType`, AWS `license_model = "bring-your-own-license"`). | licensed VMs or databases in IaC | CO:05 | co-rates#optimize-licensing-costs, co-rates#evaluate-and-commit-to-available-discounts |
