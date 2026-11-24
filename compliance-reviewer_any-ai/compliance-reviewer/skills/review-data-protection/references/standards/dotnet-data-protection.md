# .NET data classification — localized summary

- Sources: learn.microsoft.com — "Data classification in .NET" (`ms.date` 2025-03-21)
- Localized: 2026-11-24 · Elements: learn.microsoft.com 2 (prefix `DND-`; counted in this skill's per-website budget)
- Applies when language `csharp` is detected and `Microsoft.Extensions.Compliance.*` is referenced, or when the files
  hold personal data and could use it (cite DND-01 in the recommendation only, then).
- Level: `SHOULD` for vendor recommendations; **(Default)** marks an element that states API behaviour. Levels are
  informational: every Finding takes its check's default severity. Redaction of logged data is judged by
  `review-security-operational` (SEC-OP-03), not here.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Pinned version | Source name for `Finding.standard` |
|-----|---------------|----------------|------------------------------------|
| mdc | https://learn.microsoft.com/dotnet/core/extensions/data-classification | ms.date 2025-03-21 | Microsoft Learn — Data classification in .NET |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| DND-01 | SHOULD | Label sensitive data with `DataClassification` values from a named taxonomy, applied through `DataClassificationAttribute` subclasses (or bound from configuration); use `DataClassification.None` or `Unknown` to state an explicit choice. | personal-data properties without classification attributes where `Microsoft.Extensions.Compliance` is referenced | DPR-08 | mdc#create-custom-classification-attributes, mdc#create-custom-classifications, mdc#bind-data-classification-settings |
| DND-02 | SHOULD | **(Default)** Classifications combined in a `DataClassificationSet` act as one classification (logical AND): redaction configured for the set doesn't apply to data classified with only one of its members. | redactor registered for a set while properties carry a single classification | DPR-08 | mdc#create-custom-classifications |
