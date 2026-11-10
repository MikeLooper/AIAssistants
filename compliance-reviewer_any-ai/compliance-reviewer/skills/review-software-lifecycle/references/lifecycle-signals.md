# Lifecycle signals — lookup table

Local lookup table, not a standard. Use it to classify CI/CD, settings and version evidence for SL-01 … SL-12; cite
the SV/SSDF/SLSA/OSC elements, never this file. If a platform, tool or setting isn't listed and you can't classify
it, add `localized-standard-gap: unrecognized <kind> <name>` to `notes`.

## 1. Platform and forge detection (all checks)

- GitHub: `.github/workflows/*.yml`, `.github/` folder.
- Azure DevOps: `azure-pipelines*.yml`, `.azuredevops/`.
- GitLab: `.gitlab-ci.yml`, `.gitlab/`.
- Jenkins: `Jenkinsfile`.
- Others: `.circleci/config.yml`, `bitbucket-pipelines.yml`.
- CODEOWNERS is supported on GitHub and GitLab. Azure DevOps uses a required-reviewer *policy* (settings-as-code
  only).

## 2. Pre-merge CI triggers — OSC-06, SSDF-01, SLSA-02, SLSA-09 (SL-01)

- Pass: GitHub `on: pull_request` (or `merge_group`). GitLab `rules: if: $CI_PIPELINE_SOURCE == "merge_request_event"`
  or MR pipelines. Azure Pipelines `pr:` trigger (GitHub/Bitbucket repos) or a build-validation policy in
  settings-as-code. Jenkins multibranch with PR discovery.
- Fail: only `push`, `schedule` or `workflow_dispatch` triggers. No pipeline definition in the repository.
- Skip, don't fail: Azure Repos ignore a `pr:` block; without settings-as-code a pre-merge build isn't visible.

## 3. Settings-as-code — SSDF-11, SSDF-15, SLSA-10 … SLSA-14, OSC-01 … OSC-03, OSC-05 (SL-04)

- Recognized forms: Terraform `github_branch_protection`, `github_repository_ruleset` (`required_pull_request_reviews`,
  `required_status_checks`, `allows_force_pushes = false`, `allows_deletions = false`, `require_code_owner_reviews`,
  `required_signatures`, tag rules); `azuredevops_branch_policy_min_reviewers`, `azuredevops_branch_policy_build_validation`;
  `gitlab_branch_protection`, `gitlab_tag_protection`; Probot `.github/settings.yml` `branches:`; exported ruleset
  JSON.
- Fail: `allows_force_pushes = true`, `required_approving_review_count = 0`, no status checks, `enforce_admins = false`
  (OSC-02).
- None of these present: skip the setting elements ("repository settings not visible in files"). Docs claims are
  not evidence.

## 4. CODEOWNERS — OSC-04, SSDF-10 (SL-04)

- Pass: `CODEOWNERS` in the root, `.github/` or `docs/` (GitHub), or `.gitlab/` (GitLab), with a `*` rule or rules
  covering pipeline and build files.
- Fail: missing on a GitHub or GitLab repo; a file with no rule covering `.github/workflows/` (or the CI files).

## 5. Workflow injection — OSC-07, OSC-08 (SL-09)

- Pass: untrusted values passed via `env:` and quoted as `"$VAR"`.
- Fail (GitHub): `pull_request_target`/`workflow_run` + `actions/checkout` with
  `ref: ${{ github.event.pull_request.head.sha }}` (or `.head.ref`); `${{ github.event.issue.title }}`/`.body`,
  `pull_request.title`/`.body`, `comment.body`, `review.body`, `head_ref`, `head_commit.message`, `pages.*.page_name`
  inside `run:`.
- Fail (Azure Pipelines): `$(System.PullRequest.SourceBranch)` or `$(Build.SourceVersionMessage)` macros inside
  `script:`.
- Fail (GitLab): `$CI_MERGE_REQUEST_TITLE`/`$CI_COMMIT_MESSAGE` used unquoted in `script:`.

## 6. Token scopes and pinning — OSC-09 … OSC-13, SSDF-05, SLSA-08 (SL-10)

- Pass (GitHub): top-level `permissions: {}` or `contents: read`, job-level writes; `uses: owner/repo@<40-hex SHA>`
  (a version comment is allowed).
- Pass (Azure Pipelines): `persistCredentials: false`; template `resources.repositories` with `ref:` to a commit.
- Pass (GitLab): `include:` with `ref:` SHA; CI job token allowlist.
- Pass (all): images `@sha256:<digest>`; installs with `npm ci`, `pip install --require-hashes`,
  `dotnet restore --locked-mode`, `poetry install --no-update`.
- Fail: no `permissions:` (inherits the repo default), `permissions: write-all`, `contents: write` at the top level;
  `uses: …@v3`/`@main`; `FROM image:tag` without digest; `curl … | sh`, `wget … | bash`, `iex (iwr …)`;
  `npm install`/`pip install pkg` without pins in CI.
