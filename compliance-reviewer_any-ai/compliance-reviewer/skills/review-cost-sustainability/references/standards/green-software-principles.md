# Green Software Foundation — Principles of Green Software Engineering — localized summary

- Source site: learn.greensoftware.foundation
- Pinned source: Green-Software-Foundation/learn @ dbe70f6e4e2640485b320dfd85ae5f368d2e1e88 (2026-05-21)
- Citation base: https://learn.greensoftware.foundation/ (the published site has no commit permalink; the pinned commit above identifies the localized text)
- Localized: 2026-11-07 · Elements: 4 (cap 100)
- Source name for `Finding.standard`: `Green Software Foundation Principles`
- Level: every element is `REVIEW` (the source uses no normative keywords); severity is the owning check's default.
- Anchor(s): `<page>#<section anchor>`, primary first. Citation URL: citation base + page + `/#` + primary anchor (e.g. `https://learn.greensoftware.foundation/carbon-awareness/#demand-shifting`).

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| GSFL-01 | REVIEW | Demand shifting: run time- or location-flexible work when and where grid carbon intensity is lower. | batch/cron, region choice | COST-09 | carbon-awareness#demand-shifting |
| GSFL-02 | REVIEW | Energy proportionality: run fewer, well-used servers instead of many lightly loaded ones. | compute | COST-10 | energy-efficiency#energy-proportionality |
| GSFL-03 | REVIEW | Hardware efficiency: raise device utilization through shared cloud capacity and consolidation, and avoid hardware provisioned for rare peaks. | compute | COST-10 | hardware-efficiency#increasing-device-utilization, hardware-efficiency#embodied-carbon |
| GSFL-04 | REVIEW | Measure with a rate-based metric such as the Software Carbon Intensity (SCI = ((E × I) + M) per R), not only totals. | docs | COST-06 | measurement#the-sci-equation, measurement#how-to-calculate-your-sci-score |
