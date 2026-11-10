# Checklist — Maintainability

Subject: Maintainability

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|------------------|----------|--------|
| MAINT-01 | README & Onboarding | A README states the project's purpose and documents setup, run and test instructions | Warning | MR-01–MR-06 | MR |
| MAINT-02 | Repository Layout | Repository layout and module boundaries are clear, consistent and match any documented structure | Information | MR-07–MR-12 | MR |
| MAINT-03 | Prerequisites & Configuration | Prerequisites, toolchain versions, environment variables/config keys and local dependencies are documented | Warning | MR-13–MR-16 | MR |
| MAINT-04 | Technical Debt | Technical-debt markers and warning suppressions in the reviewed files are tracked and justified, not piling up | Information | MR-17–MR-19 | MR |
| MAINT-05 | Deprecated Code | Superseded code in the reviewed files is marked deprecated with a replacement and removal target, and isn't still used silently | Information | MR-20–MR-23 | MR |
| MAINT-06 | Contributing Guide | A contributing guide explains the development workflow, pre-submit checks and conventions | Information | MR-24–MR-26 | MR |
| MAINT-07 | Change History | Change history is recorded per version and matches the published version | Information | MR-27–MR-29 | MR |
| MAINT-08 | Architecture Docs | Architecture and significant decisions are documented in editable form | Information | MR-30–MR-32 | MR |
| MAINT-09 | Docs Accuracy | Documentation matches the code: commands, keys, versions, paths and links are current | Warning | MR-33–MR-36 | MR |
| MAINT-10 | License & Conduct | The repository states its license (`LICENSE`/`LICENSE.md` or a manifest license field), consistently; public or open-source repos also have a code of conduct | Information | MR-37–MR-39 | MR |

Source key: MR = Compliance Reviewer Maintainability Rubric (`standards/maintainability-rubric.md`).
