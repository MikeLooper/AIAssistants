# Language Guidance — Java (Security)

Reference: OWASP Java Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html

- Secrets via Spring Cloud Config/Vault or environment variables, not plaintext in `application.properties`/`application.yml` committed to source control.
- SLF4J/Logback structured logging with parameterized messages (`log.info("User {}", id)`), not string concatenation of sensitive data.
- `@ControllerAdvice`/`@ExceptionHandler` returns a generic error body in production; detailed stack traces disabled outside dev profiles.
