# Checklist — Security: Web & API

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| SEC-WA-01 | A Content-Security-Policy header is set and avoids broad `unsafe-inline`/`unsafe-eval` | Warning | https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html |
| SEC-WA-02 | `Strict-Transport-Security` is set for HTTPS-only sites | Warning | https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html |
| SEC-WA-03 | `X-Content-Type-Options: nosniff` is set | Warning | https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html |
| SEC-WA-04 | Clickjacking protection is set (`X-Frame-Options` or `frame-ancestors` CSP directive) | Warning | https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html |
| SEC-WA-05 | CORS is scoped to specific trusted origins, not a wildcard combined with credentials | Error | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html |
| SEC-WA-06 | All endpoints are served over HTTPS/TLS, with HTTP redirected or rejected | Error | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html |
| SEC-WA-07 | Error responses don't leak stack traces, internal paths, or framework version info | Warning | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html |
