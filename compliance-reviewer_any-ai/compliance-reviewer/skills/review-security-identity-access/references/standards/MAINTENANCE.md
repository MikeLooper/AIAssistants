# Maintenance — Security: Identity & Access localized standards

**Maintainers only. Workers never load this file.** Background and design decisions: `docs/plan_localize-review-security-identity-access.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-5; precedent: Cost & Sustainability DEC-1). `review-dependency-management`
also uses cheatsheetseries.owasp.org (15) and top10.owasp.org (9); those budgets are separate.

| Website | Local file(s) | Elements | Cap | Note |
|---|---|---|---|---|
| cheatsheetseries.owasp.org | owasp-identity-access.md (80) + aspnetcore-identity.md (14) + node-identity-access.md (3) | **97** | 100 | **Headroom: 3** (Node.js sheet, 3 elements, added 2026-11-09). The §7.3 follow-ups need ≈ 12; decide them against this headroom or record an exception. |
| top10.owasp.org | owasp-identity-access.md | 16 | 100 | A01:2025 (7) + A07:2025 (9) |
| docs.spring.io | spring-security.md | 13 | 100 | Spring Security Reference 7.1, 9 pages |
| docs.djangoproject.com | django-auth.md | 11 | 100 | Django 6.1, 7 pages (`ref/settings/` selected settings only) |
| expressjs.com | node-identity-access.md | 2 | 100 | Production Best Practices: Security (2026-11-09) |
| **Total** | | **139** | | |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID.
- Every element ID is listed by exactly one check in `../checklist.md`, and the "Check" column of its row names that check.
- Level:
  - OWASP cheat sheets: `MUST` where the source says must/must not/never/do not/"is mandatory"/"is required", or states a
    prohibited practice; `SHOULD` for should/recommended/prefer/consider.
  - Top 10: `MUST` for "How to prevent" bullets, `REVIEW` for "Description" weaknesses (`REVIEW` is treated like `MUST`).
  - Framework files: the level of the OWASP element the framework element implements, or `SHOULD` when the vendor only recommends.
- Primary anchor first; list every absorbed anchor so coverage stays auditable. Rows ≈ 220 characters at most.
- A framework default may appear only in a framework file, with the version it was read from. Workers may rely on no
  other default (`SKILL.md` step 3).
- Framework files are split **by language** (matching `compliance-review-core/references/languages.md` ids). A new
  framework file gets a line in `SKILL.md` and a row in the budget table.

## Refresh procedure

1. **Cadence:**
   - OWASP file: quarterly, or when run notes contain ≥ 3 `localized-standard-gap` or any `localized-standard-stale`
     entry for this skill. These sheets change often (Session Management changed 2026-11-05, Password Storage 2026-10-30).
   - Spring: within two weeks of each Spring Security minor release (May/November).
   - Django: within two weeks of each feature release.
2. **Detect drift:**
   - OWASP cheat sheets: compare the latest commit SHA of each pinned file
     (`https://api.github.com/repos/OWASP/CheatSheetSeries/commits?path=cheatsheets/<Name>_Cheat_Sheet.md&per_page=1`)
     with the pinned SHA. If they differ, diff the text and the anchor list.
   - Top 10: `https://api.github.com/repos/OWASP/Top10/commits?path=2025/docs/en/<A01|A07 file>.md&per_page=1`; also check
     whether a newer edition renumbers A01/A07.
   - Spring: `https://api.spring.io/projects/spring-security/releases` (entry with `current: true`). On a new minor,
     re-read the 9 pages and diff the anchors and the defaults in SPS-03, SPS-11, SPS-12.
   - Django: the redirect target of `https://docs.djangoproject.com/en/stable/`. On a new version, re-read the 7 pages and
     the listed settings defaults (DJ-04 … DJ-08).
