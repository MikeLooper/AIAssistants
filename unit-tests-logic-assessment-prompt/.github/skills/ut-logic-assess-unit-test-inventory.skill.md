# Skill: ut-logic-assess-unit-test-inventory

## Goal
Identify unit test classes, their related code classes, and test methods mapped to targeted code elements.

## Inputs
- Test files for NUnit, JUnit, pytest/unittest.
- `Classes`
- `Class Elements`

## Outputs
### Unit Test Classes
Each record must contain:
- `Unit test class name`
- `Code class name`

### Unit Test Elements
Each record must contain:
- `Unit test class name`
- `Related code class name`
- `Name of test method`
- `Name of code class method or property that is being tested by the test method`

## Detection Rules
- NUnit: `[Test]`, `[TestCase]`, `[Theory]`, `[TestCaseSource]`.
- JUnit: `@Test`, `@ParameterizedTest`, `@TestFactory` (treat generated tests carefully).
- unittest: methods prefixed with `test_` in `TestCase` classes.
- pytest: test functions/methods prefixed `test_`.

## Mapping Hints
- Prefer direct symbol references and assertions in the same test body.
- Fixture setup alone does not imply coverage.
- Parameterized tests must still include explicit branch-relevant assertions.

## Quality Checks
- Every `Unit Test Elements` row must reference a known code class.
- If a test class targets multiple code classes, create multiple `Unit Test Classes` records.
