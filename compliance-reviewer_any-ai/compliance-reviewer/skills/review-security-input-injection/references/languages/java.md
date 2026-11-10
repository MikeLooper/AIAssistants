# Detection signals — Java (Security: Input & Injection)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only when untrusted data reaches it or the setting is explicit (`SKILL.md`
step 3). The only Java defaults a worker may rely on are those stated in `java-input.md` (JVA-12, JVA-14, JVA-15).
Spring Boot multipart limits, Thymeleaf and SnakeYAML version defaults are not localized: report explicit values only,
and add a `localized-standard-gap` note for a missing setting.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `Statement.execute*` with concatenation; `JdbcTemplate.query(sql + v)`; `String.format` into SQL | DAOs, repositories | SQL built from untrusted values | JVA-03, SQL-01 |
| `createQuery`/`createNativeQuery` with `+`; `@Query("… " + …)` | JPA repositories, services | JPQL/HQL/native injection | JVA-01, SQL-02 |
| `prepareCall("{call p('" + v + "')}")`; `EXECUTE IMMEDIATE` with concatenation in PL/SQL | DAOs, `*.sql` | Procedure injection | SQL-03 |
| `JpaSort.unsafe(` with request data; `Sort.by(request…)` into `@Query`; `ORDER BY " + sort` | repositories, controllers | Unallowlisted sort/identifiers | JVA-14, SQL-04 |
| `@Query` `LIKE '%" + …` or `LIKE CONCAT` built from input in native queries | repositories | Hand-built LIKE | JVA-15 |
| `spring.datasource.username=root`/`postgres`/`sa` | `application*.properties/yml` | Over-privileged database account | SQL-07 |
| `Runtime.getRuntime().exec(String)`; `ProcessBuilder` with request data; `"sh", "-c"` / `"cmd", "/c"` with input | services | Command injection | JVA-04, INJ-04, INJ-05 |
| `ScriptEngineManager…eval`, SpEL `parseExpression(input)`, OGNL/EL evaluation of input | services, controllers | Expression/script injection | JVA-06, INJ-03, A05-07 |
| `InitialContext.lookup(input)`; LDAP `search(…, "(uid=" + v + ")")`; `XPath.evaluate("…" + v)` | directory/XML code | JNDI/LDAP/XPath injection | JVA-06, INJ-06 |
| `DocumentBuilderFactory`/`SAXParserFactory`/`XMLInputFactory`/`TransformerFactory`/`SchemaFactory` used on untrusted XML without explicit `FEATURE_SECURE_PROCESSING`, `ACCESS_EXTERNAL_DTD/SCHEMA/STYLESHEET` or `disallow-doctype-decl` | XML parsing code | External connections not restricted | JVA-12, XML-02 |
| `setXIncludeAware(true)`; `IS_SUPPORTING_EXTERNAL_ENTITIES = true`; FSP set `false` | XML parsing code | XML inclusion enabled | JVA-05, XML-01 |
| DTD support left on (`jdk.xml.dtd.support` unset) where no DTD is needed | XML config | DTDs not disabled | JVA-13 |
| `ObjectInputStream.readObject`/`readUnshared` without `setObjectInputFilter` / `jdk.serialFilter` | consumers, caches, servlets | Unfiltered Java deserialization | JVA-10, JVA-02, DES-05 |
| `XMLDecoder`; XStream without allowlist; `new Yaml()` without `SafeConstructor`; `kryo.setRegistrationRequired(false)`; fastjson autotype | serializers | Unsafe deserialization libraries | DES-05, DES-06 |
| Jackson `enableDefaultTyping`/`activateDefaultTyping`, `@JsonTypeInfo(use = Id.CLASS)` | `ObjectMapper` config, DTOs | Payload selects the type | DES-02 |
| Sensitive fields in `Serializable` classes without `transient` | DTOs, entities | Data leakage via serialization | DES-07 |
| JSP `<%= request.getParameter(…) %>`, `out.print(param)`, JSTL `<c:out escapeXml="false">`; XML built by concatenation | JSP, servlets | Unencoded output | JVA-07, XSS-01 |
| Thymeleaf `th:utext` with user data | templates | Escape hatch (Thymeleaf not localized; note gap for defaults) | XSS-02 |
| Global "XSS filter" servlet/filter that encodes request parameters | `web.xml`, filters | Interceptor instead of output encoding | XSS-10 |
| `new File(base, input)` / `Paths.get(input)` without normalization and prefix check | file services | Path traversal | JVA-08 |
| `MultipartFile.getOriginalFilename()` in a storage path; type decided by `getContentType()` only | upload controllers | Client filename/type trusted | FU-04, FU-03 |
| `ZipInputStream` loops without byte/entry limits | upload/import code | Zip bomb | JVA-11, FU-05 |
| Spring Boot `spring.servlet.multipart.max-file-size=-1` / `max-request-size=-1` | `application*.properties/yml` | Unlimited upload size (explicit only) | FU-05 |
| Uploads written under `src/main/webapp`, `static/` or `public/` | upload code | Uploads in webroot | FU-07 |
| `Double.parseDouble(input)` in monetary or limit logic without `isNaN`/`isInfinite` checks | services | NaN/Infinity accepted | JVA-09 |
| Request DTOs without Bean Validation constraints (`@Size`, `@Min`, `@Max`, `@Pattern`) or without `@Valid` | DTOs, controllers | Missing field rules | IV-02, IV-07 |
| `Pattern.compile` with nested quantifiers on unbounded input; `find()` used for full validation | validators | ReDoS / partial match | IV-08 |
