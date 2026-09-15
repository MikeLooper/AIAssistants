---
name: northwind-exercises
description: Manage the Northwind exercise catalog and execution scope. Use when running, interpreting, or reporting on Northwind exercise parts; read the matching reference file for the exact exercise requirements and track credits used per exercise.
---

# Northwind Exercises

The exact requirements are split by part under `references/`:

- [Part 1](references/part-1.md)
- [Part 2](references/part-2.md)
- [Part 3](references/part-3.md)
- [Part 4](references/part-4.md)

## Use

1. Read the reference file for every requested part before querying data.
2. Preserve the exercise numbering and wording in the reference file when naming report sections.
3. Run exercises in numerical order within each requested part.
4. Track the credits consumed by each exercise from the available tool or run usage data. If usage is unavailable, record `Unavailable` rather than estimating.
5. After all requested parts finish, write a separate cost summary in `docs/` named:
   `northwind-exercise-cost-summary-<yyyyMMdd>-<HHmmss>.md`
6. Use one timestamp captured from the local system clock for that cost-summary file. Include the timestamp, requested parts, and one row per exercise with its part/exercise number, credits used, and a short status. End with an overall credits total. Sum only numeric credit values; do not treat unavailable values as zero.

The cost summary is separate from the per-part result reports. It must not replace or be appended to a part report.
