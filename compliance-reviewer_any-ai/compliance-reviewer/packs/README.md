# Review packs (generated)

Each `*.md` file here except this README is generated. Don't edit one by hand.

- `<skill>.md`: everything a worker needs for one `review-*` skill, in one file. It holds `SKILL.md`, `references/checklist.md`, the skill's other reference files and its language-neutral standards, without citation metadata.
- `<skill>.<language>.md`: the language-specific part (`references/languages/<language>.md` plus the standards files that load only for that language).

The worker's dispatch payload lists the packs to read for each subject, so a worker reads one or two files per skill instead of four to seven. The source files under `compliance-reviewer/skills/` stay the source of truth.

```
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py packs build [skill ...]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py packs check [skill ...]
```

`labels` runs the same check: it fails while any pack differs from what `build` would produce now. See `compliance-reviewer/skills/compliance-report/SKILL.md`, section "Review packs".