3. **Update:** keep IDs stable (new IDs only, `(retired)` for removed rules). Keep cheatsheetseries.owasp.org ≤ 100 for
   this skill. Update the coverage map below, the "Localized" dates and versions in the file headers, `../sources.md`,
   and the URL list in `compliance-review-core/references/approved-sources.md` when a version path changes
   (e.g. `/reference/7.1/` → `/reference/7.2/`, `/en/6.1/` → `/en/6.2/`).
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo); run any Python over them with `-I`.
   - Script-check: every element ID in exactly one check, matching its row's "Check" column; every signal row in
     `../languages/*.md` names at least one existing element ID; every listed anchor exists as an `id` on its
     published page; every H2/H3/H4 anchor of the 8 cheat sheets, every H2/H3 anchor of the vendor pages and every
     A01/A07 Description / How-to-prevent bullet appears in the coverage map below — zero unaccounted.
   - Run reviews against small sample repos (plan §9 step 10): `validate` passes,
     `14-review-security-identity-access.json` has `urlsFetched: []` and 11 check results, expected findings cite the
     element IDs, SHOULD elements are one severity lower.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-security-identity-access` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Refresh due

- **2026-11-30:** Spring Security 7.2 GA (7.2.0-RC1 at snapshot). Re-pin `spring-security.md` to `/reference/7.2/`,
  re-check SPS rows and anchors, update `approved-sources.md` paths and `../sources.md`.
- **Django 6.2** (next feature release): re-pin `django-auth.md` and re-read the listed settings defaults.

## Localization log

### 2026-11-08 — initial localization

- Snapshot taken on 2026-11-08 (planning) and re-taken the same day at implementation (plan §9 step 1), into a scratch
  folder: 8 cheat sheets, 2 Top 10 pages, 9 Spring pages, 7 Django pages, plus the GitHub commits API and
  `api.spring.io` releases. The user approved the non-allowlisted fetches for planning and again for implementation.
- Pins confirmed unchanged against the plan (GitHub commits API, latest commit per file):

  | Page | Commit | Date |
  |---|---|---|
  | Authentication | 684d6d9d9f1a0c680ad30219f46ae4e2debf9440 | 2026-10-04 |
  | Authorization | cfd69aabc7e6090867afdc440f838b3a97cca21b | 2026-10-09 |
  | JSON Web Token | 25d263ce3c974aca348bfe0224ad14c70e561730 | 2026-10-04 |
  | OAuth 2.0 | 995524d4a18e64672c80c8e13869d29ef850bd43 | 2026-10-03 |
  | Session Management | 757270a26306e5edda9957bb7f86cfcde03c30f9 | 2026-11-05 |
  | Password Storage | 87a1faf18a29a5c33d040b000eb3c60330c30b2c | 2026-10-30 |
  | Zero Trust Architecture | 67663b741d666fbb2e75525fd85aa2b63290014a | 2026-10-04 |
  | .NET Security | 3cfa49de48236c667ddf1d0f9dc79e13e672b56d | 2026-10-18 |
  | Top 10 A01:2025, A07:2025 | d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966 | 2025-12-24 |

- Versions: Spring Security 7.1.2 is `current` GA (`api.spring.io`; pages report `data-version="7.1.2"`); 7.2.0-RC1 is a
  pre-release, so no re-pin was needed. `docs.djangoproject.com/en/stable/` redirects to `/en/6.1/`.
- Anchors: all 176 element anchors (including SPS-03's two added anchors) exist as `id`s on the published pages.
- Defaults quoted from the sources (the only defaults workers may rely on):
  - DJ-04 `AUTH_PASSWORD_VALIDATORS`: "Default: [] (Empty list) … By default, no validation is performed and all passwords are accepted."
  - DJ-05 `SESSION_COOKIE_SECURE`: "Default: False".
  - DJ-06 `CSRF_COOKIE_SECURE`: "Default: False".
  - DJ-07 `SESSION_COOKIE_HTTPONLY`: "Default: True"; `SESSION_COOKIE_SAMESITE`: "Default: 'Lax'".
  - DJ-08 `SESSION_COOKIE_AGE`: "Default: 1209600 (2 weeks, in seconds)".
  - DJ-03: "Django … uses PBKDF2 by default" (`topics/auth/passwords`).
  - SPS-11: "Validate its signature … Validate the JWT's exp and nbf timestamps and the JWT's iss claim" (runtime
    expectations); "Boot also has the audiences property for validating the aud claim" (no `aud` validation is listed
    among the defaults).
  - SPS-12: "By default, NimbusJwtDecoder, and hence Resource Server, will only trust and verify tokens using RS256."
  - SPS-06: "Spring Security protects against this automatically by creating a new session or otherwise changing the
    session ID when a user logs in."
  - SPS-13: PKCE is used automatically for public clients; for confidential clients it is on unless
    `ClientRegistration.clientSettings.requireProofKey` is set to `false`.
- Thresholds re-read: PBKDF2-HMAC-SHA256 600,000 / -SHA512 220,000 / -SHA1 1,400,000 (legacy only); Argon2id
  m=19 MiB, t=2, p=1; scrypt N=2^17, r=8, p=1; bcrypt work factor minimum 10, 72-byte input; session ID ≥ 64 bits
  entropy; idle timeouts 2–5 min (high value) / 15–30 min (low risk); minimum password length 8 with MFA / 15 without,
  maximum ≥ 64; HMAC secret ≥ output size and ≥ 160 bits entropy.
- Corrections made while checking rows:
  - **SPS-03**: the plan's "(Boot doesn't enable it by default)" isn't stated on the pinned page and was removed. The
    page does state that `@Secured` needs `securedEnabled = true` and `@RolesAllowed` needs `jsr250Enabled = true`;
    both were added, with anchors `ms#use-secured` and `ms#use-jsr250`. Signal file `java.md` updated to match.
- Level judgments (rows kept at `MUST` although the primary section has no RFC keyword):
  - ATN-18: imperative prohibition ("as risk signals, not as substitutes for authentication").
  - ATZ-03: the section states that validating "on just the majority of requests is insufficient".
  - JWT-01: imperative ("Make sure that `alg: none` is not accepted").
  - JWT-06: the sheet's verification examples require `exp` (`options={"require": ["exp", "iss", "aud"]}`).
  - SES-03: "It is therefore required to … limit the accepted session ID tracking mechanisms to just cookies."
  - SES-13: `ses#session-expiration` says "it is mandatory to set expiration timeouts for every session".
  - PWS-04: explicit floor ("with a minimum of 10").
  - Framework MUST rows (ASP-06, ASP-12, ASP-14, SPS-03, SPS-06, SPS-09, SPS-11, DJ-01, DJ-03, DJ-04, DJ-05, DJ-09)
    take the level of the OWASP MUST element they implement (SES-04/05, OAU-01, SES-03, ATZ-03, SES-11, PWS-01, JWT-05,
    ATZ-02, PWS-01, T10-09, SES-04, SES-11/SES-15).
- Sample-repo review runs (plan §9 step 10) were deferred by the user on 2026-11-08; see "Open items".

### 2026-11-09 — JavaScript/TypeScript (afterplanning WP-12f phase 2)

- `node-identity-access.md` (NDA-01 … NDA-05) and `../languages/javascript.md` from the OWASP Node.js Security Cheat Sheet (commit
  eeaa1e474bc2ef98119a3de7bafd067f52faf35e, 2026-11-05) and the Express page (session cookies, memory store, brute force). Closes this skill's JavaScript follow-up (plan C-12).
  Check count unchanged. Framework defaults beyond those stated in `node-identity-access.md` (Fastify, NestJS, Next.js, Koa, Passport,
  logger masking) stay unlocalized; workers add `localized-standard-gap` notes.

