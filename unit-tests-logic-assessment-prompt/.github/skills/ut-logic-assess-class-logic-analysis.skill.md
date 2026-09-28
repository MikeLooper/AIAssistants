# Skill: ut-logic-assess-class-logic-analysis

## Goal
Extract branch-level logic summaries for each class element.

## Inputs
- `Classes`
- `Class Elements`
- Source code AST or equivalent structural parse.

## Outputs
### Class Logic
Each record must contain:
- `Code class name`
- `Name of method or property`
- `Type of element` (`Method` or `Property`)
- `Logic branch summary`

## Branch Patterns to Capture
- `if/else` true and false paths.
- `switch/case`, `match/case`, and default paths.
- Guard clauses and early returns.
- Null/None checks.
- Exception paths (thrown/caught behavior branches).
- Loop outcome branches (zero iterations vs one-or-more where meaningful).

## Summary Style
- Use short, testable branch statements.
- Example: "returns validation error when input is null".
- Avoid implementation noise and line references.

## Quality Checks
- Every `Class Logic` row must map to an existing `Class Elements` row.
- Avoid duplicate branch summaries for the same element unless semantically distinct.
