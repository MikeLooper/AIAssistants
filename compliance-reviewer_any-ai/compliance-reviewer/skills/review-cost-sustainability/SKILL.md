---
name: review-cost-sustainability
description: 'Reviews right-sizing, autoscaling, environment and data lifecycle cost, and green software practices visible in infrastructure-as-code, against the Azure Well-Architected Framework (Cost Optimization, Sustainability) and Green Software Foundation guidance. Use when the compliance-reviewer orchestrator delegates the Operations / Cost & Sustainability subject. Marked N/A when no IaC is found.'
user-invocable: false
---

# Review: Cost & Sustainability

Assesses cost efficiency and sustainability as visible in IaC, deployment, scheduler and pipeline configuration,
using local, pinned summaries of the Azure Well-Architected Framework and Green Software Foundation guidance.

## Inputs

IaC compute/scaling/sizing, autoscaling, storage lifecycle and retention, backup/replication, log-workspace,
policy/budget, CDN/gateway, scheduler (cron/CronJob/timer) and CI/CD pipeline files, per `compliance-inventory`.
The orchestrator marks this subject N/A when `iacFound` is false.

## Standards (local, authoritative)

- `references/standards/azure-well-architected-cost-sustainability.md` — WAF-01…WAF-51. Always load.
- `references/standards/green-software-patterns.md` — GSP-01…GSP-23. Always load.
- `references/standards/green-software-principles.md` — GSFL-01…GSFL-04. Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md` and the three standards files.
2. Note whether the IaC is Azure (`*.bicep`, ARM deploymentTemplate JSON, or Terraform `azurerm` provider). Scope `A`
   elements apply only to Azure IaC; otherwise skip them ("Azure-specific element; target IaC is not Azure").
3. For each active check (COST-01…COST-03, COST-05…COST-10; COST-04 is retired and is not written to
   `checkResults`), evaluate only the elements it lists whose "Applies when" condition holds in the subject's files.
   If none apply, mark the check N/A with that reason (e.g. COST-08 when no backup/replication config exists;
   COST-09 when no region, CDN, compression or schedule settings are in scope).
4. Evidence rule: fail an element only on concrete evidence in the files (e.g. a fixed high SKU with N instances and
   no autoscaler or recorded justification; a storage account with no lifecycle rule; a log workspace with no
   retention). Don't fail on assumed demand. Use confidence `medium` unless the evidence is unambiguous.
5. Excess only (COST-08): fail backup retention, replication or DR capacity only when it **exceeds** the
   requirements stated in the repo (tier, SLO, RTO, RPO, retention rule). Never fail it for being insufficient or
   missing — that is assessed by `review-disaster-recovery`. If no requirement is stated, don't judge proportionality
   ("no stated recovery target to judge against"); only the cheaper-tier placement of long-term backups (WAF-36) can
   still be evaluated.
6. Severity: every element's level is REVIEW, so each Finding takes the check's default severity from
   `checklist.md`; `checkResults.severityIfFailed` is always that default.
7. Citations: `standard` = "<source name> — <element ID>" (source name from the standards file header);
   `url` = the citation the standards file header defines (WAF: citation base + page path + "#" + primary anchor;
   GSFL: base + page + "/#" + anchor; GSP: base + page path + "#solution"). `urlsFetched` stays empty.
8. Boundaries: **owned here** — autoscale maximums, over-provisioning, data archive and purge; excess backup/DR
   capacity (COST-08, see step 5); telemetry volume and over-retention. **Don't fail for** too few instances or
   zones, or too little redundancy (review-reliability AZRL-27/48; this skill fails only *excess*); missing or
   insufficient backup or DR (review-disaster-recovery; see step 5); caching, compression, async I/O or offloading in
   code (review-performance; WAF-41/42 judge only CDN/gateway config); missing logging coverage or retention below a
   requirement (review-monitoring step 6, review-observability; this skill judges only excess volume and
   over-retention, WAF-32/33); whether security inspection hops exist (security skills; WAF-45 judges only their
   cost); load or performance tests (review-testing TST-12).

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
