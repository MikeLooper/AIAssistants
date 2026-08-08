---
description: Unit test creation and maintenance standards for Java/Spring Boot test work in this repository.
applyTo: "src/test/java/**/*.java"
---

# Unit Test Instructions: Java (JUnit 5 + Spring Boot)

## Purpose and Scope
These instructions define how GitHub Copilot should create and maintain unit tests in this repository.

Scope restriction:
- These instructions apply only to creating and maintaining unit tests and their direct test support files.
- These instructions do not apply to production feature development, refactoring, or infrastructure tasks.

Hard constraints:
- Do not modify production classes while building or updating unit tests unless the user explicitly requests production-code changes.
- Use JUnit 5 (Jupiter) for test definitions and assertions.
- Use Mockito for mocks/stubs in unit tests.
- Use Spring Boot test slices (for example, `@WebMvcTest`) only when endpoint/controller behavior is under test.
- Keep one top-level class per test file.

## How This Instructions File Is Used
When a request involves creating, updating, or validating unit tests, Copilot must:
1. Follow this file as the primary standard for test structure, naming, implementation style, and validation.
2. Generate any missing unit test classes and methods required by these rules.
3. Validate test execution and fix test-project issues until tests run successfully (without changing production classes unless explicitly requested).
4. Keep all test artifacts aligned with these requirements over time.

## Source-to-Test Mapping Rules
For the Java application in this repository:

Rules:
- Source classes live under `src/main/java/...`.
- Matching tests live under `src/test/java/...`.
- The test package/folder should mirror the source package/folder where practical.
- Example:
  - Source: `src/main/java/com/pilotapi/service/CategoryService.java`
  - Test: `src/test/java/com/pilotapi/service/CategoryServiceTest.java`

## Test Project Directory Structure Rules
The arrangement of unit test classes should mirror source package structure.

Requirements:
- Directory trees for test classes and source classes should match where applicable.
- Controller tests should use `*WebMvcTest` naming and remain under `src/test/java/com/pilotapi/controller`.
- Service tests should use `*ServiceTest` naming and remain under `src/test/java/com/pilotapi/service`.

Optional support layout:
- Reusable test-only helpers may be placed under `src/test/java/com/pilotapi/testing/...`.
- Test resources should be placed under `src/test/resources/...`.

## Class-Level Coverage Requirements
Each production class with business logic should have a matching unit test class or equivalent coverage.

Rules:
- If a matching unit test class does not exist, create it.
- Keep test class placement consistent with package mapping rules.
- Validate tests after creating/updating classes.

## Method and Property Coverage Requirements
Each method with observable behavior should have one or more corresponding tests.

Rules:
- Add missing test methods for uncovered behavior.
- Cover success, failure, and edge-case logic paths.
- Validate tests after creating/updating methods.

## Test Class and Method Conventions
Test methods must:
- Follow Arrange, Act, Assert (AAA) structure.
- Use descriptive names that capture method/behavior/expected result.
- Existing underscore style is acceptable and should be kept consistent within a class.

Variable rules in unit tests:
- Prefer local variables scoped to each test.
- Avoid mutable shared state unless required by framework setup.

## Framework Conventions for This Repository
Service-unit tests:
- Use JUnit 5 + Mockito (`@ExtendWith(MockitoExtension.class)`).
- Mock collaborators and verify behavior/output.
- Do not start Spring context for pure unit tests.

Controller tests:
- Use `@WebMvcTest(<Controller>.class)`.
- Use `MockMvc` + `@MockBean` for service dependencies.
- Validate HTTP status and payload contract.

## Validation and Error Correction
After creating or updating tests, verify all unit tests can run successfully.

Requirements:
- Run Maven test workflow for the affected scope, then full suite when needed.
- Correct discovered test-project errors.
- Do not alter production code solely to make tests pass unless explicitly requested.

## Appendix A: Additional Best Practices and Recommendations
These recommendations supplement required rules above.

1. Test design quality
- Keep each test focused on one behavior.
- Prefer one assertion theme per test.
- Use explicit input values to make intent obvious.
- Include happy-path, boundary, null/empty, invalid input, and exception-path tests where applicable.

2. Deterministic tests
- Avoid reliance on current time, random values, external state, network calls, and environment-specific behavior unless fully controlled by fixtures/mocks.
- Use stable test data and controlled setup.

3. Readability and maintainability
- Keep AAA sections visually clear.
- Use descriptive variable names.
- Prefer behavior-focused assertions.

4. Doubles and resources
- Keep reusable doubles/helpers in a consistent test-only package.
- Keep test resources in `src/test/resources` and reference them predictably.

5. Coverage discipline
- Add tests for both positive and negative outcomes.
- Add regression tests when defects are found.
- Ensure new behavior is not left without matching tests.

6. File and class hygiene
- Keep one top-level class per file.
- Keep package and folder organization aligned with source code.
