# Checklist — Monitoring

Health checks (formerly MON-01) and SLO/SLI documentation (formerly MON-04) are source/doc-visible and now live in `review-observability` as `OBS-06`/`OBS-07`. This checklist keeps only the checks that need infrastructure-as-code or monitoring config to evaluate; the subject is skipped entirely (N/A) when `iacFound` is false — see `compliance-inventory`.

Each check is evaluated against the local standards elements it lists (see `standards/`). Every element belongs to exactly one check.
Sources: WAFM = `standards/azure-well-architected-monitoring.md`; SREM = `standards/google-sre-monitoring-alerting.md`.

| id | Check | Default severity | Elements | Source |
|----|-------|-------------------|----------|--------|
| MON-01 | Alert rules cover error rate, latency (percentiles), saturation/resource exhaustion, traffic anomalies, async backlog, critical jobs, dependencies and security events (auth failures, privileged changes, secret access, firewall/WAF denies) | Warning | WAFM-01–WAFM-10, WAFM-41, WAFM-42, SREM-01–SREM-05 | WAFM, SREM |
| MON-02 | Alerts, notification targets and dashboards are defined as version-controlled code, deployed with the workload, templated and tested | Information | WAFM-11–WAFM-13, SREM-06–SREM-09 | WAFM, SREM |
| MON-03 | Alerts are actionable: symptom-based, SLO- or baseline-derived thresholds over sustained windows, severity-classified, aggregated, scoped, with context | Warning | WAFM-14–WAFM-19, SREM-10–SREM-17 | WAFM, SREM |
| MON-04 | Every alert is routed: notification target, owner, severity-based paging vs ticketing, de-duplication/inhibition, incident tooling and runbooks; security alerts reach a security owner or SIEM | Warning | WAFM-20–WAFM-22, WAFM-43, WAFM-44, SREM-18–SREM-20 | WAFM, SREM |
| MON-05 | Dashboards present actionable health: golden signals and health states with drill-down, audience-specific, parameterized, trends and target attainment | Information | WAFM-23–WAFM-29, SREM-21–SREM-24 | WAFM, SREM |
| MON-06 | Telemetry reaches monitoring from all layers: resource diagnostics routed, black-box probes, platform-health alerts, network monitoring, protected stores with explicit retention | Warning | WAFM-30–WAFM-40, SREM-25–SREM-28 | WAFM, SREM |

Totals: 44 WAFM + 28 SREM = 72 elements across 6 checks.
