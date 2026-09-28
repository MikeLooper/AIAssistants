# Checklist — Software Quality

Merged from the former `review-software-quality`, `review-design-patterns` and `review-architecture-patterns` skills. `DP-03` ("no God object/class") was dropped as a duplicate of `SQ-04`; keep evidence for that check under `SQ-04` going forward.

## Sub-subject: Software Quality

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| SQ-01 | Functions/methods stay reasonably short and single-purpose (no god-functions) | Warning | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability |
| SQ-02 | Cyclomatic complexity is kept low; deeply nested conditionals are refactored | Warning | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability |
| SQ-03 | No significant duplicated code blocks across the reviewed files | Warning | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability |
| SQ-04 | Classes/modules have a single, clear responsibility (no god-classes/god-objects) | Warning | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability |
| SQ-05 | Parameter lists are short; related parameters are grouped into objects/records | Information | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability |
| SQ-06 | Error paths are handled, not silently swallowed (functional suitability/reliability) | Error | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#reliability |
| SQ-07 | Naming is descriptive and consistent (usability of the code itself) | Information | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability |
| SQ-08 | No obvious dead code or commented-out blocks left in place | Information | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability |

## Sub-subject: Design Patterns

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| DP-01 | No singleton used for shared mutable state across requests (in server contexts) | Warning | fallback rubric |
| DP-02 | Inheritance depth is shallow; composition preferred over deep inheritance chains | Information | fallback rubric |
| DP-04 | Patterns applied match an actual recurring problem (no needless indirection) | Information | fallback rubric |
| DP-05 | Factory/builder patterns are used consistently where object construction is complex | Information | fallback rubric |
| DP-06 | Observer/event patterns don't leak subscriptions (no missing unsubscribe/dispose) | Warning | fallback rubric |

## Sub-subject: Architecture Patterns

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| AP-01 | Presentation/API layer does not access the database directly, bypassing business/data layers | Warning | https://learn.microsoft.com/azure/architecture/patterns/ |
| AP-02 | Business logic is not embedded in controllers/handlers; it lives in a dedicated layer | Warning | https://learn.microsoft.com/azure/architecture/patterns/ |
| AP-03 | No circular dependencies between modules/projects | Warning | fallback rubric |
| AP-04 | Modules have high cohesion (related functionality grouped together) | Information | fallback rubric |
| AP-05 | Cloud design patterns (retry, circuit breaker, cache-aside, queue-based leveling) are used where the architecture needs resilience/scale | Information | https://learn.microsoft.com/azure/architecture/patterns/ |
| AP-06 | Cross-cutting concerns (logging, auth, validation) are centralized, not duplicated per module | Warning | fallback rubric |

