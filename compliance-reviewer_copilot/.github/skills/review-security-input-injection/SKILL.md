---
name: review-security-input-injection
description: 'Reviews input validation, injection prevention, SQL injection prevention, query parameterization, XML security and file upload handling. Use when the compliance-reviewer orchestrator delegates the Security / Input & Injection subject.'
user-invocable: false
---

# Review: Security — Input & Injection

Assesses input validation, injection prevention (SQL, command, LDAP, etc.), query parameterization, XML security and file upload handling.

## Inputs

Request handlers/controllers, data access/ORM code, file upload handlers, XML parsing code, per `compliance-inventory`. Also load `references/languages/<id>.md` for each detected language.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, and any matching `references/languages/<id>.md`.
2. Check that all external input (query params, body, headers, file names) is validated (allow-list, type, length) before use.
3. Check database access uses parameterized queries/prepared statements or a vetted ORM, never string-concatenated SQL.
4. Check XML parsing disables external entity resolution (XXE prevention) and DTD processing where not required.
5. Check file upload handling validates type/size, stores outside the web root or with randomized names, and scans/limits execution risk.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
