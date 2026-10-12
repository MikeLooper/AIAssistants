# Language Guidance — C#/.NET

Reference: https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions

| id | Check | Default severity |
|----|-------|-------------------|
| CS-CS-01 | PascalCase for types/methods/properties, camelCase for locals/parameters, `_camelCase` for private fields (per team convention if documented) | Warning |
| CS-CS-02 | `var` used where the type is apparent; explicit types where it improves clarity | Information |
| CS-CS-03 | `async`/`await` used consistently; no `.Result`/`.Wait()` blocking on async code | Warning |
| CS-CS-04 | `IDisposable` resources are wrapped in `using`/`using` declarations | Warning |
| CS-CS-05 | Nullable reference types are enabled and warnings addressed, where the project targets a version that supports them | Information |
