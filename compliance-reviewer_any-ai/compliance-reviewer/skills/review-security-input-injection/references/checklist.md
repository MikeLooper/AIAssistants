# Checklist — Security: Input & Injection

Each check is evaluated through the elements it lists; every element belongs to exactly one check. Element
definitions, anchors and citation bases are in `standards/`. Severity rules (SHOULD elements one level lower) are in
`../SKILL.md`.

| id | Check | Default severity | Elements | Source |
|----|-------|------------------|----------|--------|
| SEC-II-01 | All untrusted input (parameters, bodies, headers, file names, messages, stored data crossing a trust boundary) is validated server-side by allowlist rules for type, length, range and structure, within size and parser limits, before use; only intended fields are bound | Error | IV-01…09, A05-01, A05-05, NET-14, JVA-08, JVA-09, PY-07, NDI-01, NDI-02, NDI-03, NDI-06 | IV, A05, NET, JVA, PY, NDI |
| SEC-II-02 | No untrusted data is concatenated or interpolated into SQL or ORM query text, including stored procedures and raw-SQL APIs; no manual escaping | Error | SQL-01, SQL-02, SQL-03, SQL-05, SQL-06, A05-02, A05-03, NET-01, NET-07, JVA-01, JVA-03, PY-03, PY-05 | SQL, QP, A05, NET, JVA, PY |
| SEC-II-03 | Database access binds values through server-side parameterized APIs or a vetted ORM, maps dynamic identifiers and sort order to fixed allowlists, and uses a least-privilege database account | Error | QP-01, QP-02, SQL-04, SQL-07, A05-04, A05-06, NET-02, JVA-14, JVA-15 | QP, SQL, A05, NET, JVA |
| SEC-II-04 | OS commands and other interpreters (`eval`/script engines, LDAP, XPath, NoSQL, JNDI, mail protocols) never receive unvalidated input: safe or parameterized APIs, argument arrays without a shell, allowlisted commands and arguments | Error | INJ-01…06, A05-07, NET-15, JVA-04, JVA-06, PY-01, NDI-05 | INJ, A05, NET, JVA, PY, NDI |
| SEC-II-05 | XML parsers handling untrusted input disable DTDs (or, if required, external entities/DTD loading with expansion limits), reject malformed documents and validate against local, restrictive schemas | Error | XML-01…05, NET-05, NET-08, JVA-05, JVA-12, JVA-13, PY-04 | XML, NET, JVA, PY |
| SEC-II-06 | File uploads allowlist extensions after decoding, don't trust `Content-Type`, check signatures and content, limit size (including decompressed size), use server-generated names and store outside the webroot | Error | FU-01…07, FU-10, NET-10, NET-11, JVA-11, PY-08 | FU, NET, JVA, PY |
| SEC-II-07 | Uploaded files can't be executed or served as active content from their storage location: ID-mapped handlers, no execute permissions, no per-directory overrides, separate serving domain | Error | FU-08, FU-09, NET-12, PY-09, PY-10 | FU, NET, PY |
| SEC-II-08 | Untrusted data rendered into HTML, JavaScript, CSS or URL contexts is encoded for that context by framework auto-escaping or an encoder, escape hatches and unsafe DOM sinks aren't used with it, and user HTML is sanitized | Error | XSS-01…10, NET-03, NET-06, NET-13, JVA-07, PY-06, NDI-04 | XSS, NET, JVA, PY, NDI |
| SEC-II-09 | Untrusted data isn't deserialized with native or type-polymorphic serializers; data formats map to DTOs, the payload never selects types, and unavoidable native deserialization is filtered or signed | Error | DES-01…09, NET-04, NET-09, JVA-02, JVA-10, PY-02 | DES, NET, JVA, PY |

| SEC-II-10 | Server-side requests to URLs or hosts derived from untrusted input are restricted: allowlisted destinations built from a fixed scheme, port and path, HTTP(S) only, no automatic redirects, resolved IPs validated before connecting, internal and metadata addresses blocked after normalization | Error | SSRF-01…08 | SSRF |

Totals: 66 OWASP cheat-sheet + 7 A05 + 15 NET + 15 JVA + 10 PY + 6 NDI = 119 elements across 10 checks.
