---
name: review-monitoring
description: 'Reviews alerting rules, alert quality and routing, dashboards-as-code and the wiring of platform telemetry, probes and platform-health alerts, against the Azure Well-Architected Framework and Google SRE guidance. Use when the compliance-reviewer orchestrator delegates the Monitoring subject. Marked N/A when no IaC is found.'
user-invocable: false
---

# Review: Monitoring

Assesses the parts of monitoring that are visible in infrastructure-as-code and monitoring config: alert rules,
notification routing, dashboards, external probes, diagnostic routing and platform-health alerts. It uses local,
pinned summaries of the Azure Well-Architected Framework and Google's SRE books. Health check endpoints and SLO/SLI
documentation are reviewed by `review-observability`.

This subject is entirely IaC-driven: when `compliance-inventory` reports `iacFound: false`, the orchestrator marks it
`applicable: false` and skips the worker call rather than invoking this skill.

## Inputs

Monitoring-as-code (alert rules, notification targets, dashboards, probes, SLO definitions), diagnostic or log-export
settings, and telemetry-store IaC, per `compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/azure-well-architected-monitoring.md` — WAFM-01…WAFM-40. Always load.
- `references/standards/google-sre-monitoring-alerting.md` — SREM-01…SREM-28. Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, `references/monitoring-iac-signals.md` and the two
   standards files.
2. Classify each file against `monitoring-iac-signals.md` (alert rule, notification target, dashboard, probe,
   diagnostic routing, platform-health alert, SLO definition, telemetry store). Note whether the IaC is Azure
   (`*.bicep`, ARM deploymentTemplate JSON, or Terraform `azurerm` provider). Scope `A` elements apply only to Azure
   IaC; otherwise skip them ("Azure-specific element; target IaC is not Azure").
3. No monitoring-as-code: if no file defines an alert rule or a dashboard, fail MON-02 (confidence `high`) and MON-01
   (confidence `low`; note that alerting configured only in a portal can't be seen from the repo), mark MON-03,
   MON-04 and MON-05 N/A ("no monitoring-as-code in scope"), and still evaluate MON-06.
4. Stated SLO: find any SLO, SLI target or availability target in the files (docs, IaC SLO resources, SLO recording
   rules, tags, alert descriptions). If none is stated, skip SLO-dependent elements (SREM-13, the target part of
   WAFM-27, the SLO-derived part of WAFM-14) with reason "no stated SLO to judge against". Never fail for the missing
   SLO itself (that is OBS-07).
5. For each check (MON-01…MON-06), evaluate only the elements it lists whose "Applies when" condition holds. If none
   apply, mark the check N/A with that reason. Security-event alerting (WAFM-41/42 under MON-01, WAFM-43/44 under
   MON-04) applies only when the IaC defines the resources whose signals it alerts on; fail it only when such resources
   exist and no alert rule or SIEM routing covers them (confidence `medium`; portal-configured SIEM rules can't be seen).
6. Retention (WAFM-36, SREM-26): fail only when retention is missing or below a stated requirement. Never fail for
   keeping more (telemetry cost is assessed by `review-cost-sustainability`).
7. Evidence rule: fail only on concrete evidence in the files, e.g. a single-sample evaluation window, an alert rule
   with no notification target, a dashboard with only CPU panels, a resource with no diagnostic routing. Don't fail
   for a missing health endpoint (OBS-06) or for code-level instrumentation (`review-observability`). Use confidence
   `medium` unless the evidence is unambiguous.
8. Severity: every Finding takes the check's default severity from `checklist.md` regardless of element level;
   `checkResults.severityIfFailed` is always that default.
9. Citations: `standard` = "<source name> — <element ID>" (source name from the standards file header);
   `url` = citation base + page path + "#" + primary anchor (first listed). `urlsFetched` stays empty.
10. Boundaries: **owned here** — all alert rules (MON-01/03), including latency-percentile, retry/failure-rate,
    dead-letter and security-event alerts (sign-in failure spikes, privileged changes, secret-access anomalies,
    WAF/firewall blocks) and their routing to a security owner or SIEM (MON-04); dashboards (MON-05); external probes
    and their thresholds (MON-06, WAFM-32); retention (step 6); telemetry-store access control (WAFM-37); alert-rule
    tests (SREM-08, MON-02). **Don't fail for** code instrumentation, health-endpoint implementation or SLO
    documentation (review-observability; see step 7); load-balancer routing and restart probe configuration
    (review-reliability AZRL-49/50; MON-06 judges only probes that raise alerts, WAFM-32); backup success and
    failover readiness as recovery posture (review-disaster-recovery; this skill judges only the alert rules);
    telemetry cost, sampling and over-retention (review-cost-sustainability; see step 6); sensitive data or secrets
    in log content (review-security-operational); application unit and integration tests (review-testing; alert-rule
    tests stay here).

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