## Open items

- Plan §10 follow-ups (changes outside this skill): reviewed and closed by `docs/plan_localize-afterplanning-changes.md` on 2026-11-09 (see its Appendix A). Open hand-offs: none.
- Plan §9 step 10: run reviews against sample repos (ASP.NET Core JWT + cookie login; Spring Boot with `csrf.disable()`
  and `NoOpPasswordEncoder`; Django defaults + SPA `localStorage` token; a target with no auth).

## Follow-up candidates (plan §7.3)

| Candidate | Est. elements | Status |
|---|---|---|
| Re-authentication for sensitive features and after risk events; email-change flow | 3 | Open (DEC-8; cap headroom) |
| MFA availability and phishing-resistant factors; no SMS-only MFA | 3 (+1 T10) | Open (DEC-8) |
| Password-manager-friendly fields | 1 | Open (cap headroom) |
| Server-side session token storage as hashed verifiers | 1 | Open (cap headroom) |
| Verify all cookies of a multi-cookie session | 1 | Open (cap headroom) |
| Prefer ABAC/ReBAC over chained role checks | 1 | Open (design preference) |
| Sender-constrained access tokens (DPoP/mTLS) | 1 | Open ("may" in source) |
| Microsoft Learn ASP.NET Core docs (JwtBearer / cookie defaults) | ≈ 10 | Open (new website) |
| Flask / FastAPI auth and session docs | ≈ 6 each | Open (new websites) |
| ASVS v5.0 V6–V9 | > 100 | Open (would need an exception) |

## `localized-standard-gap` / `localized-standard-stale` log

| Date | Run | Note | Action |
|---|---|---|---|
| — | — | (none yet) | — |

## Coverage map

Every H2/H3/H4 anchor of the 8 pinned cheat sheets, every H2/H3 anchor of the pinned vendor pages and every A01/A07
Description and How-to-prevent bullet is listed once: mapped to element IDs, or given a reason code. Django
`ref/settings/` is localized for selected settings only (DJ-04 … DJ-08, DJ-11 anchors); its other settings are out of
scope. Snapshot 2026-11-08: 601 headings + 41 bullets, 0 unaccounted.

### Top 10 bullets

| Bullet | Mapped to / reason |
|---|---|
| A01 Description 1 (least privilege / deny by default) | T10-01 |
| A01 Description 2 (bypass by URL/state/HTML tampering) | T10-04, T10-05 |
| A01 Description 3 (IDOR) | T10-03 |
| A01 Description 4 (API missing access control for POST/PUT/DELETE) | T10-04 |
| A01 Description 5 (elevation of privilege) | T10-04, T10-05 |
| A01 Description 6 (JWT/cookie/hidden-field metadata manipulation) | T10-05 |
| A01 Description 7 (CORS misconfiguration) | Oweb (SEC-WA-05) |
| A01 Description 8 (force browsing) | T10-04 |
| A01 Prevent 1 (deny by default) | T10-01 |
| A01 Prevent 2 (implement once, reuse; minimize CORS) | T10-02 (CORS part: Oweb) |
| A01 Prevent 3 (record ownership) | T10-03 |
| A01 Prevent 4 (business limits in domain models) | owned by `review-software-quality` |
| A01 Prevent 5 (directory listing, `.git`, backups in web roots) | Oweb / Oops |
| A01 Prevent 6 (log access-control failures, alert) | T10-06 |
| A01 Prevent 7 (rate-limit API and controller access) | owned by `review-reliability` REL-06 (plan C-4) |
| A01 Prevent 8 (invalidate sessions on logout; short-lived JWTs) | T10-07 (session part: T10-12, SES-15) |
| A01 Prevent 9 (declarative access-control toolkits) | T10-02 |
| A07 Description 1 (credential stuffing) | T10-11 (MFA part: F) |
| A07 Description 2 (brute force not blocked) | T10-11 |
| A07 Description 3 (default/weak/well-known passwords) | T10-08, T10-09 |
| A07 Description 4 (known-breached credentials at signup) | T10-09 |
| A07 Description 5 (knowledge-based recovery) | T10-16 |
| A07 Description 6 (plaintext/encrypted/weakly hashed stores) | T10-15 |
| A07 Description 7 (missing/ineffective MFA) | F |
| A07 Description 8 (weak MFA fallbacks) | F |
| A07 Description 9 (session ID in URL/hidden field) | T10-12 |
| A07 Description 10 (session ID reused after login) | T10-12 |
| A07 Description 11 (sessions/tokens not invalidated on logout/inactivity) | T10-12 |
| A07 Description 12 (credential scope/audience not asserted) | T10-14 |
| A07 Prevent 1 (MFA) | F |
| A07 Prevent 2 (password managers) | F |
| A07 Prevent 3 (no default credentials) | T10-08 |
| A07 Prevent 4 (weak-password checks) | T10-09 |
| A07 Prevent 5 (breached-credential checks) | T10-09 |
| A07 Prevent 6 (align with NIST 800-63b) | T10-09 |
| A07 Prevent 7 (no forced rotation) | T10-09 |
| A07 Prevent 8 (no account enumeration) | T10-10 |
| A07 Prevent 9 (limit/delay failed logins; log and alert) | T10-11 |
| A07 Prevent 10 (server-side built-in session manager) | T10-12 |
| A07 Prevent 11 (premade, well-trusted auth system) | T10-13 |
| A07 Prevent 12 (verify intended use: `aud`, `iss`, scopes) | T10-14 |

