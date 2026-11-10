# Semantic Versioning 2.0.0 — localized summary

- Source site: semver.org · Version: 2.0.0 (`/spec/v2.0.0.html`; same text as `https://semver.org/`) · `semver/semver` HEAD f99d5485190a (2025-11-05)
- Citation base: https://semver.org/spec/v2.0.0.html
- Localized: 2026-11-09 (from the plan's 2026-11-09 planning snapshot) · Elements: 11 (cap 100)
- Source name for `Finding.standard`: Semantic Versioning 2.0.0
- Level: the source's RFC 2119 keyword (MUST/SHOULD) or `REVIEW` (FAQ guidance), for information only; severity is the owning check's default.
- Anchors: spec items have no anchors of their own. Cite the section anchor and name the item ("item 6") in the finding text.
- Version fields per ecosystem and their SemVer mapping: `../lifecycle-signals.md` §9 (SKILL.md version-ecosystem rule).

| Key | Page path | Note |
|-----|-----------|------|
| sv  | (citation base) | Items 1–11 under `semantic-versioning-specification-semver`; BNF grammar; FAQ entries |

Every element belongs to **SL-03**.

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| SV-01 | MUST | The published version has the form X.Y.Z, non-negative integers without leading zeros (ecosystem mapping per `lifecycle-signals.md` §9). | a version is declared | SL-03 | sv#semantic-versioning-specification-semver (item 2), sv#backusnaur-form-grammar-for-valid-semver-versions |
| SV-02 | MUST | A versioned library, package or API declares its public API (in code or docs), so that version bumps have a meaning. | publishes a library, package or versioned API | SL-03 | sv#semantic-versioning-specification-semver (item 1), sv#documenting-the-entire-public-api-is-too-much-work |
| SV-03 | MUST | Released versions are immutable: changes ship as a new version. No re-publishing the same version, no constant version with publish-on-every-build. | publish step in scope | SL-03 | sv#semantic-versioning-specification-semver (item 3) |
| SV-04 | SHOULD | Software used in production or depended on by others is at 1.0.0 or later. 0.y.z signals unstable initial development. | 0.y.z version and a production deploy or public package | SL-03 | sv#how-do-i-know-when-to-release-100, sv#semantic-versioning-specification-semver (items 4, 5) |
| SV-05 | MUST | PATCH only for backward-compatible fixes, MINOR for backward-compatible additions **or new deprecations**, MAJOR for any incompatible API change. | change log or release notes label changes per version | SL-03 | sv#semantic-versioning-specification-semver (items 6–8) |
| SV-06 | MUST | Versions increase numerically (1.9.0 → 1.10.0), and lower components reset to 0 on a bump (1.4.2 → 1.5.0, not 1.5.2). | version history visible in a change log | SL-03 | sv#semantic-versioning-specification-semver (items 2, 7, 8) |
| SV-07 | MUST | Pre-release: hyphen + dot-separated identifiers of `[0-9A-Za-z-]`, none empty, numeric ones without leading zeros (ecosystem equivalents accepted). | a pre-release version is declared | SL-03 | sv#semantic-versioning-specification-semver (item 9) |
| SV-08 | MUST | Build metadata follows `+` with valid identifiers and is never the only difference between two releases. | build metadata in a version or version template | SL-03 | sv#semantic-versioning-specification-semver (item 10) |
| SV-09 | SHOULD | Functionality is deprecated (documented, released in a minor version) before it's removed in a major version. | change log shows removals | SL-03 | sv#how-should-i-handle-deprecating-functionality |
| SV-10 | REVIEW | An accidental breaking change in a minor or patch release is fixed by a new release that restores compatibility, and is documented. Released versions are never modified. | change log mentions such a case | SL-03 | sv#what-do-i-do-if-i-accidentally-release-a-backward-incompatible-change-as-a-minor-version |
| SV-11 | REVIEW | `v1.2.3` isn't a semantic version: a `v` prefix is fine in tag names, but the manifest version has no prefix. | manifest version or tag pattern in scope | SL-03 | sv#is-v123-a-semantic-version |
