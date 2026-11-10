# Maintenance — Security: Input & Injection localized standards

**Maintainers only. Workers never load this file.** Design decisions are recorded inline where they apply (DEC-n: this skill's localization decisions; D-n and C-n: cross-skill decisions and follow-ups); the planning documents they came from aren't kept in this repo.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website and per host (plan DEC-6; www.oracle.com and docs.oracle.com are separate).
`review-security-identity-access` (94) and `review-dependency-management` (15) also use cheatsheetseries.owasp.org;
those budgets are separate.

| Website | Local file(s) | Elements | Cap | Note |
|---|---|---|---|---|
| cheatsheetseries.owasp.org | owasp-input-injection.md (66, incl. 8 SSRF) + dotnet-input.md (6) + java-input.md (2) + node-input.md (5) | **79** | 100 | Headroom 21 (Node.js sheet, 5 elements, added 2026-11-09) |
| top10.owasp.org | owasp-input-injection.md | 7 | 100 | A05:2025 |
| learn.microsoft.com | dotnet-input.md | 9 | 100 | 7 pages |
| www.oracle.com | java-input.md | 9 | 100 | Secure Coding Guidelines 11.0, sections 1, 3, 5, 8 |
| docs.oracle.com | java-input.md | 2 | 100 | JAXP Security Guide, Java SE 25 |
| docs.spring.io | java-input.md | 2 | 100 | Spring Data JPA 4.1, JPA Query Methods |
| docs.python.org | python-input.md | 4 | 100 | Python 3.15, 4 pages |
| docs.djangoproject.com | python-input.md | 6 | 100 | Django 6.1, 6 pages (selected sections/settings) |
| expressjs.com | node-input.md | 1 | 100 | Production Best Practices: Security (2026-11-09) |
| **Total** | | **119** | | |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Prefixes stay distinct
  from `review-security-identity-access` (A05 vs T10; NET/JVA/PY vs ASP/SPS/DJ) (plan DEC-9).
- Every element ID is listed by exactly one check in `../checklist.md`, and the "Check" column of its row names that check.
- Level:
  - OWASP cheat sheets: `MUST` where the source says must/must not/never/do not/"is essential", gives an unqualified
    imperative, or names a prohibited practice or anti-pattern; `SHOULD` for should/recommended/prefer/consider/"if available".
  - Top 10: `MUST` for "How to prevent" bullets, `REVIEW` for "Description" weaknesses (`REVIEW` is treated like `MUST`).
  - Vendor files: the level of the OWASP element the vendor element supports, or `SHOULD` when the vendor only recommends.
- **(Default)** elements state API behaviour or a default. Add one only with the version it was read from and the source
  sentence quoted in the localization log. Workers may rely on no other default (`SKILL.md` step 3).
- Vendor elements state behaviour and defaults; they never relax an OWASP element (plan DEC-8).
- Primary anchor first; list every absorbed anchor so coverage stays auditable. Rows ≈ 220 characters at most.
  Microsoft API-reference pages (`dtd`, `arg`) have no section ids: use the page key alone.
- Vendor files are split **by language** (matching `compliance-review-core/references/languages.md` ids). A new vendor
  file gets a line in `SKILL.md`, a row in `../sources.md` and a row in the budget table.

## Refresh procedure

1. **Cadence:**
   - OWASP file: quarterly, or when run notes contain ≥ 3 `localized-standard-gap` or any `localized-standard-stale`
     entry for this skill. These sheets change often: four were committed on 2026-11-08 and XSS Prevention on 2026-11-01.
   - Microsoft Learn: on each ASP.NET Core/.NET major release (November) — re-pin `view=` — and when `ms.date` changes
     on the unversioned pages (`efsql`, `bf`).
   - Oracle: on each Java LTS release (re-pin `/javase/<n>/`) and when the Secure Coding Guidelines' document version changes.
   - Spring Data JPA: within two weeks of each minor release.
   - Python: within two weeks of each feature release (October). Django: within two weeks of each feature release.
2. **Detect drift:**
   - OWASP cheat sheets: compare the latest commit SHA of each pinned file
     (`https://api.github.com/repos/OWASP/CheatSheetSeries/commits?path=cheatsheets/<Name>_Cheat_Sheet.md&per_page=1`)
     with the pinned SHA. If they differ, diff the text and the anchor list.
   - Top 10: `https://api.github.com/repos/OWASP/Top10/commits?path=2025/docs/en/A05_2025-Injection.md&per_page=1`; also
     check whether a newer edition renumbers A05.
   - Microsoft Learn: the `ms.date` meta tag of each page and the current ASP.NET Core / .NET version.
   - Oracle: the "Document version" line of the Secure Coding Guidelines; the current Java LTS for the JAXP guide.
   - Spring Data JPA: the `version` meta tag of the query-methods page (4.1.2 at localization). The
     `https://api.spring.io/projects/spring-data-jpa/releases` endpoint returned only links on 2026-11-08, so the page
     meta tag was used.
   - Python: the version in the title of `https://docs.python.org/3/`. Django: the redirect target of
     `https://docs.djangoproject.com/en/stable/`.
   - On any vendor change, re-read the pinned sections and the stated defaults (NET-07, NET-08, NET-11, NET-14, JVA-12,
     JVA-14, JVA-15, PY-01, PY-04, PY-05, PY-06, PY-08, PY-10).
3. **Update:** keep IDs stable (new IDs only, `(retired)` for removed rules). Keep every website ≤ 100 for this skill,
   and decide follow-up candidates against the remaining headroom. Update the coverage map below, the "Localized" dates
   and versions in the file headers, `../sources.md`, and the URL list in `compliance-review-core/references/approved-sources.md`
   when a version path changes (e.g. `/3.15/` → `/3.16/`, `aspnetcore-10.0` → `aspnetcore-11.0`, `/javase/25/` →
   `/javase/29/`, `/en/6.1/` → `/en/6.2/`).
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo); run any Python over them with `-I`.
   - Script-check: every element ID in exactly one check, matching its row's "Check" column; every signal row in
     `../languages/*.md` names at least one existing element ID; every listed anchor exists as an `id` on its published
     page; every H2/H3/H4 anchor of the 10 cheat sheets, every A05 Description / How-to-prevent bullet and every H2/H3
     anchor of the pinned vendor sections appears in the coverage map below — zero unaccounted.
   - Run reviews against small sample repos (plan §9 step 10): `validate` passes,
     `15-review-security-input-injection.json` has `urlsFetched: []` and 9 check results, expected findings cite the
     element IDs, SHOULD elements are at Warning, stdlib `xml.etree` alone produces no XXE finding.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-security-input-injection` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Refresh due

- **ASP.NET Core / .NET 11** (November 2026): re-pin `view=aspnetcore-11.0` / `view=net-11.0` and re-read NET-08, NET-11,
  NET-13, NET-14.
- **Django 6.2** (next feature release): re-pin `python-input.md` and re-read the listed settings defaults (PY-08, PY-10).
- **Python 3.16** (October 2027): re-pin `/3.16/` and re-read PY-01, PY-04.

## Localization log

### 2026-11-08 — initial localization

- Snapshot taken on 2026-11-08 (planning) and re-taken the same day at implementation (plan §9 step 1), into a scratch
  folder: 10 cheat sheets (published HTML and the Markdown at each pinned SHA), the A05 page (HTML and Markdown), 20
  vendor pages, the GitHub commits API, `api.spring.io`, `docs.python.org/3/` and `docs.djangoproject.com/en/stable/`.
  The user approved the non-allowlisted fetches for planning and again for implementation.
- Pins confirmed unchanged against the plan (GitHub commits API, latest commit per file):

  | Page | Commit | Date (UTC) |
  |---|---|---|
  | Input Validation | b9500094c1122068fed472de2c5594dcca19ef05 | 2026-10-03 |
  | Injection Prevention | 9a91ba5afc717829ef2dbc1b97feeaad65cc7510 | 2026-11-08 19:46 |
  | SQL Injection Prevention | 9a91ba5afc717829ef2dbc1b97feeaad65cc7510 | 2026-11-08 19:46 |
  | Query Parameterization | 9a91ba5afc717829ef2dbc1b97feeaad65cc7510 | 2026-11-08 19:46 |
  | XML Security | 6f207d0496698a29ca006083587473a97a2aa6d8 | 2026-11-08 21:10 |
  | File Upload | 89a49d9d8d85b74ecf42459d0b86d96bc13a9780 | 2026-10-04 |
  | Cross Site Scripting Prevention | 3b93fa9b20ff78b65b0627266c22c5ef72c4dfaa | 2026-11-01 |
  | Deserialization | 16a0ed800ae13c8b2068b29845b2acadb9e8ed79 | 2026-10-04 |
  | .NET Security | 3cfa49de48236c667ddf1d0f9dc79e13e672b56d | 2026-10-18 |
  | Java Security | f1d0311aaadac4c315471feb8947c9fbb3cbb32e | 2026-10-22 |
  | Top 10 A05:2025 | d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966 | 2025-12-24 |

- DEC-10 same-day-commit check: the four sheets committed on 2026-11-08 were re-read from the Markdown at the pinned
  SHAs. Every H2/H3/H4 heading of the Markdown exists as an `id` on the published page (differences were only slug
  punctuation and duplicate-heading suffixes), and the rows' key sentences were found in the pinned Markdown.
- Versions: ASP.NET Core 10.0 / .NET 10 (`view=`); `ms.date` — EF Core SQL Queries 2022-09-19, BinaryFormatter guide
  2022-03-02, file uploads 2026-10-03, XSS 2026-05-13, model validation 2026-10-26. Oracle Secure Coding Guidelines
  "Document version: 11.0, Last updated: June 2025". JAXP guide Java SE 25. Spring Data JPA 4.1.2 (page `version` meta).
  Python 3.15.2 (`docs.python.org/3/`). Django 6.1 (`/en/stable/` redirects to `/en/6.1/`).
- Anchors: all 185 element anchors exist as `id`s on the published pages.
- Defaults quoted from the sources (the only defaults workers may rely on):
  - NET-07: "The FromSql and FromSqlInterpolated methods are safe against SQL injection, and always integrate parameter
    data as a separate SQL parameter. However, the FromSqlRaw method can be vulnerable to SQL injection attacks, if
    improperly used." / FromSqlRaw "allows interpolating variable data directly into the SQL string".
  - NET-08: "The default is Prohibit."
  - NET-11: "the default maximum request body size is 30,000,000 bytes, which is approximately 28.6 MB";
    `MultipartBodyLengthLimit` "The default is 134,217,728 (128 MB)".
  - NET-14: "For web apps, it's the app's responsibility to inspect ModelState.IsValid and react appropriately."
  - NET-15: "Strings added to the list don't need to be previously escaped." / "Using an instance of this type with
    untrusted data is a security risk."
  - JVA-12: "While FSP is enabled by default in the JDK, the default configuration does not restrict external entity
    resolution. For comprehensive security, explicitly set FSP through the API and configure external access
    restrictions as needed." / "external connections … are not disabled by default. To ensure external access is
    properly restricted, FSP needs to be explicitly set".
  - JVA-14: "By default, Spring Data JPA rejects any Order instance containing function calls, but you can use
    JpaSort.unsafe to add potentially unsafe ordering."
  - JVA-15: "the respective arguments for these queries will get sanitized. This means if the arguments actually contain
    characters recognized by LIKE as wildcards these will get escaped so they match only as literals."
  - PY-01: "If the shell is invoked explicitly, via shell=True, it is the application's responsibility to ensure that all
    whitespace and metacharacters are quoted appropriately to avoid shell injection vulnerabilities."
  - PY-04: "By default, Expat itself does not access local files or create network connections. Expat versions lower
    than 2.7.2 may be vulnerable to the 'billion laughs', 'quadratic blowup' and 'large tokens' vulnerabilities" /
    "xmlrpc is vulnerable to the 'decompression bomb' attack."
  - PY-05: "Don't make either of these mistakes" (string formatting / quoting `%s`); "using the params argument and
    leaving the placeholders unquoted protects you from SQL injection".
  - PY-08: `DATA_UPLOAD_MAX_MEMORY_SIZE` "Default: 2621440 (i.e. 2.5 MB)"; `DATA_UPLOAD_MAX_NUMBER_FIELDS` "Default:
    1000"; `DATA_UPLOAD_MAX_NUMBER_FILES` "Default: 100"; "You can set this to None to disable the check."
  - PY-10: `FILE_UPLOAD_PERMISSIONS` "Default: 0o644".
- Corrections made while checking rows:
  - **JVA-15**: the plan's anchor `sdj#jpa.query-methods.query-creation` (flagged "to be confirmed") is not where the
    LIKE-escaping sentence is. It sits in `sdj#jpa.sample-app.finders.strategies`, now the primary anchor;
    `sdj#jpa.query-methods.at-query.advanced-like` added.
  - **NET-09**: the bf page says DoS attacks "cannot be mitigated with a SerializationBinder or any other BinaryFormatter
    configuration switch"; wording changed from "a SerializationBinder doesn't fix it" to "a SerializationBinder or
    configuration switch can't mitigate it".
  - **XML-05**: primary anchor changed from `xml#dealing-with-invalid-xml-documents` to the more specific
    `xml#remote-schema-poisoning`; `xml#schema-poisoning` added.
  - **PY-08**: `dsec#form-submissions` added (source of the "limit request body size in your web server" SHOULD).
  - Anchors added for coverage only (no change of meaning): INJ-04 `inj#operating-system-commands`; INJ-06
    `inj#query-languages`; XML-04 `xml#document-without-schema`, `xml#improper-data-validation`; XSS-01
    `xss#output-encoding`; XSS-05 `xss#common-mistake`; XSS-10 `xss#sole-reliance-on-content-security-policy-csp-headers`;
    DES-01 `des#guidance-on-deserializing-objects-safely`, `des#php`, `des#clear-box-review` (PHP `unserialize` is
    covered as a native format); DES-02 `des#clear-box-review_3`; DES-03 `des#net-csharp`; DES-04 `des#python`;
    NET-01 `dnet#input-handling`; NET-06 `dnet#legacy-net-framework`; NET-07 `efsql#basic-sql-queries`; NET-09
    `bf#deserialization-vulnerabilities`; NET-11 `upl#size-validation`, `upl#per-request-body-size-limits`; NET-13
    `axss#encode-url-parameters`; JVA-12 `jaxp#JSSEC-GUID-61FD4DB8-…`.
  - A05 Description bullet 4 ("potentially hostile data is directly used or concatenated") is folded into A05-02.
