# {{targetName}} — Compliance Review

_Generated {{generatedAt}} · Run `{{runId}}`_

## 1. Summary

**Overall score: {{overallScore}}/100 — {{overallBand}}**

| Subject | Score | Band |
|---------|-------|------|
{{#subjectScores}}
| {{subject}} | {{score}}/100 | {{band}} |
{{/subjectScores}}

**Findings by severity:** Error: {{errorCount}} · Warning: {{warningCount}} · Information: {{infoCount}}

### Top 5 Risks

{{#topRisks}}
1. **[{{severity}}] {{title}}** — {{subject}} ({{file}}). {{recommendation}} [{{standard}}]({{url}})
{{/topRisks}}

## 2. Things Done Well

{{#strengthsBySubject}}
### {{subject}}

{{#strengths}}
- {{title}} — {{file}}
{{/strengths}}

{{/strengthsBySubject}}

## 3. Recommended Improvements

### Errors

{{#errorFindings}}
- **{{title}}** — {{subject}} ({{file}}, lines {{lineStart}}-{{lineEnd}}). {{recommendation}} [{{standard}}]({{url}})
{{/errorFindings}}

### Warnings

{{#warningFindings}}
- **{{title}}** — {{subject}} ({{file}}, lines {{lineStart}}-{{lineEnd}}). {{recommendation}} [{{standard}}]({{url}})
{{/warningFindings}}

### Information

{{#infoFindings}}
- **{{title}}** — {{subject}} ({{file}}, lines {{lineStart}}-{{lineEnd}}). {{recommendation}} [{{standard}}]({{url}})
{{/infoFindings}}

## 4. Full Results

{{#subjects}}
### {{name}}

| Check | Result | Evidence |
|-------|--------|----------|
{{#checks}}
| {{checkId}} | {{result}} | {{evidenceOrReason}} |
{{/checks}}

{{/subjects}}

## 5. Appendix

- **Run:** `{{runId}}` · Target: `{{targetPath}}` · Git HEAD: `{{targetGitHead}}`
- **Started:** {{startedAt}} · **Completed:** {{completedAt}}
- **Subjects skipped:** {{skippedSubjects}}
- **URLs fetched:** {{urlsFetched}}
- **Link approvals:** {{linkApprovals}}
