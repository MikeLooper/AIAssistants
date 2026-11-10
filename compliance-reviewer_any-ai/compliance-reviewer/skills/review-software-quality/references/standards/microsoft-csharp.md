# Microsoft C# coding conventions and identifier names — localized summary

- Source site: learn.microsoft.com · Repo `dotnet/docs` (locale-less URLs) · pins per page below
- Citation base: https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/
- Localized: 2026-11-09 · Elements: 24 (learn.microsoft.com budget shared with `azure-architecture.md`: 44 of 100)
- Source name for `Finding.standard`: Microsoft C# conventions
- Level: informational only (the pages mix "Use"/"Do"/"Consider"); severity is the owning check's default.
- **Load only when C# is detected; apply only to `.cs` files.** A documented team convention (`.editorconfig`
  naming or formatting rules, `dotnet format`, StyleCop config) prevails over these defaults (SKILL.md).
- The `cc` page is written for docs samples; sample-only rules (65-character lines, `var` in samples) aren't
  localized.

| Key | Page path | Pin |
|-----|-----------|-----|
| cc | `coding-conventions` | ms.date 2025-01-15; commit 156931bb4ec1 (updated 2026-03-30) |
| in | `identifier-names` | ms.date 2025-10-10; commit 6b2c20688c8f (updated 2026-07-14) |

| ID | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-----------------------|--------------|-------|-----------|
| MSC-01 | PascalCase for types, namespaces, public (and protected) members, methods and local functions. | C# | CS-05 | in#pascal-case, in#naming-conventions |
| MSC-02 | Interfaces start with `I`. Attribute types end with `Attribute`. | C# | CS-05 | in#naming-conventions, in#pascal-case |
| MSC-03 | camelCase for parameters and locals. Private and internal non-constant fields use `_camelCase`, and private/internal statics `s_`/`t_` (or the convention in `.editorconfig` naming rules). | C# | CS-05 | in#camel-case, in#naming-conventions |
| MSC-04 | Constants (fields and locals, any access level) use PascalCase. | C# | CS-05 | in#naming-conventions |
| MSC-05 | Enums: singular noun for non-flags, plural for flags. No identifiers with two consecutive underscores. | C# | CS-05 | in#naming-conventions |
| MSC-06 | Names are meaningful and descriptive, with clarity over brevity: no non-standard abbreviations, and single letters only for simple loop counters. | C# | CS-01 | in#naming-conventions |
| MSC-07 | Generic type parameters are descriptive and prefixed with `T`, or a single `T` when self-explanatory. | C# generics | CS-05 | in#type-parameter-naming-guidelines |
| MSC-08 | Primary-constructor parameters: camelCase on classes and structs, PascalCase on records. | C# 12+ primary constructors | CS-05 | in#primary-constructor-parameters, cc#constructors-and-initialization |
| MSC-09 | Catch only exceptions that can be properly handled. Don't catch `System.Exception` without an exception filter. Use specific exception types for meaningful messages. | C# exception handling | SQ-06 | cc#language-guidelines |
| MSC-10 | Use async/await for I/O-bound work, and be deliberate about `ConfigureAwait` in library code. (Blocking on async results is PERF-02.) | C# async code | CS-05 | cc#language-guidelines |
| MSC-11 | Use language keywords (`string`, `int`, `nint`) instead of runtime type names, and `int` rather than unsigned types unless needed. | C# | CS-05 | cc#language-guidelines |
| MSC-12 | `var` only when the type is apparent from the right side (`new`, cast, literal). Explicit type in `foreach`. Never `var` in place of `dynamic`. | C# | CS-05 | cc#implicitly-typed-local-variables |
| MSC-13 | String interpolation for short concatenation, `StringBuilder` for appending in loops, raw string literals over escape sequences. | C# strings | CS-05 | cc#string-data |
| MSC-14 | Modern initialization: `required` properties, object initializers, target-typed `new()`, collection expressions. | C# 11+ | CS-05 | cc#constructors-and-initialization, cc#new-operator, cc#arrays-and-collections |
| MSC-15 | Use `Func<>`/`Action<>` instead of defining custom delegate types. | C# delegates | CS-05 | cc#delegates |
| MSC-16 | Use a `using` statement or declaration instead of `try`/`finally` whose only purpose is `Dispose`. (Locks and resources on security-relevant exception paths: SEC-OP-10.) | `IDisposable` in scope | CS-05 | cc#try-catch-and-using-statements-in-exception-handling |
| MSC-17 | Use `&&`/`\|\|` (short-circuit) instead of `&`/`\|` in boolean comparisons. | C# | CS-05 | cc#-and--operators |
| MSC-18 | Call static members through the declaring class name, never through a derived class. | C# | CS-05 | cc#static-members |
| MSC-19 | LINQ: meaningful query variable names, PascalCase anonymous-type properties, `where` before other clauses, multiple `from` instead of `join` for inner collections. | LINQ query syntax | CS-05 | cc#linq-queries |
| MSC-20 | File-scoped namespace declarations; `using` directives outside the namespace. | C# 10+ | CS-05 | cc#file-scoped-namespace-declarations, cc#place-the-using-directives-outside-the-namespace-declaration |
| MSC-21 | Layout: four-space indents with no tabs, Allman braces, one statement and one declaration per line, blank line between members, parentheses to make clauses apparent. | C# | CS-05 | cc#layout-conventions, cc#style-guidelines |
| MSC-22 | Comments: `//` on its own line, one space after the delimiter, starting with a capital letter and ending with a period. No `/* */` for long explanations. | C# comments | CS-05 | cc#comment-style |
| MSC-23 | XML documentation comments on methods, classes, fields and all public members. | public C# API | CS-04 | cc#comment-style |
| MSC-24 | Conventions are enforced by tooling: `.editorconfig` style and naming rules and code analysis. | C# project | CS-02 | cc#tools-and-analyzers |
