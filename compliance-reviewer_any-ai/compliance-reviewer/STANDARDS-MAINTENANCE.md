# Maintaining the localized standards

**Maintainers only.** The orchestrator and workers never load this file. It is the central description of how the standards, requirements and specifications that the `review-*` skills extracted from external sources are kept current. The detailed, source-specific procedure for each subject stays in that skill's `references/standards/MAINTENANCE.md`; this file says how those procedures fit together and how to run one.

## Strategy in one paragraph

Reviews never fetch URLs. Each subject reviews against **local, pinned summaries** of its external sources (`references/standards/<source>.md`), so a review's result depends only on files in this repo. The price is that those summaries drift as the sources change. Drift is managed by **scheduled and triggered refreshes** done by a maintainer, outside any review: fetch the pinned source pages (the only time fetching is allowed), compare them with the recorded pins, update the affected elements without ever reusing an ID, re-verify coverage with a script, run a sample review, and log what changed. Reviews feed the loop back by writing `localized-standard-gap` and `localized-standard-stale` notes into their transition files.

## What gets maintained

Per subject skill, `compliance-reviewer/skills/review-<name>/`:

| File | What it holds | Changed when |
|---|---|---|
| `references/standards/<source>.md` | Header with pinned version / commit SHA / page dates / hashes, citation base URL and "Localized" date; one row per element (stable ID, the source's own level wording, summary, "applies when", anchors) | A source changes, or a gap is closed |
| `references/standards/MAINTENANCE.md` | Element budget per website, editing rules, **refresh procedure** (cadence, drift detection, update, verify), pins and watch items, "Refresh due" dates, localization log, open items, gap log, anchor coverage map | Every refresh (log, pins, coverage map) |
| `references/standards/pins.json` | Machine-readable pins for the drift checker (see "Drift checker" below); values copied from the file headers, or recorded baselines | Every time a header pin changes |
| `references/checklist.md` | `Subject:` line, then the checks: ID, `Sub-subject` label and the element IDs each check owns | Elements are added, retired or moved between checks; checks are added or retired |
| `references/sources.md` | Human-readable source list with pins and retrieval dates | Pins or retrieval dates change |
| `SKILL.md` → `## Standards (local, authoritative)` | Which standards files workers load | A standards file is added, renamed or removed |
| `references/languages/<id>.md`, `*-signals.md` | Lookup tables (libraries, defaults, config keys, IaC resource types) | A review logs a gap for an unrecognized library, setting or resource type. No source refresh needed |
| Local rubrics (`*-rubric.md`) | Rules written in this repo, not extracted from a website | Findings quality issues or disputes; versioned (patch = wording, minor = elements, major = scoring) |

Shared files:

- `compliance-review-core/references/approved-sources.md` — the maintainer-only registry of the exact pages a maintainer may fetch for each subject. Update it whenever a pinned URL or version path changes. Site-wide prefixes aren't allowed.
- `compliance-reviewer/README.md` → **Maintenance** — score-comparability notes (see "Record" below).

## Vendor-neutral elements

Every active element must apply to any codebase in its language, whatever the cloud or host. Vendor sources (Azure Well-Architected Framework, Azure Architecture Center, the Microsoft REST API Guidelines' Azure edition, Azure SDK guidance) are used for their generic guidance only. When a source rule names a vendor-only mechanism (a product, SKU, `x-ms-*` header, `api-version` parameter, host-name pattern or vendor SDK), either generalize it to the cloud-neutral rule it illustrates, naming the vendor form only as one example that satisfies it, or retire it when nothing generic is left. Don't add elements that apply only to one vendor (the former Scope `A`). Vendor names may still appear in lookup tables (`languages/*.md`, `*-signals.md`) next to their equivalents from other vendors. Applied across all skills on 2026-11-12 (see the README's Maintenance notes). On refresh, re-apply the same generalization to changed source text.

## When to refresh

Each skill's `MAINTENANCE.md` is authoritative for its cadence; this table is the overview.

| Subject skill | Sources (pinned) | Scheduled cadence | Extra triggers |
|---|---|---|---|
| review-api-design | OpenAPI 2.0/3.0.4/3.1.2/3.2.1; Microsoft REST API Guidelines, Azure edition (commit SHA; generic rules only, Azure-only mechanisms generalized or retired); Azure SDK trace-context guidance | Quarterly | Azure guideline History table gains an entry |
| review-cost-sustainability | Azure WAF cost + sustainability pages; Green Software Foundation principles and patterns | Quarterly | — |
| review-dependency-management | OWASP A03:2025 and supply-chain cheat sheets; .NET, Java, Python, Spring, Node.js lifecycle data | Lifecycle files quarterly; OWASP quarterly | Within 2 weeks of vendor GA events (.NET Nov, Java Mar/Sep, Python Oct, Spring May/Nov, Node.js Apr/Oct); dates in "Refresh due"; any stale note |
| review-disaster-recovery | Azure WAF Reliability (DR); NIST SP 800-34 Rev. 1; OWASP secrets backup | Quarterly | New NIST revision or withdrawal |
| review-maintainability | Local rubric only (no website) | Every 6 months | A disputed finding |
| review-mcp-server | MCP specification revision 2026-07-28 (stdio, tools; commit SHAs); MCP Security Best Practices and Local Server Security; modelcontextprotocol.info best practices; CSA Agentic MCP guide v1 (draft); The New Stack (partial, manual) | Quarterly | New MCP specification revision; official SDK major version; CSA final version |
| review-monitoring | Azure WAF monitoring/alerting; Google SRE books | Quarterly | — |
| review-observability | OpenTelemetry (semconv v1.45.0, spec v1.62.0); Azure WAF observability | Quarterly | Semconv minor release touching HTTP, DB, messaging, exception or resource conventions |
| review-performance | Azure WAF Performance Efficiency; Architecture Center antipatterns and caching | Quarterly | — |
| review-reliability | Azure WAF Reliability; Architecture Center resiliency patterns | Quarterly | Shared pages with Disaster Recovery: refresh both |
| review-security-identity-access | OWASP cheat sheets, Top 10:2025 A01/A07; ASP.NET Core, Spring Security 7.1, Django 6.1, Node.js | OWASP quarterly | Within 2 weeks of Spring Security minor and Django feature releases; dates in "Refresh due"; any stale note |
| review-security-input-injection | OWASP cheat sheets, A05; Microsoft Learn (.NET 10), Java SE 25, Spring Data JPA 4.1, Python 3.15, Django 6.1, Node.js | OWASP quarterly | Each pinned vendor release; dates in "Refresh due"; any stale note |
| review-security-operational | OWASP cheat sheets, A09/A10; Microsoft Learn, Spring Boot 4.1, Django 6.1, Python 3.15, Node.js | OWASP quarterly | Each pinned vendor release; new Top 10 edition; dates in "Refresh due"; any stale note |
| review-security-web-api | OWASP cheat sheets, A02; ASP.NET Core 10, Spring Security 7.1 / Framework 7.0, Django 6.1, MDN, Node.js | OWASP quarterly | Each pinned vendor release; new Top 10 edition; dates in "Refresh due"; any stale note |
| review-software-lifecycle | SemVer 2.0.0; NIST SSDF 1.1; SLSA v1.2; OpenSSF Scorecard v5.6.0 | Every 6 months | Watch items (SSDF 1.2 final, new SLSA/Scorecard release) |
| review-software-quality | ISO/IEC 25010:2023; Azure Architecture Center; Fowler; Microsoft C#; Google Java/TypeScript Style; PEP 8/257; local rubric | Every 6 months | Watch items (pinned commits / `ms.date`) |
| review-testing | Martin Fowler testing articles; Microsoft unit-testing; OWASP; SSDF PW.8; Scorecard; Azure WAF PE:06/RE:08; local rubric | Every 12 months | Watch items |
| review-twelve-factor | 12factor.net (text hashes); local rubric | Every 12 months | Changed hash, footer date or factor list |

Triggers that apply to **every** skill:

- **Gap threshold:** 3 or more `localized-standard-gap` notes for the skill since its last refresh (some skills exclude named note types; see their `MAINTENANCE.md`).
- **Stale note:** any `localized-standard-stale` note. Skills with version-pinned vendor files write it when a review runs more than 9 months after a standards file's "Localized" date.
- **Shared source changes:** OWASP Top 10, SSDF and Scorecard are pinned by several skills. When one re-pins, check the others (Testing, Software Lifecycle and the four security skills).
- **Open items:** a skill's "Open items" or "Refresh due" section lists outstanding work (for example first full re-verification against live sources). Clear those before relying on the skill's scores.

## How to refresh a subject

Run this in a **maintenance session**, not during a review. Fetching is allowed here, but only for pages listed for that subject in `approved-sources.md`.

1. **Collect feedback.** Gather the notes reviews left for maintainers and copy each relevant one into the skill's gap log (date, run ID, description):

   ```powershell
   Select-String -Path transitions\*\*.json -Pattern 'localized-standard-(gap|stale)' | Select-Object Path, Line
   ```

   ```bash
   grep -o 'localized-standard-\(gap\|stale\)[^"]*' transitions/*/*.json
   ```

   Notes live only in the transition files; the rendered report doesn't show them. A gap about an unrecognized library, setting or resource type is closed by editing the lookup table (`languages/<id>.md`, `*-signals.md`); it doesn't need a source refresh.
2. **Detect drift.** Start with the drift checker: `python compliance-reviewer/scripts/check_source_drift.py check <skill>`. It flags which pinned sources changed; then follow the skill's "Detect drift" / "Drift checks" step for those sources and for anything the checker lists as `manual`. The common techniques are:
   - GitHub-hosted sources (OWASP, Azure API guidelines, PEPs, Google style, SLSA, Scorecard, GSF): compare the latest commit SHA of the pinned file (`https://api.github.com/repos/<owner>/<repo>/commits?path=<file>&per_page=1`) with the pin.
   - Microsoft Learn: compare `ms.date`, the "Last updated" footer and `git_commit_id` with the pins (`ms.date` alone is unreliable), follow redirects, and check the section `toc.json` for added or removed pages.
   - Versioned vendor docs (Spring, Django, Python, .NET, Java): compare the current release (release APIs, `/stable/` redirect, page title) with the pinned version path.
   - Sources with no feed (12factor.net, martinfowler.com, iso25000.com): compare extracted-text hashes or revision lists.

   Download pages into a scratch folder outside the repo, and run any Python over them with `python -I`. If nothing changed, record the check date in the localization log and stop.
3. **Update elements.** Follow the skill's "Rules for editing elements":
   - IDs are stable forever. Add new IDs only; mark removed rules `(retired)`; never reuse an ID.
   - Keep the level in the source's own words (`REVIEW` for locally derived rules).
   - Every element belongs to exactly one check; keep `checklist.md` in step.
   - Every new check gets a `Sub-subject` label (Title Case, `&` not `and`, no ` / `, at most about 32 characters). A retired check stays as a table row whose Check cell starts with `*(retired`. Labels are stable like check IDs: change one only in a dated, recorded edit (a localization-log entry; plus a README score-comparability note if it moves a check to another subject).
   - Stay within 100 elements per skill per website unless an exception is recorded in the budget table.
   - Don't add elements another subject owns (each skill's `SKILL.md` lists its boundaries).
   - Update the file header pins and "Localized" date, `sources.md`, the coverage map, and `approved-sources.md` if a URL or version path changed.
4. **Verify.**
   - Run `python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py labels <skill>`; it must report `ok: true`.
   - Script-check as the skill describes: IDs contiguous, element-to-check mapping holds, every cited anchor exists in the pinned source, every normative anchor of the pinned pages is in the coverage map with zero unaccounted.
   - Run a review of the subject against the small sample repos described in the skill's verify step, then `python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py validate transitions/<runId>`. Expect `ok: true`, `urlsFetched: []`, the expected check count, and citations that use pinned URLs and element IDs.
5. **Record.**
   - Add a dated entry to the skill's localization log (snapshot pins, what changed and why). Clear handled "Refresh due" and "Open items" entries, and add new dated ones for the next known vendor events.
   - If the check count, a check's meaning or severities changed, add a dated **score-comparability note** to the Maintenance section of `compliance-reviewer/README.md` ("scores before and after that date aren't directly comparable").
   - Bump `schemaVersion` only if a transition or finding schema changed.

## Usage: the refresh command

The steps above are packaged as a command whose neutral procedure is [REFRESH.md](REFRESH.md). It never edits an element before you approve the change list.

| Tool | How to run it |
|------|---------------|
| Claude Code | `/refresh-standards [<skill> ... \| all] [check \| gaps \| full]` |
| GitHub Copilot | prompt `/refresh-standards` with the same arguments |
| Codex and others | ask to "refresh the localized standards" (`AGENTS.md` points at `REFRESH.md`) |
| Paste-in chat | paste `REFRESH.md` and attach the skill folder; the drift script must then be run by you |

Modes:

- `check` (default for `all`): lint the manifests and report drift. Example: `/refresh-standards all`.
- `gaps`: collect `localized-standard-gap` / `localized-standard-stale` notes from `transitions/` into the gap logs and report which skills reached a trigger. Example: `/refresh-standards all gaps`.
- `full` (default for one skill): drift check, diff, proposed element changes, then apply, verify and record. Example: `/refresh-standards security-web-api`.

Review the drift report and the element diff before accepting changes: element wording decides findings.

## Drift checker

`compliance-reviewer/scripts/check_source_drift.py` (Python 3, standard library only; maintainers only, never run during a review) automates the pin comparisons of the "Detect drift" step for every skill.

```
python compliance-reviewer/scripts/check_source_drift.py lint  [skill ...]
python compliance-reviewer/scripts/check_source_drift.py check [skill ...] [--md <scratch>/drift.md] [--json] [--method M] [--record-baselines]
```

- `lint` (offline): every `pins.json` is well formed; every pin it copies from a header is literally present in that header; every standards file has a check or is listed under `unpinned`; every URL is in `approved-sources.md`; every active element is listed in its skill's `checklist.md`. Exits 1 on errors.
- `check` (network): fetches only URLs in `approved-sources.md` (anything else is refused) and reports each check as `unchanged`, `changed`, `no-baseline`, `manual` or `error`. Exits 1 when something changed, 2 on fetch errors only. `--md` writes a report to paste into a localization log; keep it outside the repo.
- `--record-baselines` stores today's value for checks that have none and marks them `"baseline": "<date>"`. A baseline records "the source as of that date", not "as of localization", so note it in the localization log.
- GitHub API calls are limited to 60 an hour without a token; set `GITHUB_TOKEN` for `check all` runs repeated within an hour.

`pins.json` (one per skill, next to `MAINTENANCE.md`) holds `checks`, optional `unpinned` (file → reason) and optional `lint.elementsNotInChecklist` (ID prefixes). Each check has an `id`, the standards `file` it pins, a `method`, optional `note` and `watch: true` (a watch item, such as a draft that becomes final). Methods:

| Method | Fields | Changed when |
|--------|--------|--------------|
| `github-commit` | `repo`, `path`, `ref`, `pinned` (SHA or prefix), `pinnedDate` | the newest commit touching `path` differs from the pin and is dated after `pinnedDate` |
| `github-release` | `repo`, `pinned` (tag) | the latest release tag differs |
| `learn-page` | `url`, `msDate`, `gitCommit` | the page's `ms.date` or `git_commit_id` meta value differs, or the page moved |
| `redirect` | `url`, `expect` | the final URL no longer contains `expect` (e.g. Django `/en/stable/` → `/en/6.1/`) |
| `regex` | `url`, `pattern` (one group), `pinned` | the captured value differs (versions in titles or meta tags, page commits) |
| `http-status` | `url`, `pinned` | the status differs (e.g. a draft's final page stops returning 404) |
| `json` | `url`, `select`, `first`, `hash`, `pinned` | the selected value (or its hash) differs; `select` is a small path language: `a.b[*]`, `a[k=v]`, `a[0]`, trailing `{x,y}` projection |
| `text-hash` | `url`, `pinned`, optional `startMarker`/`endMarker` or `extract: "ids"` | the SHA-256 prefix of the page text (or of its sorted `id` attributes) differs |
| `manual` | `note` | always listed, for steps with no approved machine-readable signal |

The checker only detects that a source changed. Deciding what the change means, diffing the localized sections, anchor coverage and the sample review stay with the maintainer (the refresh command walks through them).

## Adding a new localized source

Adding a source (rather than refreshing one) follows the localization recipe in `compliance-reviewer/README.md` → Maintenance → "Localize a subject's standards". Worked example: `skills/review-api-design/`. The result must include a `MAINTENANCE.md` with the sections above, a `pins.json` entry for each pinned source (with its drift-check URL added to `approved-sources.md`), and a row in the cadence table in this file, so the source enters this refresh cycle. Run `check_source_drift.py lint <skill>` before finishing.
