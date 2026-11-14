# Azure Well-Architected Framework — Reliability (Disaster Recovery) — localized summary

- Source site: learn.microsoft.com (azure/well-architected)
- Pinned pages: see the page table below (path + `ms.date` at retrieval)
- Citation base: https://learn.microsoft.com/azure/well-architected/
- Localized: 2026-11-08 · Elements: 46 IDs, 42 active (cap 100); WAFR-05, WAFR-19, WAFR-20, WAFR-41 retired 2026-11-12
- Source name for `Finding.standard`: `Azure Well-Architected Framework`
- Level: every element is `REVIEW` (the source uses no normative keywords); severity is the owning check's default.
- Scope column: G = generic (any cloud / Kubernetes). Every active element is Scope G. The Azure-only elements were retired on 2026-11-12; each had a G counterpart that still applies to Azure IaC.
- RE column: the WAF Reliability checklist code the element implements (traceability only).
- Anchor(s): `<page key>#<section anchor>`, primary first. Table rows have no anchors of their own, so the anchor is the section that holds the row. `dg-dr#suggested-actions` = backup and restore; `-1` = active-passive cold standby; `-2` = warm standby; `-3` = active-active.
- Citation URL: citation base + page path + `#` + primary anchor, with no locale segment.

| Key | Page path | ms.date |
|-----|-----------|---------|
| re-check | reliability/checklist | 2023-11-15 |
| re-prin | reliability/principles | 2025-09-30 |
| re-met | reliability/metrics | 2024-08-16 |
| re-red | reliability/redundancy | 2025-08-13 |
| re-test | reliability/reliability-test | 2026-05-27 |
| re-dr | reliability/disaster-recovery | 2025-11-19 |
| dg-dr | design-guides/disaster-recovery | 2025-09-19 |
| dg-az | design-guides/regions-availability-zones | 2025-09-08 |

## DR-01 — Backups configured for stateful stores

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-01 | REVIEW | G | Every stateful store (database, object/file storage, persistent volume, stateful VM disk) has backup or point-in-time restore enabled. No single tool covers everything: check each store. | stateful store | RE:09 | re-dr#implement-robust-backup-strategies, re-prin#design-for-recovery, dg-dr#recovery-strategy-for-backup-and-restore |
| WAFR-02 | REVIEW | G | Backup frequency or PITR window is consistent with the stated RPO (backup frequency determines the recovery point). | backup config + stated RPO | RE:09 | dg-dr#suggested-actions, dg-az#locally-redundant-deployments-with-backup-across-regions |
| WAFR-03 | REVIEW | G | Backup retention periods are set explicitly and meet stated regulatory or business retention needs. | backup config | RE:09 | dg-dr#suggested-actions, re-dr#implement-robust-backup-strategies |
| WAFR-04 | REVIEW | G | Backups account for dependencies between data stores, so a restore gives a consistent state across stores that reference each other. | multiple stores | RE:09 | re-dr#design-recovery-aware-architecture |
| WAFR-05 (retired) | — | — | *(retired 2026-11-12, Azure-only: Azure Backup / PaaS PITR; judged generically by WAFR-01)* | — | — | re-dr#azure-facilitation, dg-dr#suggested-actions, re-red#azure-facilitation |

## DR-02 — Backups tested and restorable

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-06 | REVIEW | G | A documented restore procedure exists: steps per store, target restore environment, approval and escalation contacts. | stateful store | RE:09 | dg-dr#suggested-actions, re-dr#implement-robust-backup-strategies |
| WAFR-07 | REVIEW | G | Restores are tested on a defined cadence driven by how often backup config, schema or infrastructure change (e.g. quarterly restore drills). | stateful store | RE:08 | re-test#backup-and-restore, dg-dr#suggested-actions-1 |
| WAFR-08 | REVIEW | G | Restore tests run in an environment isolated from production (e.g. staging). | restore tests/scripts | RE:08 | re-test#backup-and-restore, dg-dr#suggested-actions-1 |
| WAFR-09 | REVIEW | G | Restore tests validate data integrity and completeness, not only that the restore job succeeded. | restore tests/scripts | RE:08 | re-test#backup-and-restore, dg-dr#test-regularly-and-improve-the-plan |
| WAFR-10 | REVIEW | G | Restore duration and data loss are measured against RTO/RPO and the results recorded. | restore tests/docs | RE:08 | re-test#backup-and-restore, dg-dr#suggested-actions-1 |

## DR-03 — Recovery targets documented

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-11 | REVIEW | G | The workload has a documented criticality tier (e.g. mission-critical, business-critical, business-operational, administrative); flows or components with different criticality are tiered separately. | always | RE:09 | re-dr#prioritize-by-business-impact, dg-dr#select-your-criticality-tier, dg-dr#classify-your-workload |
| WAFR-12 | REVIEW | G | RTO and RPO are documented as time values derived from the tier, per component or flow where they differ. | always | RE:04 | re-dr#prioritize-by-business-impact, re-met#define-recovery-metrics, re-check#checklist |
| WAFR-13 | REVIEW | G | Targets reflect platform recovery guarantees, and targets not yet tested are marked as not guaranteed. | targets documented | RE:04 | re-met#define-recovery-metrics |
| WAFR-14 | REVIEW | G | DR scope is stated: which environments and components are covered, and which shared or third-party dependencies the plan relies on (and their own failover). | targets documented | RE:09 | re-dr#prepare-infrastructure-and-recovery-procedures, dg-dr#watch-out-for-these-friction-points |

