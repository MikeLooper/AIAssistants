# Checklist — Disaster Recovery

Subject: Disaster Recovery

Each check is evaluated against the local standards elements it lists (see `standards/`). Every element belongs to exactly one check.
Sources: WAFR = `standards/azure-well-architected-reliability-dr.md`; SP34 = `standards/nist-sp-800-34-contingency-planning.md`; OSM = `standards/owasp-secrets-backup.md`.

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|-------------------|----------|--------|
| DR-01 | Disaster Recovery | Backups or point-in-time restore are configured for every stateful store, with frequency matching RPO and explicit retention | Error | WAFR-01–WAFR-05, SP34-01, SP34-02 | WAFR, SP34 |
| DR-02 | Disaster Recovery | Backups are restorable: a restore procedure exists and restores are tested on a cadence, in isolation, for integrity, against RTO/RPO | Warning | WAFR-06–WAFR-10, SP34-03, SP34-04 | WAFR, SP34 |
| DR-03 | Disaster Recovery | A criticality tier and RTO/RPO targets (per component where they differ), recovery priorities and DR scope are documented | Warning | WAFR-11–WAFR-14, SP34-05–SP34-08 | WAFR, SP34 |
| DR-04 | Disaster Recovery | Multi-region posture and data replication meet the stated tier (never failed for exceeding it) | Information | WAFR-15–WAFR-20, SP34-09–SP34-11 | WAFR, SP34 |
| DR-05 | Disaster Recovery | A DR plan/runbook covers activation criteria, sequenced failover and separate failback, post-recovery validation, communication/escalation, and stays reachable in an outage | Information | WAFR-21–WAFR-27, SP34-12–SP34-17 | WAFR, SP34 |
| DR-06 | Disaster Recovery | Backups and recovery assets are protected: cross-region copies, immutability/soft delete, consistency, encryption with separate keys, delete protection; secret stores are backed up with a break-glass path | Warning | WAFR-28–WAFR-32, SP34-18, SP34-19, OSM-01 | WAFR, SP34, OSM |
| DR-07 | Disaster Recovery | The environment is recoverable as code: region-parameterized IaC with secondary-region parity, pipelines usable in an outage, idempotent recovery automation | Warning | WAFR-33–WAFR-37, SP34-20 | WAFR, SP34 |
| DR-08 | Disaster Recovery | Failover is configured to the stated tier: traffic routing with health probes, automatic data failover, standby capacity, replication-lag monitoring | Information | WAFR-38–WAFR-42, SP34-21 | WAFR, SP34 |
| DR-09 | Disaster Recovery | DR is tested and maintained: drill types and cadence, end-to-end failover/failback tests, results against RTO/RPO, regular plan review | Information | WAFR-43–WAFR-46, SP34-22–SP34-25 | WAFR, SP34 |

Checks: 9 (DR-01…DR-09). Elements: 46 WAFR + 25 SP34 + 1 OSM = 72.