- Level judgments (rows kept at `MUST` although the primary section has no RFC keyword): IV-02, IV-06 (framed as the
  required validation strategy); INJ-01 ("The preferred option"; kept MUST because the sheet's rule list is normative and
  A05-04 matches); XML-01 (the sheet states disabling DTDs is the defense); XSS-09 ("Try to refactor … to remove references
  to unsafe sinks", read with the safe-sink rule); vendor (Default) rows take the level of the OWASP element they support.
- Sample-repo review runs (plan §9 step 10) were deferred by the user on 2026-11-08; see "Open items".

### 2026-11-09 — SSRF added (afterplanning WP-9, decision D-1)

- Pinned the OWASP Server-Side Request Forgery Prevention Cheat Sheet at commit
  0765662030093f8b9251399439580e7507148018 (2026-11-08, the last commit touching the sheet's `.md`). New elements
  SSRF-01 … SSRF-08 and new check SEC-II-10 (Error). Input & Injection grew from 9 to 10 checks; scores before and after
  aren't directly comparable (README).
- Not localized: the network-layer protections (firewall/egress rules, segmentation) and IMDSv2 (`#imdsv2-in-aws`) are
  IaC controls that this subject doesn't receive (README "Known coverage gaps"); `#semgrep-rules` and
  `#tools-and-code-used-for-schemas` are tooling (CTX); the input-validation library tables in Case 1 are background
  for SSRF-03 (no (Default) element added). The plan's "responses not reflected raw" clause isn't in the sheet, so
  SEC-II-10 doesn't include it.
- SSRF anchor coverage: `introduction`, `context` (BG); `overview-of-a-ssrf-common-flow` (SSRF-05); `cases` (PARENT);
  `case-1-…` and `available-protections` (SSRF-01 … SSRF-04, SSRF-08); `example` (BG); `case-2-…`,
  `challenges-in-blocking-urls-at-application-layer`, `available-protections_1` (SSRF-04 … SSRF-08);
  `imdsv2-in-aws` (IaC gap); `deny-list-last-resort` (SSRF-06); `semgrep-rules`, `tools-and-code-used-for-schemas`,
  `references` (CTX).

### 2026-11-09 — JavaScript/TypeScript (afterplanning WP-12f phase 2)

- `node-input.md` (NDI-01 … NDI-06) and `../languages/javascript.md` from the OWASP Node.js Security Cheat Sheet (commit
  eeaa1e474bc2ef98119a3de7bafd067f52faf35e, 2026-11-05) and the Express page (open redirects). Closes this skill's JavaScript follow-up (plan C-13).
  Check count unchanged. Framework defaults beyond those stated in `node-input.md` (Fastify, NestJS, Next.js, Koa, Passport,
  logger masking) stay unlocalized; workers add `localized-standard-gap` notes.

## Open items

- Plan §9 step 10: run reviews against sample repos — (a) ASP.NET Core with `FromSqlRaw($"…{q}")`, `@Html.Raw(comment)`,
  `DtdProcessing.Parse`, `BinaryFormatter`, `Path.Combine(dir, file.FileName)`; (b) Spring Boot with `Statement`
  concatenation, `JpaSort.unsafe(param)`, a default `DocumentBuilderFactory` on uploads, `ObjectInputStream` on a request;
  (c) Django with `.raw(f"…")`, `mark_safe(user)`, `subprocess.run(…, shell=True)`, `pickle.loads`,
  `DATA_UPLOAD_MAX_MEMORY_SIZE = None`; (d) a JSON-only API with DTO validation and no uploads, XML or templates
  (expect SEC-II-05/06/07/08 N/A with reasons).
- Plan §10 C-1, C-2 (description), C-9 and C-10 were applied on 2026-11-08. The remaining hand-offs were closed by
  the cross-skill follow-up pass (2026-11-09): C-2 SSRF → SEC-II-10 here (D-1); C-5 labels; C-6 →
  dependency-management boundary step; C-7 rate limiting → `review-reliability` AZRL-32; C-11 worker rule in
  `WORKER.md`; C-13 JavaScript language id and `languages/javascript.md`. Open: none.

## Follow-up candidates (plan §7.3)

| Candidate | Est. elements | Status |
|---|---|---|
| XXE Prevention Cheat Sheet | ≈ 8 | Open (DEC-3, user choice) |
| OS Command Injection Defense Cheat Sheet | ≈ 5 | Open (DEC-3) |
| LDAP Injection Prevention, XPath Injection Prevention, NoSQL Security | ≈ 3 each | Open (scope) |
| Mass Assignment Cheat Sheet | ≈ 4 | Open (scope) |
| DOM based XSS Prevention Cheat Sheet | ≈ 6 | Open (scope) |
| Server-Side Request Forgery Prevention Cheat Sheet | 8 | Done 2026-11-09 (SSRF-01 … SSRF-08, SEC-II-10; D-1) |
| Unicode normalization and email validation (`ivl`, already pinned) | 2 | Open (weak code evidence) |
| Flask/Jinja2 autoescape and `Markup`; FastAPI/Pydantic validation | ≈ 4 each | Open (DEC-5, new websites) |
| Thymeleaf `th:utext`; Spring MVC validation; Spring Boot multipart limits | ≈ 5 | Open (DEC-5) |
| Hibernate native query guidance | ≈ 3 | Open (DEC-5) |
| lxml (`resolve_entities`, `no_network`, `huge_tree`) and PyYAML loaders | ≈ 4 | Open (new websites) |
| Microsoft Learn System.Xml security page (404 at planning) and .NET Framework `XmlDocument`/`XmlTextReader` defaults | ≈ 3 | Open (page location unknown) |
| ASP.NET Core `MaxModelValidationErrors`/`MaxValidationDepth` (`val#maximum-errors`, `val#maximum-recursion`); JSON `MaxDepth`; jQuery Unobtrusive error-message encoding (`val#html-encoding-and-error-message-security`) | ≈ 3 | Open (scope) |
| `pickle` restricted `Unpickler.find_class` (`ppkl#restricting-globals`) | 1 | Open (scope) |
| ASVS v5.0 V1, V2, V5 | > 60 | Open (would need its own budget decision) |

## `localized-standard-gap` / `localized-standard-stale` log

| Date | Run | Note | Action |
|---|---|---|---|
| — | — | (none yet) | — |

## Coverage map

Every H2/H3/H4 anchor of the 10 pinned cheat sheets, every A05 Description and How-to-prevent bullet, and every H2/H3
anchor of the pinned vendor sections is listed once: mapped to element IDs, or given a reason code. Vendor pages that
are localized for selected sections only (`psub`, `ppkl`, `psql`, `dqs`, `dset`, `dtpl`, `dutl`, `scg` sections 1, 3,
5, 8) list only those sections and the anchors inside them; their other sections are out of scope [M]. Microsoft Learn
page chrome (`ms--*`) is ignored. Snapshot 2026-11-08: 347 script-checked headings (cheat sheets, A05, `efsql`, `upl`,
`axss`, `val`, `bf`, `jaxp`, `sdj`, `dsec`, `dsql`) + 11 A05 bullets, 0 unaccounted.

### Top 10 bullets

| Bullet | Mapped to / reason |
|---|---|
| A05 Description 1 (user-supplied data not validated, filtered or sanitized) | A05-01 |
| A05 Description 2 (dynamic queries / non-parameterized calls without escaping) | A05-02 |
| A05 Description 3 (unsanitized data in ORM search parameters) | A05-03 |
| A05 Description 4 (hostile data directly used or concatenated) | A05-02 |
| A05 Description paragraph (NoSQL, OS command, ORM, LDAP, EL/OGNL injection) | A05-07 |
| A05 Description paragraph (code review plus SAST/DAST/IAST and fuzzing in CI/CD) | Otest (plan C-8) |
| A05 Description paragraph (LLM prompt injection) | Oscope (future AI-security subject) |
| A05 Prevent 1 (safe API / parameterized interface / ORM; stored-procedure note) | A05-04 |
| A05 Prevent 2 (positive server-side input validation) | A05-05 |
| A05 Prevent 3 (escape residual dynamic queries; structure names can't be escaped) | A05-06 |
| A05 Warning (escaping is error-prone) | B |

### Page headings

| Code | Reason for not localizing |
|---|---|
| B | background, definitions, examples, test techniques or references; no testable rule |
| P | parent heading; its rules are localized through the child anchors listed as mapped |
| C | Top 10 context (background, score table, attack scenarios, CWE list), not a requirement |
| N | database-administration, OS or deployment control; not visible in application code |
| M | framework mechanics or customization, or a section outside the pinned scope; not a security rule |
| V | older-version duplicate section on a versioned Microsoft Learn page (`-1`/`-2` suffix, or a repeated id) |
| S | restates or duplicates a localized element (named in brackets where useful) |
| D | framework behaviour that meets the OWASP element by default; nothing to fail |
| F | follow-up candidate (plan §7.3) |
| Oia | owned by `review-security-identity-access` (already localized there) |
| Oops | owned by `review-security-operational` (logs, secrets, encryption, deployment config) |
| Oweb | owned by `review-security-web-api` (HTTPS, security headers, CSP, CORS) |
| Orel | owned by `review-reliability` (download/request rate limits) |
| Odep | owned by `review-dependency-management` |
| Otest | owned by testing/CI subjects |
| Oscope | out of this subject's scope |

### Input Validation CS (`ivl`)

- Mapped: `introduction` → IV-01; `input-validation-strategies` → IV-02; `allowlist-vs-denylist` → IV-03; `parse-safely-then-validate` → IV-04, IV-05; `validate-structured-data` → IV-06, IV-07; `regular-expressions-regex` → IV-08; `validating-rich-user-content` → XSS-08; `common-pitfalls` → IV-01, IV-03, IV-09 (logging rejected input verbatim: Oops)
- Not localized [B]: `references`
- Not localized [F]: `validating-free-form-unicode-text`, `email-address-validation`
- Not localized [P]: `implementing-input-validation`
- Not localized [S]: `file-upload-validation` (pointer; FU-02, FU-03)

### Injection Prevention CS (`inj`)

- Mapped: `forms-of-injection` → INJ-06; `query-languages` → INJ-06; `xpath-injection` → INJ-06; `scripting-languages` → INJ-03; `operating-system-commands` → INJ-04; `remediation` → INJ-04, INJ-05; `network-protocols` → INJ-06; `rule-2-use-a-safe-api` → INJ-01; `rule-3-contextually-escape-user-data` → INJ-02
- Not localized [B]: `introduction`, `application-types`, `a1-new-application`, `a2-productive-open-source-application`, `a3-productive-closed-source-application`, `how-to-test-for-the-issue`, `example-code-java`, `references`
- Not localized [P]: `injection-prevention-rules`
- Not localized [S]: `rule-1-perform-proper-input-validation` (IV-01 … IV-03)

### SQL Injection Prevention CS (`sql`)

- Mapped: `introduction` → SQL-01; `basic-sql-injection` → SQL-01; `sql-injection-with-procedure-calls` → SQL-03; `sql-injection-in-orm-query-languages` → SQL-02; `sql-injection-inside-stored-procedures-and-functions` → SQL-03; `parameterized-queries` → SQL-01; `allow-list-input-validation` → SQL-04; `manually-escaping-strongly-discouraged` → SQL-05; `least-privilege` → SQL-07; `least-admin-privileges-for-multiple-dbs` → SQL-07; `input-validation` → SQL-06
- Not localized [B]: `references`
- Not localized [N]: `minimizing-application-and-os-privileges`, `details-of-least-privilege-when-developing`, `enhancing-least-privilege-with-sql-views`
- Not localized [Otest]: `testing-and-detection`
- Not localized [P]: `examples-of-injections`, `primary-defenses`, `hardening`

### Query Parameterization CS (`qp`)

- Mapped: `parameterized-query-examples` → QP-01; `prepared-statement-examples` → QP-02; `stored-procedure-examples` → SQL-03
- Not localized [B]: `introduction`, `using-java-built-in-feature`, `using-java-with-jpahibernate`, `using-net-built-in-feature`, `using-asp-net-built-in-feature`, `using-ruby-with-activerecord`, `using-ruby-built-in-feature`, `using-php-with-php-data-objects`, `using-cold-fusion-built-in-feature`, `using-perl-with-database-independent-interface`, `using-rust-with-sqlx`, `oracle-using-plsql`, `sql-server-using-transact-sql`, `references`

### XML Security CS (`xml`)

- Mapped: `handling-malformed-xml-documents` → XML-03; `applications-processing-malformed-data` → XML-03; `dealing-with-invalid-xml-documents` → XML-04; `document-without-schema` → XML-04; `unrestrictive-schema` → XML-04; `improper-data-validation` → XML-04; `schema-poisoning` → XML-05; `remote-schema-poisoning` → XML-05; `xml-entity-expansion` → XML-01, XML-02
- Not localized [B]: `introduction`, `definition-of-a-malformed-xml-document`, `malformed-xml-documents-require-extra-time`, `malformed-document-to-malformed-document`, `well-formed-document-to-well-formed-document-normalized`, `handling-coercive-parsing`, `violation-of-xml-specification-rules`, `string-data-types`, `numeric-data-types`, `general-data-restrictions`, `jumbo-payloads`, `traditional-jumbo-payloads`, `small-jumbo-payloads`, `references` (attack descriptions and schema detail folded into XML-02/XML-04)
- Not localized [N]: `local-schema-poisoning` (file permissions / supplier trust; embedded DTDs covered by XML-01)
- Not localized [P]: `dealing-with-malformed-xml-documents`

### File Upload CS (`fu`)

- Mapped: `introduction` → FU-06, FU-08 (CSRF/authorization bullets: Oia; library updates: Odep); `extension-validation` → FU-02; `list-allowed-extensions` → FU-01; `block-extensions` → FU-01; `content-type-validation` → FU-03; `file-signature-validation` → FU-03; `filename-safety` → FU-04; `file-content-validation` → FU-06; `file-storage-location` → FU-07, FU-08, FU-09, FU-10; `filesystem-permissions` → FU-09; `upload-and-download-limits` → FU-05 (download limits: Orel)
- Not localized [B]: `file-upload-threats`, `malicious-files`, `public-file-retrieval`, `java-code-snippets`, `references`
- Not localized [Oia]: `user-permissions`
- Not localized [P]: `file-upload-protection`

### Cross Site Scripting Prevention CS (`xss`)

- Mapped: `framework-security` → XSS-01, XSS-02; `xss-defense-philosophy` → XSS-01; `output-encoding` → XSS-01; `output-encoding-for-html-contexts` → XSS-03; `output-encoding-for-html-attribute-contexts` → XSS-03, XSS-04; `output-encoding-for-javascript-contexts` → XSS-04; `output-encoding-for-css-contexts` → XSS-06; `output-encoding-for-url-contexts` → XSS-05; `common-mistake` → XSS-05; `dangerous-contexts` → XSS-07; `html-sanitization` → XSS-08; `safe-sinks` → XSS-09; `other-controls` → XSS-10 (CSP/Trusted Types: Oweb; cookie attributes: Oia); `xss-prevention-rules-summary` → XSS-05; `common-anti-patterns-ineffective-approaches-to-avoid` → XSS-10; `sole-reliance-on-content-security-policy-csp-headers` → XSS-10; `reliance-on-http-interceptors` → XSS-10
- Not localized [B]: `introduction`, `problem-1-assumption-browser-versions-support-csp-equally`, `problem-2-issues-supporting-legacy-applications`, `problem-1-encoding-for-specific-context-not-satisfactory-for-all-uri-paths`, `problem-2-interceptor-approach-can-lead-to-broken-rendering-caused-by-improper-or-double-encoding`, `problem-3-interceptors-not-effective-against-dom-based-xss`, `problem-4-interceptors-not-effective-where-data-from-responses-originates-outside-your-application`, `summary`, `related-articles`, `references`
- Not localized [S]: `output-encoding-rules-summary` (XSS-03 … XSS-06)

### Deserialization CS (`des`)

- Mapped: `what-is-deserialization` → DES-01; `guidance-on-deserializing-objects-safely` → DES-01; `php` → DES-01; `clear-box-review` → DES-01; `python` → DES-04; `clear-box-review_1` → DES-04; `java` → DES-05; `clear-box-review_2` → DES-05; `prevent-data-leakage-and-trusted-field-clobbering` → DES-07; `prevent-deserialization-of-domain-objects` → DES-07; `harden-your-own-javaioobjectinputstream` → DES-05; `other-deserialization-libraries-and-formats` → DES-02, DES-06; `net-csharp` → DES-03; `clear-box-review_3` → DES-02; `general-precautions` → DES-02, DES-03, DES-09; `known-net-rce-gadgets` → DES-09; `using-alternative-data-formats` → DES-01; `only-deserialize-signed-data` → DES-08
- Not localized [B]: `introduction`, `opaque-box-review`, `opaque-box-review_1`, `opaque-box-review_2`, `mitigation-toolslibraries`, `detection-tools`, `references`
- Not localized [N]: `harden-all-javaioobjectinputstream-usage-with-an-agent`
- Not localized [P]: `language-agnostic-methods-for-deserializing-safely`

### .NET Security CS (`dnet`)

- Mapped: `input-handling` → NET-01; `sql-injection` → NET-01, NET-02; `cross-site-scripting-xss` → NET-03; `serialization-and-xml` → NET-04, NET-05; `legacy-net-framework` → NET-06; `aspnet-mvc-and-web-forms` → NET-06 (CSRF part: Oia)
- Not localized [B]: `introduction`, `references`
- Not localized [F]: `os-command-injection` (pointer to the OS Command Injection Defense sheet; DEC-3)
- Not localized [Oia]: `authentication-and-authorization`, `account-protection`, `passwords`, `authentication-cookies`, `authorization`, `redirects`, `cross-site-request-forgery`, `forms-authentication`
- Not localized [Oops]: `data-protection`, `encryption-for-storage`, `encryption-for-transmission`, `configuration-and-deployment`, `windows-communication-foundation-wcf`

### Java Security CS (`jsec`)

- Mapped: `serialization` → JVA-02; `sql-and-jpa-injections` → JVA-01
- Not localized [B]: `references`

### Top 10 A05:2025 (`a05`)

- Mapped: `description` → A05-01, A05-02, A05-03, A05-07; `how-to-prevent` → A05-04, A05-05, A05-06
- Not localized [C]: `background`, `score-table`, `example-attack-scenarios`, `references`, `list-of-mapped-cwes`

### Microsoft Learn: EF Core SQL queries (`efsql`)

- Mapped: `basic-sql-queries` → NET-07; `passing-parameters` → NET-07; `dynamic-sql-and-parameters` → NET-07; `executing-non-querying-sql` → NET-07
- Not localized [M]: `composing-with-linq`, `including-related-data`, `change-tracking`, `querying-scalar-non-entity-types`, `querying-unmapped-types`, `unmapped-complex-types`, `limitations`

### Microsoft Learn: file uploads, ASP.NET Core 10.0 (`upl`)

- Mapped: `security-considerations` → NET-10, NET-12; `file-name-security` → NET-10; `size-validation` → NET-11; `multipart-body-length-limit` → NET-11; `kestrel-maximum-request-body-size` → NET-11; `per-request-body-size-limits` → NET-11; `request-body-size-limits-summary` → NET-11
- Not localized [B]: `related-content`
- Not localized [M]: `storage-scenarios`, `small-and-large-files`, `file-upload-scenarios`, `buffering`, `streaming`, `upload-small-files-with-buffered-model-binding-to-physical-storage`, `upload-small-files-with-buffered-model-binding-to-a-database`, `upload-large-files-with-streaming`, `match-name-attribute-value-to-parameter-name-of-post-method`, `other-kestrel-limits`, `iis`, `troubleshoot`, `not-found-error-when-deployed-to-an-iis-server`, `connection-failure`, `null-reference-exception-with-iformfile`, `stream-was-too-long`
- Not localized [P]: `validation`, `server-and-app-configuration`
- Not localized [S]: `content-validation` (FU-06), `file-extension-validation` (FU-01, FU-02), `file-signature-validation` (FU-03)
- Not localized [V]: every anchor ending in `-1` or `-2`

### Microsoft Learn: XSS, ASP.NET Core 10.0 (`axss`)

- Mapped: `protect-your-application-against-xss` → NET-13; `explore-javascript-encoding-with-razor` → NET-13; `access-encoders-in-code` → NET-13; `encode-url-parameters` → NET-13; `determine-when-and-where-to-encode` → NET-13
- Not localized [B]: `related-content`
- Not localized [D]: `explore-html-encoding-with-razor` (Razor encodes by default; bypasses are NET-03)
- Not localized [M]: `customize-the-encoders`
- Not localized [S]: `use-validation-as-an-xss-prevention-technique` (XSS-10)

### Microsoft Learn: model validation, ASP.NET Core 10.0 (`val`)

- Mapped: `model-state` → NET-14; `client-side-validation` → NET-14
- Not localized [B]: `related-content`, `additional-resources`
- Not localized [F]: `maximum-errors`, `maximum-recursion`, `html-encoding-and-error-message-security`
- Not localized [M]: `rerun-validation`, `validation-attributes`, `built-in-attributes`, `error-messages`, `use-json-property-names-in-validation-errors`, `non-nullable-reference-types-and-required-attribute`, `non-nullable-reference-types-and-the-required-attribute`, `non-nullable-properties-on-generic-types-and-required-attribute`, `required-validation-on-the-server`, `required-validation-on-the-client`, `remote-attribute`, `additional-fields`, `alternatives-to-built-in-attributes`, `custom-attributes`, `ivalidatableobject`, `custom-validation`, `validationresult`, `top-level-node-validation`, `automatic-short-circuit`, `unobtrusive-validation`, `add-validation-to-dynamic-forms`, `add-validation-to-dynamic-controls`, `custom-client-side-validation`, `attributeadapter-for-client-side-validation`, `iclientmodelvalidator-for-client-side-validation`, `disable-client-side-validation`, `problem-details`
- Not localized [V]: every anchor ending in `-1`

### Microsoft Learn: BinaryFormatter security guide (`bf`)

- Mapped: `deserialization-vulnerabilities` → NET-09; `binaryformatter-security-vulnerabilities` → NET-09; `preferred-alternatives` → NET-04; `dangerous-alternatives` → NET-09
- Not localized [B]: `the-risks-of-assuming-data-to-be-trustworthy`, `see-also`

### Microsoft Learn: API reference pages (`dtd`, `arg`)

- Mapped: `dtd` `definition` → NET-08; `arg` `definition` → NET-15

### Oracle Secure Coding Guidelines, sections 1, 3, 5, 8 (`scg`)

- Mapped: `1-1` → JVA-05, JVA-11; `3-2` → JVA-03; `3-3` → JVA-07; `3-4` → JVA-04; `3-5` → JVA-05; `3-8` → JVA-06; `3-9` → JVA-09; `5-1` → JVA-08; `8-6` → JVA-10
- Not localized [M]: `1-2`, `1-3`, `1-4`, `3-1`, `3-6`, `3-7`, `5-2`, `5-3`, `5-4`, `8-5` (resource limits, library design, Security-Manager, mutable inputs, JNI and native topics outside request-input handling)
- Not localized [P]: `1`, `3`, `5`, `8`
- Not localized [S]: `8-1`, `8-2`, `8-3`, `8-4` (DES-05, DES-07)

### Oracle JAXP Security Guide, Java SE 25 (`jaxp`)

- Mapped: `JSSEC-GUID-61FD4DB8-244C-41B2-BC21-01B01C5D40EC` (Configuring JAXP for Secure XML Processing) → JVA-12; `JSSEC-GUID-82A5172C-C75E-4276-93C4-C3D2774C97E1` (General Recommendations) → JVA-13
- Not localized [B]: `JSSEC-GUID-3FB69003-1E4A-435C-B519-4B9D07630460` (Security Issues in XML Processing), `JSSEC-GUID-8105D3DD-C50A-43E2-93F8-A65CE4817966` (Appendix A, glossary)
- Not localized [M]: `JSSEC-GUID-825CBA59-583D-4F25-B1B8-945ED5B1470D` (Handling Errors), `JSSEC-GUID-8E8BFEFB-97C8-4B6D-A1ED-4B90B69B629B` (Appendix B, naming)
- Not localized [P]: `JSSEC-GUID-D97A1F1D-8DDF-4D19-A7E5-99099F27346E` (page title)

### Spring Data JPA: JPA Query Methods (`sdj`)

- Mapped: `jpa.sample-app.finders.strategies` → JVA-15; `jpa.query-methods.at-query.advanced-like` → JVA-15; `jpa.query-methods.sorting` → JVA-14; `_jpasort_unsafe_limitations` → JVA-14
- Not localized [M]: `jpa.query-methods.declared-queries`, `jpa.query-methods.query-creation`, `jpa.query-methods.named-queries`, `jpa.query-methods.named-queries.annotation-based-configuration`, `jpa.query-methods.named-queries.xml-named-query-definition`, `jpa.query-methods.named-queries.declaring-interfaces`, `jpa.query-methods.at-query.native`, `jpa.query-methods.query-introspection-rewriting`, `jpa.query-methods.query-rewriter`, `jpa.query-methods.scroll`, `jpa.named-parameters`, `jpa.query.spel-expressions`, `jpa.query.other-methods`, `jpa.modifying-queries`, `jpa.modifying-queries.derived-delete`, `jpa.query-hints`, `jpa.query-hints.comments`, `jpa.entity-graph`, `repositories.scrolling`, `repositories.scrolling.offset`, `repositories.scrolling.keyset`
- Not localized [P]: `jpa.query-methods.at-query`

### Python 3.15 (`pxml`, `psub`, `ppkl`, `psql`)

- Mapped: `pxml` `xml-vulnerabilities` → PY-04; `psub` `security-considerations` → PY-01; `ppkl` `module-pickle` → PY-02; `psql` `how-to-use-placeholders-to-bind-values-in-sql-queries` → PY-03
- Not localized [B]: `pxml` `module-xml`
- Not localized [F]: `ppkl` `restricting-globals`
- Not localized [M]: all other sections of `psub`, `ppkl` and `psql`

### Django 6.1: Security in Django (`dsec`)

- Mapped: `always-sanitize-user-input` → PY-07; `cross-site-scripting-xss-protection` → PY-06; `sql-injection-protection` → PY-05; `user-uploaded-content` → PY-08, PY-09; `form-submissions` → PY-08
- Not localized [B]: `security-in-django`, `limitations-and-considerations`, `additional-security-topics`
- Not localized [Oia]: `cross-site-request-forgery-csrf-protection`, `session-security`
- Not localized [Oweb]: `clickjacking-protection`, `ssl-https`, `host-header-validation`, `referrer-policy`, `cross-origin-opener-policy`, `cross-origin-resource-sharing-cors`, `content-security-policy`

### Django 6.1: raw SQL (`dsql`)

- Mapped: `raw-sql-fragments` → PY-05; `performing-raw-queries` → PY-05; `passing-parameters-into-raw` → PY-05; `executing-custom-sql-directly` → PY-05
- Not localized [M]: `mapping-query-fields-to-model-fields`, `index-lookups`, `deferring-model-fields`, `connections-and-cursors`, `calling-stored-procedures`
- Not localized [P]: `performing-raw-sql-queries`

### Django 6.1: selected reference sections (`dqs`, `dset`, `dtpl`, `dutl`)

- Mapped: `dqs` `extra` → PY-05; `dset` `data-upload-max-memory-size`, `data-upload-max-number-fields`, `data-upload-max-number-files` → PY-08; `dset` `file-upload-permissions` → PY-10; `dtpl` `autoescape`, `safe` → PY-06; `dutl` `module-django.utils.safestring` → PY-06
- Not localized [M]: all other sections of these pages