## DR-04 — Multi-region posture and data replication meet the stated tier

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-15 | REVIEW | G | The deployment pattern meets the stated tier's minimum posture (SKILL.md tier table). Fail only when below it. | stated tier/targets | RE:09 | dg-dr#select-your-criticality-tier, dg-az#combine-multi-zone-and-multi-region-approaches, re-red#use-an-active-passive-architecture-design-as-a-cost-effective-dr-approach |
| WAFR-16 | REVIEW | G | Stateful data is replicated according to RPO: synchronous (across zones) for near-zero RPO, asynchronous cross-region otherwise; replication is configured on the data store. | stated RPO + stateful store | RE:09 | re-dr#design-recovery-aware-architecture, dg-az#data-replication, dg-az#synchronous-data-replication, dg-az#asynchronous-data-replication, dg-dr#suggested-actions-1 |
| WAFR-17 | REVIEW | G | The secondary region is geographically distant enough not to share the same disaster. | multi-region or cross-region backup | RE:05 | re-red#strengthen-fault-tolerance-with-geo-distant-deployments, dg-az#deployment-approach-4-multi-region-deployments |
| WAFR-18 | REVIEW | G | Secondary-region and backup locations satisfy stated data-residency requirements. | residency stated | RE:09 | dg-az#data-residency, dg-dr#suggested-actions-1 |
| WAFR-19 (retired) | — | — | *(retired 2026-11-12, Azure-only: Azure geo-redundant storage SKUs; judged generically by WAFR-16 and WAFR-28)* | — | — | dg-dr#suggested-actions-1, dg-az#region-architectures |
| WAFR-20 (retired) | — | — | *(retired 2026-11-12, Azure-only: Azure data-service geo-replication; judged generically by WAFR-16)* | — | — | dg-dr#suggested-actions-1, re-red#azure-facilitation |

## DR-05 — DR plan and runbook

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-21 | REVIEW | G | A DR runbook gives step-by-step failover instructions, references the scripts and tools to run, lists prerequisites (credentials, configuration) and names an owner for each step. | always | RE:09 | dg-dr#dr-runbook, re-dr#establish-communication-protocols |
| WAFR-22 | REVIEW | G | DR activation criteria (what counts as a disaster vs. an incident) and who may declare one are documented. | runbook exists | RE:09 | re-dr#define-disaster-thresholds, dg-dr#dr-communication-plan, dg-dr#watch-out-for-these-friction-points, dg-dr#suggested-actions-1 |
| WAFR-23 | REVIEW | G | Recovery is sequenced by dependency and priority at component, data and workload level (e.g. databases before the apps that use them). | runbook exists | RE:09 | re-dr#prepare-infrastructure-and-recovery-procedures, dg-dr#dr-runbook |
| WAFR-24 | REVIEW | G | A failback procedure exists and is separate from failover. | runbook exists | RE:09 | re-dr#prepare-infrastructure-and-recovery-procedures, dg-dr#dr-runbook, dg-dr#watch-out-for-these-friction-points |
| WAFR-25 | REVIEW | G | Post-failover tasks (DNS, traffic routing, connection strings) and post-recovery health and data-integrity checks are documented. | runbook exists | RE:09 | re-dr#prepare-infrastructure-and-recovery-procedures, dg-dr#dr-runbook |
| WAFR-26 | REVIEW | G | A communication and escalation plan exists: roles, contacts, channels, escalation triggers and severity levels. | runbook exists | RE:09 | dg-dr#dr-communication-plan, dg-dr#dr-escalation-plan, re-dr#establish-communication-protocols |
| WAFR-27 | REVIEW | G | The runbook is version-controlled and stored where it stays reachable during a regional outage (replicated, offline or printable copy). | runbook exists | RE:09 | re-dr#ensure-accessibility-during-outages, dg-dr#dr-runbook |