### Page headings

| Code | Reason for not localizing |
|---|---|
| B | background, definitions, examples or references; no testable rule |
| P | parent heading; its rules are localized through the child anchors listed as mapped |
| C | Top 10 context (background, score table, attack scenarios, CWE list), not a requirement |
| N | organizational, device, network or platform control; not visible in application code |
| M | framework mechanics, customization or migration detail; not a security rule |
| X | optional or defense-in-depth layer; no code evidence of a defect |
| F | follow-up candidate (plan §7.3; DEC-8 or cap headroom) |
| S | superseded by a more precise element (SES-02 entropy rule) |
| S17 | background for SES-17 (the actionable rule is the localStorage warning) |
| D | framework behaviour that meets the OWASP element by default (Django rehashes on login / ignores session IDs in URLs); nothing to fail |
| Oinj | owned by `review-security-input-injection` (`docs/plan_localize-review-security-input-injection.md`) |
| Oops | owned by `review-security-operational` (logs, secrets, encryption, deployment config) |
| Oweb | owned by `review-security-web-api` (HTTPS/HSTS, security headers; `docs/plan_localize-review-security-web-api.md`) |
| Odep | owned by `review-dependency-management` |
| Otest | owned by `review-testing` TST-10 (STS-01) (plan C-5) |
| Oscope | out of identity scope (WCF transport configuration) |
| O mig | framework migration guidance; version support belongs to `review-dependency-management` |

### Authentication CS (`atn`)

- Mapped: `authentication-solution-and-sensitive-accounts` → ATN-01; `implement-proper-password-strength-controls` → ATN-02, ATN-03, ATN-04, ATN-05, ATN-06; `compare-password-hashes-using-safe-functions` → ATN-07; `change-password-feature` → ATN-08; `transmit-passwords-only-over-tls-or-other-strong-transport` → ATN-09; `authentication-responses` → ATN-10, ATN-11; `protect-against-automated-attacks` → ATN-12; `login-throttling` → ATN-12; `security-questions-and-memorable-words` → ATN-13; `logging-and-monitoring` → ATN-14; `openid-connect-oidc` → ATN-15; `oidc-implementation-guidance` → ATN-15; `secure-federated-account-linking` → ATN-16, ATN-17; `adaptive-or-risk-based-authentication` → ATN-18
- Not localized [B]: `introduction`, `for-more-detailed-information-check`, `implement-secure-password-recovery-mechanism`, `store-passwords-in-a-secure-fashion`, `tls-client-authentication`, `oauth-20-and-21`, `saml`, `fido`, `hardware-backed-key-storage`, `references`
- Not localized [F]: `require-re-authentication-for-sensitive-features`, `re-authentication-after-risk-events`, `when-to-trigger-re-authentication`, `re-authentication-mechanisms`, `implementation-recommendations`, `multi-factor-authentication`, `password-managers`, `changing-a-users-registered-email-address`, `recommended-process-if-the-user-has-multifactor-authentication-enabled`, `recommended-process-if-the-user-does-not-have-multifactor-authentication-enabled`, `notes-on-the-above-processes`
- Not localized [Oinj]: `user-ids`, `usernames`
- Not localized [P]: `authentication-general-guidelines`, `authentication-and-error-messages`, `use-of-authentication-protocols-that-require-no-password`
- Not localized [X]: `consider-strong-transaction-authentication`, `captcha`

### Authorization CS (`atz`)

- Mapped: `enforce-least-privileges` → ATZ-01; `deny-by-default` → ATZ-02; `validate-the-permissions-on-every-request` → ATZ-03; `ensure-lookup-ids-are-not-accessible-even-when-guessed-or-cannot-be-tampered-with` → ATZ-04; `enforce-authorization-checks-on-static-resources` → ATZ-05; `verify-that-authorization-checks-are-performed-in-the-right-location` → ATZ-06; `exit-safely-when-authorization-checks-fail` → ATZ-07; `implement-appropriate-logging` → ATZ-08
- Not localized [B]: `introduction`, `references`
- Not localized [F]: `prefer-attribute-and-relationship-based-access-control-over-rbac`
- Not localized [Odep]: `thoroughly-review-the-authorization-logic-of-chosen-tools-and-technologies-implementing-custom-logic-if-necessary`
- Not localized [Otest]: `create-unit-and-integration-test-cases-for-authorization-logic`
- Not localized [P]: `recommendations`

### JSON Web Token CS (`jwt`)

- Mapped: `not-using-jwts` → JWT-10; `public-key-signatures` → JWT-09; `mac` → JWT-08; `claims` → JWT-06; `unsecured-jwts` → JWT-01; `key-type-confusion` → JWT-02; `trusting-key-material-named-in-the-token-header` → JWT-03; `issuer-and-audience-confusion` → JWT-04, JWT-05; `cross-jwt-and-token-type-confusion` → JWT-07; `jwt-denylist` → JWT-10; `signed-jwts-are-not-confidential` → JWT-11; `using-jwe` → JWT-11
- Not localized [B]: `introduction`, `token-structure`, `example`, `header-fields`, `references`
- Not localized [P]: `considerations-about-using-jwts`, `public-key-signatures-vs-mac`, `threats-on-jwts`, `jwt-revocation`, `token-confidentiality-and-jwe`
- Not localized [X]: `token-status-list`, `replay-protection`

### OAuth 2.0 CS (`oau`)

