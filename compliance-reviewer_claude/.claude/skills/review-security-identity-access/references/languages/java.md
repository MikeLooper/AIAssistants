# Language Guidance — Java (Security)

Reference: OWASP Java Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html

- Use Spring Security (or an equivalent vetted framework) rather than hand-rolled auth filters.
- Method-level security annotations (`@PreAuthorize`, `@Secured`) present on sensitive service methods, not just at the controller.
- Password hashing via `BCryptPasswordEncoder`/`Argon2PasswordEncoder`, not `MessageDigest`-based custom hashing.
- Session fixation protection enabled (Spring Security's default `sessionFixation().migrateSession()` or equivalent).
