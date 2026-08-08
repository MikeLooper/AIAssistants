# Unit Test Logic Assessment Agent

This package defines a prompt-driven AI agent that evaluates unit tests based on code logic and element coverage, not line coverage.

## Scope
- Languages: C#, Java, Python
- Test frameworks: NUnit, JUnit, pytest/unittest
- Mapping mode: Strict explicit evidence by default
- Output mode: Markdown report by default

## Files
- `ut-logic-assess-agent.prompt.md`: Orchestrator prompt for the agent.
- `skills/ut-logic-assess-class-inventory.skill.md`: Build `Classes` and `Class Elements`.
- `skills/ut-logic-assess-class-logic-analysis.skill.md`: Build `Class Logic` branch summaries.
- `skills/ut-logic-assess-unit-test-inventory.skill.md`: Build `Unit Test Classes` and `Unit Test Elements`.
- `skills/ut-logic-assess-test-to-element-mapping.skill.md`: Produce tested/not-tested element sets and logic coverage sets.
- `skills/ut-logic-assess-coverage-metrics.skill.md`: Calculate required percentages.
- `skills/ut-logic-assess-reporting.skill.md`: Build standard and detailed reports.
- `skills/ut-logic-assess-quality-guardrails.skill.md`: Enforce read-only and quality constraints.
- `templates/invocation-template.md`: Copy/paste request templates with placeholders for repo path, report mode, and output file.
- `samples/standard-report.sample.md`: Example of expected standard report output.
- `samples/detailed-report.sample.md`: Example of expected detailed report output.

## Quick Start
1. Open `templates/invocation-template.md`.
2. Copy Template A (standard) or Template B (detailed).
3. Replace placeholders:
   - `{{PROJECT_ROOT}}`
   - `{{REPORT_PATH}}`
4. Send the filled prompt to your AI assistant.
5. Compare the output against sample files in `samples/`.

## Run Modes
1. Standard report:
   - Required sections only: `Untested Classes`, `Not Tested Class Elements`, `Logic Covered`, `Logic Not Covered`, Summary.
2. Detailed report:
   - Standard report plus: `Classes`, `Class Logic`, `Unit Test Classes`, `Unit Test Elements`, `Tested Class Elements`.

## Core Guardrail
- Do not modify any code class.

## Develoment

This agent and related skills are all prefixed with 'ut-logic-assess-' to allow these files to be copied into another repository and not conflict with any pre-existing files.
This prefix also ensures unique names for calling individual skills directly.