- Mapped: `oauth-20-essential-basics` → OAU-01, OAU-02, OAU-03; `pkce-proof-key-for-code-exchange-mechanism` → OAU-04; `implicit-grant-deprecated-do-not-use` → OAU-04, OAU-05; `token-replay-prevention` → OAU-09; `access-token-privilege-restriction` → OAU-07, OAU-08; `resource-owner-password-credentials-grant` → OAU-06; `client-authentication` → OAU-10; `other-recommendations` → OAU-11
- Not localized [B]: `terminology`, `references`
- Not localized [F]: `pop-mechanisms-comparison`, `when-to-use-pop-tokens`

### Session Management CS (`ses`)

- Mapped: `session-id-entropy` → SES-02; `session-id-content-or-value` → SES-02; `built-in-session-management-implementations` → SES-01; `used-vs-accepted-session-id-exchange-mechanisms` → SES-03; `secure-attribute` → SES-04; `httponly-attribute` → SES-05; `samesite-attribute` → SES-06, SES-07; `cookie-name-prefixes` → SES-08; `domain-and-path-attributes` → SES-09; `expire-and-max-age-attributes` → SES-10; `the-localstorage-api` → SES-17; `session-id-generation-and-verification-permissive-and-strict-session-management` → SES-12; `renew-the-session-id-after-any-privilege-level-change` → SES-11; `session-expiration` → SES-13; `idle-timeout` → SES-13; `absolute-timeout` → SES-14; `logout-button` → SES-15; `web-content-caching-and-clear-site-data` → SES-16; `limits-of-logout-on-browser-close` → SES-15
- Not localized [B]: `introduction`, `references`, `additional-resources`, `references_1`
- Not localized [F]: `server-side-session-token-storage`, `reauthentication-after-risk-events`, `considerations-when-using-multiple-cookies`, `reauthentication-after-risk-events_1`
- Not localized [Oinj]: `manage-session-id-as-any-other-user-input`
- Not localized [Oops]: `logging-sessions-life-cycle-monitoring-creation-usage-and-destruction-of-session-ids`
- Not localized [Oweb]: `transport-layer-security`
- Not localized [P]: `session-id-properties`, `session-management-implementation`, `cookies`, `session-id-life-cycle`, `automatic-session-expiration`, `manual-session-expiration`, `additional-client-side-defenses-for-session-management`, `session-attacks-detection`
- Not localized [S]: `session-id-length`
- Not localized [S17]: `html5-web-storage-api`, `scope`, `duration`, `offline-access`, `use-case`, `the-sessionstorage-api`, `scope_1`, `duration_1`, `offline-access_1`, `use-case_1`, `web-workers`, `use-case_2`
- Not localized [X]: `session-id-name-fingerprinting`, `renewal-timeout`, `initial-login-timeout`, `disable-web-browser-cross-tab-sessions`, `automatic-client-logout`, `session-id-guessing-and-brute-force-detection`, `detecting-session-id-anomalies`, `binding-the-session-id-to-other-user-properties`, `simultaneous-session-logons`, `session-management-waf-protections`

### Password Storage CS (`pws`)

- Mapped: `introduction` → PWS-01, PWS-10; `hashing-vs-encryption` → PWS-01; `salting` → PWS-06; `peppering` → PWS-07; `common-requirements-for-peppering-strategies` → PWS-07 (section context); `pre-hashing-peppers` → PWS-07 (section context); `post-hashing-peppers` → PWS-07 (section context); `upgrading-the-work-factor` → PWS-08; `argon2id` → PWS-02; `scrypt` → PWS-03; `bcrypt` → PWS-04; `input-limits-of-bcrypt` → PWS-04; `pre-hashing-passwords-with-bcrypt` → PWS-04; `pbkdf2` → PWS-05; `upgrading-legacy-hashes` → PWS-08; `international-characters` → PWS-09
- Not localized [B]: `background`, `when-password-hashes-can-be-cracked`, `references`
- Not localized [P]: `methods-for-enhancing-password-storage`, `using-work-factors`, `password-hashing-algorithms`
- Not localized [X]: `parallel-pbkdf2`, `pbkdf2-pre-hashing`

### Zero Trust Architecture CS (`zta`)

- Mapped: `2-all-communication-is-secured-regardless-of-network-location` → ZTA-01; `3-access-to-resources-is-granted-on-a-per-session-basis` → ZTA-02; `6-all-authentication-and-authorization-is-dynamic-and-strictly-enforced` → ZTA-02; `managing-user-accounts` → ZTA-03; `access-controls` → ZTA-03; `network-controls` → ZTA-05; `securing-applications` → ZTA-04; `technical-mistakes` → ZTA-05
- Not localized [F]: `multi-factor-authentication-mfa`
- Not localized [N]: `introduction`, `1-all-data-sources-and-computing-services-are-resources`, `4-access-is-determined-by-dynamic-policy`, `5-monitor-and-measure-the-security-posture-of-all-assets`, `7-collect-information-to-improve-security-posture`, `core-zero-trust-architecture-components`, `how-zero-trust-addresses-modern-security-challenges`, `traditional-vs-zero-trust-responses`, `modern-threats-that-require-zero-trust`, `zta-decision-making-in-action`, `case-study-1-working-late-from-home`, `case-study-2-new-contractor-laptop`, `case-study-3-cross-team-project-access`, `what-these-cases-show`, `device-security`, `trusting-devices`, `protecting-endpoints`, `network-architecture`, `micro-segmentation`, `application-and-data-protection`, `protecting-data`, `monitoring-and-analytics`, `security-operations`, `key-metrics-to-track`, `implementation-steps`, `phase-1-get-the-basics-right`, `phase-2-add-zero-trust-controls`, `phase-3-advanced-capabilities`, `phase-4-keep-getting-better-ongoing`, `legacy-system-challenges`, `common-problems`, `solutions-that-work`, `cloud-security`, `multi-cloud-considerations`, `container-security`, `common-mistakes-to-avoid`, `organizational-mistakes`, `compliance-benefits`, `framework-mapping`, `technology-components`, `policy-as-code-continuous-verification-telemetry-signals`, `1-policy-as-code-pac`, `2-continuous-verification`, `3-telemetry-signals`, `4-zero-trust-security-loop`, `references`
- Not localized [P]: `core-zero-trust-principles`, `identity-and-access-management`

