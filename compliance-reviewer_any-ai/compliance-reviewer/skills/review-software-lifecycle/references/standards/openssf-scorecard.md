# OpenSSF Scorecard checks v5.6.0 — localized summary

- Source site: github.com · Version: ossf/scorecard release v5.6.0 (published 2026-10-12; tag ref 30831805a70d), `docs/checks.md` (generated from `checks.yaml`)
- Citation base: https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md
- Localized: 2026-11-09 (from the plan's 2026-11-09 planning snapshot) · Elements: 21 from 9 checks (cap 100)
- Source name for `Finding.standard`: OpenSSF Scorecard v5.6.0
- Level: every element is `REVIEW` (Scorecard describes heuristics, not normative requirements); severity is the owning check's default.
- Anchors: lower-case check names on `checks.md`. Citation: `Finding.url` = citation base + `#` + anchor, e.g. `https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#token-permissions`.
- Platform: Scorecard documents GitHub. For Azure Pipelines, GitLab CI and Jenkins apply the equivalents in `../lifecycle-signals.md`; if none exists, skip the element with "no equivalent on <platform>".

| Key | Page path | Note |
|-----|-----------|------|
| sc  | (citation base) | One H2 section per check |

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| OSC-01 | REVIEW | (Tier 1) Default and release branches block force pushes and deletion. | settings-as-code in scope | SL-04 | sc#branch-protection |
| OSC-02 | REVIEW | (Tier 2) Changes need a pull request with ≥ 1 approval, also for administrators; the most recent push is approved; the branch is up to date before merging. | settings-as-code in scope | SL-04 | sc#branch-protection |
| OSC-03 | REVIEW | (Tier 3) At least one status check must pass before merging. | settings-as-code in scope | SL-04 | sc#branch-protection |
| OSC-04 | REVIEW | A CODEOWNERS file exists in a supported location and covers the repository or at least its sensitive paths (pipelines, build config). | forge supports CODEOWNERS | SL-04 | sc#branch-protection |
| OSC-05 | REVIEW | (Tiers 4–5) Code-owner review or ≥ 2 reviewers are required, stale approvals are dismissed on new commits, and administrators are included. | settings-as-code in scope | SL-04 | sc#branch-protection |
| OSC-06 | REVIEW | CI runs on pull/merge requests before merge, not only on push, schedule or manual triggers. | CI files in scope | SL-01 | sc#ci-tests |
| OSC-07 | REVIEW | No `pull_request_target` or `workflow_run` workflow checks out and runs the PR's untrusted code (head ref/SHA). | GitHub workflows in scope | SL-09 | sc#dangerous-workflow |
| OSC-08 | REVIEW | Untrusted context values (issue/PR title and body, comment body, head ref, commit message) are never interpolated into inline scripts; pass them through environment variables instead. | CI files in scope | SL-09 | sc#dangerous-workflow |
| OSC-09 | REVIEW | Workflow tokens are least privilege: top-level `permissions` are read-only or empty, and write scopes are declared per job. | CI files in scope | SL-10 | sc#token-permissions |
| OSC-10 | REVIEW | Sensitive write scopes (`actions`, `checks`, `contents`, `deployments`, `packages`, `security-events`, `statuses`) are granted only to jobs that need them, such as release/publish jobs. | CI files in scope | SL-10 | sc#token-permissions |
| OSC-11 | REVIEW | Third-party actions, reusable workflows and pipeline tasks/templates are pinned to a full commit SHA, not a mutable tag or branch. | CI files in scope | SL-10 | sc#pinned-dependencies |
| OSC-12 | REVIEW | Container images used for building and releasing (Dockerfile `FROM`, job `container:`/`services:`) are pinned by digest. | CI Dockerfiles or job containers in scope | SL-10 | sc#pinned-dependencies |
| OSC-13 | REVIEW | Build and CI scripts don't pipe downloads into a shell, and CI installs use locked or hashed forms (`npm ci`, `pip --require-hashes`, `dotnet restore --locked-mode`). | CI/build scripts in scope | SL-10 | sc#pinned-dependencies |
| OSC-14 | REVIEW | A SAST tool (e.g. CodeQL, Semgrep, SonarQube/SonarCloud) runs on pull requests and/or pushes to the default branch. | always | SL-11 | sc#sast |
| OSC-15 | REVIEW | A security policy (`SECURITY.md`, case-insensitive) exists in the root, `.github/` or `docs/`. | always | SL-07 | sc#security-policy |
| OSC-16 | REVIEW | The policy gives a private reporting channel: an email address or an http(s) URL for reporting vulnerabilities. | security policy exists | SL-07 | sc#security-policy |
| OSC-17 | REVIEW | The policy has free text on the vulnerability process, disclosure expectations or timelines, beyond a bare link. | security policy exists | SL-07 | sc#security-policy |
| OSC-18 | REVIEW | The release workflow signs release artifacts (`.sig`, `.asc`, `.minisig`, `.sigstore`, `.sigstore.json`). | publishes artifacts | SL-05 | sc#signed-releases |
| OSC-19 | REVIEW | The release workflow publishes SLSA provenance (`*.intoto.jsonl` or a registry attestation) with every release. | publishes artifacts | SL-05 | sc#signed-releases |
| OSC-20 | REVIEW | Releases are published as a package or image through a packaging step in CI (registry push), so users get updates through a package manager. | publishes artifacts | SL-02 | sc#packaging |
| OSC-21 | REVIEW | No generated executable artifacts (`.exe`, `.dll`, `.so`, `.dylib`, `.jar`, `.war`, `.class`, `.pyc`, …) are committed. Reviewable scripts, generated source and generated docs are allowed. | always (committed-binary rule) | SL-12 | sc#binary-artifacts |
