---
description: Test resources and fixture standards for Java/Spring Boot tests in this repository.
applyTo: "src/test/resources/**"
---

# Test Resource Instructions: Java/Spring Boot

## Purpose and Scope
These instructions define how GitHub Copilot should create and maintain files under `src/test/resources`.

Scope restriction:
- These instructions apply only to test resource files and folders.
- These instructions do not apply to production resources under `src/main/resources`.

## Directory and Naming Conventions
Rules:
- Keep test data organized by feature or test type when practical.
- Prefer lowercase, descriptive file names.
- Use stable, explicit names for fixture files to avoid ambiguity.

## Deterministic Fixture Rules
Rules:
- Keep fixtures deterministic and repeatable.
- Avoid values that depend on current time, locale, timezone, random data, or external systems unless explicitly controlled.
- Keep fixture payloads minimal while still representing the behavior under test.

## Security and Data Hygiene
Rules:
- Do not store secrets, API keys, private certificates, or real credentials in test resources.
- Do not include production PII in fixtures.
- Use sanitized or synthetic data only.

## Format-Specific Guidance
JSON/YAML:
- Keep structure valid and consistent with the DTO/API contract under test.
- Include only fields needed by the test unless full-schema coverage is the test objective.

SQL scripts:
- Keep scripts idempotent where practical for repeatable local runs.
- Separate setup and cleanup intent clearly when both are required.

## Validation Workflow
After creating or updating test resources:
- Ensure referenced resource paths in tests remain correct.
- Run the affected tests.
- Correct broken resource loading paths or malformed resource content.

## Maintainability
- Prefer small focused fixtures over one large shared fixture when possible.
- Remove orphaned resources that are no longer referenced by tests.
- Keep comments in resource files concise and only where they add clear value.
