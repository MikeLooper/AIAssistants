# Compliance Reviewer Maintainability Rubric — local standard

- Source: authored in this repository (no external source; see `../sources.md`)
- Version: 1.1 · Created: 2026-11-08 (MR-37 … MR-39 added 2026-11-09) · Elements: 39 (cap 100)
- Source name for `Finding.standard`: `Compliance Reviewer Maintainability Rubric`
- Citation base (relative to `docs/reports/`): `../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md`
- Level: every element is `REVIEW`; severity always comes from the owning check (SKILL.md).
- "Docs" means README, CONTRIBUTING, CHANGELOG, the `docs/` folder and ADRs in the subject's file list.
- A debt marker is *tracked* when it has an issue key, an issue URL, or an owner plus a date.

| ID | Level | Requirement | Applies when | Check |
|----|-------|-------------|--------------|-------|
| <a id="mr-01"></a>MR-01 | REVIEW | A root README exists and its opening section states what the project is and does. | always (evidence rule for "missing") | MAINT-01 |
| <a id="mr-02"></a>MR-02 | REVIEW | README (or a doc it links) gives setup or install steps that work from a clean checkout. | README exists | MAINT-01 |
| <a id="mr-03"></a>MR-03 | REVIEW | README gives the command(s) to build and run the application or library locally. | README exists | MAINT-01 |
| <a id="mr-04"></a>MR-04 | REVIEW | README gives the command(s) to run the automated tests. | README exists and test code or a test config is in the listing | MAINT-01 |
| <a id="mr-05"></a>MR-05 | REVIEW | Commands are copy-pasteable: in fenced code blocks, with any placeholders explained. | README has commands | MAINT-01 |
| <a id="mr-06"></a>MR-06 | REVIEW | README links to the deeper docs that exist (docs folder, CONTRIBUTING, architecture, CHANGELOG). | such docs exist in the listing | MAINT-01 |
| <a id="mr-07"></a>MR-07 | REVIEW | The top-level layout follows one recognizable convention for the stack (e.g. `src/` + `tests/`, one project per folder) and applies it consistently. | folder listing in scope | MAINT-02 |
| <a id="mr-08"></a>MR-08 | REVIEW | Folder, project and module names state their responsibility; no catch-all folders (`misc`, `stuff`, `temp`, `new`, `old`) hold production code. | folder listing in scope | MAINT-02 |
| <a id="mr-09"></a>MR-09 | REVIEW | Test code is kept apart from production code (separate folder or project, or one consistent naming pattern). | test code present | MAINT-02 |
| <a id="mr-10"></a>MR-10 | REVIEW | Where docs describe the intended structure, the actual layout matches it. | docs describe the structure | MAINT-02 |
| <a id="mr-11"></a>MR-11 | REVIEW | Build output, caches and generated code (`bin/`, `obj/`, `dist/`, `node_modules/`, `__pycache__/`) aren't committed, or generated code is marked and kept separate. | folder listing in scope | MAINT-02 |
| <a id="mr-12"></a>MR-12 | REVIEW | A multi-module repository has a root-level map of its modules (solution or workspace file, or a README section). | more than one module, project or deployable | MAINT-02 |
| <a id="mr-13"></a>MR-13 | REVIEW | Required tools and versions (runtime/SDK, package manager, database, container engine) are stated in docs or pinned (`global.json`, `.nvmrc`, `.python-version`, `.tool-versions`, `rust-toolchain*`). | always | MAINT-03 |
| <a id="mr-14"></a>MR-14 | REVIEW | Every env var or config key the reviewed files read is documented with purpose and example, or listed in a template (`.env.example`, sample settings). | the reviewed files read env vars or config keys | MAINT-03 |
| <a id="mr-15"></a>MR-15 | REVIEW | Secrets are documented by name and where to get them only; templates and samples hold placeholders, not real-looking values. | a template or sample config exists | MAINT-03 |
| <a id="mr-16"></a>MR-16 | REVIEW | External services needed to run locally (database, queue, cache, cloud emulator) have setup steps or a local stack (`docker-compose*`, dev container). | the app depends on external services | MAINT-03 |
| <a id="mr-17"></a>MR-17 | REVIEW | `TODO`/`FIXME`/`HACK`/`XXX` markers carry a tracking reference: issue key or URL, or owner plus date. | markers present in reviewed source files | MAINT-04 |
| <a id="mr-18"></a>MR-18 | REVIEW | Untracked markers don't pile up: fewer than 3 per reviewed file, and no untracked `FIXME`/`HACK` in error-handling, security or data-access code. | markers present in reviewed source files | MAINT-04 |
| <a id="mr-19"></a>MR-19 | REVIEW | Suppressed warnings (`#pragma warning disable`, `[SuppressMessage]`, `@SuppressWarnings`, `eslint-disable`, `# noqa`, `# type: ignore`) give a reason next to them. | suppressions present in reviewed source files | MAINT-04 |
| <a id="mr-20"></a>MR-20 | REVIEW | Deprecated APIs use the language mechanism (`[Obsolete]`, `@Deprecated`, `DeprecationWarning` / `@deprecated`, JSDoc `@deprecated`) with a message naming the replacement. | deprecated or legacy code in reviewed files | MAINT-05 |
| <a id="mr-21"></a>MR-21 | REVIEW | Each deprecation states a removal target (version or date) or a tracking reference. | deprecation markers present | MAINT-05 |
| <a id="mr-22"></a>MR-22 | REVIEW | Code marked deprecated isn't still called from other reviewed non-test code without a justified suppression. | deprecation markers present | MAINT-05 |
| <a id="mr-23"></a>MR-23 | REVIEW | Superseded copies kept side by side (`FooOld`, `LegacyBar`, `v1/` next to `v2/`) carry a deprecation marker or retirement plan. Unreachable or commented-out code is SQ-08. | legacy-named or versioned copies in reviewed files or the listing | MAINT-05 |
| <a id="mr-24"></a>MR-24 | REVIEW | A CONTRIBUTING guide (or a README section) explains the workflow: branching, pull requests and review expectations. | always (evidence rule for "missing") | MAINT-06 |
| <a id="mr-25"></a>MR-25 | REVIEW | It says how to run formatters, linters and tests before submitting, and the commands match the tooling config in the repo. | guide exists | MAINT-06 |
| <a id="mr-26"></a>MR-26 | REVIEW | It states the coding conventions or points to the enforced config (`.editorconfig`, linter or formatter config). | guide exists | MAINT-06 |
| <a id="mr-27"></a>MR-27 | REVIEW | A CHANGELOG or release-notes file exists, or the README links to release notes. | repo publishes versioned artifacts (publishable manifest name + version, release pipeline, or versioned API) | MAINT-07 |
| <a id="mr-28"></a>MR-28 | REVIEW | Entries are grouped by version with a date, and call out breaking changes and deprecations. | change log exists | MAINT-07 |
| <a id="mr-29"></a>MR-29 | REVIEW | The latest version in the change log matches the version in the manifest in scope. | change log and manifest both in scope | MAINT-07 |
| <a id="mr-30"></a>MR-30 | REVIEW | An architecture overview names the main components, what each is responsible for and how they interact (text or diagram). | more than one module, project or deployable, or a layered structure | MAINT-08 |
| <a id="mr-31"></a>MR-31 | REVIEW | Significant decisions are recorded (ADRs or a decisions section) with context and consequences. | same as MR-30 | MAINT-08 |
| <a id="mr-32"></a>MR-32 | REVIEW | Diagrams are kept in an editable source form (Mermaid, PlantUML, draw.io, Structurizr), not only as images. | diagrams present | MAINT-08 |
| <a id="mr-33"></a>MR-33 | REVIEW | Commands, scripts and paths named in docs exist (e.g. a documented `npm run test` is defined in `package.json`; a referenced folder is in the listing). | docs name commands, scripts or paths | MAINT-09 |
| <a id="mr-34"></a>MR-34 | REVIEW | Env vars and config keys named in docs still exist in the templates or reviewed code (no stale entries). Missing documentation is MR-14. | docs name env vars or keys | MAINT-09 |
| <a id="mr-35"></a>MR-35 | REVIEW | Versions stated in docs (runtime, SDK, framework) match the manifests or toolchain pins in scope. | docs state versions and a manifest or pin is in scope | MAINT-09 |
| <a id="mr-36"></a>MR-36 | REVIEW | Relative links in docs point to files and anchors that exist. | docs contain relative links | MAINT-09 |
| <a id="mr-37"></a>MR-37 | REVIEW | The repository states its license: a `LICENSE`/`LICENSE.md`/`COPYING` file at the root, or a license field in the root package manifest (`license` in `package.json`/`pyproject.toml`, `<licenses>` in `pom.xml`, `PackageLicenseExpression` in a `*.csproj`). | always (root listing in scope) | MAINT-10 |
| <a id="mr-38"></a>MR-38 | REVIEW | A license stated in more than one place is consistent (the license file and the manifest field name the same license). | license file and manifest field both in scope | MAINT-10 |
| <a id="mr-39"></a>MR-39 | REVIEW | Public or open-source repositories have a code of conduct (`CODE_OF_CONDUCT*` at the root, in `.github/` or in `docs/`), or the README or CONTRIBUTING links one. | the repo is public or open source (an OSI license, a public package manifest or a public forge URL in the files) | MAINT-10 |
