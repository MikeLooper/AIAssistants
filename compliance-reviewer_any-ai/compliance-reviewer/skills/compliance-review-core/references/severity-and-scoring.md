# Severity and Scoring

## Wording-to-Severity Mapping

Use the source's own wording first:

| Wording | Severity |
|---------|----------|
| DO / MUST / REQUIRED / SHALL | Error |
| DO NOT / MUST NOT / SHALL NOT | Error |
| SHOULD / YOU SHOULD / RECOMMENDED | Warning |
| SHOULD NOT / YOU SHOULD NOT / NOT RECOMMENDED | Warning |
| MAY / YOU MAY / OPTIONAL | Information |

### Microsoft Azure API Guidelines (explicit mapping)

- `DO` items → **Error** if not implemented.
- `DO NOT` items → **Error** if violated.
- `YOU SHOULD` items → **Warning** if not implemented.
- `YOU SHOULD NOT` items → **Warning** if violated.
- `YOU MAY` items → **Information** if not implemented.

### Skills with localized standards

When a skill reviews against local standards elements (`references/standards/`), each `Finding.severity` comes from the failed element's level, using the table above, unless the skill's `SKILL.md` states its own severity rule (e.g. `review-cost-sustainability`, `review-disaster-recovery`, `review-monitoring`, `review-software-lifecycle`, `review-software-quality`, `review-testing` and `review-twelve-factor` use the check's default severity for every Finding). `checkResults.severityIfFailed` is always the check's default severity from the skill's `checklist.md`, so scoring stays stable from run to run.

## Fallback Rubric

For sources that don't use DO/SHOULD/MAY wording, assign severity by impact:

| Impact | Severity |
|--------|----------|
| An exploitable security flaw or a risk of data loss | Error |
| A gap against best practice | Warning |
| A stylistic or optional point | Information |

## Scoring Formula

```
score = (weighted checks passed) / (weighted checks that apply) * 100
```

- Weights: Error = 5, Warning = 2, Information = 1.
- A check result of **N/A** is excluded from both numerator and denominator.
- Compute one score per subject, then an overall score. The overall score is the weighted average of subject scores; when subjects have different total applicable weights, weight each subject's contribution by its own total applicable weight so subjects with more applicable checks aren't diluted.

## Rating Bands

| Score | Band |
|-------|------|
| 90–100 | Excellent |
| 75–89 | Good |
| 60–74 | Fair |
| Below 60 | Poor |

Apply the same bands to the overall score and to each subject score.

## Confidence and Effort Do Not Affect Scoring

Every `Finding` also carries `confidence` (High/Medium/Low) and `effort` (Small/Medium/Large), but neither term appears in the scoring formula above. Scoring is driven entirely by `checkResults` (pass/fail/N/A) and each check's severity weight. The two fields are used only downstream, in `compliance-report`'s aggregate step:

- `confidence` — orders (and can filter) the top-5-risks selection: prefer high-confidence Errors/Warnings over low-confidence ones of the same severity.
- `effort` — a tiebreaker for ordering the top-5-risks list, smallest effort first, so quick wins surface among equal-severity/confidence findings.

Do not weight a subject's or the overall score by confidence or effort. A Low-confidence failed check still counts as a full failure at its severity weight; if a worker isn't confident enough to call a check failed, it should mark the check `N/A` (excluded from scoring) with a reason, rather than reporting a low-confidence fail.
