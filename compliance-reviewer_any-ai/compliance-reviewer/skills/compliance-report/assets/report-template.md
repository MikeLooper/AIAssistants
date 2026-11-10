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
1. **[{{severity}}] {{title}}** — {{where}} ({{file}}). {{recommendation}} {{cite}}
{{/topRisks}}

## 2. Things Done Well

{{#strengthsBySubject}}
### {{subject}}

{{#strengths}}
- {{#tag}}[{{tag}}] {{/tag}}{{title}} — {{file}}
{{/strengths}}

{{/strengthsBySubject}}

## 3. Recommended Improvements

### Errors

{{#errorFindings}}
- **{{title}}** — {{where}} ({{file}}, lines {{lineStart}}-{{lineEnd}}). {{recommendation}} {{cite}}
{{/errorFindings}}

### Warnings

{{#warningFindings}}
- **{{title}}** — {{where}} ({{file}}, lines {{lineStart}}-{{lineEnd}}). {{recommendation}} {{cite}}
{{/warningFindings}}

### Information

{{#infoFindings}}
- **{{title}}** — {{where}} ({{file}}, lines {{lineStart}}-{{lineEnd}}). {{recommendation}} {{cite}}
{{/infoFindings}}

## 4. Full Results

{{#subjects}}
### {{name}}

{{#subSubjects}}
{{#heading}}
#### {{heading}}

{{/heading}}
| Check | Result | Evidence |
|-------|--------|----------|
{{#checks}}
| {{checkId}} | {{result}} | {{evidenceOrReason}} |
{{/checks}}

{{/subSubjects}}

{{/subjects}}

## 5. Appendix

- **Run:** `{{runId}}` · Target: `{{targetPath}}` · Git HEAD: `{{targetGitHead}}`
- **Started:** {{startedAt}} · **Completed:** {{completedAt}}
- **Run flags:** {{runFlags}}
- **Subjects skipped:** {{skippedSubjects}}
- **URLs fetched:** {{urlsFetched}}
- **Link approvals:** {{linkApprovals}}
