# Subject-to-File Map

| Subject skill | Files to include |
|----------------|-------------------|
| review-software-quality | all source files (sampled if very large), files with high change frequency if git history is available, entry points, module/project folder structure, IaC files (for layering/coupling checks) |
| review-software-lifecycle | `.github/workflows/*`, `azure-pipelines.yml`, `Jenkinsfile`, `CHANGELOG*`, version files, branch protection docs, `SECURITY.md` |
| review-twelve-factor | config files, `Dockerfile`, `docker-compose*.yml`, entry point files, dependency manifests, `.env.example` |
| review-api-design | `openapi.*`, `swagger.*`, controllers/routers, API-related DTOs |
| review-security-identity-access | auth middleware/filters, login/token code, session config, identity provider config |
| review-security-input-injection | request handlers/controllers, data access/ORM code, file upload handlers, XML parsing code |
| review-security-web-api | HTTP middleware/response header config, CORS config, REST controllers |
| review-security-operational | error handling middleware, logging config/code, secrets/config loading code |
| review-coding-standards | all source files (sampled if very large) |
| review-testing | test folders, test config, CI test steps |
| review-observability | logging/tracing/metrics setup, OpenTelemetry config, health check endpoints, SLO docs |
| review-dependency-management | dependency manifests, lock files, `02-analyzers.json` if present |
| review-reliability | HTTP client config, retry/circuit-breaker code, health check registration |
| review-performance | caching code/config, async I/O usage, connection pool config |
| review-disaster-recovery | backup/restore scripts, IaC with region/replication settings, DR runbooks — skipped when `iacFound` is false |
| review-monitoring | alert/dashboard-as-code files — skipped when `iacFound` is false |
| review-cost-sustainability | IaC scaling/sizing settings, autoscaling config — skipped when `iacFound` is false |
| review-maintainability | README/docs files, folder structure, module boundaries |

Skills not listed with a distinct scope (e.g. those relying entirely on `02-analyzers.json`) use the analyzer output alone when no relevant source files exist.