### .NET Security CS (identity sections) (`dnet`)

- Mapped: `authentication-and-authorization` → ASP-01; `account-protection` → ASP-02, ASP-03; `passwords` → ASP-04, ASP-05; `authentication-cookies` → ASP-06, ASP-07, ASP-08; `authorization` → ASP-09, ASP-10, ASP-11; `redirects` → ASP-12; `cross-site-request-forgery` → ASP-13; `aspnet-mvc-and-web-forms` → ASP-13; `forms-authentication` → ASP-14
- Not localized [B]: `introduction`, `references`
- Not localized [Oinj]: `input-handling`, `sql-injection`, `os-command-injection`, `cross-site-scripting-xss`, `serialization-and-xml`
- Not localized [Oops]: `data-protection`, `encryption-for-storage`, `encryption-for-transmission`, `configuration-and-deployment`
- Not localized [Oscope]: `windows-communication-foundation-wcf`
- Not localized [P]: `legacy-net-framework`

### Top 10 A01:2025 (`a01`)

- Mapped: `description` → T10-03, T10-04, T10-05; `how-to-prevent` → T10-01, T10-02, T10-03, T10-06, T10-07
- Not localized [C]: `background`, `score-table`, `example-attack-scenarios`, `references`, `list-of-mapped-cwes`

### Top 10 A07:2025 (`a07`)

- Mapped: `description` → T10-14, T10-15, T10-16; `how-to-prevent` → T10-08, T10-09, T10-10, T10-11, T10-12, T10-13, T10-14
- Not localized [C]: `background`, `score-table`, `example-attack-scenarios`, `references`, `list-of-mapped-cwes`

### Spring: authorize-http-requests (`ahr`)

- Mapped: `match-by-httpmethod` → SPS-01; `authorize-requests` → SPS-01; `favor-permitall` → SPS-02
- Not localized [M]: `request-authorization-architecture`, `_authorizationfilter_is_last_by_default`, `_all_dispatches_are_authorized`, `_authentication_lookup_is_deferred`, `authorizing-endpoints`, `match-requests`, `match-by-ant`, `match-by-regex`, `match-by-dispatcher-type`, `match-by-mvc`, `match-by-custom`, `customizing-authorization-managers`, `authorization-expressions`, `using-authorization-expression-fields-and-methods`, `using_path_parameters`, `remote-authorization-manager`, `migrate-authorize-requests`, `_migrating_expressions`, `security-matchers`, `_further_reading`

### Spring: method-security (`ms`)

- Mapped: `method-security-architecture` → SPS-03; `favor-granting-authorities` → SPS-05; `request-vs-method` → SPS-04; `authorizing-with-annotations` → SPS-03 (section context); `use-preauthorize` → SPS-04 (section context); `use-postauthorize` → SPS-04; `use-secured` → SPS-03; `use-jsr250` → SPS-03; `enable-annotation` → SPS-03 (section context); `using_method_parameters` → SPS-04 (section context); `authorize-object` → SPS-04
- Not localized [M]: `unanimous-based-authorization-decisions`, `repeated-annotations`, `annotation-method-pointcuts`, `annotation-method-interceptors`, `use-prefilter`, `use-postfilter`, `class-or-interface-annotations`, `meta-annotations`, `use-intercept-methods`, `use-programmatic-authorization`, `_using_a_custom_bean_in_spel`, `custom-authorization-managers`, `customizing-expression-handling`, `pre-post-authorize-aot`, `use-aspectj`, `match-by-pointcut`, `weave-aspectj`, `changing-the-order`, `authorization-expressions`, `using-authorization-expression-fields-and-methods`, `customizing-authorization-managers`, `_using_authorizereturnobject_at_the_class_level`, `_programmatically_proxying`, `_manual_construction`, `_proxying_collections`, `_proxying_classes`, `_support_for_all_method_security_annotations`, `custom_advice`, `_working_with_jackson`, `authorize-return-object-aot`, `fallback-values-authorization-denied`, `_using_the_denied_result_from_the_method_invocation`, `deciding-return-based-parameters`, `_combining_with_meta_annotation_support`, `_use_a_custom_bean_instead_of_subclassing_defaultmethodsecurityexpressionhandler`, `_further_reading`
- Not localized [O mig]: `migration-enableglobalmethodsecurity`, `servlet-replace-globalmethodsecurity-with-methodsecurity`

### Spring: session-management (`sm`)

- Mapped: `ns-session-fixation` → SPS-06; `_configuring_session_fixation_protection` → SPS-06
- Not localized [M]: `understanding-session-management-components`, `the-sessionmanagementfilter`, `customizing-where-authentication-is-stored`, `store-authentication-manually`, `properly-clearing-authentication`, `stateless-authentication`, `requireexplicitsave`, `how-it-works-requireexplicitsave`, `ns-concurrent-sessions`, `_detecting_timeouts`, `_customizing_the_invalid_session_strategy`, `clearing-session-cookie-on-logout`, `use-securitycontextholderstrategy`, `session-mgmt-force-session-creation`, `_what_to_read_next`

### Spring: logout (`lo`)

