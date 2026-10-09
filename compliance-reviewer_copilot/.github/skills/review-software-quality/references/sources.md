# Sources — Software Quality

- ISO/IEC 25010 quality model: https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- Azure Architecture Center — Cloud Design Patterns (proposed source, for `AP-*` checks): https://learn.microsoft.com/azure/architecture/patterns/
- C#/.NET: https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions
- Java: https://google.github.io/styleguide/javaguide.html
- Python: https://peps.python.org/pep-0008/

Fetch the ISO 25010 page only if a citation anchor for a specific characteristic (e.g. maintainability, reliability) is needed beyond the checklist. The Azure Architecture Center link is a proposed source; confirm the user has accepted it for this run before fetching beyond the checklist.

No single authoritative URL was supplied for the Design Patterns (`DP-*`) checks. Use the fallback rubric in `compliance-review-core`'s `severity-and-scoring.md` for their severity. If the user approves a specific patterns reference (e.g. a Gang-of-Four summary or Refactoring.Guru) for a run, add it here and to the allowlist for that run only.

Generic coding-standards core checks (`CS-01`..`CS-04`) without a language use the fallback rubric in `compliance-review-core`'s `severity-and-scoring.md`.
