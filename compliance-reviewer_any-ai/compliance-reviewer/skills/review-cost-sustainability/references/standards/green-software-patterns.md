# Green Software Patterns — localized summary

- Source site: patterns.greensoftware.foundation
- Pinned source: Green-Software-Foundation/patterns @ 36ccf754849bce89af87fb5222f7bce069cd2ffd (2026-09-10)
- Citation: `https://patterns.greensoftware.foundation/<page path>#solution` (one page per pattern; the published site has no commit permalink; the pinned commit above identifies the localized text)
- Localized: 2026-11-07 · Elements: 23, covering 24 of 59 patterns (cap 100)
- Source name for `Finding.standard`: `Green Software Patterns`
- Level: every element is `REVIEW` (the source uses no normative keywords); severity is the owning check's default.
- Page path: primary page first; a merged element lists every page it absorbs.

| ID | Level | Pattern (summary) | Applies when | Check | Page path |
|----|-------|-------------------|--------------|-------|-----------|
| GSP-01 | REVIEW | Rightsize VMs to their observed utilization (vCPU/memory). | VMs | COST-01 | operations/capacity-management/match-utilization-requirements-of-vm |
| GSP-02 | REVIEW | Pick the pre-configured server size that best matches the process's utilization. | VMs / node pools | COST-01 | operations/capacity-management/match-utilization-requirements-with-pre-configured-server |
| GSP-03 | REVIEW | Evaluate non-x86 CPU architectures (e.g. Arm) for energy efficiency and performance. | compute SKUs | COST-01 | architecture/technology-selection/evaluate-other-cpu-architectures |
| GSP-04 | REVIEW | Drive average CPU utilization to an optimal level. Autoscale targets aren't set so low that instances sit idle. | autoscaler | COST-02 | operations/capacity-management/optimize-avg-cpu-utilization |
| GSP-05 | REVIEW | Scale infrastructure with user load, scaling back in periods of low or no activity. | autoscaler | COST-02 | operations/capacity-management/scale-infrastructure-with-user-load |
| GSP-06 | REVIEW | Scale Kubernetes workloads on relevant demand metrics (e.g. KEDA), down to zero when idle. | Kubernetes | COST-02 | operations/capacity-management/scale-kubernetes-workloads-based-on-events |
| GSP-07 | REVIEW | Scale logical components independently instead of scaling the whole application. | multi-component | COST-02 | architecture/system-topology/scale-logical-components-independently |
| GSP-08 | REVIEW | Keep components stateless (state externalized) so they can run small and scale freely. | app hosting config | COST-02 | architecture/system-topology/implement-stateless-design |
| GSP-09 | REVIEW | Scale down applications and hardware that aren't in use, on a schedule. | non-prod / idle apps | COST-03 | operations/capacity-management/scale-down-unused-applications |
| GSP-10 | REVIEW | Scale Kubernetes Deployments/StatefulSets to zero outside working hours. | Kubernetes non-prod | COST-03 | operations/capacity-management/scale-down-kubernetes-workloads |
| GSP-11 | REVIEW | Minimize the total number of deployed environments. | environments | COST-03 | development/minimizing-deployed-environments |
| GSP-12 | REVIEW | Decommission unused assets. Consolidate sparsely used instances (e.g. small databases) into one. | any IaC | COST-03 | operations/resource-lifecycle/remove-unused-assets |
| GSP-13 | REVIEW | Delete unused storage resources. | storage | COST-07 | operations/resource-lifecycle/delete-unused-storage-resources |
| GSP-14 | REVIEW | Set retention policies on storage so unused data is deleted automatically. | storage | COST-07 | operations/resource-lifecycle/set-retention-policy-on-storage-resources |
| GSP-15 | REVIEW | Move data off underutilized storage resources and consolidate. | storage | COST-07 | operations/resource-lifecycle/optimise-storage-resource-utilisation |
| GSP-16 | REVIEW | Compress stored data with a tool suited to each use case. | storage | COST-07 | development/data-handling/compress-stored-data |
| GSP-17 | REVIEW | Match service-level objectives (and the redundancy built for them) to what users actually need. | redundancy config | COST-08 | requirements/match-slo |
| GSP-18 | REVIEW | Choose the region closest to where most network traffic goes. | region choice | COST-09 | architecture/system-topology/choose-region-closest-to-users |
| GSP-19 | REVIEW | Cache static data (images, audio) instead of re-transferring it. | static content | COST-09 | development/data-handling/cache-static-data |
| GSP-20 | REVIEW | Compress transmitted data, and enable all supported text-compression formats on the server. | HTTP endpoints | COST-09 | development/data-handling/compress-transmitted-data, development/web-performance/enable-text-compression |
| GSP-21 | REVIEW | Time-shift recurring jobs (e.g. Kubernetes CronJobs) using carbon-intensity forecasts. | batch/cron | COST-09 | operations/time-shift-kubernetes-cron-jobs |
| GSP-22 | REVIEW | Containerize workloads with minimal dependencies. | compute | COST-10 | architecture/system-topology/containerize-your-workload-where-applicable |
| GSP-23 | REVIEW | Use serverless services where requirements allow. | compute | COST-10 | architecture/technology-selection/use-serverless |
