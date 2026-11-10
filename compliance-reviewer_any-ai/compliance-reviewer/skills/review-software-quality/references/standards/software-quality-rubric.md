# Compliance Reviewer Software Quality Rubric — local standard

- Source: authored in this repository (no external source; see `../sources.md`)
- Version: 1.1 · Created: 2026-11-09 (SQR-37 added the same day) · Elements: 37 (no website, no cap)
- Source name for `Finding.standard`: `Compliance Reviewer Software Quality Rubric`
- Citation base (relative to `docs/reports/`): `../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md` + `#sqr-NN`
- Level: informational only; severity always comes from the owning check (SKILL.md).
- "Smell" is this rubric's own name for the smell (common industry vocabulary, no source attribution). "—" means
  the element has no smell name.
- **Thresholds are triggers, not verdicts.** Fail only when the threshold is exceeded **and** reading the code
  confirms the smell (MFB-05). Counts are reading estimates: state the counted value in the evidence excerpt and use
  confidence `medium` unless the value is at least twice the threshold. An approved analyzer output (step `02`) may
  support a count but is never required.

## Thresholds

| Measure | Threshold | Element |
|---|---|---|
| Function length | > 60 logical lines (non-blank, non-comment), or > 30 with ≥ 2 distinct jobs | SQR-01 |
| Estimated cyclomatic complexity | > 15 | SQR-03 |
| Control-flow nesting | > 4 levels | SQR-04 |
| Duplicated block | ≥ 10 consecutive lines in ≥ 2 places | SQR-06 |
| Class or module size | > 500 lines, or > 20 public methods, or > 10 constructor dependencies | SQR-08 |
| Parameters | > 5 (constructor injection excluded) | SQR-11 |
| Inheritance depth | > 3 project-defined levels | SQR-21 |

## Elements

