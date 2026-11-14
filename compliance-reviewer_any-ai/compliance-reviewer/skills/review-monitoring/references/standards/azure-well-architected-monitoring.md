# Azure Well-Architected Framework — Monitoring and alerting — localized summary

- Source site: learn.microsoft.com (azure/well-architected)
- Pinned pages: see the page table below (path + `ms.date` at retrieval)
- Citation base: https://learn.microsoft.com/azure/well-architected/
- Localized: 2026-11-08 (security-alerting rows WAFM-41 … WAFM-44: 2026-11-09) · Elements: 44 IDs, 41 active (cap 100); WAFM-31, WAFM-34, WAFM-44 retired 2026-11-12
- Source name for `Finding.standard`: `Azure Well-Architected Framework`
- Level: every element is `REVIEW` (the source uses no normative keywords); severity is the owning check's default.
- Scope column: G = generic (any cloud / Kubernetes / SaaS monitoring). Every active element is Scope G. The Azure-only elements were retired on 2026-11-12; each had a G counterpart that still applies to Azure IaC.
- Anchor(s): `<page key>#<section anchor>`, primary first. Rows of the `dg-mon` antipattern table have no anchors of their own, so the anchor is the table's section.
- Citation URL: citation base + page path + `#` + primary anchor, with no locale segment.

| Key | Page path | ms.date |
|-----|-----------|---------|
| oe-check | operational-excellence/checklist | 2026-02-11 |
| re-check | reliability/checklist | 2023-11-15 |
| oe-obs | operational-excellence/observability | 2026-10-24 |
| re-mon | reliability/monitoring | 2026-10-24 |
| dg-mon | design-guides/monitoring | 2026-02-18 |
| dg-hm | design-guides/health-modeling | 2026-02-11 |
| pe-mon | performance-efficiency/monitoring | 2026-04-20 |
| se-mon | security/monitor-threats (SE:10; commit bb2e40b7f88c, retrieved 2026-11-09) | 2024-02-13 |

`oe-check` (OE:07) and `re-check` (RE:10) are traceability only: OE:07 = "design a monitoring stack that captures operational telemetry, metrics and logs"; RE:10 = "continuously measure and track system health … retained and accessible".

## MON-01 — Alert coverage of key failure conditions

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| WAFM-01 | REVIEW | G | Alert rules cover failed requests / error rate for each user-facing service or entry point. | user-facing service in IaC | re-mon#monitor-all-layers-of-the-system, dg-mon#phase-3---correlation-aggregation-analysis |
| WAFM-02 | REVIEW | G | Alert rules cover latency on user-facing flows, using percentiles (p95/p99) rather than averages. | user-facing service | pe-mon#use-percentile-based-metrics, re-mon#monitor-user-experience, pe-mon#create-scoped-and-actionable-performance-alerts |
| WAFM-03 | REVIEW | G | Alert rules cover resource exhaustion and capacity limits (CPU, memory, disk, connections, quotas) of constrained resources, and the capacity ceiling of each deployment unit or stamp. | compute/data resources in IaC | re-mon#define-and-monitor-stamp-capacity, dg-mon#phase-3---correlation-aggregation-analysis |
| WAFM-04 | REVIEW | G | Alerts exist at two levels: end-to-end user experience and critical internal transactions, not only resource metrics. | user-facing service | pe-mon#create-scoped-and-actionable-performance-alerts, re-mon#make-alerts-actionable-with-a-health-model |
| WAFM-05 | REVIEW | G | Asynchronous flows are covered on completion as well as acceptance (queue depth or oldest-message age). | queues/event streams in IaC | dg-hm#identify-health-signals |
| WAFM-06 | REVIEW | G | Critical scheduled or background jobs are monitored for both execution and a valid result (ran on schedule; output not empty or malformed). | scheduled jobs in IaC | re-mon#monitor-workload-functionality |
| WAFM-07 | REVIEW | G | Dependency health is covered: dependency error rate, timeouts and latency, or indirect signals when the dependency can't be alerted on directly; retry and transient-fault rates. | external/backend dependencies | pe-mon#create-scoped-and-actionable-performance-alerts, re-mon#detect-failure-modes |
| WAFM-08 | REVIEW | G | The data/storage layer is covered: availability, write failures, query latency, timeouts, locks and resource pressure. | data stores in IaC | re-mon#monitor-all-layers-of-the-system |
| WAFM-09 | REVIEW | G | Where several instances, zones or regions are deployed, load imbalance across them and standby-region readiness are monitored. | redundant instances/regions | re-mon#monitor-load-distribution-across-redundant-instances, dg-hm#model-the-design |
| WAFM-10 | REVIEW | G | Scaling behaviour is observable: scale-out/scale-in events and cold-start latency. | autoscaling in IaC | pe-mon#monitor-elasticity |
| WAFM-41 | REVIEW | G | Alert rules cover identity and access security signals the IaC can express: sign-in or authorization failure spikes against a baseline, privilege escalation and role or policy changes, account creation or deletion, and unusual secret or key access. | identity, secret-store or role resources, or auth logs routed, in IaC | se-mon#identity-and-access-monitoring, se-mon#detect-abuse |
| WAFM-42 | REVIEW | G | Alert rules cover unexpected system and network security events: resource creation or deletion and configuration drift, failed patch or update runs, and firewall/WAF denies or unexpected DNS destinations. | firewall, WAF, network or update-management resources in IaC | se-mon#capture-system-changes, se-mon#network-monitoring |

