# Skill: ut-logic-assess-quality-guardrails

## Goal
Enforce correctness, safety, and reproducibility constraints.

## Guardrails
- Do not modify any code class.
- Perform read-only analysis of code and tests.
- Prefer explicit evidence over heuristic assumptions.
- Surface uncertain mappings instead of silently counting them as covered.

## Best Practices
- Normalize names and signatures before comparisons.
- De-duplicate records using stable identities.
- Keep a short rationale for each ambiguous mapping decision.
- Separate discovery errors from coverage outcomes.
- If parsing fails for a file, report file and reason in a diagnostics appendix.

## Validation Checklist
1. All 10 required lists were produced.
2. Every list contains required attributes.
3. All four required metrics were computed.
4. Standard or detailed sections match request mode.
5. No write operations were performed on code classes.

## Failure Policy
- If critical discovery fails, return partial report with `Assessment Incomplete` note and enumerate missing artifacts.