- Mapped: `logout-java-configuration` → SPS-07; `clear-all-site-data` → SPS-07; `creating-custom-logout-endpoint` → SPS-07 (section context)
- Not localized [M]: `customizing-logout-uris`, `add-logout-handler`, `customizing-logout-success`, `testing-logout`, `jc-logout-references`

### Spring: csrf (`csrf`)

- Mapped: `csrf-integration-mobile` → SPS-08; `disable-csrf` → SPS-08; `csrf-considerations-login` → SPS-08 (section context); `csrf-considerations-logout` → SPS-08 (section context)
- Not localized [M]: `csrf-components`, `migrating-to-spring-security-6`, `csrf-token-repository`, `csrf-token-repository-httpsession`, `csrf-token-repository-cookie`, `csrf-token-repository-custom`, `csrf-token-request-handler`, `csrf-token-request-handler-breach`, `csrf-token-request-handler-plain`, `csrf-token-request-handler-custom`, `deferred-csrf-token`, `csrf-integration`, `csrf-integration-form`, `csrf-integration-javascript`, `csrf-access-denied-handler`, `csrf-testing`, `csrf-considerations`, `considerations-csrf-timeouts`, `csrf-considerations-multipart`, `csrf-considerations-override-method`, `csrf-further-reading`

### Spring: password-storage (`pw`)

- Mapped: `authentication-password-storage-dpe` → SPS-09; `authentication-password-storage-dep-getting-started` → SPS-09; `authentication-password-storage-bcrypt` → SPS-09 (section context); `authentication-password-storage-argon2` → SPS-09 (section context); `authentication-password-storage-pbkdf2` → SPS-09 (section context); `authentication-password-storage-scrypt` → SPS-09 (section context); `authentication-compromised-password-check` → SPS-10
- Not localized [M]: `authentication-password-storage-history`, `authentication-password-storage-dpe-format`, `authentication-password-storage-dpe-encoding`, `authentication-password-storage-dpe-matching`, `authentication-password-storage-boot-cli`, `authentication-password-storage-dpe-troubleshoot`, `authentication-password-storage-other`, `password4j`, `password4j-argon2`, `password4j-bcrypt`, `password4j-scrypt`, `password4j-pbkdf2`, `password4j-ballooning`, `authentication-password-storage-configuration`, `authentication-change-password-configuration`

### Spring: resource-server/jwt (`rsj`)

- Mapped: `_runtime_expectations` → SPS-11; `_supplying_audiences` → SPS-11; `oauth2resourceserver-jwt-decoder-algorithm` → SPS-12; `oauth2resourceserver-jwt-boot-algorithm` → SPS-12 (section context); `oauth2resourceserver-jwt-decoder-secret-key` → SPS-12; `oauth2resourceserver-jwt-validation` → SPS-11; `oauth2resourceserver-jwt-validation-custom` → SPS-11 (section context)
- Not localized [M]: `oauth2resourceserver-jwt-minimaldependencies`, `oauth2resourceserver-jwt-minimalconfiguration`, `_specifying_the_authorization_server`, `_startup_expectations`, `oauth2resourceserver-jwt-architecture`, `oauth2resourceserver-jwt-jwkseturi`, `oauth2resourceserver-jwt-sansboot`, `oauth2resourceserver-jwt-jwkseturi-dsl`, `oauth2resourceserver-jwt-decoder-dsl`, `oauth2resourceserver-jwt-decoder-bean`, `oauth2resourceserver-jwt-decoder-builder`, `oauth2resourceserver-jwt-decoder-jwk-response`, `oauth2resourceserver-jwt-decoder-public-key`, `oauth2resourceserver-jwt-decoder-public-key-boot`, `oauth2resourceserver-jwt-decoder-public-key-builder`, `oauth2resourceserver-jwt-authorization`, `method-security-has-scope`, `oauth2resourceserver-jwt-authorization-extraction`, `oauth2resourceserver-jwt-validation-clockskew`, `oauth2resourceserver-jwt-validation-rfc9068`, `oauth2resourceserver-jwt-claimsetmapping`, `oauth2resourceserver-jwt-claimsetmapping-singleclaim`, `oauth2resourceserver-jwt-claimsetmapping-add`, `oauth2resourceserver-jwt-claimsetmapping-remove`, `oauth2resourceserver-jwt-claimsetmapping-rename`, `oauth2resourceserver-jwt-timeouts`, `custom-principal`, `custom-user-details-service`

### Spring: client/authorization-grants (`ocg`)

- Mapped: `oauth2-client-authorization-code` → SPS-13; `oauth2-client-authorization-code-authorization` → SPS-13 (section context); `oauth2-client-authorization-code-authorization-request` → SPS-13 (section context)
- Not localized [M]: `oauth2-client-authorization-code-authorization-request-resolver`, `oauth2-client-authorization-code-authorization-request-repository`, `oauth2-client-authorization-code-access-token`, `oauth2-client-authorization-code-access-token-request`, `oauth2-client-authorization-code-access-token-response`, `oauth2-client-authorization-code-access-token-response-client-dsl`, `oauth2-client-refresh-token`, `oauth2-client-refresh-token-access-token`, `oauth2-client-refresh-token-access-token-request`, `oauth2-client-refresh-token-access-token-response`, `oauth2-client-refresh-token-authorized-client-provider-builder`, `oauth2-client-client-credentials`, `oauth2-client-client-credentials-access-token`, `oauth2-client-client-credentials-access-token-request`, `oauth2-client-client-credentials-access-token-response`, `oauth2-client-client-credentials-authorized-client-provider-builder`, `oauth2-client-client-credentials-authorized-client-manager`, `oauth2-client-jwt-bearer`, `oauth2-client-jwt-bearer-access-token`, `oauth2-client-jwt-bearer-access-token-request`, `oauth2-client-jwt-bearer-access-token-response`, `oauth2-client-jwt-bearer-authorized-client-provider-builder`, `oauth2-client-jwt-bearer-authorized-client-manager`, `oauth2-client-token-exchange`, `oauth2-client-token-exchange-access-token`, `oauth2-client-token-exchange-access-token-request`, `oauth2-client-token-exchange-access-token-response`, `oauth2-client-token-exchange-authorized-client-provider-builder`, `oauth2-client-token-exchange-authorized-client-manager`

