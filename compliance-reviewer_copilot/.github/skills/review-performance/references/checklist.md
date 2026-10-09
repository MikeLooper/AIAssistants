# Checklist — Performance

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| PERF-01 | Expensive/repeated reads use a cache with a sane invalidation/expiry strategy | Warning | https://learn.microsoft.com/azure/well-architected/performance-efficiency/ |
| PERF-02 | I/O-bound operations in request-handling paths use async/non-blocking APIs | Warning | https://learn.microsoft.com/azure/well-architected/performance-efficiency/ |
| PERF-03 | DB/HTTP clients use connection pooling rather than a new connection per call | Warning | https://learn.microsoft.com/azure/well-architected/performance-efficiency/ |
| PERF-04 | No obvious N+1 query pattern in data access code | Warning | https://learn.microsoft.com/azure/well-architected/performance-efficiency/ |
| PERF-05 | No repeated expensive work inside hot loops that could be hoisted/batched/memoized | Information | https://learn.microsoft.com/azure/well-architected/performance-efficiency/ |