- Jenkins has no token-permission scopes: skip OSC-09/OSC-10 ("no equivalent on Jenkins").
- Secret storage, OIDC and long-lived credentials are not judged here (review-security-operational SMG-12).

## 7. Release, packaging and environments — SSDF-09, SSDF-13, SLSA-01, OSC-20 (SL-02)

- Pass: release workflow on `release:`/tag push (`v*`); registry push (`dotnet nuget push`, `mvn deploy`,
  `gradle publish`, `twine upload`/`pypa/gh-action-pypi-publish`, `docker push`/`docker/build-push-action`); release
  tools (`release-please`, `semantic-release`, GoReleaser, JReleaser); GitHub `environment:` with protection, Azure
  Pipelines `deployment` jobs with `environment:`, GitLab `environment:` + `when: manual`/protected environments.
- Fail: publish from a script meant for workstations (`publish.ps1` with a local API key); production deploy in the
  same job as the PR build; publish on every push with a constant version (also SV-03).

## 8. Provenance and signing — SSDF-03, SSDF-12, SSDF-14, SLSA-03 … SLSA-07, OSC-18, OSC-19 (SL-05)

- Pass: `actions/attest-build-provenance`, `slsa-framework/slsa-github-generator` (L3 generator), `sigstore/cosign`
  (`cosign sign`/`attest`), `sigstore/gh-action-sigstore-python`, PyPI trusted publishing with attestations,
  `npm publish --provenance`, `dotnet nuget sign`, `maven-gpg-plugin`/Gradle `signing` plugin, `gpg --detach-sign`,
  published `SHA256SUMS`.
- Reproducible settings (SSDF-03): `<Deterministic>`/`<ContinuousIntegrationBuild>`, Maven
  `project.build.outputTimestamp`, `SOURCE_DATE_EPOCH`.
- Fail: provenance generated by a custom script using a producer key (SLSA-04).
- Note, don't fail here: signing key material read from a file committed to the repo (security finding, not
  lifecycle).

## 9. Version fields and SemVer mapping — SV-01 … SV-11 (SL-03)

- .NET: `<Version>`, `<VersionPrefix>` + `<VersionSuffix>`, `Directory.Build.props`, `GitVersion.yml`/MinVer/
  Nerdbank (`version.json`).
- Java: Maven `<version>` (`-SNAPSHOT` = pre-release), Gradle `version =`.
- Python: `pyproject.toml` `[project] version` or dynamic (`setuptools_scm`). PEP 440: `1.4` → `1.4.0`;
  `1.0a1`/`b1`/`rc1`/`.dev1` = pre-release; `.post1` accepted.
- Not judged: `<AssemblyVersion>`/`<FileVersion>` 4-part values.
- Fail: `v1.2.3` in a manifest (SV-11), leading zeros (`1.02.0`), two-part non-PEP 440 versions (`1.2` in
  `.csproj`/`pom.xml`), the same fixed version published by every build (SV-03).

## 10. Committed binaries — OSC-21 (SL-12)

- Fail patterns: `*.exe`, `*.dll`, `*.so`, `*.dylib`, `*.a`, `*.lib`, `*.o`, `*.obj`, `*.jar`, `*.war`, `*.ear`,
  `*.class`, `*.pyc`, `*.pyo`, `*.whl`, `*.nupkg`, `*.msi`.
- Exclude: paths matched by the target's `.gitignore`; `bin/`, `obj/`, `target/`, `build/`, `dist/`, `out/`,
  `__pycache__/`, `.venv/`, `node_modules/`; binaries referenced by a manifest (review-dependency-management DEP-08).
- Detection uses a name glob over the target, not the capped file list.
- `gradle-wrapper.jar` is common: report it, with a remark that wrapper validation
  (`gradle/actions/wrapper-validation`) mitigates it.

## 11. SAST and gates — SSDF-04, SSDF-06 … SSDF-08, SSDF-16, OSC-14 (SL-11)

- Pass: `github/codeql-action` (`init` + `analyze`), Azure DevOps `AdvancedSecurity-Codeql-*` tasks, GitLab
  `SAST.gitlab-ci.yml` template, Semgrep (`semgrep ci`), SonarScanner with quality gate wait
  (`sonar.qualitygate.wait=true`), Security Code Scan / `Microsoft.CodeAnalysis.NetAnalyzers` with
  `TreatWarningsAsErrors`, SpotBugs + FindSecBugs with `failOnError`, Bandit without `--exit-zero`; SARIF upload
  (`github/codeql-action/upload-sarif`).
- Fail: tool configured but only on `schedule`/manual; `continue-on-error: true` on the analysis step;
  `--exit-zero`/`ignoreFailures = true`; analyzers disabled (`<RunAnalyzers>false</RunAnalyzers>`).
- Lint/format rule content is not judged here (review-software-quality).
