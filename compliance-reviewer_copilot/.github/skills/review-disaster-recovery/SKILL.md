---
name: review-disaster-recovery
description: 'Reviews backup, restore, RPO/RTO targets and multi-region posture. Use when the compliance-reviewer orchestrator delegates the Operations / Disaster Recovery subject.'
user-invocable: false
---

# Review: Disaster Recovery

Assesses backup/restore practices, documented RPO/RTO targets, and multi-region posture.

## Inputs

Backup/restore scripts, IaC with region/replication settings, DR runbooks, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check backups are configured for stateful stores (databases, blob storage) and are tested/restorable, not just taken.
3. Check RPO/RTO targets are documented somewhere in the repo (runbook, README, IaC comments) even if approximate.
4. Check IaC for multi-region/replication settings if the app's criticality warrants it; otherwise mark N/A with a reason.
5. If no DR-related files exist in scope at all, mark the whole subject's checks N/A rather than inventing findings.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
