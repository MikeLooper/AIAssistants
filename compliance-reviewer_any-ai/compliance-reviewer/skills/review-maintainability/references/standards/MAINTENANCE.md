# Maintenance — Maintainability localized standard

**Maintainers only. Workers never load this file.** Design decisions are recorded inline where they apply (DEC-n: this skill's localization decisions; D-n and C-n: cross-skill decisions and follow-ups); the planning documents they came from aren't kept in this repo.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget

| Source | Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|---|
| Compliance Reviewer Maintainability Rubric | none (written in this repo) | maintainability-rubric.md | 39 | 100 | Cap applied voluntarily (plan DEC-1); no external website is localized |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. The prefix is `MR-` (plan DEC-7) so it can't be confused with `MAINT-` check IDs or other skills' element prefixes.
- Every row starts with `<a id="mr-NN"></a>` (lower-case ID) so each element has its own link target.
- Level: every element is `REVIEW`. Severity always comes from the owning check's default (plan DEC-4; `SKILL.md` step 7).
- Each element belongs to exactly one check. The rubric's Check column and the Elements column in `../checklist.md` must agree.
- Keep rows to one line (≈ 200 characters where possible).
- Debt-marker threshold for MR-18 (plan DEC-8): 3 or more untracked markers in one reviewed file, or any untracked `FIXME`/`HACK` in error-handling, security or data-access code.
- Citation URL (plan DEC-5): written relative to `docs/reports/`; `compliance_report.py render` rebases it onto the actual `--out` folder (plan C-4). The `standard` text always names the element.
- Version (rubric header and `../sources.md`): wording-only edits bump the patch number; added or retired elements bump the minor number; a change to how checks are scored bumps the major number and needs a score-comparability note in `compliance-reviewer/README.md`.
- No URLs: the **Maintainability** section of `compliance-review-core/references/approved-sources.md` lists none. Add URLs there (as Maintenance-only) only if the rubric is grounded in an external standard (review step 5).

## Review procedure

There is no external source to drift, so maintenance is driven by findings quality rather than by source releases.

1. **Cadence:** every six months, or when run notes contain 3 or more `localized-standard-gap` entries for this skill, or when a reviewer disputes a maintainability finding as unclear.
2. **Collect:** gather the `localized-standard-gap` notes and any disputed findings from recent `transitions/*/27-review-maintainability.json` files into the gap log below.
3. **Update:** reword elements (patch bump), add elements with new IDs or retire them (minor bump), keep the total at or under 100, keep the Elements column in `../checklist.md` in step, and update the version in the rubric header and `../sources.md`.
4. **Verify:**
   - Script-check: IDs contiguous (retired rows included); every row has its `<a id>` anchor; every MR ID is listed by exactly one check in `../checklist.md` and matches the rubric's Check column.
   - Run a review against small sample repos: (a) README, CONTRIBUTING, CHANGELOG, ADRs and `.env.example` present; (b) only a minimal README; (c) a source file with untracked TODOs and an `[Obsolete]` method still called. Expect: `validate` passes; `27-review-maintainability.json` has `urlsFetched: []`; all 9 checks present; citations use the rubric name, MR IDs and `#mr-NN` links that resolve from `docs/reports/`; MAINT-04/05 notes carry the scope line; (b) gives "missing" findings only where the listing is in scope.
5. **If the rubric is ever grounded in an external standard** (for example ISO/IEC 25010, reversing plan DEC-1): localize it as a separate standards file under the per-website cap, add its URLs to the **Maintainability** section of `approved-sources.md` as Maintenance-only, and add an anchor coverage map here.

## Version log

- **1.0 — 2026-11-08** — initial rubric from the Maintainability localization (36 elements, 9 checks). Wording shortened against the planned element inventory to keep rows near 200 characters, meaning unchanged: MR-08, MR-11, MR-13, MR-14, MR-19, MR-20, MR-23, MR-27, MR-34.

- **1.1 — 2026-11-09** — MR-37 … MR-39 and check MAINT-10 (license and code of conduct; afterplanning WP-12d, closes
  maintainability C-6 and lifecycle C-5). Local rubric, no fetch. Maintainability grew from 9 to 10 checks; scores
  before and after aren't directly comparable (README). OpenSSF Scorecard's License check (pinned by
  `review-software-lifecycle`) is a related reference but isn't cited, so the rubric stays source-free.

## Open items

- Follow-ups outside this skill: reviewed and closed in the cross-skill follow-up pass of 2026-11-09. Open hand-offs: none.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Derivation map

There is no external source, so this maps the pre-localization checks and `SKILL.md` procedure steps to MR elements instead of an anchor coverage map.

| Old check / SKILL.md step (before 2026-11-08) | MR elements |
|---|---|
| Step 1 (load checklist and sources) | new `SKILL.md` step 1 also loads the rubric |
| MAINT-01 / step 2 (README covers setup, running, testing) | MR-01 … MR-06 |
| MAINT-02 / step 3 (module/folder boundaries; no duplication with software quality) | MR-07 … MR-12; ownership line in new `SKILL.md` step 6 |
| MAINT-03 / step 5 (prerequisites, env vars, build/run steps) | MR-13 … MR-16 (build/run commands: MR-03) |
| MAINT-04 / step 4 (TODO/FIXME/HACK markers) | MR-17 … MR-19 |
| MAINT-05 / step 4 (deprecated-but-still-used code) | MR-20 … MR-23 |
| New, plan DEC-2: MAINT-06 contributing guide | MR-24 … MR-26 |
| New, plan DEC-2: MAINT-07 change history | MR-27 … MR-29 |
| New, plan DEC-2: MAINT-08 architecture and decisions | MR-30 … MR-32 |
| New, plan DEC-2: MAINT-09 docs in sync with code | MR-33 … MR-36 |
| New, afterplanning WP-12d: MAINT-10 license and code of conduct | MR-37 … MR-39 |
