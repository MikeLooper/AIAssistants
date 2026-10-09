---
name: review-cost-sustainability
description: 'Reviews right-sizing, scaling configuration and green software principles. Use when the compliance-reviewer orchestrator delegates the Operations / Cost & Sustainability subject.'
user-invocable: false
---

# Review: Cost & Sustainability

Assesses right-sizing, autoscaling configuration, and adherence to green software principles.

## Inputs

IaC scaling/sizing settings, autoscaling config, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check compute resources are sized appropriately for stated workload (no obviously oversized fixed SKUs without justification, where this is visible in IaC).
3. Check autoscaling (horizontal or vertical) is configured for variable load, rather than a fixed always-on peak-sized deployment.
4. Check for idle-resource waste: dev/test environments that run 24/7 without a scale-to-zero or scheduled shutdown, if visible in IaC.
5. Check for green software principles: efficient algorithms/data transfer, avoiding unnecessary polling, batching where possible.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