| ID | Smell | Criterion (fail when …) | Applies when | Check | ISO |
|----|-------|-------------------------|--------------|-------|-----|
| <a id="sqr-01"></a>SQR-01 | Long Function | A function or method body exceeds 60 logical lines (non-blank, non-comment), or exceeds 30 and does ≥ 2 distinct jobs. Confirm by reading. | any function | SQ-01 | ISO-29 |
| <a id="sqr-02"></a>SQR-02 | — | One function mixes abstraction levels: I/O or framework calls, parsing/mapping and business rules interleaved in one body. | any function > 20 lines | SQ-01 | ISO-30 |
| <a id="sqr-03"></a>SQR-03 | — | Estimated cyclomatic complexity > 15 (1 + each `if`, `else if`, `case`, loop, `catch`, `&&`, `\|\|`, `?:`, `??`, comprehension `if`). | any function | SQ-02 | ISO-29 |
| <a id="sqr-04"></a>SQR-04 | — | Control-flow nesting deeper than 4 levels. | any function | SQ-02 | ISO-29 |
| <a id="sqr-05"></a>SQR-05 | — | A condition with > 3 boolean operands, or a negated compound condition, is written inline and unnamed in a branch. | any branch | SQ-02 | ISO-29 |
| <a id="sqr-06"></a>SQR-06 | Duplicated Code | ≥ 10 consecutive lines that are identical apart from identifiers or literals appear in ≥ 2 places in the reviewed files. | ≥ 2 reviewed files or functions | SQ-03 | ISO-30 |
| <a id="sqr-07"></a>SQR-07 | Repeated Switches | The same `switch`/`if` chain on the same type code or discriminator appears in ≥ 3 places. | type-code branching | SQ-03 | ISO-30 |
| <a id="sqr-08"></a>SQR-08 | Large Class | A class or module > 500 lines, or > 20 public methods, or > 10 constructor-injected dependencies. Confirm by reading. | any class/module | SQ-04 | ISO-27 |
| <a id="sqr-09"></a>SQR-09 | Divergent Change | One class owns unrelated responsibilities (e.g. `*Manager`/`*Helper`/`*Utils` mixing persistence, formatting and business rules). | any class | SQ-04 | ISO-27 |
| <a id="sqr-10"></a>SQR-10 | Feature Envy | A method uses another object's data and methods more than its own, so the behavior belongs elsewhere. | any method | SQ-04 | ISO-27 |
| <a id="sqr-11"></a>SQR-11 | Long Parameter List | More than 5 parameters (excluding constructor dependency injection, which SQR-08 covers). | any function | SQ-05 | ISO-29 |
| <a id="sqr-12"></a>SQR-12 | Data Clumps | The same group of ≥ 3 parameters or fields recurs together in ≥ 2 signatures or classes. | ≥ 2 signatures | SQ-05 | ISO-30 |
| <a id="sqr-13"></a>SQR-13 | Flag Argument | A boolean or enum argument only selects which behavior the function performs. | any function | SQ-05 | ISO-29 |
| <a id="sqr-14"></a>SQR-14 | — | A catch-all (`catch (Exception)`, `catch (Throwable)`, `except Exception`) appears below a process or request boundary without translating, rethrowing or a documented reason. (Empty or unlogged catches are SEC-OP-02.) | exception handling present | SQ-06 | ISO-19 |
| <a id="sqr-15"></a>SQR-15 | — | Exceptions are used for normal control flow, e.g. thrown and caught in the same method to break a loop, or to test existence. | exception handling present | SQ-06 | ISO-29 |
| <a id="sqr-16"></a>SQR-16 | — | Thrown exceptions are generic (`Exception`, `RuntimeException`, bare `raise Exception("…")`) where a specific built-in or domain type exists. | code throws | SQ-06 | ISO-29 |
| <a id="sqr-17"></a>SQR-17 | Dead Code | Unreachable code, private members never referenced in the reviewed files, or parameters never read. (Reachable superseded code is MAINT-05.) | any file | SQ-08 | ISO-29 |
| <a id="sqr-18"></a>SQR-18 | — | A block of ≥ 3 consecutive commented-out code lines. | any file | SQ-08 | ISO-29 |
| <a id="sqr-19"></a>SQR-19 | Global Data | A singleton, static field or module-level global holds per-request or per-user mutable state in a server context (web handlers, workers). | server code | DP-01 | ISO-02 |
| <a id="sqr-20"></a>SQR-20 | Mutable Data | Shared static or singleton mutable state is changed from concurrent code without synchronization or a concurrent collection. | concurrent code | DP-01 | ISO-17 |
| <a id="sqr-21"></a>SQR-21 | — | An inheritance chain of > 3 project-defined levels (framework base classes not counted). | class hierarchies | DP-02 | ISO-30 |
| <a id="sqr-22"></a>SQR-22 | Refused Bequest | A subclass overrides inherited members to throw "not supported" or do nothing, or uses only a small part of its base. | class hierarchies | DP-02 | ISO-30 |
| <a id="sqr-23"></a>SQR-23 | Middle Man / Speculative Generality | A pass-through class whose methods mostly delegate unchanged, or an abstraction with one implementation and no use as a test, DI or plugin seam. | abstractions present | DP-04 | ISO-29 |
| <a id="sqr-24"></a>SQR-24 | — | A type is named for a pattern it doesn't implement, or implements one without the varying problem (a "Factory" that only calls `new` with no choice, a "Strategy" with one strategy and no seam). | pattern names present | DP-04 | ISO-29 |
| <a id="sqr-25"></a>SQR-25 | — | Complex construction (≥ 4 optional settings or a multi-step setup) is repeated at ≥ 2 call sites instead of a factory, builder or options object. | complex construction | DP-05 | ISO-30 |
| <a id="sqr-26"></a>SQR-26 | — | A subscription to a longer-lived publisher (`+=` events, `addListener`, observables, signal handlers) is never removed or disposed. | event subscriptions | DP-06 | ISO-17 |
| <a id="sqr-27"></a>SQR-27 | — | Presentation or API code (controllers, handlers, views, endpoints) directly uses data-access primitives (`DbContext`/`DbSet`, `EntityManager`, JDBC `Connection`, SQLAlchemy `Session`, raw SQL) instead of the business or data layer, in a codebase that has such a layer. | layered code | AP-01 | ISO-27 |
| <a id="sqr-28"></a>SQR-28 | — | Business rules (validation beyond request shape, calculations, state transitions) live in controllers or handlers and aren't reused through the domain layer. | layered code | AP-02 | ISO-27 |
| <a id="sqr-29"></a>SQR-29 | — | A dependency cycle among reviewed projects, packages or modules (project references, `import` chains), or a lower layer importing a higher one. | ≥ 2 modules | AP-03 | ISO-27 |
| <a id="sqr-30"></a>SQR-30 | Shotgun Surgery | One change would have to touch many unrelated modules, or one module mixes unrelated domain areas. (Repository-level layout is MAINT-02.) | ≥ 2 modules | AP-04 | ISO-27 |
| <a id="sqr-31"></a>SQR-31 | — | The same cross-cutting code (auth checks, logging scaffolding, input validation, error mapping) is repeated in ≥ 3 handlers instead of middleware, filters, decorators or aspects. | ≥ 3 handlers | AP-06 | ISO-30 |
| <a id="sqr-32"></a>SQR-32 | Mysterious Name | Names don't reveal intent: single letters outside loops and lambdas, misleading or type-encoded names, meaningless abbreviations, inconsistent terms for one concept. | any code | CS-01 | ISO-29 |
| <a id="sqr-33"></a>SQR-33 | — | Formatting (indentation, braces, spacing, line breaks) is inconsistent within the reviewed files, and no formatter or `.editorconfig` configuration enforces it. | any code | CS-02 | ISO-29 |
| <a id="sqr-34"></a>SQR-34 | Comments | Comments restate the code, are stale or contradict it, or explain *what* where a better name would do. Missing *why* on non-obvious decisions. (TODO/FIXME tracking is MAINT-04.) | comments present | CS-03 | ISO-29 |
| <a id="sqr-35"></a>SQR-35 | — | Exported or public functions, classes and modules lack documentation comments (generic rule for languages without a localized guide). | language not C#/Java/Python | CS-04 | ISO-29 |
| <a id="sqr-36"></a>SQR-36 | — | Static checking that the project has adopted isn't applied consistently: C# `<Nullable>enable</Nullable>` with nullable warnings suppressed or ignored; a Python type checker configured (mypy/pyright) but public signatures unannotated; Java nullness annotations used inconsistently. | the project opts in (config present) | CS-05 | ISO-30 |
| <a id="sqr-37"></a>SQR-37 | — | Multi-step business workflows (checkout, approval, onboarding) don't validate state transitions on the server: no state machine or equivalent guard, so steps can be skipped, repeated or reordered by calling endpoints directly, or sequencing is left to the front end. Reference: OWASP REST Security Cheat Sheet `#preventing-out-of-order-api-execution` (@97cb8a3c). | multi-step workflow exposed through separate endpoints or handlers | AP-02 | ISO-22 |
