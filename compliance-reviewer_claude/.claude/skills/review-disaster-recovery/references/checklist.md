# Checklist — Disaster Recovery

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| DR-01 | Backups are configured for stateful stores (databases, blob storage) | Error | https://learn.microsoft.com/azure/well-architected/reliability/ |
| DR-02 | Backups are tested/restorable (a restore procedure exists, not just a backup schedule) | Warning | https://learn.microsoft.com/azure/well-architected/reliability/ |
| DR-03 | RPO/RTO targets are documented somewhere in the repo | Warning | https://learn.microsoft.com/azure/well-architected/reliability/ |
| DR-04 | Multi-region or replication is configured where the app's criticality warrants it | Information | https://learn.microsoft.com/azure/well-architected/reliability/ |
| DR-05 | A DR runbook or documented recovery procedure exists | Information | https://learn.microsoft.com/azure/well-architected/reliability/ |
