# Detection signals — Java (Data Protection)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). JPA `AttributeConverter`, Hibernate and Spring Data defaults aren't localized: judge explicit code
only, and add a `localized-standard-gap` note when a decision depends on a default.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `@Entity` fields `ssn`, `cardNumber`, `iban`, `dateOfBirth` with no `@Convert(converter = …Encrypt…)` or tokenization | entities | Sensitive personal data stored in plaintext | A04-04, CSD-01 |
| `Cipher.getInstance("AES")`, `"AES/ECB/…"`, `"RSA/ECB/PKCS1Padding"`, `MessageDigest.getInstance("MD5")` over personal fields | crypto helpers | Weak storage encryption | CSD-03, A04-05 |
| `@RestController` method returning an `@Entity` or `repository.findAll()` directly | controllers | Over-exposure on output | BOP-03, BOP-01 |
| Returned entity without `@JsonIgnore` on `password`, `ssn` or internal flags; no `@JsonView` or DTO | entities, controllers | Sensitive properties serialized | JVD-01, JVD-02 |
| `@RequestParam String email`, `@GetMapping("/users/{email}")`, `redirect:/…?email=` | controllers | Personal data in URLs | QSE-01 |
| `sentry.max-request-body-size=always`, no `dataCollection.userInfo=false`, `Sentry.setUser(...)` with email | `application*.properties`/`.yml`, config classes | Error tracker sends user data | TPS-02 |
| `data.sql`, `import.sql`, Flyway `V*__seed*.sql`, `src/test/resources/*.json` with names, emails, card numbers | resources, migrations | Seed data (synthetic or real-looking) | SP122-06, RSV-01 |