## MON-02 — Alerts and dashboards are defined as code

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| WAFM-11 | REVIEW | G | Alert rules, notification targets, dashboards and health definitions are version-controlled IaC or config, not only portal-built. | always (IaC present) | dg-hm#maintain-your-health-model, oe-check#checklist |
| WAFM-12 | REVIEW | G | Monitoring config is deployed by automation with the workload, so it stays current as components are added or removed. | monitoring-as-code present | dg-hm#maintain-your-health-model |
| WAFM-13 | REVIEW | G | Monitoring and alerting are included in workload testing (rules are validated, not only deployed). | monitoring-as-code present | oe-obs#use-observability-to-support-continuous-improvement |

## MON-03 — Alert quality and actionability

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| WAFM-14 | REVIEW | G | Thresholds reflect workload health: derived from SLOs (when stated) or historical baselines, not arbitrary values, and fit load that varies by time of day or season. | alert rules present | oe-obs#define-alerts-around-meaningful-operational-conditions, dg-mon#best-practices-for-alerts, dg-hm#identify-health-signals |
| WAFM-15 | REVIEW | G | Alerts trigger on a sustained breach over an evaluation window, not on a single sample or transient blip. | alert rules present | re-mon#make-alerts-actionable-with-a-health-model, pe-mon#create-scoped-and-actionable-performance-alerts |
| WAFM-16 | REVIEW | G | Each alert carries context: condition and threshold breached, likely impact, components involved, where to investigate. | alert rules present | pe-mon#create-scoped-and-actionable-performance-alerts, dg-mon#best-practices-for-alerts, oe-obs#define-alerts-around-meaningful-operational-conditions |
| WAFM-17 | REVIEW | G | Alerts are classified by severity (e.g. critical, warning, informational), aligned with customer impact. | alert rules present | dg-mon#best-practices-for-alerts, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
| WAFM-18 | REVIEW | G | Correlated signals are aggregated (health state, composite or grouped alert) so one failure raises one alert, not a per-resource alert storm. | several alert rules on related resources | dg-hm#set-actionable-alerts, oe-obs#define-alerts-around-meaningful-operational-conditions, dg-mon#best-practices-for-alerts |
| WAFM-19 | REVIEW | G | Alerts are scoped deliberately; production alerting is driven by production data, not mixed with non-production signals. | alert rules + multiple environments | oe-obs#define-alerts-around-meaningful-operational-conditions, pe-mon#segment-signals-by-environment-and-purpose, dg-hm#continuous-validation |

## MON-04 — Alert routing and ownership

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| WAFM-20 | REVIEW | G | Every alert rule is wired to a notification target (action group, receiver, topic, channel). No orphaned rules. | alert rules present | oe-obs#define-alerts-around-meaningful-operational-conditions, dg-mon#best-practices-for-alerts |
| WAFM-21 | REVIEW | G | Each alert has an owning team; business-flow alerts reach application owners and component alerts reach operators. | alert rules present | oe-obs#define-alerts-around-meaningful-operational-conditions, dg-mon#best-practices-for-alerts, dg-hm#set-actionable-alerts |
| WAFM-22 | REVIEW | G | Alerts integrate with incident/ticketing tooling and, where safe, automated remediation or scaling, and tie into operational runbooks. | alert rules present | dg-mon#best-practices-for-alerts, oe-obs#define-alerts-around-meaningful-operational-conditions, dg-hm#set-actionable-alerts |
| WAFM-43 | REVIEW | G | Security alerts and security-relevant logs are routed to a security owner or a SIEM where they are correlated across sources, not only to the operations channel, and the security data sink outlives the resources it watches. | security alert rules or security logs in IaC | se-mon#centralized-threat-detection-with-correlated-logs, se-mon#store-aggregate-and-analyze-data |
| WAFM-44 (retired) | — | — | *(retired 2026-11-12, Azure-only: Defender for Cloud / Sentinel; judged generically by WAFM-43)* | — | se-mon#azure-facilitation |

