# Checklist — Cost & Sustainability

Each check is evaluated against the local standards elements it lists (see `standards/`). Every element belongs to exactly one check.
Sources: WAF = `standards/azure-well-architected-cost-sustainability.md`; GSFL = `standards/green-software-principles.md`; GSP = `standards/green-software-patterns.md`.

| id | Check | Default severity | Elements | Source |
|----|-------|-------------------|----------|--------|
| COST-01 | Compute and service tiers are sized to the workload; no unjustified oversized fixed SKU or unused premium features | Warning | WAF-01–WAF-08, GSP-01–GSP-03 | WAF, GSP |
| COST-02 | Autoscaling is configured for variable load, scales in as well as out, with sensible metrics, cooldowns and maximums | Warning | WAF-09–WAF-13, GSP-04–GSP-08 | WAF, GSP |
| COST-03 | Non-production environments are scaled down, scheduled off or ephemeral, kept few, and free of orphaned resources | Information | WAF-14–WAF-20, GSP-09–GSP-12 | WAF, GSP |
| COST-04 | *(retired 2026-11-07: not evaluated, not written to `checkResults`; ID never reused)* | — | — | — |
| COST-05 | Resources carry consistent cost-allocation and owner metadata, enforced or inherited automatically | Warning | WAF-21–WAF-23 | WAF |
| COST-06 | Spending guardrails and efficiency targets exist: budgets/alerts, policy limits, pre-deploy cost checks, documented cost model or carbon metric | Information | WAF-24–WAF-29, GSFL-04 | WAF, GSFL |
| COST-07 | Storage tiers, lifecycle rules and bounded log/telemetry retention and volume keep data growth in check | Warning | WAF-30–WAF-35, GSP-13–GSP-16 | WAF, GSP |
| COST-08 | Backup retention, replication and DR capacity are proportionate to stated requirements | Information | WAF-36–WAF-38, GSP-17 | WAF, GSP |
| COST-09 | Region placement, data transfer, caching/compression and batch timing minimize transfer and consider carbon intensity | Information | WAF-39–WAF-45, GSFL-01, GSP-18–GSP-21 | WAF, GSFL, GSP |
| COST-10 | Platform choice, consolidation and pricing model fit the workload (PaaS/serverless/containers, density, spot, licensing) | Information | WAF-46–WAF-51, GSFL-02, GSFL-03, GSP-22, GSP-23 | WAF, GSFL, GSP |

Active checks: 9 (COST-01…COST-03, COST-05…COST-10). Elements: 51 WAF + 4 GSFL + 23 GSP = 78.
