# Checklist — Monitoring

Health checks (formerly MON-01) and SLO/SLI documentation (formerly MON-04) are source/doc-visible and now live in `review-observability` as `OBS-06`/`OBS-07`. This checklist keeps only the checks that need infrastructure-as-code to evaluate; the subject is skipped entirely (N/A) when `iacFound` is false — see `compliance-inventory`.

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| MON-01 | Alerting rules exist for error rate, latency and resource exhaustion | Warning | https://learn.microsoft.com/azure/well-architected/operational-excellence/ |
| MON-02 | Alerts/dashboards are defined as code/config in the repo, not only manual portal setup | Information | https://learn.microsoft.com/azure/well-architected/operational-excellence/ |
