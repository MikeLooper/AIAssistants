# Language Guidance — Java (Security)

Reference: OWASP Java Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html

- JPA/Hibernate with named/positional parameters; flag `Statement` with concatenated SQL instead of `PreparedStatement`.
- `DocumentBuilderFactory`/`SAXParserFactory` with `FEATURE_SECURE_PROCESSING` and external entities disabled.
- File uploads validated via Spring's `MultipartFile` content-type/size limits; stored outside `webapp`/classpath roots.
