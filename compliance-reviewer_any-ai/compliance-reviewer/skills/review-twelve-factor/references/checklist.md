# Checklist — Twelve-Factor App

Subject: Twelve-Factor

Elements are defined in `standards/` (TFA in `twelve-factor-app.md`; TFR in `twelve-factor-rubric.md`).
Every element belongs to exactly one check. N/A rules by deployable kind: rubric applicability table.

| id | Sub-subject | Check | Default severity | Elements |
|----|-------------|-------|------------------|----------|
| TF-01 | I. Codebase | I. Codebase: one version-controlled codebase per app, with shared code consumed as libraries or project references and no per-deploy code copies | Warning | TFA-01, TFA-02, TFA-03, TFA-04, TFR-01, TFR-02 |
| TF-02 | II. Dependencies | II. Dependencies: every dependency is explicitly declared in a manifest and isolated at run time, the same way in development and production, with no reliance on undeclared system packages or tools (lock files: DEP-02) | Error | TFA-05, TFA-06, TFA-07, TFA-08, TFA-09, TFA-10, TFR-03, TFR-04, TFR-05 |
| TF-03 | III. Config | III. Config: deploy-varying values (backing-service handles, credentials, per-deploy values) come from the environment or the platform (env vars, mounted config, secret manager), never from code constants or environment-named files committed with deploy values | Error | TFA-11, TFA-12, TFA-13, TFA-14, TFA-15, TFA-16, TFA-17, TFR-06, TFR-07, TFR-08 |
| TF-04 | IV. Backing services | IV. Backing services: every backing service is an attached resource reached through a handle from config, swappable without code changes | Warning | TFA-18, TFA-19, TFA-20, TFA-21, TFA-22, TFR-09 |
| TF-05 | V. Build, release, run | V. Build, release, run: built once, combined with config at release, run unchanged; nothing built or modified at run time; deployments reference unique immutable release IDs | Warning | TFA-23, TFA-24, TFA-25, TFA-26, TFA-27, TFA-28, TFA-29, TFR-10, TFR-11 |
| TF-06 | VI. Processes | VI. Processes: stateless, share-nothing processes; persistent and session state in backing services; no sticky sessions; local disk as scratch only | Warning | TFA-30, TFA-31, TFA-32, TFA-33, TFR-12, TFR-13 |
| TF-07 | VII. Port binding | VII. Port binding: network services are self-contained and export their service by binding a port, with no runtime-injected web server | Information | TFA-34, TFA-35, TFA-36, TFA-37, TFR-14 |
| TF-08 | VIII. Concurrency | VIII. Concurrency: work is split into process types scaled by count under a process manager; no daemonizing, PID files or multi-process containers | Information | TFA-38, TFA-39, TFA-40, TFR-15 |
| TF-09 | IX. Disposability | IX. Disposability: fast startup without long blocking work, and graceful shutdown on SIGTERM that actually reaches the process | Warning | TFA-41, TFA-42, TFA-43, TFR-16, TFR-17 |
| TF-10 | X. Dev/prod parity | X. Dev/prod parity: development uses the same type and version of each backing service as production | Warning | TFA-44, TFA-45, TFA-46, TFA-47, TFR-18 |
| TF-11 | XI. Logs | XI. Logs: each process writes an event stream to stdout; the app doesn't write, rotate or route log files | Warning | TFA-48, TFA-49, TFA-50, TFA-51, TFR-19 |
| TF-12 | XII. Admin processes | XII. Admin processes: admin and migration tasks ship with the app and run as one-off processes against the same release, config and dependency isolation | Information | TFA-52, TFA-53, TFA-54, TFA-55, TFR-20 |
