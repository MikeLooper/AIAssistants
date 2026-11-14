---
name: review-disaster-recovery
description: 'Reviews backup, restore, recovery targets (RTO/RPO), DR runbooks, multi-region and failover posture, recoverability as code and DR testing, against the Azure Well-Architected Framework (Reliability) and NIST SP 800-34. Use when the compliance-reviewer orchestrator delegates the Disaster Recovery subject. Marked N/A when no IaC is found.'
user-invocable: false
---

# Review: Disaster Recovery

Assesses whether the workload can recover from data loss and regional disasters, as visible in IaC, backup and
restore scripts, pipeline files and DR documentation, using local, pinned summaries of the Azure Well-Architected
Framework (Reliability) and NIST SP 800-34 Rev. 1.

## Inputs

Stateful-store IaC (databases, storage, volumes) with their backup/replication settings, backup/restore scripts,
region and traffic-routing IaC, deployment pipeline files, and DR documentation (runbooks, README, ADRs), per
`compliance-inventory`. The orchestrator marks this subject N/A when `iacFound` is false.

## Standards (local, authoritative)

- `references/standards/azure-well-architected-reliability-dr.md` — WAFR-01…WAFR-46 (WAFR-05, WAFR-19, WAFR-20, WAFR-41 retired). Always load.
- `references/standards/nist-sp-800-34-contingency-planning.md` — SP34-01…SP34-25. Always load.
- `references/standards/owasp-secrets-backup.md` — OSM-01 (secret-store backup and break-glass). Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md` and the three standards files.
2. Every active element is generic and applies to any cloud, Kubernetes or on-premises IaC; judge each one by the
   cloud-neutral requirement, using the target's own resource types as evidence. Retired rows are not evaluated.
3. Find the stated recovery tier or targets (criticality tier, SLO, RTO, RPO, FIPS 199 impact) in the files. Map them
   to the minimum posture with the tier table below. If none is stated, DR-04 and DR-08 are N/A ("no stated recovery
   target to judge against"); DR-03 reports the missing targets.

   | Stated tier / target | Minimum posture |
   |---|---|
   | Tier 0 / SLO > 99.99 % / RTO seconds, RPO ≈ 0 / FIPS 199 high + mission-critical | Active-active multi-region, zone-redundant per region, near-zero-lag replication |
   | Tier 1 / ≈ 99.95 % / RTO, RPO minutes | Active-active or warm standby in a second region; cross-region data replication |
   | Tier 2 / ≈ 99.9 % / RTO, RPO hours / FIPS 199 moderate | Warm or cold standby redeployable from IaC; cross-region replication or geo-redundant backups |
   | Tier 3 / < 99.9 % / RTO hours–days / FIPS 199 low | Backup and restore with backups copied to another region |

4. Stateful stores: DR-01, DR-02 and DR-06 apply when a stateful store (database, object/blob/file storage,
   persistent volume, VM disk with state, durable queue) is visible in the files; otherwise mark them N/A ("no
   stateful store in scope"). A stateful store with no backup or point-in-time restore fails DR-01. OSM-01 applies when
   a secret or key store is defined in the IaC; a missing break-glass procedure is evidence only when the repo's docs
   are in the file list.
5. For each check (DR-01…DR-09), evaluate only the elements it lists whose "Applies when" condition holds. If none
   apply, mark the check N/A with that reason.
6. Sufficiency only: fail an element only when protection is absent or below the stated tier/targets. Never fail
   anything for exceeding them (over-provisioning is assessed by `review-cost-sustainability`).
7. Evidence rule: fail only on concrete evidence in the files. A missing document is evidence only for DR-03, DR-05
   and DR-09, and only when the repo's docs or README are in the file list. Use confidence `medium` unless the
   evidence is unambiguous.
8. Severity: every Finding takes the check's default severity from `checklist.md` regardless of element level;
   `checkResults.severityIfFailed` is always that default.
9. Citations: `standard` = "<source name> — <element ID>" (source name from the standards file header).
   WAF `url` = citation base + page path + "#" + primary anchor (first listed). NIST `url` = citation base +
   "#page=" + PDF page, with the primary section in `notes`. OSM `url` = citation base + "#" + anchor.
   `urlsFetched` stays empty.
10. Boundaries: **owned here** — cross-region posture (DR-04/08), backups (DR-01), delete protection (WAFR-31,
    DR-06), restore tests (DR-02) and DR drills (DR-09). **Don't fail for** in-region HA, zone redundancy, instance
    counts, routing and restart probes (review-reliability AZRL-27/29/48–51); alert rules on replication lag or
    backup failure (review-monitoring; this skill judges failover configuration, WAFR-42, as posture only);
    resilience, fault-injection or chaos tests (review-testing TST-13; this skill keeps restore tests and drills);
    encryption and key management of the live data store (review-security-operational; this skill keeps backup
    encryption with separate keys, SP34-18); over-provisioned DR capacity (review-cost-sustainability; see step 6).

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
