# Checklist — Security: Operational

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| SEC-OP-01 | Exceptions are caught and handled; clients never see stack traces or internal error details | Warning | https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html |
| SEC-OP-02 | Errors are still logged internally with enough context to diagnose (not silently swallowed) | Warning | https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html |
| SEC-OP-03 | Logs never contain passwords, tokens, full card numbers, or other secrets/PII in cleartext | Error | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html |
| SEC-OP-04 | User-controlled input written to logs is sanitized against log injection (e.g. newline stripping) | Warning | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html |
| SEC-OP-05 | No hardcoded secrets (API keys, connection strings, credentials) in source or config committed to the repo | Error | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html |
| SEC-OP-06 | Secrets are sourced from a vault/secret manager or environment injection, not plain config files in version control | Error | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html |
| SEC-OP-07 | The review prioritized high-risk areas (auth, data handling, error paths) per the Secure Code Review method | Information | https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html |
