# Maintenance — Twelve-Factor App localized standards

**Maintainers only. Workers never load this file.** Design decisions are recorded inline where they apply (DEC-n: this skill's localization decisions; D-n and C-n: cross-skill decisions and follow-ups); the planning documents they came from aren't kept in this repo.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1). No other skill uses 12factor.net.

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| 12factor.net | twelve-factor-app.md | 55 | 100 | 12 factor pages + `/` (provenance only). Per page: cb 4, dep 6, cfg 7, bs 5, brr 7, proc 4, port 4, conc 3, disp 3, dpp 4, logs 4, adm 4, idx 0 |
| — (local) | twelve-factor-rubric.md | 20 | n/a | Compliance Reviewer Twelve-Factor Rubric v1.0 |

The whole site holds about 75 statements that could become elements, so even full coverage stays under the cap.

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID.
- Every TFA and TFR ID must be listed by exactly one check in `../checklist.md`.
- Rows cite a **page key**, never an anchor: the factor pages have no section anchors below the factor heading, and
  both ids on each page (e.g. `#iii_config`, `#store_config_in_the_environment`) point at its top (plan DEC-11).
- Levels are informational; severity is always the check's default (plan DEC-7). The pages mix "never", "must",
  "should" and description; never map those words to severities.
- One-line paraphrases only (≈ 200 characters); never reproduce the source text beyond short quoted terms.
- English pages only. Translations under `/<locale>/` are never used.

## Rubric: applicability, equivalents and signals

The applicability table and the TFR "Accepted modern equivalents" and "Fail signals" columns are lookup tables. A
change is a rubric edit: no source refresh, but log it below with a date and reason, and add a README note if the
change would shift scores. Extend them when run notes log `deployable kind unclear` or `unknown framework <name>`.

| Rule | Reason |
|---|---|
| Applicability by deployable kind (libraries and clients: TF-01, TF-02 only) | The introduction scopes the methodology to software-as-a-service apps (`idx-01`, `idx-11`). Avoids findings like "library does not bind a port" (plan DEC-9). |
| Unclear kind → long-running service, confidence `low` | Conservative default; the gap note feeds this table. |
| Modern equivalents pass (TFR-06 and the equivalents column) | User decision DEC-3: the 2011 tool names are examples. Platform-injected config passes TF-03, consistent with SEC-OP-06. |
| TFR-01: TF-01 never fails for missing Git data | The hard rules forbid reading Git data beyond `rev-parse HEAD` (plan DEC-13). |
| TFR-03: lock files aren't judged | User decision DEC-4: DEP-02 owns lock files; one gap shouldn't fail two checks. |
| TFR-07: hardcoded credentials fail TF-03 and SEC-OP-05 | Plan DEC-14: different standards and remedies; cross-skill dedup merges the evidence. To use a single owner, make TFR-07 exclude literal secrets. |
| TFR-17 / TFR-20: migrations on every startup are a recommendation | Fail signal only if sample runs show it matters (plan F-5). |
| TFR-19: buffered stdout is a recommendation | The source asks for unbuffered output, but buffering is rarely visible in configuration. |
| Development-gated config passes everywhere except TF-10 | TF-10 is the only factor that compares development against production. |

## Pins and watch items

- **Pin:** footer "Written by Adam Wiggins • Last updated 2017" plus the 13 text hashes in the
  `twelve-factor-app.md` header (extraction below). There is no version number and no change feed.
- **Watch for a revised edition (plan F-1):** a new footer date, new or renamed factor pages, or a changed factor list
  on `/`.
- **Upstream repositories:** the footer links the site's open-source repositories. They are known upstream but **not**
  pinned or allowlisted (plan DEC-2). Adopt a commit pin only if cosmetic page changes cause false drift alarms
  (plan F-2).

## Refresh procedure

1. **Cadence:** every twelve months (the text has been stable since 2017). Refresh earlier on a watch item above, or
   when run notes contain ≥ 3 `localized-standard-gap` entries for this skill. "Deployable kind unclear" and
   unknown-framework entries count toward the rubric, not toward a source refresh.
2. **Drift check:** download the 13 pages (the maintenance-only URLs in
   `compliance-review-core/references/approved-sources.md`, section Twelve-Factor App) into a scratch folder, never
   into the repo, and recompute the hashes with the snippet below.
   - **Every hash matches:** record the check date in the log. Nothing else changes.
   - **A hash differs:** diff the extracted text against the previous snapshot. Markup or footer-only changes need
     only a hash update. A changed sentence means updating the affected coverage-map rows and elements.
   - **The factor list on `/` changes, a factor page is added or renamed, or the footer date changes:** treat it as a
     new edition and re-run the full localization (plan §12 steps 1–8).
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep 12factor.net ≤ 100 elements.
   Update the coverage map, the header hashes and retrieval date, `../sources.md`, and the URL list in
   `approved-sources.md` if a page moves.
