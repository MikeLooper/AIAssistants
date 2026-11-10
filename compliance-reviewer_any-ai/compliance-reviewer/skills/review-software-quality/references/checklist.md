# Checklist — Software Quality

Subject: Software Quality

Elements are defined in `standards/` (SQR in `software-quality-rubric.md`; AAS in `azure-architecture.md`; MFB in
`fowler-bliki.md`; FRC in `fowler-refactoring-catalog.md` (remedies only); MSC in `microsoft-csharp.md`; GJS in
`google-java-style.md`; PEP in `python-peps.md`). ISO elements classify findings and belong to no check.
Language elements (MSC, GJS, PEP) apply only when that language is detected, and only to its files.

Retired — don't evaluate or write to `checkResults`, never reuse: DP-03 (→ SQ-04), SQ-07 (→ CS-01), AP-05
(→ review-reliability / review-performance), CS-CS-01…05, CS-JV-01…05, CS-PY-01…05 (→ language elements under
CS-05, CS-04 and SQ-06; retired 2026-11-09).

| id | Sub-subject | Check | Default severity | Elements (remedies) |
|----|-------------|-------|------------------|---------------------|
| SQ-01 | Software Quality | Functions are short and single-purpose (no Long Function, no mixed abstraction levels) | Warning | SQR-01, SQR-02, MFB-05 (FRC-01, FRC-02) |
| SQ-02 | Software Quality | Complexity is kept low: no high estimated cyclomatic complexity, deep nesting or unnamed compound conditions | Warning | SQR-03, SQR-04, SQR-05 (FRC-03, FRC-04, FRC-05) |
| SQ-03 | Software Quality | No significant duplicated code or repeated switches across the reviewed files | Warning | SQR-06, SQR-07 (FRC-06, FRC-07, FRC-08) |
| SQ-04 | Software Quality | Classes and modules have one clear responsibility (no Large Class, divergent responsibilities, Feature Envy or behaviorless data classes in the domain) | Warning | SQR-08, SQR-09, SQR-10, MFB-06 (FRC-09, FRC-10) |
| SQ-05 | Software Quality | Parameter lists are short; related parameters are grouped; no flag arguments | Information | SQR-11, SQR-12, SQR-13 (FRC-11, FRC-12, FRC-13) |
| SQ-06 | Software Quality | Exceptions are designed at the right granularity: specific types caught and thrown, catch-alls only at boundaries, no exceptions as control flow (swallowed errors: SEC-OP-02) | Warning | SQR-14, SQR-15, SQR-16, MSC-09, PEP-18, GTS-20, GTS-21 (FRC-14) |
| SQ-07 | — | *(retired 2026-11-09: folded into CS-01; ID not reused)* | — | — |
| SQ-08 | Software Quality | No dead code (unreachable, unused private members or parameters) and no commented-out code blocks | Information | SQR-17, SQR-18 (FRC-15) |
| DP-01 | Design Patterns | No singleton, static or global holds per-request or unsynchronized shared mutable state (scale-out bottlenecks: PERF-08) | Warning | SQR-19, SQR-20 (FRC-16) |
| DP-02 | Design Patterns | Inheritance is shallow, with composition preferred; no Refused Bequest | Information | SQR-21, SQR-22 (FRC-17, FRC-18) |
| DP-03 | — | *(retired 2026-11-09: folded into SQ-04; ID not reused)* | — | — |
| DP-04 | Design Patterns | Patterns and abstractions match a real problem (no Middle Man, speculative abstraction, misnamed patterns or pass-through CRUD tiers) | Information | SQR-23, SQR-24, AAS-04 (FRC-19, FRC-20) |
| DP-05 | Design Patterns | Complex construction goes through a factory, builder or options object instead of being repeated | Information | SQR-25 (FRC-21) |
| DP-06 | Design Patterns | Observer and event subscriptions to longer-lived publishers are removed or disposed | Warning | SQR-26 |
| AP-01 | Architecture Patterns | The presentation/API layer doesn't bypass business and data layers to reach data access; dependencies run downwards | Warning | SQR-27, AAS-02, AAS-03, MFB-01 |
| AP-02 | Architecture Patterns | Business rules live in the domain layer, not in controllers, handlers or gateways, and domain logic is kept apart from infrastructure; multi-step workflows guard their state transitions on the server | Warning | SQR-28, SQR-37, AAS-10, AAS-18, AAS-19, MFB-02, MFB-03 |
| AP-03 | Architecture Patterns | No circular dependencies between modules or projects, and no lower layer depending on a higher one | Warning | SQR-29, AAS-01 |
| AP-04 | Architecture Patterns | Modules are cohesive and loosely coupled (no Shotgun Surgery, ball of mud, monolithic front end or worker, or chatty coupling) | Information | SQR-30, AAS-06, AAS-16, AAS-17, AAS-20, MFB-04 |
| AP-05 | — | *(retired 2026-11-09: cloud resilience and caching patterns, owned by review-reliability REL-02/REL-04 and review-performance; ID not reused)* | — | — |
| AP-06 | Architecture Patterns | Cross-cutting concerns (auth checks, logging scaffolding, validation, error mapping) are centralized, not repeated per handler or service | Warning | SQR-31, AAS-12, AAS-13, AAS-14 |
| AP-07 | Architecture Patterns | With ≥ 2 deployable units, the code respects its architecture style's constraints: services own their data, no shared domain libraries or schemas, front end and worker coupled only via the queue, no DB entities as events or payloads | Warning | AAS-05, AAS-07, AAS-08, AAS-09, AAS-11, AAS-15 |
| CS-01 | Coding Standards | Names are descriptive, intention-revealing and consistent across the codebase | Information | SQR-32, MSC-06 (FRC-22, FRC-23) |
| CS-02 | Coding Standards | Formatting is consistent, or enforced by formatter, analyzer or `.editorconfig` configuration | Information | SQR-33, MSC-24 |
| CS-03 | Coding Standards | Comments explain *why*, are current, and don't restate the code (commented-out code: SQ-08) | Information | SQR-34 |
| CS-04 | Coding Standards | Public APIs (exported functions, classes, modules) have well-formed documentation comments | Information | SQR-35, MSC-23, GJS-33, GJS-34, PEP-21, PEP-22, PEP-23, GTS-22 |
| CS-05 | Coding Standards | Code follows the applicable language style guide, or the documented team convention, and applies adopted static checking consistently | Warning | SQR-36; MSC-01 … MSC-05, MSC-07, MSC-08, MSC-10 … MSC-22; GJS-01 … GJS-32; PEP-01 … PEP-17, PEP-19, PEP-20; GTS-01 … GTS-19, GTS-23 |
| CS-CS-01…05 | — | *(retired 2026-11-09: C# language checks, now language elements under CS-05, CS-04 and SQ-06; IDs not reused)* | — | — |
| CS-JV-01…05 | — | *(retired 2026-11-09: Java language checks, now language elements under CS-05, CS-04 and SQ-06; IDs not reused)* | — | — |
| CS-PY-01…05 | — | *(retired 2026-11-09: Python language checks, now language elements under CS-05, CS-04 and SQ-06; IDs not reused)* | — | — |

23 active checks (SQ 7, DP 5, AP 6, CS 5). 143 scored elements, 23 remedy elements (FRC) and 40 classification
elements (ISO).
