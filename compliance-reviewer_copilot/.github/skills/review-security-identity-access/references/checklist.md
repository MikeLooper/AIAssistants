# Checklist — Security: Identity & Access

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| SEC-IA-01 | Protected endpoints enforce authentication server-side (not just client-side) | Error | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html |
| SEC-IA-02 | Authorization checks are performed server-side for every sensitive action (no missing function-level access control) | Error | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html |
| SEC-IA-03 | JWTs are validated for signature, issuer, audience and expiry before trust | Error | https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html |
| SEC-IA-04 | OAuth2 flows use the appropriate grant type and validate redirect URIs/state | Error | https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html |
| SEC-IA-05 | Session cookies are Secure, HttpOnly and SameSite; sessions expire and rotate on privilege change | Error | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html |
| SEC-IA-06 | Passwords are stored with a strong adaptive hash (bcrypt/argon2/scrypt/PBKDF2), never plaintext or reversible encryption | Error | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html |
| SEC-IA-07 | No custom/home-grown cryptography or hashing is used for credentials | Error | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html |
| SEC-IA-08 | Access decisions follow least privilege / explicit verification (Zero Trust) rather than implicit network trust | Warning | https://cheatsheetseries.owasp.org/cheatsheets/Zero_Trust_Architecture_Cheat_Sheet.html |