4. **Rubric:** changes to the applicability table, equivalents and signals need no source refresh (see above).
5. **Verify:**
   - Script-check: every element ID is in exactly one check of `../checklist.md` and the per-check counts match plan
     §9; every paragraph, list item and table row on the 13 pages appears in the coverage map below — zero
     unaccounted.
   - Run a review against small sample repos (plan §12 step 8): `validate` passes, `12-review-twelve-factor.json` has
     `urlsFetched: []`, 12 checks are present, citations use page URLs or `#tfr-NN` paths, element IDs and source
     names.
6. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-twelve-factor` (maintainers only, never during a review) recomputes the 13 text hashes with the same extraction as the snippet below and compares them with `pins.json`. Update `pins.json` and the header together when a hash changes.

### Extraction and hash

Maintainers only, never run during a review. Python stdlib; save the pages as `index.html`, `codebase.html`, … and
run with `-I` from outside the snapshot folder.

```python
# usage: python -I hash12f.py <snapshot-dir>   (files: index.html, codebase.html, …)
import hashlib, html, pathlib, re, sys
d = pathlib.Path(sys.argv[1])
for f in sorted(d.glob("*.html")):
    t = f.read_text(encoding="utf-8")
    s = t.find('id="introduction"' if f.stem == "index" else 'id="factor"')
    e = t.find('id="locales"', s)
    body = t[t.rfind("<", 0, s):t.rfind("<", 0, e)]          # from the start tag holding the first id to the locale switcher
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip()
    print(f.stem, hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], len(text.split()))
