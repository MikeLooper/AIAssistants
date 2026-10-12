# Checklist — Cost & Sustainability

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| COST-01 | Compute resources are sized to the stated workload, not an unjustified oversized fixed SKU | Warning | https://learn.microsoft.com/azure/well-architected/cost-optimization/ |
| COST-02 | Autoscaling is configured for variable load rather than a fixed peak-sized deployment | Warning | https://learn.microsoft.com/azure/well-architected/cost-optimization/ |
| COST-03 | Non-production environments have a scale-to-zero or scheduled shutdown where visible in IaC | Information | https://learn.microsoft.com/azure/well-architected/cost-optimization/ |
| COST-04 | The app avoids unnecessary polling/chatty calls that waste compute and energy | Information | https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-get-started |
