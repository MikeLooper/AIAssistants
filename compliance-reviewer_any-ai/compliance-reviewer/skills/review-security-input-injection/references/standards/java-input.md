# Java / JDK / Spring Data JPA input & injection guidance — localized summary

- Sources: cheatsheetseries.owasp.org — OWASP Java Security Cheat Sheet @ OWASP/CheatSheetSeries
  f1d0311aaadac4c315471feb8947c9fbb3cbb32e (2026-10-22); www.oracle.com — Secure Coding Guidelines for Java SE,
  document version 11.0 (June 2025), sections 1, 3, 5, 8 only; docs.oracle.com — JAXP Security Guide, Java SE 25;
  docs.spring.io — Spring Data JPA reference 4.1 (4.1.2), JPA Query Methods
- Localized: 2026-11-08 · Elements: 15 — cheatsheetseries.owasp.org 2 (counted with `owasp-input-injection.md`: 66, cap 100);
  www.oracle.com 9 (cap 100); docs.oracle.com 2 (cap 100); docs.spring.io 2 (cap 100)
- Applies when language `java` is detected. Spring Data JPA elements (JVA-14, JVA-15) apply when `spring-data-jpa` or
  `spring-boot-starter-data-jpa` is a dependency; JDK, Oracle-guideline and OWASP elements always.
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element it supports
  and name the JVA element in the recommendation. Where vendor guidance is weaker than an OWASP element, the OWASP
  element decides. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only Java defaults a worker may rely on. Spring Boot multipart limits, Thymeleaf,
  Hibernate native APIs and SnakeYAML version defaults are **not** localized: report only explicit insecure settings
  there, and add a `localized-standard-gap` note for a missing setting.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| jsec | https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html | commit f1d0311a (2026-10-22) | OWASP Java Security Cheat Sheet |
| scg | https://www.oracle.com/java/technologies/javase/seccodeguide.html | document version 11.0 (June 2025) | Oracle Secure Coding Guidelines for Java SE |
| jaxp | https://docs.oracle.com/en/java/javase/25/security/java-api-xml-processing-jaxp-security-guide.html | Java SE 25 | Oracle JAXP Security Guide (Java SE 25) |
| sdj | https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html | Spring Data JPA 4.1.2 | Spring Data JPA Reference — JPA Query Methods |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| JVA-01 | MUST | JPA/Hibernate isn't blanket protection: JPQL/HQL must be parameterized too. | `em.createQuery("… " + v)` | SEC-II-02 | jsec#sql-and-jpa-injections |
| JVA-02 | MUST | Don't deserialize untrusted data — including data read back from a database. | `readObject` on DB blobs or request streams | SEC-II-09 | jsec#serialization |
| JVA-03 | MUST | INJECT-2: avoid dynamic SQL; use `PreparedStatement`/`CallableStatement`, not `Statement`, or a well-written higher-level library. | `Statement.executeQuery(sql + v)` | SEC-II-02 | scg#3-2 |
| JVA-04 | MUST | INJECT-4: no untrusted data on the command line of new processes (option injection via leading `-`/`/`, argument splitting). | `Runtime.exec`/`ProcessBuilder` with request data | SEC-II-04 | scg#3-4 |
| JVA-05 | MUST | INJECT-5/DOS-1: restrict XML inclusion (DTD system entities, XInclude, XSLT `document()`) and set `XMLConstants.FEATURE_SECURE_PROCESSING` with reasonable limits. | XInclude enabled; FSP explicitly `false` | SEC-II-05 | scg#3-5, scg#1-1 |
| JVA-06 | MUST | INJECT-8: don't run untrusted code: `javax.script` evaluation, XSLT extension functions (FSP disables them), JNDI lookups with untrusted names (LDAP/RMI remote class loading). | `ScriptEngine.eval(input)`; `new InitialContext().lookup(input)` | SEC-II-04 | scg#3-8 |
| JVA-07 | MUST | INJECT-3: sanitize/encode untrusted data in generated HTML/XML with a library, taking particular care in JSP. | `out.print(request.getParameter(…))` in JSP/servlets; XML built by string concatenation | SEC-II-08 | scg#3-3 |
| JVA-08 | MUST | INPUT-1: validate untrusted input before use, including `../` directory traversal in file names; validate again immediately before a security-sensitive use. | `new File(base, request.getParameter("name"))` | SEC-II-01 | scg#5-1 |
| JVA-09 | SHOULD | INJECT-9: reject NaN/Infinity from untrusted floating-point input before sensitive calculations. | `Double.valueOf(input)` feeding prices/limits unchecked | SEC-II-01 | scg#3-9 |
| JVA-10 | MUST | SERIAL-6: filter untrusted serial data with serialization filters (allowlist per context; `ObjectInputFilter`, `jdk.serialFilter`). | `ObjectInputStream` with no filter on any external stream | SEC-II-09 | scg#8-6 |
| JVA-11 | SHOULD | DOS-1: limit decompressed size rather than trusting compressed size or metadata (zip bombs). | `ZipInputStream` loops with no byte/entry limit | SEC-II-06 | scg#1-1 |
| JVA-12 | MUST | (Default) FSP is on by default, but the JDK doesn't restrict external connections unless FSP is set **explicitly** through the API or External Access Properties are set; a factory parsing untrusted XML with neither (nor `disallow-doctype-decl`) fails XML-02. | `DocumentBuilderFactory.newInstance()` / `SAXParserFactory` / `XMLInputFactory` / `TransformerFactory` on untrusted input with no explicit settings | SEC-II-05 | jaxp#JSSEC-GUID-F84BE9C4-AFC4-4555-8B3B-4A0F9DE836DD, jaxp#JSSEC-GUID-61FD4DB8-244C-41B2-BC21-01B01C5D40EC |
| JVA-13 | SHOULD | Disable DTDs (`jdk.xml.dtd.support` or `disallow-doctype-decl`) when not needed, tighten processing limits, and resolve required external resources only through a resolver/catalog. | DTD support left on for parsers that never need it | SEC-II-05 | jaxp#JSSEC-GUID-82A5172C-C75E-4276-93C4-C3D2774C97E1 |
| JVA-14 | MUST | (Default) Spring Data JPA rejects `Sort` orders containing functions by default; `JpaSort.unsafe(…)` bypasses that check and must never carry user-supplied sort input. | `JpaSort.unsafe(request.getParameter("sort"))` | SEC-II-03 | sdj#jpa.query-methods.sorting, sdj#_jpasort_unsafe_limitations |
| JVA-15 | SHOULD | (Default) Derived `LIKE` queries (`Containing`, `StartingWith`, …) escape wildcard characters in arguments; hand-written `@Query` `LIKE` with concatenation doesn't. | `@Query("… LIKE '%" + …)`; native queries with concatenation | SEC-II-03 | sdj#jpa.sample-app.finders.strategies, sdj#jpa.query-methods.at-query.advanced-like |
