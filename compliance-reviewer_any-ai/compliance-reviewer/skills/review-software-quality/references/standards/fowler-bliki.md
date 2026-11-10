# Martin Fowler bliki — localized summary

- Source site: martinfowler.com · Version: articles as dated below
- Citation base: https://martinfowler.com/bliki/
- Localized: 2026-11-09 · Elements: 6 (cap 100)
- Source name for `Finding.standard`: Martin Fowler bliki
- Level: informational only; severity is the owning check's default.
- Anchors: the pages have no section anchors. Cite the page URL.

| Key | Page path | Pin |
|-----|-----------|-----|
| cs | `CodeSmell.html` | 2006-02-09 |
| pdd | `PresentationDomainDataLayering.html` | 2015-08-26 |

| ID | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-----------------------|--------------|-------|-----------|
| MFB-01 | Presentation, domain logic and data access are separated, and dependencies run presentation → domain → data, never upwards. | layered code | AP-01 | pdd |
| MFB-02 | Validations and calculations belong in the domain layer, not in UI or controller code (which is also harder to test). | layered code | AP-02 | pdd |
| MFB-03 | The domain treats data sources as abstractions. The data layer converts storage formats, optionally through a mapper so the domain doesn't depend on storage. | layered code | AP-02 | pdd |
| MFB-04 | When a layer grows too large, the top level is split into domain-oriented modules, each layered internally. | ≥ 2 modules | AP-04 | pdd |
| MFB-05 | A code smell is a quickly spotted indication of a deeper problem that needs investigation. It isn't always a problem (the basis of the threshold-plus-confirmation rule). | any SQ-01 finding | SQ-01 | cs |
| MFB-06 | A data class with no behavior, whose logic lives in other classes, is a smell. Ask what behavior should move into it. (DTOs and records at boundaries are exempt.) | domain-layer classes | SQ-04 | cs |
