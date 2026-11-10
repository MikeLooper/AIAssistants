# Standards Refresh Procedure

You are refreshing the localized standards that the `review-*` skills review against. This is **maintenance work, never part of a compliance review**. The strategy is in `compliance-reviewer/STANDARDS-MAINTENANCE.md`; each skill's source-specific rules are in `compliance-reviewer/skills/<skill>/references/standards/MAINTENANCE.md`.

This file is AI-provider neutral. All paths are relative to the repository root. Arguments (may be empty): `[<skill> ... | all] [check | gaps | full]`, taken from the user's request. A skill may be named with or without its `review-` prefix.

## Modes

| Mode | What it does | Default when |
|------|--------------|--------------|
| `check` | Lint the manifests and report source drift. Edits nothing except, with approval, empty baselines in `pins.json`. | `all` or several skills are named |
| `gaps` | Collect `localized-standard-gap` / `localized-standard-stale` notes from `transitions/` into each skill's gap log and report which skills reached a refresh trigger. | — |
| `full` | `check`, then refresh the named skill: diff the changed sources, propose element changes, apply the approved ones, verify and record. | exactly one skill is named |

## Capability mapping

| Capability | Examples |
|------------|----------|
| **ask the user** | Claude `AskUserQuestion`; Copilot ask-questions tool; otherwise ask in plain chat and wait for the reply |
| **shell** | Bash / PowerShell / terminal tool |
| **fetch** | Claude `WebFetch`; Copilot fetch tool; otherwise the shell with Python `urllib`. Prefer the drift script, which enforces the allowlist itself |
| **todo list** | Claude `TodoWrite`; Copilot todo tool; otherwise a Markdown checklist in chat |

## Constraints

- **Allowlist.** Fetch only URLs listed in `compliance-reviewer/skills/compliance-review-core/references/approved-sources.md`, under the section of the skill being refreshed. If a source moved or a new page is needed, ask the user before adding it to the registry, and never add a site-wide prefix.
- **Scratch space.** Save downloaded pages and drift reports in a scratch or temp folder outside the repo, in a new empty folder. Run any Python over downloaded files with `python -I`, from outside that folder.
- **No silent edits.** Never change an element row, a check or a pin until the user has approved the specific change list (step 6).
- **Writes allowed:** the refreshed skill's folder (`SKILL.md`, `references/**`, including `pins.json`), `approved-sources.md`, the Maintenance section of `compliance-reviewer/README.md` (score-comparability notes) and the cadence table in `STANDARDS-MAINTENANCE.md`. Read `transitions/` but never change it. Don't touch other skills except to note a shared-source change for them.
- **Editing rules** come from the skill's `MAINTENANCE.md` ("Rules for editing elements"): IDs are stable forever (new IDs only, `(retired)` for removed rules), levels keep the source's own wording, each element belongs to exactly one check, at most 100 elements per website unless an exception is recorded, and nothing another subject owns. Every new check gets a `Sub-subject` label in `checklist.md`, and labels are stable like IDs (see step 3 of `STANDARDS-MAINTENANCE.md`).
- Don't read Git history of this repo unless the user asks.

## Procedure

1. **Parse the request.** Work out the skills and the mode. If nothing was named, show the cadence table from `STANDARDS-MAINTENANCE.md` and ask which skills and which mode. Build the todo list.
2. **Lint.** Run `python compliance-reviewer/scripts/check_source_drift.py lint <skills>`. On errors, show them and ask whether to fix the manifests first (a header and its `pins.json` disagreeing usually means a refresh was half-recorded).
3. **Collect notes** (`gaps` and `full`). Search `transitions/*/*.json` for `localized-standard-gap` and `localized-standard-stale`. Group them by skill (the transition file name carries the skill) and count those dated after the skill's last localization-log entry. Show the counts against the triggers (3 or more gaps, or any stale note; some skills exclude named note types). With approval, add each new note to the skill's gap log (date, run ID, description). For a gap about an unrecognized library, setting or resource type, propose the lookup-table edit (`languages/<id>.md`, `*-signals.md`); it needs no source refresh. In `gaps` mode, stop here and summarize.
4. **Detect drift.** Run `python compliance-reviewer/scripts/check_source_drift.py check <skills> --md <scratch>/drift-<YYYY-MM-DD>.md`. Without a `GITHUB_TOKEN` the GitHub API allows 60 requests an hour; for `all`, warn the user before running. Report:
   - `changed` rows (what moved, from which pin to which current value) and which standards file each affects;
   - `error` rows (fetch failures, missing pages, rate limit);
   - `manual` rows and the skill's dated "Refresh due" entries that are now due;
   - `no-baseline` rows: offer `--record-baselines`, which stores today's values in `pins.json` marked `baseline`.
   A shared source (OWASP Top 10, SSDF, Scorecard, a cheat sheet used by several skills) that changed affects every skill that pins it; list them. In `check` mode, stop here and suggest next steps (`full` per skill with drift).
5. **Diff the changed sources** (`full`). Read the skill's `MAINTENANCE.md`, its standards files and `pins.json`. For each `changed` source, fetch the pinned version (commit permalink, versioned path or saved snapshot, as the skill's drift step describes) and the current version, then diff the normative text and the anchor list for the localized sections only. A change only in markup, navigation or unrelated sections needs only a pin update.
6. **Propose changes and ask.** Present one table per standards file: element ID (new IDs for additions), action (`edit` / `add` / `retire` / `pin only`), the source sentence and anchor, the proposed summary and level, and the owning check. Also list knock-on edits: checklist element lists, check counts, `sources.md`, the coverage map, `pins.json`, `approved-sources.md` (moved or re-versioned URLs). Ask the user to approve all, some or none.
7. **Apply the approved changes.** Edit element rows; update each file header (pins, "Localized" date, element counts); update the checklist, `sources.md`, the coverage map and `pins.json` (copy the new pin values exactly as written in the header, and drop the `baseline` mark where the header now records the value). Keep each site within its element budget.
8. **Verify.**
   - Run `lint` again; it must report `ok: true`.
   - If `checklist.md` changed, run `python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py labels <skill>`; it must report `ok: true`.
   - Run `check <skill>` again; refreshed sources must now be `unchanged`.
   - Do the script checks the skill's `MAINTENANCE.md` verify step lists (IDs contiguous, element-to-check mapping, every cited anchor in the pinned source, coverage map with zero unaccounted).
   - Tell the user which sample-repo review the verify step asks for. It runs separately (`/compliance-reviewer <sample> <skill>` or the tool's equivalent), followed by `compliance_report.py validate`.
9. **Record.** Add a dated localization-log entry (pins before and after, what changed, why). Clear handled "Refresh due" and "Open items" entries and add dated ones for the next known vendor events. If the check count, a check's meaning or a severity changed, add a dated score-comparability note to the Maintenance section of `compliance-reviewer/README.md`.
10. **Summarize** what was checked, what changed, what was deferred (with reasons), and what still needs the sample review.
