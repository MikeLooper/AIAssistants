# Checklist — Twelve-Factor App

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| TF-01 | I. Codebase — one codebase tracked in version control, many deploys | Warning | https://12factor.net/codebase |
| TF-02 | II. Dependencies — explicitly declared and isolated (manifest + lock file, no reliance on system packages) | Error | https://12factor.net/dependencies |
| TF-03 | III. Config — stored in environment variables, not in code | Error | https://12factor.net/config |
| TF-04 | IV. Backing services — attached as resources via config (URL/credentials), not hardwired | Warning | https://12factor.net/backing-services |
| TF-05 | V. Build, release, run — the three stages are strictly separated | Warning | https://12factor.net/build-release-run |
| TF-06 | VI. Processes — executed as stateless, share-nothing processes | Warning | https://12factor.net/processes |
| TF-07 | VII. Port binding — the app is self-contained and exports services via port binding | Information | https://12factor.net/port-binding |
| TF-08 | VIII. Concurrency — scales out via the process model | Information | https://12factor.net/concurrency |
| TF-09 | IX. Disposability — fast startup and graceful shutdown on SIGTERM | Warning | https://12factor.net/disposability |
| TF-10 | X. Dev/prod parity — dev, staging and prod stay as similar as possible | Warning | https://12factor.net/dev-prod-parity |
| TF-11 | XI. Logs — treated as event streams, written to stdout, not managed by the app | Warning | https://12factor.net/logs |
| TF-12 | XII. Admin processes — run as one-off processes in an identical environment | Information | https://12factor.net/admin-processes |
