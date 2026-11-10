# Microsoft .NET unit testing best practices — localized summary

- Source site: learn.microsoft.com · Version: `dotnet/core/testing/unit-testing-best-practices`, `ms.date` 2026-11-05,
  `git_commit_id` 3733dc918e2e037a94c719296e4d964cd460acf1 (retrieved 2026-11-09)
- Citation base: https://learn.microsoft.com/dotnet/core/testing/unit-testing-best-practices (locale-less)
- Localized: 2026-11-09 · Elements: 16 (cap 100)
- Source name for `Finding.standard`: Microsoft .NET unit testing best practices
- Level: informational only; severity is the owning check's default.
- **Applies to every language.** The page targets .NET, but the localized rules (naming, arrange/act/assert, no logic,
  one act, seams) are language-neutral. xUnit- and MSTest-specific notes are not localized.
- Anchors are the heading slugs. Citation: `Finding.url` = citation base + `#` + primary anchor, e.g.
  `https://learn.microsoft.com/dotnet/core/testing/unit-testing-best-practices#avoid-coding-logic-in-unit-tests`.

| Key | Page path | Pin |
|-----|-----------|-----|
| ut | (citation base) | `ms.date` 2026-11-05 @ 3733dc918e2e |

| ID | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-----------------------|--------------|-------|-----------|
| MSU-01 | Unit tests are fast (milliseconds each), so the whole unit suite can run on every change. | unit tests | TST-01 | ut#characteristics-of-good-unit-tests |
| MSU-02 | Unit tests are isolated: they have no dependency on outside factors such as the file system or a database. | unit tests | TST-05 | ut#characteristics-of-good-unit-tests |
| MSU-03 | Unit tests are repeatable: the same code gives the same result on every run. | unit tests | TST-05 | ut#characteristics-of-good-unit-tests |
| MSU-04 | Tests are self-checking. Pass or fail is decided automatically, with no human inspection of output. | any tests | TST-03 | ut#characteristics-of-good-unit-tests |
| MSU-05 | A coverage percentage doesn't measure quality, and overly ambitious coverage goals are counterproductive. | coverage threshold configured | TST-02 | ut#code-coverage-and-code-quality |
| MSU-06 | Fake, stub and mock are used correctly. A mock is asserted against and a stub isn't, and names say which is which. | unit tests with doubles | TST-04 | ut#unit-testing-terminology |
| MSU-07 | Unit tests have no infrastructure dependencies. Unit and integration tests live in separate projects or folders, so the unit project doesn't reference infrastructure packages. | unit tests | TST-01 | ut#avoid-infrastructure-dependencies |
| MSU-08 | Test names state the unit under test, the scenario and the expected behavior, using one consistent convention. | any tests | TST-08 | ut#follow-test-naming-standards |
| MSU-09 | Arrange, act and assert are visibly separated, and assertions aren't mixed into the act step. | any tests | TST-08 | ut#arrange-your-tests |
| MSU-10 | Test inputs are the simplest values that verify the behavior, with no extra properties or arbitrary values. | any tests | TST-08 | ut#write-minimally-passing-tests |
| MSU-11 | No unexplained "magic" literals. Meaningful values are named constants. | any tests | TST-08 | ut#avoid-magic-strings |
| MSU-12 | Test bodies contain no logic (`if`, loops, `switch`, string building). Parameterized tests are used instead. | any tests | TST-08 | ut#avoid-coding-logic-in-unit-tests |
| MSU-13 | Test-specific setup is visible in the test or a helper, and isn't hidden in a shared setup/teardown that tests don't all need. | any tests | TST-08 | ut#use-helper-methods-instead-of-setup-and-teardown |
| MSU-14 | Each test has a single act step. Multiple cases use separate or parameterized tests. | any tests | TST-08 | ut#avoid-multiple-act-tasks |
| MSU-15 | Private behavior is verified through the public method that uses it. | any tests | TST-03 | ut#validate-private-methods-with-public-methods |
| MSU-16 | Static dependencies such as the current time are reached through a seam (an interface or provider) so tests control them. | time or static dependencies | TST-05 | ut#handle-stub-static-references-with-seams |