```

For the coverage check, number the `<p>`, innermost `<li>` and `<tr>` blocks of the same extracted region per page
(`idx-01`, `cb-01`, …, skipping headings) and diff the numbers against the map below.

## Localization log

### 2026-11-09 — initial localization

- Implementation re-snapshot (plan §12 step 1) taken on 2026-11-09 into a scratch folder: all 13 hashes and word
  counts matched the planning snapshot (plan §5), and every page's footer reads "Last updated 2017". No differences
  to log.
- Every TFA row was checked against its page text; no row reproduces more than a one-line paraphrase.
- Anchor survey: no section anchors below the factor heading on any page; citations use the bare page URL (DEC-11).
- Plan defects fixed: (1) TF-02 no longer asks for a lock file (DEC-4); (2) TF-01 uses `targetGitHead` and never
  fails for missing Git data (TFR-01, DEC-13); (3) applicability by deployable kind added (DEC-9). Also: modern
  equivalents (DEC-3), pass/fail signals per factor, explicit ownership boundaries replacing the unworkable
  cross-check with `review-security-operational`, and a description matching the orchestrator.
- User decisions recorded in the plan: DEC-2 (footer date + text-hash pin), DEC-3 (modern equivalents pass), DEC-4
  (TF-02 scope), DEC-5 (12factor.net plus a local rubric; *Beyond the Twelve-Factor App* not used).
- Subject string confirmed as `Twelve-Factor` (orchestrator table and README; the report script uses it verbatim).
- Checklist mapping checked by script on 2026-11-09: 75 element IDs (55 TFA, 20 TFR), each in exactly one check;
  per-check counts match plan §9.
- Coverage map built from a block dump of the snapshot (106 numbered blocks). Script check on 2026-11-09: every block
  appears in the map below, zero unaccounted.

## Open items

- Follow-ups outside this skill: reviewed and closed in the cross-skill follow-up pass of 2026-11-09. Open hand-offs: none.
1. Run the plan §12 step 8 sample-repo reviews (three variants: C# Web API, Python Flask service, Java library). Skipped by user decision on 2026-11-09.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken). Count
"deployable kind unclear" and unknown-framework entries separately: they are input for the rubric tables.

## Coverage map

Block IDs are `<page key>-NN`, numbered as described under "Extraction and hash". Reason codes for "not localized":
- **APPL** — provenance of the rubric's applicability table; not an element.
- **CTX** — background, definition, narrative or summary table; no rule a repository can pass or fail on its own.
- **EX** — tool or product examples only; modern equivalents are in the rubric.
- **ORG** — organizational practice; not visible in a repository.
- **NV** — not visible in a repository (release cadence, remote execution mechanism).
- **NJ** — not judged (language choice).
- **OWN-<subject>** — owned by another subject skill (REL reliability REL-07, OBS observability / MON monitoring, DR
  disaster recovery, SL software lifecycle).

### idx (`/`)

| Block | Content | Covered by / reason |
|---|---|---|
| idx-01 | Methodology for software-as-a-service apps | APPL |
| idx-02 … idx-06 | Goals: declarative setup, clean OS contract, cloud suitability, minimal divergence, scaling | CTX (each goal is a factor) |
| idx-07 | Any language, any combination of backing services | APPL |
| idx-08 … idx-10 | Background and motivation | CTX |
| idx-11 | Who should read: apps that run as a service, their ops engineers | APPL |
| (headings) | The twelve factors list | CTX (duplicates the factor pages; watched for drift) |

### cb (`codebase`)

| Block | Content | Covered by / reason |
|---|---|---|
| cb-01 | Always tracked in version control; repo definition | TFA-01 |
| cb-02 | Codebase = one repo or repos sharing a root commit | TFA-01 |
| cb-03 | One-to-one correlation between codebase and app | TFA-02 |
| cb-04 | Several codebases = distributed system; each component complies | TFA-03 |
| cb-05 | Apps sharing code is a violation; factor into libraries | TFA-02 |
| cb-06 | One codebase, many deploys; definition of a deploy | TFA-04 (deploy definition: CTX) |
| cb-07 | Same codebase across deploys, different versions; commit example | TFA-04 (example: CTX) |

### dep (`dependencies`)

| Block | Content | Covered by / reason |
|---|---|---|
| dep-01 | Packaging systems; site packages vs vendoring | CTX |
| dep-02 | Never rely on system-wide packages; declare completely; isolation; same spec in prod and dev | TFA-05, TFA-06, TFA-08 |
| dep-03 | Bundler/Pip/Virtualenv/Autoconf examples; declaration and isolation together | TFA-07 (tool names: EX) |
| dep-04 | New developer needs runtime + dependency manager; deterministic build command | TFA-09 (`bundle install`, `lein deps`: EX) |
| dep-05 | No implicit system tools (ImageMagick, curl); vendor them | TFA-10 |

### cfg (`config`)

| Block | Content | Covered by / reason |
|---|---|---|
| cfg-01 … cfg-04 | Config = what varies between deploys: resource handles, credentials, per-deploy values | TFA-11 |
| cfg-05 | Constants in code violate strict separation | TFA-12 |
| cfg-06 | Open-source litmus test | TFA-13 |
| cfg-07 | Internal application config isn't config (Rails routes, Spring wiring) | TFA-14 (examples: EX) |
| cfg-08 | Config files outside VCS: improvement, but weaknesses | TFA-15 |
| cfg-09 | Store config in env vars | TFA-16 |
| cfg-10 | Grouping into named environments doesn't scale | TFA-17 |
| cfg-11 | Env vars are granular, orthogonal, managed per deploy | TFA-17 |

### bs (`backing-services`)

| Block | Content | Covered by / reason |
|---|---|---|
| bs-01 | Backing service definition; local examples | TFA-18 (products: EX) |
| bs-02 | Third-party services examples | TFA-18 (products: EX) |
| bs-03 | No distinction local vs third party; swap with config change only | TFA-19, TFA-20 |
| bs-04 | Each distinct backing service is a resource; loose coupling | TFA-21, TFA-22 |
| bs-05 | Attach and detach at will; restore-from-backup scenario | TFA-22 (backup and restore: OWN-DR) |

### brr (`build-release-run`)

| Block | Content | Covered by / reason |
|---|---|---|
| brr-01 | Three stages turn a codebase into a deploy | CTX (stages in TFA-23 … TFA-25) |
| brr-02 | Build stage | TFA-23 |
| brr-03 | Release stage | TFA-24 |
| brr-04 | Run stage | TFA-25 |
| brr-05 | Strict separation; no code changes at run time | TFA-26 |
| brr-06 | Release management, rollback; Capistrano example | TFA-28 (Capistrano: EX) |
| brr-07 | Unique release ID; append-only; immutable | TFA-27 |
| brr-08 | Builds initiated by developers; run stage with few moving parts | TFA-29 (who triggers builds: OWN-SL) |

### proc (`processes`)

| Block | Content | Covered by / reason |
|---|---|---|
| proc-01 | The app runs as one or more processes | CTX |
| proc-02 | Stand-alone script vs many process types | CTX |
| proc-03 | Stateless, share-nothing; persist in a backing service | TFA-30 |
| proc-04 | Memory/disk as single-transaction cache only | TFA-31 |
| proc-05 | Compile assets in the build stage | TFA-32 (asset packager names: EX) |
| proc-06 | No sticky sessions; session state in an expiring datastore | TFA-33 |

### port (`port-binding`)

| Block | Content | Covered by / reason |
|---|---|---|
| port-01 | Apps sometimes run inside a webserver container (Apache module, Tomcat) | TFA-34 (examples: EX) |
| port-02 | Self-contained; exports HTTP by binding a port | TFA-34 |
| port-03 | Local URL; routing layer in deployment | TFA-36 (local URL example: EX) |
| port-04 | Webserver library via dependency declaration, in user space; port contract | TFA-35, TFA-36 |
| port-05 | Non-HTTP services by port binding (ejabberd, Redis) | TFA-37 (examples: EX) |
| port-06 | One app as another's backing service via URL in config | TFA-37 |

### conc (`concurrency`)

| Block | Content | Covered by / reason |
|---|---|---|
| conc-01 | PHP-under-Apache and JVM uberprocess forms | CTX |
| conc-02 | Processes are first class; work assigned to process types | TFA-38 |
| conc-03 | Internal multiplexing allowed; must also span processes and machines | TFA-39 |
| conc-04 | Share-nothing scale-out; process formation | TFA-38, TFA-39 |
| conc-05 | Never daemonize or write PID files; rely on the process manager | TFA-40 |

### disp (`disposability`)

| Block | Content | Covered by / reason |
|---|---|---|
| disp-01 | Processes are disposable | TFA-41 |
| disp-02 | Minimize startup time | TFA-42 |
| disp-03 | Graceful SIGTERM shutdown of web processes; short requests | TFA-43 |
| disp-04 | Worker shutdown: return job, NACK, release locks; reentrant jobs | OWN-REL (REL-07; plan DEC-10) |
| disp-05 | Robust against sudden death; crash-only design | OWN-REL (REL-07, REL-08) |

### dpp (`dev-prod-parity`)

| Block | Content | Covered by / reason |
|---|---|---|
| dpp-01 | Historical gaps between development and production | CTX |
| dpp-02 | Time gap | NV (release cadence; release automation is OWN-SL SL-02) |
| dpp-03 | Personnel gap | ORG |
| dpp-04 | Tools gap | TFA-44 |
| dpp-05 | Designed for continuous deployment by keeping gaps small | CTX |
| dpp-06 | Make the time gap small | NV (OWN-SL SL-02) |
| dpp-07 | Make the personnel gap small | ORG |
| dpp-08 | Make the tools gap small | TFA-44 |
| dpp-09 … dpp-13 | Traditional vs twelve-factor summary table | CTX (summary of dpp-02 … dpp-08) |
| dpp-14 | Backing services are where parity matters; adapter libraries | TFA-45 |
| dpp-15 … dpp-18 | Adapter library table (ActiveRecord, Celery, ActiveSupport::Cache) | EX |
| dpp-19 | Appeal of lightweight local services (SQLite vs PostgreSQL) | TFA-45 |
| dpp-20 | Resist different backing services, even behind adapters | TFA-45 |
| dpp-21 | Packaged services, declarative provisioning, containers | TFA-47 (Homebrew, Chef, Puppet, Vagrant: EX) |
| dpp-22 | Adapters are for porting; same type and version everywhere | TFA-45, TFA-46 |

### logs (`logs`)

| Block | Content | Covered by / reason |
|---|---|---|
| logs-01 | Logs give visibility; a logfile is only an output format | TFA-48 |
| logs-02 | Aggregated, time-ordered stream; one event per line; no beginning or end | TFA-48 (line format: OWN-OBS OBS-01) |
| logs-03 | Never route or store the stream; no logfiles; unbuffered stdout | TFA-49, TFA-50 |
| logs-04 | Execution environment captures and routes; destinations not configurable by the app | TFA-51 (Logplex, Fluentd: EX) |
| logs-05 | Routing to files, tail, Splunk, Hadoop/Hive for introspection | OWN-OBS / OWN-MON (analysis) |
| logs-06 … logs-08 | Finding past events, graphing trends, alerting | OWN-OBS / OWN-MON |

### adm (`admin-processes`)

| Block | Content | Covered by / reason |
|---|---|---|
| adm-01 | Process formation vs one-off admin tasks | TFA-52 |
| adm-02 … adm-04 | Migrations, consoles, one-time scripts committed to the repo | TFA-52 |
| adm-05 | Identical environment, against a release; admin code ships with app code | TFA-53, TFA-54 |
| adm-06 | Same dependency isolation on all process types | TFA-55 |
| adm-07 | Preference for REPL languages; ssh or remote execution in production | NJ (language choice); NV (remote execution) |