## DR-06 — Backup and recovery-asset protection

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-28 | REVIEW | G | Backups are copied or stored in a different region from the primary data (geo-redundant backup vault, cross-region copy). | backup config | RE:09 | re-dr#implement-robust-backup-strategies, dg-dr#suggested-actions, dg-az#zone-redundant-deployments-with-backup-across-regions |
| WAFR-29 | REVIEW | G | Backups are immutable or protected against deletion and alteration (e.g. immutability policy, soft delete, WORM, vault lock). | backup config | RE:09 | re-prin#design-for-recovery |
| WAFR-30 | REVIEW | G | Backups are transactionally consistent (application-consistent snapshots or database-native backups, not crash-only disk copies of running databases). | backup config | RE:09 | re-prin#design-for-recovery |
| WAFR-31 | REVIEW | G | Components that provide redundancy or recovery (data stores, DNS zones, traffic routing, backup vaults) have delete protection (resource locks, `prevent_destroy`, deletion-protection flags) as a complement to backups. | IaC for those components | RE:05 | re-red#apply-delete-protection-to-preserve-redundancy |
| WAFR-32 | REVIEW | G | DR assets (plans, credentials, certificates, keys, scripts) are protected and replicated across regions. | DR assets in scope | RE:09 | re-dr#ensure-accessibility-during-outages |

## DR-07 — Recoverable as code

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-33 | REVIEW | G | The environment is defined as IaC and parameterized by region/location, so it can be redeployed into a secondary region. | IaC | RE:09 | dg-az#locally-redundant-deployments-with-backup-across-regions, dg-dr#suggested-actions-1, re-dr#automate-recovery-procedures-safely |
| WAFR-34 | REVIEW | G | Secondary-region parity is defined in IaC: network topology, identity/RBAC, policies, security baseline and monitoring, not only compute and data. | multi-region or redeploy strategy | RE:09 | re-dr#prepare-infrastructure-and-recovery-procedures, dg-dr#suggested-actions-1 |
| WAFR-35 | REVIEW | G | Deployment pipelines and their dependencies (agents, artifact and state stores) can deploy to the secondary region when the primary is down. | pipeline files | RE:09 | re-dr#ensure-accessibility-during-outages, re-dr#automate-recovery-procedures-safely, dg-az#locally-redundant-deployments-with-backup-across-regions, dg-dr#suggested-actions-1 |
| WAFR-36 | REVIEW | G | Recovery automation is declarative and idempotent; manual approval gates are documented with owners. | recovery scripts | RE:09 | re-dr#automate-recovery-procedures-safely |
| WAFR-37 | REVIEW | G | Resources that aren't backed up can be rebuilt from version-controlled sources (IaC, images, configuration). | IaC | RE:09 | re-dr#implement-robust-backup-strategies |

## DR-08 — Failover configuration

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-38 | REVIEW | G | Global traffic routing fits the DR pattern (priority routing for active-passive; latency or weighted for active-active) with health probes per endpoint. | multi-region + stated tier | RE:09 | dg-dr#suggested-actions-1, dg-dr#suggested-actions-2, dg-dr#suggested-actions-3, re-red#use-an-active-passive-architecture-design-as-a-cost-effective-dr-approach |
| WAFR-39 | REVIEW | G | Managed data services have automatic failover enabled where supported and the tier needs it; services without it have documented manual failover steps. | multi-region data + stated tier | RE:09 | dg-dr#suggested-actions-2 |
| WAFR-40 | REVIEW | G | Standby capacity can reach full load: warm standby has autoscale rules and pre-defined scale targets; cold standby has scale parameters in IaC. Fail only when below the stated tier. | standby region | RE:09 | dg-dr#suggested-actions-1, dg-dr#suggested-actions-2, dg-dr#suggested-actions-3, re-test#incidents-and-disaster-recovery-dr |
| WAFR-41 (retired) | — | — | *(retired 2026-11-12, Azure-only: Front Door / Traffic Manager / Site Recovery; judged generically by WAFR-38)* | — | — | dg-dr#suggested-actions-1, re-dr#azure-facilitation |
| WAFR-42 | REVIEW | G | Replication health and lag are monitored with alerts, and observability covers the secondary region. | replication configured | RE:09 | dg-dr#suggested-actions-1 |

## DR-09 — DR testing and plan maintenance

| ID | Level | Scope | Requirement (summary) | Applies when | RE | Anchor(s) |
|----|-------|-------|-----------------------|--------------|----|-----------|
| WAFR-43 | REVIEW | G | The DR plan defines drill types and cadence (tabletop, non-production dry run, production drill). | always | RE:09 | re-dr#practice-with-regular-drills, dg-dr#test-regularly-and-improve-the-plan, re-test#test-and-assess-your-plan-with-tabletop-exercises |
| WAFR-44 | REVIEW | G | Full failover and failback are tested end to end (DNS switch, data consistency, client reconnection), in a non-production environment first. | multi-region or redeploy strategy | RE:08 | re-test#incidents-and-disaster-recovery-dr, re-dr#practice-with-regular-drills |
| WAFR-45 | REVIEW | G | Drill results are measured against RTO/RPO, and gaps feed back into the plan and architecture. | drill records in scope | RE:08 | re-test#incidents-and-disaster-recovery-dr, re-dr#practice-with-regular-drills, dg-dr#test-regularly-and-improve-the-plan |
| WAFR-46 | REVIEW | G | The plan is reviewed regularly (about every six months) and whenever the architecture changes, and is kept aligned with failure-mode analysis. | plan exists | RE:09 | re-dr#keep-plans-current-and-actionable, dg-dr#classify-your-workload |
