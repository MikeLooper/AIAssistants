# Invocation Template (Ready To Run)

Use one of the templates below in your AI assistant chat.
Replace placeholder values before sending.

## Variables
- `{{PROJECT_ROOT}}`: Absolute or workspace-relative repository path to assess.
- `{{DETAIL_LEVEL}}`: `standard` or `detailed`.
- `{{REPORT_PATH}}`: Markdown output file path for the report.

## Template A: Standard Report

```text
Run the Unit Test Logic Assessment agent with these settings:
- project_root: {{PROJECT_ROOT}}
- languages: ["csharp", "java", "python"]
- frameworks: ["nunit", "junit", "pytest", "unittest"]
- mapping_mode: "strict"
- detail_level: "standard"
- include_confidence_notes: true

Execution requirements:
1. Analyze in read-only mode.
2. Do not modify any code class.
3. Generate the standard report with these sections only:
   - Untested Classes
   - Not Tested Class Elements
   - Logic Covered
   - Logic Not Covered
   - Summary (Untested Class Percent, Untested Element Percent per class, Overall Untested Elements Percent, Logic Not Covered Percent per class)
4. Save the final Markdown report to: {{REPORT_PATH}}
5. If a metric denominator is zero, output N/A with a one-line reason.
```

## Template B: Detailed Report

```text
Run the Unit Test Logic Assessment agent with these settings:
- project_root: {{PROJECT_ROOT}}
- languages: ["csharp", "java", "python"]
- frameworks: ["nunit", "junit", "pytest", "unittest"]
- mapping_mode: "strict"
- detail_level: "detailed"
- include_confidence_notes: true

Execution requirements:
1. Analyze in read-only mode.
2. Do not modify any code class.
3. Generate the standard sections plus detailed sections.
4. Standard sections:
   - Untested Classes
   - Not Tested Class Elements
   - Logic Covered
   - Logic Not Covered
   - Summary
5. Additional detailed sections:
   - Classes
   - Class Logic
   - Unit Test Classes
   - Unit Test Elements
   - Tested Class Elements
6. Save the final Markdown report to: {{REPORT_PATH}}
7. If a metric denominator is zero, output N/A with a one-line reason.
```

## Example Filled Values

### Example 1 (Standard)
- `{{PROJECT_ROOT}}` = `c:/Working/Storage/Dev/GitHub/MyRepo`
- `{{DETAIL_LEVEL}}` = `standard`
- `{{REPORT_PATH}}` = `c:/Working/Storage/Dev/GitHub/MyRepo/reports/unit-test-logic-standard.md`

### Example 2 (Detailed)
- `{{PROJECT_ROOT}}` = `c:/Working/Storage/Dev/GitHub/MyRepo`
- `{{DETAIL_LEVEL}}` = `detailed`
- `{{REPORT_PATH}}` = `c:/Working/Storage/Dev/GitHub/MyRepo/reports/unit-test-logic-detailed.md`

## Optional Follow-Up Prompt

```text
Re-run the assessment and include a diagnostics appendix listing:
- files skipped,
- unresolved test-to-element mappings,
- and low-confidence branch mappings with reasons.
```
