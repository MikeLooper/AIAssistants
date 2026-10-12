---
name: review-security-operational
description: 'Reviews error handling, logging and secrets management, using the OWASP Secure Code Review Cheat Sheet as the review method. Use when the compliance-reviewer orchestrator delegates the Security / Operational subject.'
user-invocable: false
---

# Review: Security — Operational

Assesses error handling, logging practices and secrets management, following the Secure Code Review Cheat Sheet as the review method.

## Inputs

Error handling middleware, logging config/code, secrets/config loading code, per `compliance-inventory`. Also load `references/languages/<id>.md` for each detected language.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, and any matching `references/languages/<id>.md`.
2. Follow the Secure Code Review Cheat Sheet's method: prioritize high-risk areas (auth, data handling, error paths) identified from the inventory, then read for the specific anti-patterns below.
3. Check errors are caught and handled without leaking sensitive details to clients, while still being logged internally.
4. Check logs don't record secrets, tokens, passwords or full PII, and that logging can't be used for log injection (unsanitized newlines in user input written to logs).
5. Check secrets (API keys, connection strings, credentials) are not hardcoded or committed, and are sourced from a vault/environment/secret manager.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
