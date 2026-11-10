---
paths:
  - "test/**/*.cs"
---

# Tests

Full rules: `.github/instructions/unit-tests.instructions.md`. Key points:
- NUnit. Each code project `X` has an `X.Tests` project whose folder tree mirrors the source tree, with one test class per code class.
- Test classes derive from `TestBase` (`PilotApi.TestingShared`). One class per file, Arrange/Act/Assert, no class-level fields, no underscore-prefixed variables.
- Method names: `<ClassUnderTest>_<MethodOrProperty>_<ExpectedResult>_Test`.
- Doubles go in `Testing/Doubles`, helpers in `Testing/Utilities`, loaded files in `Testing/Resources`. Repository tests reach protected members through the `*RepositorySpy` doubles (`RepositoryDoublesUtilities`).
- When writing tests, don't change production classes to make tests pass.

`PilotApi.Integration.Tests` uses `WebApplicationFactory` plus fake ADO.NET doubles (`FakeDb*`, `TestableDataSourceContext`), so it needs no database. `OpenApiIntegrationTests` diffs the generated OpenAPI document against `shared/PilotSharedSource/OpenAPI/PilotApi_v1.yaml`.

`PilotApi.Architecture.Tests` (ArchUnitNET) enforces naming and layering rules, including which controller members count as endpoints that require authorization (property accessors are excluded). Run it after adding controllers, public controller members, or new types.
