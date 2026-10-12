---
name: review-security-identity-access
description: 'Reviews authentication, authorization, OAuth 2.0, JWT, session management, password storage and Zero Trust posture. Use when the compliance-reviewer orchestrator delegates the Security / Identity & Access subject.'
user-invocable: false
---

# Review: Security — Identity & Access

Assesses authentication, authorization, OAuth 2.0/JWT handling, session management, password storage and Zero Trust posture.

## Inputs

Auth middleware/filters, login/token code, session config, identity provider config, per `compliance-inventory`. Also load `references/languages/<id>.md` for each detected language.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, and any matching `references/languages/<id>.md`.
2. Check authentication is enforced on protected endpoints, and authorization checks are not just client-side.
3. Check OAuth2/JWT usage: token validation (signature, issuer, audience, expiry), no secrets in tokens, secure storage of tokens client-side where visible in code.
4. Check session management: secure/HttpOnly/SameSite cookies, session fixation prevention, session timeout.
5. Check password storage: strong adaptive hashing (bcrypt/argon2/PBKDF2), no plaintext or reversible encryption, no custom crypto.
6. Check Zero Trust posture: least privilege, explicit verification rather than implicit network trust.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
