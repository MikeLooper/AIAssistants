# Checklist — Reliability

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| REL-01 | Outbound HTTP/DB/queue calls have explicit timeouts | Error | https://learn.microsoft.com/azure/well-architected/reliability/ |
| REL-02 | Transient failures are retried with backoff (not a naive infinite/no-backoff loop) | Warning | https://learn.microsoft.com/azure/well-architected/reliability/ |
| REL-03 | Non-idempotent operations are not retried unsafely (risk of duplicate side effects) | Error | https://learn.microsoft.com/azure/well-architected/reliability/ |
| REL-04 | A circuit breaker (or equivalent) protects calls to a degraded/unavailable dependency | Warning | https://learn.microsoft.com/azure/well-architected/reliability/ |
| REL-05 | More than one instance/replica is configured for the deployed service (no single point of failure) | Warning | https://learn.microsoft.com/azure/well-architected/reliability/ |
