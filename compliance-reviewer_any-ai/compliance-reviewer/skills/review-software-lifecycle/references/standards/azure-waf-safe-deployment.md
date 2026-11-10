# Azure Well-Architected Framework — safe deployment practices — localized summary

- Source site: learn.microsoft.com (azure/well-architected)
- Pinned page: `operational-excellence/safe-deployments` (OE:11), `ms.date` 2026-02-11, `git_commit_id`
  a3fa10710fd98dabc8074a51d946c25b95c1a8bb (retrieved 2026-11-09)
- Citation base: https://learn.microsoft.com/azure/well-architected/operational-excellence/safe-deployments
- Localized: 2026-11-09 · Elements: 1 (cap 100)
- Source name for `Finding.standard`: Azure Well-Architected Framework
- Level: `REVIEW` (the page uses no normative keywords); severity is the owning check's default (`../../SKILL.md`).
- Anchors are written `sdp#<anchor>` (`sdp` = the citation base). Citation: `Finding.url` = citation base + `#` +
  primary (first) anchor.

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| SDP-01 | REVIEW | Production releases use progressive exposure (rings, canary with feature flags, blue-green or slot swap, one stamp at a time) with a health check or approval gate between stages, and the pipeline or deployment config defines a rollback path to the last known good version. | a production deployment job or deployment config is in scope | SL-02 | sdp#adopt-a-progressive-exposure-model, sdp#implement-failure-detection-mechanisms, sdp#establish-deployment-safety-guardrails |