## MON-05 — Dashboards present actionable health

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| WAFM-23 | REVIEW | G | Dashboards are organized around health (healthy / degraded / unhealthy), with drill-down from workload to component. | dashboards present | oe-obs#analyze-and-visualize-to-support-actionable-decisions, dg-mon#best-practices-for-visualization, dg-hm#visualize-the-model |
| WAFM-24 | REVIEW | G | Dashboards show actionable signals (availability, latency, errors, saturation) and business KPIs with supporting technical indicators, without decorative or redundant panels. | dashboards present | dg-mon#monitoring-antipatterns-and-how-to-avoid-them, dg-mon#best-practices-for-visualization |
| WAFM-25 | REVIEW | G | Dashboards are tailored to their audience and use (developers, operators, business stakeholders). | dashboards present | dg-mon#best-practices-for-visualization |
| WAFM-26 | REVIEW | G | Dashboards are parameterized for exploration (time range, environment, service, region or deployment). | dashboards present | dg-mon#best-practices-for-visualization, oe-obs#analyze-and-visualize-to-support-actionable-decisions |
| WAFM-27 | REVIEW | G | Target attainment (SLO/SLA, when stated) and longer-term trends (weekly/monthly) are visualized, not only real-time state. | dashboards present | re-mon#track-availability-targets, pe-mon#track-performance-over-time, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
| WAFM-28 | REVIEW | G | Health states are shown with text labels as well as colour (accessibility). | health dashboards present | dg-hm#visualize-the-model |
| WAFM-29 | REVIEW | G | Operator dashboards and status APIs that drive decisions are themselves monitored for stale or wrong values. | admin dashboards/status APIs in scope | re-mon#monitor-administrative-dashboards-and-status-apis |

## MON-06 — Telemetry reaches monitoring from all layers

| ID | Level | Scope | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| WAFM-30 | REVIEW | G | Every deployed resource routes its platform metrics and resource logs to the chosen monitoring backend (diagnostic settings, log export, agents). | IaC resources | dg-hm#use-platform-metrics-and-logs, oe-obs#standardize-data-consolidation |
| WAFM-31 (retired) | — | — | *(retired 2026-11-12, Azure-only: Log Analytics workspace / Azure Policy; judged generically by WAFM-30)* | — | dg-hm#use-platform-metrics-and-logs, dg-hm#add-application-logs |
| WAFM-32 | REVIEW | G | External (black-box) probes or availability tests check user-facing endpoints or health endpoints and feed alerts. | user-facing endpoint | dg-hm#use-health-probes, dg-hm#adopt-structural-and-functional-monitoring-techniques, re-mon#monitor-all-layers-of-the-system |
| WAFM-33 | REVIEW | G | Cloud-provider health events (outages, planned maintenance, advisories) notify the team. | cloud IaC | re-mon#be-informed-about-platform-reliability-status, oe-obs#define-alerts-around-meaningful-operational-conditions |
| WAFM-34 (retired) | — | — | *(retired 2026-11-12, Azure-only: Service Health / Resource Health alerts; judged generically by WAFM-33)* | — | re-mon#be-informed-about-platform-reliability-status, re-mon#azure-facilitation |
| WAFM-35 | REVIEW | G | The network layer is monitored where network IaC exists: connectivity/latency checks, flow logs. | network IaC | re-mon#monitor-all-layers-of-the-system |
| WAFM-36 | REVIEW | G | Telemetry retention is set explicitly to meet operational and stated compliance needs, so incident data isn't deleted too early. Sufficiency only: never fail for keeping more. | telemetry store in IaC | oe-obs#tailor-storage-and-retention-for-usage-patterns, dg-mon#telemetry-data-lifecycle-management, re-mon#track-recoverability-targets |
| WAFM-37 | REVIEW | G | Telemetry stores are protected like production data: access control, soft delete or resource locks against accidental change or deletion. | telemetry store in IaC | oe-obs#tailor-storage-and-retention-for-usage-patterns, dg-mon#telemetry-data-security |
| WAFM-38 | REVIEW | G | Self-managed telemetry pipelines buffer or queue ingestion and are redundant, so spikes don't lose data. | custom telemetry pipeline in IaC | oe-obs#design-scalable-durable-telemetry-pipelines, dg-mon#telemetry-performance-and-reliability-considerations |
| WAFM-39 | REVIEW | G | Multi-region workloads collect telemetry regionally and aggregate centrally; business-critical workloads keep autonomous (per-region) telemetry storage. | multi-region IaC | oe-obs#standardize-data-consolidation |
| WAFM-40 | REVIEW | G | Production telemetry is stored separately from non-production telemetry. | multiple environments in IaC | oe-obs#tailor-storage-and-retention-for-usage-patterns, pe-mon#segment-signals-by-environment-and-purpose |