### Spring: login/core (`olc`)

- Mapped: `oauth2login-sample-redirect-uri` → SPS-13
- Not localized [M]: `oauth2login-sample-boot`, `oauth2login-sample-initial-setup`, `oauth2login-sample-application-config`, `oauth2login-sample-boot-application`, `oauth2login-boot-property-mappings`, `oauth2login-common-oauth2-provider`, `oauth2login-custom-provider-properties`, `oauth2login-override-boot-autoconfig`, `oauth2login-register-clientregistrationrepository-bean`, `oauth2login-provide-securityfilterchain-bean`, `oauth2login-completely-override-autoconfiguration`, `oauth2login-javaconfig-wo-boot`

### Django: topics/auth/default (`auth`)

- Mapped: `changing-passwords` → DJ-09 (section context); `permissions-and-authorization` → DJ-02; `default-permissions` → DJ-02 (section context); `how-to-log-a-user-in` → DJ-09; `how-to-log-a-user-out` → DJ-09; `limiting-access-to-logged-in-users` → DJ-01
- Not localized [M]: `user-objects`, `creating-users`, `creating-superusers`, `authenticating-users`, `groups`, `programmatically-creating-permissions`, `permission-caching`, `proxy-models`, `authentication-in-web-requests`, `redirecting-unauthorized-requests-in-class-based-views`, `module-django.contrib.auth.views`, `helper-functions`, `module-django.contrib.auth.forms`, `authentication-data-in-templates`, `managing-users-in-the-admin`, `id6`, `id7`

### Django: topics/auth/passwords (`pwd`)

- Mapped: `how-django-stores-passwords` → DJ-03; `included-hashers` → DJ-03; `enabling-password-validation` → DJ-04; `included-validators` → DJ-04 (section context); `integrating-validation` → DJ-04 (section context)
- Not localized [D]: `using-argon2-with-django`, `increasing-the-work-factor`, `password-upgrading`
- Not localized [M]: `using-bcrypt-with-django`, `using-scrypt-with-django`, `increasing-the-salt-entropy`, `password-upgrading-without-requiring-a-login`, `writing-your-own-hasher`, `module-django.contrib.auth.hashers`, `module-django.contrib.auth.password_validation`, `writing-your-own-validator`

### Django: topics/http/sessions (`sess`)

- Mapped: `using-cookie-based-sessions` → DJ-10; `session-object-guidelines` → DJ-10 (section context); `browser-length-sessions-vs-persistent-sessions` → DJ-08; `session-security` → DJ-11
- Not localized [D]: `session-ids-in-urls`
- Not localized [M]: `enabling-sessions`, `configuring-the-session-engine`, `using-database-backed-sessions`, `using-cached-sessions`, `using-file-based-sessions`, `using-sessions-in-views`, `session-serialization`, `examples`, `setting-test-cookies`, `using-sessions-out-of-views`, `when-sessions-are-saved`, `clearing-the-session-store`, `settings`, `technical-details`, `the-sessionstore-object`, `extending-database-backed-session-engines`, `example`

### Django: ref/csrf (`csrf`)

- Mapped: `how-it-works` → DJ-06; `module-django.views.decorators.csrf` → DJ-06 (section context)
- Not localized [M]: `settings`, `frequently-asked-questions`, `is-posting-an-arbitrary-csrf-token-pair-cookie-and-post-data-a-vulnerability`, `is-it-a-problem-that-django-s-csrf-protection-isn-t-linked-to-a-session-by-default`, `why-might-a-user-encounter-a-csrf-validation-failure-after-logging-in`
- Not localized [Oweb]: `limitations`

### Django: ref/middleware (`mw`)

- Mapped: `module-django.contrib.auth.middleware` → DJ-01 (section context); `csrf-protection-middleware` → DJ-06 (section context)
- Not localized [M]: `available-middleware`, `module-django.middleware.cache`, `module-django.middleware.common`, `module-django.middleware.gzip`, `module-django.middleware.http`, `module-django.middleware.locale`, `module-django.contrib.messages.middleware`, `module-django.contrib.sessions.middleware`, `module-django.contrib.sites.middleware`, `middleware-ordering`
- Not localized [Oweb]: `module-django.middleware.security`, `x-frame-options-middleware`, `content-security-policy-middleware`

### Django: howto/deployment/checklist (`dep`)

- Mapped: `https` → DJ-05, DJ-06 (section context); `csrf-cookie-secure` → DJ-06; `session-cookie-secure` → DJ-05; `sessions` → DJ-08 (section context)
- Not localized [M]: `run-manage-py-check-deploy`, `switch-away-from-manage-py-runserver`, `environment-specific-settings`, `allowed-hosts`, `caches`, `databases`, `mailers-and-related-settings`, `static-root-and-static-url`, `media-root-and-media-url`, `performance-optimizations`, `conn-max-age`, `templates`, `admins-and-managers`, `customize-the-default-error-views`
- Not localized [Oops]: `secret-key`, `debug`, `error-reporting`, `logging`
- Not localized [P]: `critical-settings`
