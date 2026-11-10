# Maintenance — Security: Web & API localized standards

**Maintainers only. Workers never load this file.** Background and design decisions:
`docs/plan_localize-review-security-web-api.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website and per host (plan DEC-6). `review-security-identity-access` (94),
`review-security-input-injection` (66) and `review-security-operational` (52) also use cheatsheetseries.owasp.org;
those budgets are separate. docs.spring.io hosts both Spring Security and Spring Framework; they share one budget.

| Website | Local file(s) | Elements | Cap | Note |
|---|---|---|---|---|
| cheatsheetseries.owasp.org | owasp-web-api.md + node-web-api.md (2) | **56** | 100 | CSP 11, HDR 19, RST 12, H5 5, HST 2, TLS 5 + Node.js sheet 2 (2026-11-09). Headroom 44 |
| top10.owasp.org | owasp-web-api.md | 5 | 100 | A02:2025 (traceability elements) |
| learn.microsoft.com | dotnet-web-api.md | 10 | 100 | ASP.NET Core 10.0: enforce HTTPS (4), CORS (3), formatting (3) |
| docs.spring.io | java-web-api.md | 11 | 100 | Spring Security 7.1 (9), Spring Framework 7.0 (2) |
| docs.djangoproject.com | python-web-api.md | 9 | 100 | Django 6.1, 5 pages (selected sections/settings) |
| developer.mozilla.org | mdn-web-api.md | 1 | 100 | CSP `require-trusted-types-for` (MDN-01, 2026-11-09) |
| expressjs.com | node-web-api.md | 3 | 100 | Production Best Practices: Security (2026-11-09) |
| **Total** | | **95** | | |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Prefixes (CSP, HDR,
  RST, H5, HST, TLS, A02, DNW, JVW, PYW) stay distinct from every other localized skill (plan DEC-9; checked against
  all `references/standards/*.md` on 2026-11-09).
- Check IDs: SEC-WA-07 was narrowed once, by user decision (plan DEC-4: from "error responses don't leak stack traces,
  internal paths or version info" to version-revealing response headers only; error bodies belong to
  `review-security-operational` SEC-OP-01). SEC-WA-08 … SEC-WA-11 were added (DEC-5). Check IDs are not reused.
- Every element ID is listed by exactly one check in `../checklist.md`, and the "Check" column of its row names that check.
- Level:
  - OWASP cheat sheets: `MUST` where the source says must/must not/never/do not/ensure, gives an unqualified
    imperative ("Remove…", "Use…", "Discard…"), or names a prohibited practice (e.g. the REST sheet's "NOT OK" URL
    example); `SHOULD` for should/recommended/prefer/consider.
  - Top 10: `REVIEW` for "Description" weaknesses and mapped CWEs (`REVIEW` is treated like `MUST`).
  - Vendor files: the level of the OWASP element the vendor element supports, or `SHOULD` when the vendor only recommends.
  - HDR-11 (COEP) is **Advisory**: cited in recommendations only, never fails on its own.
- **(Default)** elements state API behaviour or a default. Add one only with the version it was read from and the source
  sentence quoted in the localization log. Workers may rely on no other default (`SKILL.md` "Standards" section).
- Vendor elements state behaviour and defaults; they never relax an OWASP element (plan DEC-8).
- HSTS threshold (plan DEC-13): `max-age` below `31536000` fails HST-01 (SHOULD); recommendations name `63072000`.
- Primary anchor first; list every absorbed anchor so coverage stays auditable. Rows ≈ 220 characters at most.
  - Headers sheet "Recommendation" headings: `recommendation`, `recommendation_1` … `recommendation_21`, in page order.
  - Django pages expose both `s-<slug>` and `<slug>` ids; use `<slug>`. Settings use `std-setting-<NAME>`.
  - Microsoft Learn pages carry several version blocks: the 10.0 block has no suffix on `ms-ssl`/`ms-cors` and the
    suffix `-2` on `ms-fmt`. Use only anchors of the block that includes `aspnetcore-10.0` (or common content).
  - Spring Security `/7.1/` paths redirect to the unversioned current pages; the version is recorded in the file header.
- Vendor files are split **by language** (matching `compliance-review-core/references/languages.md` ids). A new vendor
  file gets a line in `SKILL.md`, a row in `../sources.md` and a row in the budget table.

## Refresh procedure

1. **Cadence:**
   - OWASP file: quarterly, or when run notes contain ≥ 3 `localized-standard-gap` or any `localized-standard-stale`
     entry for this skill. The TLS sheet changed on 2026-11-08, the REST sheet on 2026-10-14.
   - Top 10: when a new edition is published (check whether A02 is renumbered).
   - Microsoft Learn: on each ASP.NET Core major release (November; re-pin `view=`), and when `ms.date` changes.
   - Spring Security and Spring Framework: within two weeks of each minor release (api.spring.io). Default-header
     changes affect JVW-01 … JVW-07; CORS default changes affect JVW-10.
   - Django: within two weeks of each feature release. Default changes to `SECURE_*` settings affect PYW-01 … PYW-08.
2. **Detect drift:**
   - OWASP cheat sheets: compare the latest commit SHA of each pinned file
     (`https://api.github.com/repos/OWASP/CheatSheetSeries/commits?path=cheatsheets/<Name>_Cheat_Sheet.md&per_page=1`)
     with the pinned SHA. If they differ, diff the text and the anchor list.
   - Top 10: `https://api.github.com/repos/OWASP/Top10/commits?path=2025/docs/en/A02_2025-Security_Misconfiguration.md&per_page=1`.
   - Microsoft Learn: the `ms.date` meta tag of each page and the current ASP.NET Core version.
   - Spring: `https://api.spring.io/projects/spring-security/releases` and
     `https://api.spring.io/projects/spring-framework/releases` (the release with `current: true`).
   - Django: the redirect target of `https://docs.djangoproject.com/en/stable/`.
   - On any vendor change, re-read the pinned sections and every element marked **(Default)**: DNW-02 … DNW-04,
     DNW-08, DNW-09, JVW-01 … JVW-07, JVW-10, PYW-01 … PYW-03, PYW-05 … PYW-09.
3. **Update:** keep IDs stable (new IDs only, `(retired)` for removed rules). Keep every website ≤ 100 for this skill,
   and decide follow-up candidates against the remaining headroom. Update the coverage map below, the "Localized" dates
   and versions in the file headers, `../sources.md`, and the URL list in
   `compliance-review-core/references/approved-sources.md` when a version path changes (e.g. `aspnetcore-10.0` →
   `aspnetcore-11.0`, `/en/6.1/` → `/en/6.2/`).
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo); run any Python over them with `-I`.
   - Script-check: 89 element IDs, each in exactly one check, matching its row's "Check" column; every signal row in
     `../languages/*.md` names at least one existing element ID; every listed anchor exists as an `id` on its published
     page (Learn anchors inside the 10.0 version block); every H2/H3/H4 anchor of the CSP, HTTP Headers, REST Security
     and HSTS sheets, the pinned sections of the HTML5 and TLS sheets, every A02 Description / How-to-prevent bullet
     and every anchor of the pinned vendor sections appears in the coverage map below — zero unaccounted.
   - Run reviews against small sample repos (plan §9 step 10): `validate` passes,
     `16-review-security-web-api.json` has `urlsFetched: []` and 11 check results, expected findings cite the element
     IDs, SHOULD elements are one level lower, HTML-only checks are N/A for API-only targets, no CORS configuration
     passes.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-security-web-api` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Refresh due

- **ASP.NET Core 11** (November 2026): re-pin `view=aspnetcore-11.0` and re-read DNW-02 … DNW-04, DNW-08, DNW-09.
- **Spring Security 7.2 / Spring Framework 7.1**: re-read JVW-01 … JVW-07 and JVW-10 within two weeks of GA.
- **Django 6.2** (next feature release): re-pin `/en/6.2/` and re-read PYW-01 … PYW-03, PYW-05 … PYW-09.
- **First full verification** (see the localization log): outstanding.

## Localization log

### 2026-11-09 — initial localization

- Written from the **planning snapshot** of 2026-11-09 (plan DEC-10). The implementation re-snapshot (plan §9 step 1)
  was **not** taken: on 2026-11-09 the user declined further fetches for this implementation. Pins, defaults and
  anchors are therefore exactly those recorded in the plan, and the following verifications are outstanding (see
  "Open items"): pinned SHAs against the GitHub commits API; text at each pinned SHA; `ms.date` values and the Learn
  10.0 version-block suffixes (`ms-fmt` `-2` in particular); Spring Security 7.1.2 / Spring Framework 7.0.10 /
  Django 6.1 versions; the (Default) source sentences; the anchor list behind the coverage map.
- Plan decisions: DEC-2 … DEC-5 were confirmed by the user on 2026-11-09 during planning; DEC-1 and DEC-6 … DEC-16
  were confirmed by the user on 2026-11-09 at implementation (plan §9 step 2), unchanged.
- Pins (from the plan, OWASP/CheatSheetSeries `cheatsheets/<Name>_Cheat_Sheet.md`; OWASP/Top10 `2025/docs/en/<page>.md`):

  | Page | Commit | Date |
  |---|---|---|
  | Content Security Policy | eaa71fb4a421dc057bf03a3856d0d34967299ff1 | 2026-10-04 |
  | HTTP Security Response Headers (`HTTP_Headers`) | 056cc10a34c9160439cb9775615770bc886847f0 | 2026-10-04 |
  | REST Security | 97cb8a3c4b62104227ba52833ff7842ff1d0c850 | 2026-10-14 |
  | HTML5 Security (CORS and offline sections only) | 3919b1c4201613389ebd3172de7122920adac40d | 2026-10-04 |
  | HTTP Strict Transport Security | fa588addf1b7541d584eb9800a85c83832fb73a8 | 2026-10-04 |
  | Transport Layer Security (protocols, ciphers, application sections) | d6474de095dedba6caf536fdf8926d6ae53f3cfc | 2026-11-08 |
  | Top 10 A02:2025 Security Misconfiguration | d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966 | 2025-12-24 |

- Versions: ASP.NET Core 10.0 (`view=aspnetcore-10.0`); `ms.date` — enforce HTTPS 2026-10-27, CORS 2026-05-12,
  formatting 2026-03-22. Spring Security 7.1.2 (current GA on api.spring.io on 2026-11-09); Spring Framework 7.0.10
  (unversioned CORS page; Spring Boot 4.1 builds on Framework 7.0). Django 6.1.
- DEC-10 disclosures (planning):
  - (a) The three then-allowlisted sheets (CSP, HTTP Headers, REST Security) were fetched without asking because they
    were allowlisted. Every other page was fetched with the user's approval on 2026-11-09.
  - (b) Fetched but not used, so not pinned: the Kestrel options page (`fundamentals/servers/kestrel/options`; it
    doesn't document the `Server` header), and the Django deployment checklist (its HTTPS section covers cookie
    flags, owned by identity-access).
  - (c) The TLS sheet's latest commit (`d6474de0`) is from 2026-11-08, the day before the snapshot.
  - (d) Spring Framework's unversioned CORS page was current 7.0 (7.0.10) on the planning day.
- **Spring HSTS default discrepancy (JVW-03), unresolved:** the Spring Security reference shows two HSTS default
  values — `max-age=31536000 ; includeSubDomains` in the defaults list (`ss-hdr#headers-default`) and the same with
  `preload` in the HSTS section's example (`ss-hdr#headers-hsts`). JVW-03 lists the defaults-list value. Neither form
  changes a verdict (both pass HST-01 and HST-02); confirm which one 7.1.2 sends at the first verification.
- (Default) source sentences: to be quoted from the source at the first verification (outstanding). The (Default)
  rows were copied from the plan's §6 planning-snapshot reading.

### 2026-11-09 — JavaScript/TypeScript (afterplanning WP-12f phase 2)

- `node-web-api.md` (NDW-01 … NDW-05) and `../languages/javascript.md` from the OWASP Node.js Security Cheat Sheet (commit
  eeaa1e474bc2ef98119a3de7bafd067f52faf35e, 2026-11-05) and the Express security best-practices page (helmet defaults, `X-Powered-By`). Closes this skill's JavaScript follow-up (plan C-12 / §7.3 Express/helmet).
  Check count unchanged. Framework defaults beyond those stated in `node-web-api.md` (Fastify, NestJS, Next.js, Koa, Passport,
  logger masking) stay unlocalized; workers add `localized-standard-gap` notes.

## Open items

- **Plan §9 step 1 / step 8 verification** (needs fetch approval): re-take the snapshot into a scratch folder,
  confirm the pins and versions above, quote every (Default) sentence in this log, confirm every anchor in the
  standards files exists on its page, and script-check the coverage map against the published heading lists.
- **Plan §9 step 10:** review runs against sample repos were not run (user chose static checks only on 2026-11-09).
  Samples: (a) ASP.NET Core API with `AllowAnyOrigin().AllowCredentials()`, `[RequireHttps]` on controllers,
  `UseHsts()` with defaults, `[FromQuery] string apiKey`, an action returning a request-derived `string`,
  `X-Powered-By` added in middleware; (b) Spring Boot MVC app with HTML views, `frameOptions(f -> f.disable())`, bare
  `@CrossOrigin`, `allowCredentials(true)` with `allowedOriginPatterns("*")`, no CSP,
  `server.ssl.enabled-protocols=TLSv1.1,TLSv1.2`; (c) Django app without `SECURE_HSTS_SECONDS`,
  `SECURE_SSL_REDIRECT = False`, `SECURE_REFERRER_POLICY = None`, `CORS_ALLOW_ALL_ORIGINS = True` with credentials,
  `SECURE_CSP` with `CSP.UNSAFE_INLINE`, templates loading `http://` scripts; (d) a well-configured app (strict CSP
  with nonces, explicit CORS origins, HTTPS-only API, proxy headers with `always`) — expect strengths, no false positives.
- Plan §10 C-1, C-2, C-12 and C-13 were applied on 2026-11-09 before the skill changes; C-14 needs no change.
  `approved-sources.md` was updated by plan §9 step 9, which closes `review-security-operational` plan C-15. The
  remaining hand-offs were closed by `docs/plan_localize-afterplanning-changes.md` (2026-11-09): C-3 records and
  management-endpoint placement (`review-security-operational` ORS-01); C-5 Trusted Types (MDN-01 here); C-6 →
  api-design boundary step; C-7 rate limiting → `review-reliability` AZRL-32; C-8 → AZPE-11 note; C-9 →
  `review-software-quality` SQR-37; C-12 → `languages/javascript.md` and `node-web-api.md`. Open: none.

## Follow-up candidates (plan §7.3)

| Candidate | Est. elements | Status |
|---|---|---|
| Kestrel `AddServerHeader` (`Server: Kestrel` by default) | 1 | Open (new page; fetch approval) |
| Spring Boot `server.server-header`, `server.ssl.*` defaults | 2 | Open (scope) |
| Framework method-mapping defaults (Spring `@RequestMapping`, ASP.NET Core routes, Django `require_http_methods`) | ≈ 3 | Open (new pages; fetch approval) |
| Django host header validation (`ALLOWED_HOSTS`, `get_host()`, `USE_X_FORWARDED_HOST`) | 2 | Open (needs a check home; currently unowned) |
| Express/helmet defaults | 5 | Done 2026-11-09: NDW-01 … NDW-05 (afterplanning WP-12f) |
| Flask (`flask-talisman`), FastAPI (CORS middleware, `TrustedHostMiddleware`) | ≈ 3 each | Open (DEC-2 scope) |
| `django-cors-headers` settings defaults | ≈ 3 | Open (third-party site) |
| OWASP Clickjacking Defense Cheat Sheet | ≈ 4 | Open (scope) |
| OWASP Third-Party JavaScript Management (SRI) | ≈ 3 | Open (scope; may belong to dependency-management) |
| HTML5 Security: web messaging, tabnabbing, sandboxed frames, local storage | ≈ 8 | Open (ownership: web-api vs. input-injection) |
| WebSocket Security Cheat Sheet | ≈ 6 | Open (scope) |
| X-Robots-Tag on private content | 1 | Open (low value from code evidence) |
| mTLS for highly privileged services | 1 | Open (architecture decision) |
| CSP Trusted Types (`require-trusted-types-for`) | 1 | Done 2026-11-09: MDN-01 under SEC-WA-01 (afterplanning WP-12a) |
| OWASP ASVS v5.0 V3 and V12 | > 40 | Open (needs its own budget decision) |

## Localization log — 2026-11-09 additions (afterplanning WP-12a)

- MDN-01 (CSP `require-trusted-types-for 'script'`) added under SEC-WA-01 from the MDN page (last modified
  2025-12-22; Baseline 2026, newly available since February 2026). The pinned OWASP CSP sheet doesn't cover Trusted
  Types (plan C-5). Level `SHOULD` (defense in depth); never an XSS finding by itself. Applies only when a CSP is set
  and the app's own scripts write to DOM sinks. Check count unchanged.
- MDN anchors: `#syntax`, `#examples` (MDN uses underscore ids such as `#browser_compatibility`; not cited).

## `localized-standard-gap` / `localized-standard-stale` log

| Date | Run | Note | Action |
|---|---|---|---|
| — | — | (none yet) | — |

## Coverage map

Every heading anchor of the CSP, HTTP Headers, REST Security and HSTS sheets, the pinned sections of the HTML5 and TLS
sheets, every A02 bullet and every anchor of the pinned vendor sections is listed once: mapped to element IDs, or
given a reason code. **Status: built from the plan's 2026-11-09 planning snapshot (plan §5–§7); not yet
script-checked against the published heading lists** (see "Open items"). Vendor pages localized for selected sections
only list those sections' anchors; their other sections are out of scope [M].

### Reason codes

| Code | Reason for not localizing |
|---|---|
| B | background, definitions, references; no testable rule |
| P | parent heading; its rules are localized through the child anchors listed as mapped |
| M | mechanics, framework customization, or a section outside the pinned scope; not a security rule |
| X | example or sample code |
| T | testing tool |
| S | restates or points to a localized element (named in brackets) |
| F | follow-up candidate (plan §7.3) |
| U | owned by `review-software-quality` (AP-02, SQR-37; decision D-5, 2026-11-09) |
| Oop | owned by `review-security-operational` |
| Oia | owned by `review-security-identity-access` |
| Oinj | owned by `review-security-input-injection` |
| Oapi | owned by `review-api-design` |
| Orel | owned by `review-reliability` |
| Operf | owned by `review-performance` |
| Odep | owned by `review-dependency-management` |

### Content Security Policy CS (`csp`)

| Anchor | Mapped to / reason |
|---|---|
| `introduction`, `context`, `defense-against-xss`, `defense-in-depth`, `references` | B (defense-in-depth status is in the SEC-WA-01 evidence note) |
| `policy-delivery` | P |
| `1-content-security-policy-header` | CSP-01 |
| `2-content-security-policy-report-only-header` | CSP-01, CSP-09 |
| `3-content-security-policy-meta-tag` | CSP-01 |
| `warning` | CSP-02 |
| `csp-types-granularallowlist-based-or-strict`, `strict-csp`, `strict-policy`, `nonce-based-strict-policy`, `hash-based-strict-policy` | CSP-03 |
| `nonce-based`, `warning_1` | CSP-04 |
| `hashes`, `strict-dynamic`, `note` | M |
| `1-restricting-inline-scripts`, `3-restricting-unsafe-javascript`, `refactoring-inline-code` | CSP-05 |
| `special-directive-sources` | CSP-05, CSP-06 |
| `basic-non-strict-csp-policy` | CSP-06, CSP-07 |
| `detailed-csp-directives`, `2-restricting-remote-scripts`, `4-restricting-form-submissions` | CSP-07 |
| `document-directives`, `fetch-directives`, `5-restricting-objects` | CSP-08 |
| `reporting-directives` | CSP-09 |
| `upgrading-insecure-requests` | CSP-10 |
| `preventing-framing-attacks-clickjacking-cross-site-leaks`, `navigation-directives`, `defense-against-framing-attacks` | CSP-11 |

### HTTP Security Response Headers CS (`hdr`)

| Anchor | Mapped to / reason |
|---|---|
| `introduction`, `security-headers`, `references`, `references_1` | B |
| `x-frame-options`, `recommendation` | HDR-01 |
| `x-xss-protection`, `recommendation_1` | HDR-02 |
| `x-content-type-options`, `recommendation_2` | HDR-03 |
| `referrer-policy`, `recommendation_3` | HDR-04 |
| `content-type`, `recommendation_4` | HDR-05 |
| `cache-control`, `recommendation_5` | HDR-06 |
| `set-cookie`, `recommendation_6` | Oia |
| `strict-transport-security-hsts`, `recommendation_7` | HDR-07 (HST-01 also cites `recommendation_7`) |
| `expect-ct`, `recommendation_8` | HDR-08 |
| `content-security-policy-csp`, `recommendation_9` | S [CSP-01 … CSP-11]; API note is the basis of the applicability rule |
| `access-control-allow-origin`, `recommendation_10` | HDR-09 |
| `cross-origin-opener-policy-coop`, `recommendation_11` | HDR-10 |
| `cross-origin-embedder-policy-coep`, `recommendation_12` | HDR-11 (advisory) |
| `cross-origin-resource-policy-corp`, `recommendation_13` | HDR-12 |
| `permissions-policy-formerly-feature-policy`, `recommendation_14` | HDR-13 |
| `server`, `recommendation_15` | HDR-14 |
| `x-powered-by`, `recommendation_16` | HDR-15 |
| `x-aspnet-version`, `recommendation_17` | HDR-16 |
| `x-aspnetmvc-version`, `recommendation_18` | HDR-17 |
| `x-robots-tag`, `recommendation_19` | F |
| `x-dns-prefetch-control`, `recommendation_20` | B (the source says not to rely on it) |
| `public-key-pins-hpkp`, `recommendation_21` | HDR-18 |
| `secure-file-download-headers` | HDR-19 |
| `adding-http-headers-in-different-technologies`, `php`, `iis`, `haproxy`, `express` | M |
| `apache`, `nginx` | M (the `always` notes are evidence-rule anchors in `owasp-web-api.md`) |
| `testing-proper-implementation-of-security-headers`, `mozilla-observatory`, `smartscanner` | T |

### REST Security CS (`rst`)

| Anchor | Mapped to / reason |
|---|---|
| `introduction` | B |
| `https` | RST-01 |
| `access-control`, `jwt` | Oia |
| `api-keys` | Oia (429 rate limiting Orel) |
| `restrict-http-methods` | RST-02 (third bullet, caller authorized for the method: Oia) |
| `input-validation` | Oinj |
| `validate-content-types` | RST-04 (parent of the two below) |
| `validate-request-content-types` | RST-03, RST-04 |
| `send-safe-response-content-types` | RST-05, RST-06 |
| `management-endpoints` | Oop (diagnostic exposure; network placement: `review-security-operational` ORS-01), Oia (authorization) |
| `error-handling` | Oop |
| `audit-logs` | Oop |
| `security-headers` | RST-06 … RST-09 |
| `cors` | RST-10 |
| `sensitive-information-in-http-requests` | RST-11, RST-12 |
| `http-return-code` | Oapi |
| `preventing-out-of-order-api-execution`, `problem`, `example`, `prevention-guidance`, `testing-checklist` | U |

### HTML5 Security CS (`h5`) — pinned sections and the rest of the page

| Anchor | Mapped to / reason |
|---|---|
| `cross-origin-resource-sharing` | H5-01, H5-02, H5-03, H5-04 |
| `offline-applications` | H5-05 |
| `introduction`, `references` | B |
| `communication-apis` | P (outside pinned scope) |
| `web-messaging`, `websockets`, `server-sent-events`, `storage-apis`, `local-storage`, `client-side-databases`, `geolocation`, `web-workers`, `tabnabbing`, `sandboxed-frames`, `credential-and-personally-identifiable-information-pii-input-hints`, `progressive-enhancements-and-graceful-degradation-risks`, `http-headers-to-enhance-security` | F (outside the user-approved CORS/offline scope, DEC-3) |

### HTTP Strict Transport Security CS (`hsts`)

| Anchor | Mapped to / reason |
|---|---|
| `introduction`, `threats`, `browser-support`, `references` | B |
| `examples` | HST-01, HST-02 |
| `problems` | HST-02 (privacy part B) |

### Transport Layer Security CS (`tls`) — pinned sections and the rest of the page

| Anchor | Mapped to / reason |
|---|---|
| `introduction`, `ssl-vs-tls`, `references` | B |
| `server-configuration` | P |
| `only-support-strong-protocols` | TLS-01 |
| `only-support-strong-ciphers` | TLS-02 |
| `set-the-appropriate-diffie-hellman-groups`, `disable-compression`, `test-the-server-configuration` | M (server/OS configuration rarely in application code; F if IaC/web-server files come into scope) |
| `patch-cryptographic-libraries` | Odep |
| `certificates` and all its subsections | M (certificate operations, not code) |
| `use-tls-for-all-pages` | TLS-03, TLS-04 |
| `do-not-mix-tls-and-non-tls-content` | TLS-05 |
| `use-secure-cookies` | Oia |
| `prevent-caching-of-sensitive-data` | HDR-06 |
| `use-http-strict-transport-security` | S [HDR-07] |
| `client-certificates-and-mutual-tls` | F |
| `public-key-pinning` | HDR-18 |

### Top 10 A02:2025 (`a02`)

| Anchor / bullet | Mapped to / reason |
|---|---|
| `background`, `score-table`, `example-attack-scenarios`, `references` | B |
| `description` — security headers/directives missing or insecure | A02-01 |
| `description` — framework security settings not secure; newer features disabled | A02-02 |
| `description` — unnecessary features enabled (ports, services, pages) | A02-03 |
| `description` — default accounts; error handling revealing information; missing hardening; out-of-date software | Oia (accounts), Oop (errors, configuration), Odep (patching), M (infrastructure hardening) |
| `how-to-prevent` — send security directives/headers | S [A02-01] |
| `how-to-prevent` — minimal platform without unnecessary features | S [A02-03] |
| `how-to-prevent` — hardening process, environment parity, patching, segmented architecture, automated verification, credentials outside code | Oop, Odep, M |
| `list-of-mapped-cwes` — CWE-942 | A02-04 |
| `list-of-mapped-cwes` — CWE-5 | A02-05 |
| `list-of-mapped-cwes` — other CWEs | Oia (cookie CWEs), Oinj (XXE), Oop (debug/configuration CWEs) |

### Microsoft Learn: enforce HTTPS, ASP.NET Core 10.0 (`ms-ssl`)

| Anchor | Mapped to / reason |
|---|---|
| `api-projects`, `http-redirect-to-https-err_invalid_redirect-on-cors-preflight-request` | DNW-01 |
| `require-https`, `https-redirection-middleware-usehttpsredirection`, `opt-out-of-httpshsts-on-project-creation` | DNW-02 (`require-https` also DNW-03) |
| `http-strict-transport-security-hsts-protocol` | DNW-03 |
| `hsts-and-api-projects` | DNW-04 |
| port configuration, edge deployments, deployment scenarios, options details, alternative approach, development-certificate and Linux trust sections, troubleshooting | M |

### Microsoft Learn: CORS, ASP.NET Core 10.0 (`ms-cors`)

| Anchor | Mapped to / reason |
|---|---|
| `set-the-allowed-origins` | DNW-05, DNW-06 |
| `enable-cors` | DNW-06 |
| `credentials-in-cross-origin-requests` | DNW-07 |
| same origin, middleware order, endpoint routing, headers, preflight, IIS, testing | M |

### Microsoft Learn: format response data, ASP.NET Core 10.0 (`ms-fmt`, 10.0 block suffix `-2`)

| Anchor | Mapped to / reason |
|---|---|
| `the-accept-header-2`, `browsers-and-content-negotiation-2` | DNW-08 |
| `special-case-formatters-2` | DNW-09 |
| `specify-a-format-2` | DNW-10 |
| XML/JSON formatter configuration, URL format mappings | M |
| `ProblemDetails` formatting | Oapi |
| polymorphic deserialization | Oinj |

### Spring Security 7.1 / Spring Framework 7.0 (`ss-hdr`, `ss-shdr`, `ss-http`, `ss-cors`, `sf-cors`)

| Anchor | Mapped to / reason |
|---|---|
| `ss-hdr#headers-default` | JVW-03 (defaults list) |
| `ss-hdr#headers-content-type-options`, `ss-shdr#servlet-headers-content-type-options`, `ss-shdr#servlet-headers-default` | JVW-01 |
| `ss-hdr#headers-frame-options`, `ss-shdr#servlet-headers-frame-options` | JVW-02 |
| `ss-hdr#headers-hsts`, `ss-shdr#servlet-headers-hsts` | JVW-03 |
| `ss-hdr#headers-cache-control`, `ss-shdr#servlet-headers-cache-control` | JVW-04 |
| `ss-hdr#headers-xss-protection`, `ss-shdr#servlet-headers-xss-protection` | JVW-05 |
| `ss-hdr#headers-csp`, `ss-shdr#servlet-headers-csp` | JVW-06 |
| `ss-shdr#servlet-headers-referrer`, `ss-shdr#servlet-headers-permissions`, `ss-shdr#servlet-headers-clear-site-data` | JVW-07 |
| custom headers, static headers, headers writer, HPKP configuration, Feature-Policy | M (HPKP → HDR-18; Feature-Policy superseded by Permissions-Policy, JVW-07) |
| `ss-http#servlet-http-redirect` | JVW-08 |
| `ss-http` proxy server configuration | M |
| `ss-cors#cors-configuration-source`, `ss-cors#cors-spring-mvc-integration`, `ss-cors#cors-preflight-request-handler` | JVW-09 |
| `sf-cors#mvc-cors-controller`, `sf-cors#mvc-cors-global` | JVW-10 (`mvc-cors-controller` also JVW-11) |
| `sf-cors#mvc-cors-credentialed-requests` | JVW-11 |
| `sf-cors` processing, CORS filter | M |

### Django 6.1 (`dj-mw`, `dj-set`, `dj-cj`, `dj-csp`, `dj-sec`)

| Anchor | Mapped to / reason |
|---|---|
| `dj-mw#module-django.middleware.security`, `dj-mw#x-content-type-options-nosniff`, `dj-set#std-setting-SECURE_CONTENT_TYPE_NOSNIFF` | PYW-01 |
| `dj-mw#http-strict-transport-security`, `dj-set#std-setting-SECURE_HSTS_SECONDS`, `dj-set#std-setting-SECURE_HSTS_INCLUDE_SUBDOMAINS` | PYW-02 |
| `dj-mw#ssl-redirect`, `dj-set#std-setting-SECURE_SSL_REDIRECT`, `dj-sec#ssl-https` | PYW-03 (`ssl-https` also PYW-04) |
| `dj-set#std-setting-SECURE_PROXY_SSL_HEADER` | PYW-04 |
| `dj-cj#setting-x-frame-options-for-all-responses`, `dj-cj#setting-x-frame-options-per-view`, `dj-set#std-setting-X_FRAME_OPTIONS` | PYW-05 |
| `dj-csp#settings`, `dj-mw#content-security-policy-middleware`, `dj-set#std-setting-SECURE_CSP`, `dj-sec#limitations-and-considerations` | PYW-06 |
| `dj-set#std-setting-SECURE_REFERRER_POLICY`, `dj-mw#referrer-policy` | PYW-07 |
| `dj-set#std-setting-SECURE_CROSS_ORIGIN_OPENER_POLICY`, `dj-mw#cross-origin-opener-policy` | PYW-08 |
| `dj-sec#cross-origin-resource-sharing-cors` | PYW-09 |
| `dj-csp` constants list, decorators, nonce generation and caching | M |
| `dj-mw` other middleware; `dj-set` all other settings | M / Oia (outside pinned scope) |
| `dj-sec` XSS, CSRF, SQL injection, session security, user-uploaded content, form submissions | Oinj / Oia |
| `dj-sec` host header validation | F |
