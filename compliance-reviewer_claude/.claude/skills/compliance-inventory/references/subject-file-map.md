# Subject-to-File Map

Every list below is expanded to concrete file paths and capped at `maxFilesPerSubject` (12) per `SKILL.md` step 6. Generated, vendored and build-output folders (`bin/`, `obj/`, `node_modules/`, `target/`, `dist/`) are always excluded.

| Subject skill | Files to include | Exclusions |
|----------------|-------------------|------------|
| review-software-quality | entry points plus one or two representative non-test source files per layer/folder (controllers, services, repositories, domain, shared/extension code) | tests, docs, prompts, config, IaC |
| review-software-lifecycle | `.github/workflows/*`, `azure-pipelines.yml`, `Jenkinsfile`, `CHANGELOG*`, version files, branch protection docs, `SECURITY.md`, `CONTRIBUTING.md` | source and test files |
| review-twelve-factor | config files, `Dockerfile`, `docker-compose*.yml`, entry point files, dependency manifests, `.env.example` | other source files, tests |
| review-api-design | `openapi.*`, `swagger.*`, controllers/routers, API-related DTOs | services, repositories, tests |
| review-security-identity-access | auth middleware/filters, login/token code, session config, identity provider config, entry point | tests, unrelated controllers |
| review-security-input-injection | request handlers/controllers, data access/ORM code, file upload handlers, XML parsing code | tests |
| review-security-web-api | HTTP middleware/response header config, CORS config, entry point, REST controllers | tests, services, repositories |
| review-security-operational | error handling middleware, logging config/code, secrets/config loading code, `appsettings*.json` | tests |
| review-testing | test project files (sampled), test config, CI test steps | production source |
| review-observability | logging/tracing/metrics setup, OpenTelemetry config, health check endpoints, SLO docs | tests, unrelated source |
| review-dependency-management | dependency manifests (including test project manifests), lock files, central package files, `02-analyzers.json` if present | all source and test code |
| review-reliability | HTTP client config, retry/circuit-breaker code, health check registration | tests, unrelated source |
| review-performance | caching code/config, async I/O usage, connection pool config | tests, unrelated source |
| review-disaster-recovery | backup/restore scripts, IaC with region/replication settings, DR runbooks — skipped when `iacFound` is false | |
| review-monitoring | alert/dashboard-as-code files — skipped when `iacFound` is false | |
| review-cost-sustainability | IaC scaling/sizing settings, autoscaling config — skipped when `iacFound` is false | |
| review-maintainability | `README*`, `CONTRIBUTING*`, docs folder (excluding prompt/history dumps), folder structure listing, module boundaries | source and test code beyond a few representative files |

Test files go only to `review-testing`; manifests go to `review-dependency-management`. Do not hand the same wide source tree to several subjects — each subject gets only the files its checklist reads.

Skills not listed with a distinct scope (e.g. those relying entirely on `02-analyzers.json`) use the analyzer output alone when no relevant source files exist.
