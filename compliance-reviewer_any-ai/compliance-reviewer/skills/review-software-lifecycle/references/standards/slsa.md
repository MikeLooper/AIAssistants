# SLSA specification v1.2 — localized summary

- Source site: slsa.dev · Version: v1.2 (Status: Approved) · slsa-framework/slsa `releases/v1.2` @ ae7fc7621500 (2026-04-14)
- Citation base: https://slsa.dev/spec/v1.2/
- Localized: 2026-11-09 (from the plan's 2026-11-09 planning snapshot) · Elements: 14 (cap 100)
- Source name for `Finding.standard`: SLSA v1.2
- Level: the source's RFC 2119 keyword (MUST/SHOULD) for information only; severity is the owning check's default.
- Citation: `Finding.url` = citation base + page path + `#` + primary anchor, e.g. `https://slsa.dev/spec/v1.2/source-requirements#history`.
- Elements on Source-track settings (SLSA-10 … SLSA-14) are judged only from settings-as-code (SKILL.md settings-visibility rule).

| Key | Page path | Note |
|-----|-----------|------|
| br  | build-requirements | Build track: producer and build-platform requirements |
| btb | build-track-basics | Build L0–L3 summaries |
| sr  | source-requirements | Source track L1–L4 |
| dp  | distributing-provenance | Where and how attestations are published |

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| SLSA-01 | MUST | Release artifacts are built on a hosted build platform able to reach the target Build level, not on a developer workstation. | publishes artifacts | SL-02 | br#choose-an-appropriate-build-platform, br#hosted, btb#build-l2-hosted-build-platform |
| SLSA-02 | MUST | The producer builds in a consistent way: one source-controlled build definition for every release, with ecosystem build metadata kept current. | always | SL-01 | br#follow-a-consistent-build-process |
| SLSA-03 | MUST | The build generates provenance that identifies each output by digest and describes how it was built (SLSA Provenance format recommended). | publishes artifacts | SL-05 | br#provenance-exists, btb#build-l1-provenance-exists |
| SLSA-04 | MUST | Provenance is authentic: it's signed by the build platform's identity (e.g. keyless OIDC attestation), not by a key the build script controls. | provenance generated | SL-05 | br#provenance-authentic, btb#build-l2-hosted-build-platform |
| SLSA-05 | MUST | (L3) Provenance is unforgeable and builds are isolated: provenance is generated in a trusted context that user build steps can't alter. | provenance generated | SL-05 | br#provenance-unforgeable, br#isolated, btb#build-l3-hardened-builds |
| SLSA-06 | MUST | The producer distributes provenance to consumers with the artifact (registry attestation, release asset) or through the package ecosystem. | provenance generated | SL-05 | br#distribute-provenance, dp#where-attestations-are-published |
| SLSA-07 | SHOULD | Attestations are tied to the specific release and artifact digests and are immutable once published. | provenance generated | SL-05 | dp#relationship-between-releases-and-attestations, dp#immutability-of-attestations |
| SLSA-08 | MUST | The build platform follows security best practice: access control, frequent updates and prompt fixing of known vulnerabilities (secret management: see SMG-12). | CI files in scope | SL-10 | br#security-best-practices |
| SLSA-09 | MUST | (Source L1) All source, including build and release configuration, is under version control. No build steps exist only outside the repository. | always | SL-01 | sr#level-1-version-controlled, sr#choose-scs |
| SLSA-10 | MUST | (Source L2) Access controls restrict sensitive operations, such as updating protected branches, to defined roles. | settings-as-code in scope | SL-04 | sr#access-and-history, sr#identity-management |
| SLSA-11 | MUST | (Source L2) Protected branches only advance to descendant revisions: force-push is prohibited. | settings-as-code in scope | SL-04 | sr#history |
| SLSA-12 | MUST | (Source L2) Release tags can't be moved or deleted (tag protection or immutable tags). | settings-as-code in scope | SL-04 | sr#access-and-history |
| SLSA-13 | MUST | (Source L3) Claims such as "every change is tested before merge" are enforced by SCS technical controls (required status checks) and documented. | settings-as-code in scope | SL-04 | sr#technical-controls, sr#level-3-continuous-technical-controls |
| SLSA-14 | MUST | (Source L4) Two trusted persons agree to each change to a protected branch, including the final revision. | settings-as-code in scope | SL-04 | sr#two-party-review, sr#level-4-two-party-review |
