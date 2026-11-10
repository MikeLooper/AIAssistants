# OWASP input & injection guidance — localized summary

- Sources: cheatsheetseries.owasp.org @ OWASP/CheatSheetSeries (per-sheet commits below);
  top10.owasp.org (A05:2025) @ OWASP/Top10 d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966 (2025-12-24)
- Localized: 2026-11-08 (SSRF section 2026-11-09) · Elements: cheatsheetseries.owasp.org 66 here + 6 in
  `dotnet-input.md` + 2 in `java-input.md` = 74 (cap 100); top10.owasp.org 7 (cap 100)
- Level: `MUST` where the source says must/must not/never/do not/"is essential", gives an unqualified imperative, or
  names a prohibited practice or anti-pattern; `SHOULD` for recommendations (should/recommended/prefer/consider/"if
  available"). Top 10 elements: `MUST` for "How to prevent" bullets, `REVIEW` for "Description" weaknesses (`REVIEW`
  is treated like `MUST`). Severity rules are in `../../SKILL.md`.
- Untrusted data: anything the application didn't create — request parameters, bodies, headers, cookies, file names
  and contents, queue messages, partner feeds, other services' responses and data previously stored by users.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.
- Citation preference: vendor element (NET/JVA/PY) → cheat-sheet element → A05 element (cite A05 only when nothing
  more specific fits; otherwise name the A05 ID in the recommendation).

| Key | Citation base | Pinned commit | Source name for `Finding.standard` |
|-----|---------------|---------------|------------------------------------|
| ivl | https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html | b9500094 (2026-10-03) | OWASP Input Validation Cheat Sheet |
| inj | https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html | 9a91ba5a (2026-11-08) | OWASP Injection Prevention Cheat Sheet |
| sql | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html | 9a91ba5a (2026-11-08) | OWASP SQL Injection Prevention Cheat Sheet |
| qp | https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html | 9a91ba5a (2026-11-08) | OWASP Query Parameterization Cheat Sheet |
| xml | https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html | 6f207d04 (2026-11-08) | OWASP XML Security Cheat Sheet |
| fu | https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html | 89a49d9d (2026-10-04) | OWASP File Upload Cheat Sheet |
| xss | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html | 3b93fa9b (2026-11-01) | OWASP Cross Site Scripting Prevention Cheat Sheet |
| des | https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html | 16a0ed80 (2026-10-04) | OWASP Deserialization Cheat Sheet |
| ssrf | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html | 07656620 (2026-11-08) | OWASP Server-Side Request Forgery Prevention Cheat Sheet |
| a05 | https://top10.owasp.org/2025/A05_2025-Injection/ | d4d000ec (2025-12-24) | OWASP Top 10:2025 A05 |

## Input Validation Cheat Sheet (IV)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| IV-01 | MUST | Validate all untrusted input on the server; client-side checks are feedback only. | validation only in JS/HTML attributes; handler uses bound values unchecked | SEC-II-01 | ivl#common-pitfalls, ivl#introduction |
| IV-02 | MUST | Per-field rules for syntax and semantics: fixed choices by exact membership; numbers/dates by type, format, min/max; strings by length and structure; objects by allowed/required fields; arrays by item count and per-item rules. | DTOs/forms with unbounded strings, numbers or arrays; free-text enums | SEC-II-01 | ivl#input-validation-strategies |
| IV-03 | MUST | Accept by allowlist and reject everything else; don't denylist or "clean" input (removing characters doesn't make data safe). | denylist regexes; `Replace("'", "")`; stripping `<script>` as a defense | SEC-II-01 | ivl#allowlist-vs-denylist, ivl#common-pitfalls |
| IV-04 | MUST | Apply request size limits before buffering/parsing and configure parser limits (e.g. maximum nesting depth). | body-size limits removed or unbounded; parser depth limits raised without bound | SEC-II-01 | ivl#parse-safely-then-validate |
| IV-05 | SHOULD | Decode once per the protocol, validate the representation actually used, and don't decode again downstream. | URL/HTML decoding after validation; double decoding of paths | SEC-II-01 | ivl#parse-safely-then-validate |
| IV-06 | MUST | Use framework or schema validators; JSON schemas set `required` and reject additional properties; nested objects and arrays have schemas and length limits. | JSON Schema without `required`/`additionalProperties: false` used as the validation gate | SEC-II-01 | ivl#validate-structured-data |
| IV-07 | MUST | Reject invalid requests instead of continuing with partially validated data; bind only intended fields (mass assignment). | validation result ignored; persistence entities bound directly from the request | SEC-II-01 | ivl#validate-structured-data |
| IV-08 | MUST | Regex validation matches the whole value, bounds input length first, avoids catastrophic backtracking, uses a timeout or non-backtracking engine where available; a timeout is a failure. | unanchored patterns; `re.match` instead of `fullmatch`; nested quantifiers on untrusted input; no regex timeout | SEC-II-01 | ivl#regular-expressions-regex |
| IV-09 | MUST | Validate data from internal APIs, partner feeds, queues and stored records when it crosses a trust boundary. | message consumers or service clients use payload fields unvalidated | SEC-II-01 | ivl#common-pitfalls |

## Injection Prevention Cheat Sheet (INJ)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| INJ-01 | MUST | Prefer a safe API that avoids the interpreter or offers a parameterized interface; beware parameterized APIs that build commands unsafely underneath. | interpreter strings built by hand where a typed/parameterized API exists | SEC-II-04 | inj#rule-2-use-a-safe-api |
| INJ-02 | MUST | Where no parameterized API exists, escape with the interpreter's own escape syntax. | ad-hoc or generic escaping for LDAP/XPath/shell | SEC-II-04 | inj#rule-3-contextually-escape-user-data |
| INJ-03 | MUST | Never pass unvalidated input to `eval` or other runtime code execution. | `eval`, `exec`, `Function()`, script engines fed request data | SEC-II-04 | inj#scripting-languages |
| INJ-04 | MUST | If an OS command is unavoidable, use a structured mechanism that separates the command from its arguments (no shell string). | `Runtime.exec(String)` with concatenation; `cmd /c`/`sh -c` with input | SEC-II-04 | inj#remediation, inj#correct-usage, inj#operating-system-commands |
| INJ-05 | MUST | Validate the command against an allowlist and each argument by allowlist (bounded length, no shell metacharacters); argument separation doesn't replace validation. | user-chosen executable; arguments unvalidated; leading `-` accepted | SEC-II-04 | inj#remediation, inj#correct-usage |
| INJ-06 | MUST | LDAP, XPath, NoSQL and network-protocol (SMTP/IMAP/FTP) commands aren't built from unvalidated input. | LDAP filters, XPath expressions, Mongo `$where`/JSON queries or SMTP headers built by concatenation | SEC-II-04 | inj#forms-of-injection, inj#query-languages, inj#xpath-injection, inj#network-protocols |

## SQL Injection Prevention Cheat Sheet (SQL)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| SQL-01 | MUST | Never concatenate or interpolate untrusted values into SQL text, whatever their source (request, other service, stored data). | `"… WHERE x = '" + v + "'"`; f-strings/`String.format`/`$""` into SQL | SEC-II-02 | sql#introduction, sql#parameterized-queries, sql#basic-sql-injection |
| SQL-02 | MUST | The same applies to ORM query languages (JPQL/HQL); an ORM is not blanket protection. | `createQuery("… '" + v + "'")` | SEC-II-02 | sql#sql-injection-in-orm-query-languages |
| SQL-03 | MUST | Bind stored-procedure arguments **and** don't concatenate inside procedures; internal dynamic SQL binds values (`EXECUTE … USING`, `sp_executesql` with parameters). | `prepareCall("{call p('" + v + "')}")`; `EXEC('…' + @p)`; `EXECUTE IMMEDIATE` with concatenation | SEC-II-02 | sql#sql-injection-inside-stored-procedures-and-functions, sql#sql-injection-with-procedure-calls, qp#stored-procedure-examples |
| SQL-04 | MUST | Map user-chosen table/column names and sort direction to a fixed, application-owned allowlist; never append supplied text; identifier quoting isn't a restriction. | `ORDER BY " + sort`; dynamic table names from input | SEC-II-03 | sql#allow-list-input-validation |
| SQL-05 | MUST | Don't use manual escaping to build SQL; replace it with parameter binding. | home-made `Escape()`/`replace("'", "''")` before concatenation | SEC-II-02 | sql#manually-escaping-strongly-discouraged |
| SQL-06 | MUST | Validation complements binding but never replaces it; validated values are still bound. | "safe because validated/int-parsed" values concatenated into SQL | SEC-II-02 | sql#input-validation |
| SQL-07 | MUST | The application's database account has least privilege: never DBA/admin/owner; separate accounts per application; read-only where only reads are needed. | connection strings using `sa`, `root`, `postgres`, `dbo`/`db_owner` roles in app config or migrations | SEC-II-03 | sql#least-privilege, sql#least-admin-privileges-for-multiple-dbs |

## Query Parameterization Cheat Sheet (QP)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| QP-01 | MUST | Parameterization happens server-side; client libraries that build the query string before sending aren't parameterization. | client-side query builders sending raw SQL to a generic execute endpoint | SEC-II-03 | qp#parameterized-query-examples |
| QP-02 | MUST | Use the platform's bind API (`PreparedStatement.setX`, `SqlParameter`/`OleDbParameter`, named parameters in HQL/Criteria, PDO `bindParam`, SQLx `bind`). | `Statement`/`SqlCommand` without `Parameters`; string building next to a bind-capable API | SEC-II-03 | qp#prepared-statement-examples |

## XML Security Cheat Sheet (XML)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| XML-01 | MUST | Disable DTD processing for untrusted XML; this blocks XXE, entity expansion ("billion laughs") and external DTD fetches. | parser explicitly allows DOCTYPE/DTD on request/upload XML | SEC-II-05 | xml#xml-entity-expansion |
| XML-02 | MUST | If a DTD is genuinely required: disable external entities and external DTD loading **and** enforce entity-expansion and size limits (blocking external entities alone doesn't stop expansion). | external entities on; resolver set; expansion limits removed | SEC-II-05 | xml#xml-entity-expansion |
| XML-03 | SHOULD | Treat malformed documents as fatal: stop processing, don't use parser recovery modes on untrusted input, validate element values within bounds. | `recover=True` (lxml) or equivalent on untrusted XML | SEC-II-05 | xml#handling-malformed-xml-documents, xml#applications-processing-malformed-data |
| XML-04 | SHOULD | Validate untrusted XML against a precise XML Schema (not a DTD): restricted types (e.g. `positiveInteger`, `decimal` not `float` for amounts), lengths, enumerations, bounded `maxOccurs`. | XML accepted with no schema; `maxOccurs="unbounded"` on request schemas | SEC-II-05 | xml#dealing-with-invalid-xml-documents, xml#document-without-schema, xml#unrestrictive-schema, xml#improper-data-validation, xml#occurrences |
| XML-05 | MUST | Use a local or known-good schema, not the location supplied in the document; remote schemas only over HTTPS with certificate and hostname verification. | schema resolved from `xsi:schemaLocation`/`DOCTYPE SYSTEM "http://…"`; TLS verification disabled for schema fetch | SEC-II-05 | xml#remote-schema-poisoning, xml#schema-poisoning, xml#man-in-the-middle-mitm-attack, xml#dns-cache-poisoning |

## File Upload Cheat Sheet (FU)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| FU-01 | MUST | Allow only the extensions the business needs; a blocklist alone is weak. | no extension check; blocklist of `.exe`/`.php` only | SEC-II-06 | fu#list-allowed-extensions, fu#block-extensions |
| FU-02 | MUST | Validate the extension after decoding the filename, defeating double extensions, null bytes, case tricks, alternative handler extensions and NTFS streams (reject `:`). | `EndsWith(".jpg")` on the raw name; case-sensitive checks | SEC-II-06 | fu#extension-validation |
| FU-03 | MUST | Don't trust the client `Content-Type`; at most use it as a quick check, combined with file-signature validation (never signature alone). | type decided by `ContentType`/`content_type` only | SEC-II-06 | fu#content-type-validation, fu#file-signature-validation |
| FU-04 | MUST | Generate the stored filename server-side (e.g. UUID). If user names are kept: maximum length, allowed characters only, no leading or sequential periods, no leading hyphen or space. | client filename used in the storage path; `Path.Combine(dir, file.FileName)` | SEC-II-06 | fu#filename-safety |
| FU-05 | MUST | Set an upload size limit; for archives, limit the decompressed size using safe extraction. | no size check; ZIP extracted without size/entry limits | SEC-II-06 | fu#upload-and-download-limits |
| FU-06 | SHOULD | Validate content by type where possible: re-encode images and strip metadata, avoid accepting ZIP, scan with antivirus/sandbox or CDR when available. | uploads stored and served with no content processing | SEC-II-06 | fu#file-content-validation, fu#introduction |
| FU-07 | MUST | Store uploads on a separate host or outside the webroot; inside the webroot only write-only with access controls on reads. | upload dir under `wwwroot`/`static`/`webapp`/`MEDIA_ROOT` served directly | SEC-II-06 | fu#file-storage-location |
| FU-08 | MUST | Serve public uploads through a handler that maps an ID to the file, not by direct path. | links to `/uploads/<original-name>` | SEC-II-07 | fu#introduction, fu#file-storage-location |
| FU-09 | MUST | Uploaded files can't execute: least-privilege file permissions, only required modes, and per-directory config overrides (`.htaccess`, `web.config`) disabled on upload directories. | executable modes on upload dirs; `AllowOverride All`; handler mappings active for upload dirs | SEC-II-07 | fu#filesystem-permissions, fu#file-storage-location |
| FU-10 | MUST | Apply the same controls to files that are emailed or processed without being stored. | attachments forwarded or parsed without validation | SEC-II-06 | fu#file-storage-location |

## Cross Site Scripting Prevention Cheat Sheet (XSS)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| XSS-01 | MUST | Render all values through the framework's automatic output encoding, which escapes every value whether trusted or not. | string-built HTML in handlers; templates with auto-escaping disabled | SEC-II-08 | xss#xss-defense-philosophy, xss#framework-security, xss#output-encoding |
| XSS-02 | MUST | Don't use framework escape hatches with unsanitized data (`dangerouslySetInnerHTML`, `bypassSecurityTrustAs*`, Lit `unsafeHTML`, raw-HTML helpers). | escape hatch fed request or stored user data | SEC-II-08 | xss#framework-security |
| XSS-03 | MUST | HTML body: HTML-entity encode; attributes: quote values and use an attribute encoder; attribute and element names stay fixed. | unquoted attribute interpolation; dynamic attribute names | SEC-II-08 | xss#output-encoding-for-html-contexts, xss#output-encoding-for-html-attribute-contexts |
| XSS-04 | MUST | JavaScript: insert untrusted data only as a quoted string via an encoder for the JS and enclosing HTML context; never in event-handler attributes; JSON responses use `application/json`. | `<script>var x = '@Model.X'</script>` without JS encoding; `onclick="…${v}"`; JSON served as `text/html` | SEC-II-08 | xss#output-encoding-for-javascript-contexts, xss#output-encoding-for-html-attribute-contexts |
| XSS-05 | MUST | URLs: percent-encode parameter values (`encodeURIComponent`), then attribute-encode; untrusted URLs in `href`/`src` are validated to an http/https allowlist (no `javascript:`). | user-supplied links rendered as `href` unchecked | SEC-II-08 | xss#output-encoding-for-url-contexts, xss#common-mistake, xss#xss-prevention-rules-summary |
| XSS-06 | MUST | CSS: don't interpolate untrusted data into CSS source; use CSSOM with a fixed property and an allowlisted value. | `style="…{{value}}"` with user data | SEC-II-08 | xss#output-encoding-for-css-contexts |
| XSS-07 | MUST | Never place untrusted data in dangerous contexts: directly in `<script>`/`<style>`, HTML comments, tag or attribute names, or `eval`/`setTimeout`/`setInterval` strings. | user data in comments or as a `setTimeout` string | SEC-II-08 | xss#dangerous-contexts |
| XSS-08 | MUST | User-authored HTML is cleaned with a maintained HTML sanitizer (e.g. DOMPurify), not modified after sanitizing; validation and regex can't replace it. | user HTML stored/rendered raw; regex "sanitizers" | SEC-II-08 | xss#html-sanitization, ivl#validating-rich-user-content |
| XSS-09 | MUST | Use safe DOM sinks (`textContent`, `value`, `createTextNode`, `setAttribute` with fixed safe names) instead of `innerHTML`/`outerHTML`/`document.write` with untrusted data; element names from an allowlist. | `el.innerHTML = data`; `document.write(location.hash)`; `$(…).html(data)` | SEC-II-08 | xss#safe-sinks |
| XSS-10 | MUST | Don't rely on input validation, request interceptors/filters, CSP or a WAF as the XSS defense; encode at the point of output. | global "XSS filter" servlet/middleware that encodes request parameters instead of output encoding | SEC-II-08 | xss#common-anti-patterns-ineffective-approaches-to-avoid, xss#reliance-on-http-interceptors, xss#sole-reliance-on-content-security-policy-csp-headers, xss#other-controls |

## Deserialization Cheat Sheet (DES)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| DES-01 | MUST | Don't deserialize untrusted data with native object formats; use a pure data format (JSON/XML) into data-transfer objects. | native serialization on request bodies, cookies, view state, queue messages | SEC-II-09 | des#using-alternative-data-formats, des#what-is-deserialization, des#guidance-on-deserializing-objects-safely, des#php, des#clear-box-review |
| DES-02 | MUST | Never let the data choose the type to instantiate (type names in payloads, polymorphic typing, `Type.GetType(<data>)`). | `TypeNameHandling` ≠ `None`; `JavaScriptTypeResolver`; Jackson default typing; fastjson autotype | SEC-II-09 | des#general-precautions, des#clear-box-review_3, des#other-deserialization-libraries-and-formats |
| DES-03 | MUST | .NET: don't use `BinaryFormatter`; inspecting the object after deserializing is too late. | `BinaryFormatter.Deserialize`; post-hoc type checks | SEC-II-09 | des#general-precautions, des#net-csharp |
| DES-04 | MUST | Python: no `pickle`/`jsonpickle` on untrusted data; YAML only via `yaml.safe_load`, no unsafe loaders or custom constructors. | `pickle.loads(request…)`; `yaml.load(…, Loader=yaml.Loader/UnsafeLoader)`; `yaml.unsafe_load` | SEC-II-09 | des#clear-box-review_1, des#python |
| DES-05 | MUST | Java: no `ObjectInputStream.readObject`/`readUnshared`, `XMLDecoder` or old XStream on untrusted data; if Java serialization is unavoidable, install a serialization filter (class allowlist + limits) before reading; `resolveClass` alone is insufficient. | `new ObjectInputStream(request.getInputStream())`; `XMLDecoder` on uploads | SEC-II-09 | des#java, des#clear-box-review_2, des#harden-your-own-javaioobjectinputstream |
| DES-06 | MUST | Java libraries: SnakeYAML only with `SafeConstructor`; Kryo with class registration on; fastjson with safemode; json-io in `USE_MAPS` mode; never Castor or `XMLDecoder`. | `new Yaml()` on untrusted input; `kryo.setRegistrationRequired(false)` | SEC-II-09 | des#other-deserialization-libraries-and-formats |
| DES-07 | SHOULD | Mark sensitive serializable fields `transient`; classes that must never be deserialized declare a `final readObject` that throws. | sensitive fields in `Serializable` DTOs | SEC-II-09 | des#prevent-data-leakage-and-trusted-field-clobbering, des#prevent-deserialization-of-domain-objects |
| DES-08 | SHOULD | If a native format must be accepted for known messages, deserialize only data with a verified signature. | native payloads accepted without integrity check | SEC-II-09 | des#only-deserialize-signed-data |
| DES-09 | SHOULD | .NET: when types must be embedded, restrict them with a custom `SerializationBinder` allowlist; keep known gadget types (e.g. `ObjectDataProvider`) out of services that deserialize. | `TypeNameHandling.Auto` without a binder | SEC-II-09 | des#general-precautions, des#known-net-rce-gadgets |

## Server-Side Request Forgery Prevention Cheat Sheet (SSRF)

Applies when the application makes an outbound request (HTTP client, URL fetcher, renderer, webhook sender) whose URL,
host or IP comes from untrusted data. Network-layer egress controls and cloud metadata settings (IMDSv2) in IaC are
not localized here (README "Known coverage gaps").

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| SSRF-01 | MUST | When the trusted destinations are known, accept only an identifier or host from the user, check it against an allowlist with exact matching, and build the request with a fixed scheme, port and path; don't accept full URLs. | `httpClient.GetAsync(request.Url)`; `requests.get(params["url"])`; `new URL(input).openStream()` | SEC-II-10 | ssrf#case-1-application-can-send-request-only-to-identified-and-trusted-applications, ssrf#available-protections |
| SSRF-02 | MUST | Disable automatic redirect following in the client that sends input-derived requests, so a validated request can't be bounced elsewhere. | `AllowAutoRedirect` left true; `allow_redirects=True`; `HttpClient.Redirect.ALWAYS`/`NORMAL` | SEC-II-10 | ssrf#available-protections |
| SSRF-03 | MUST | Validate IP addresses with a vetted parsing library and compare the normalized result; validate domain names for format without a DNS lookup before allowlist comparison. | regex-only IP checks; `startsWith("10.")`-style string tests | SEC-II-10 | ssrf#available-protections |
| SSRF-04 | MUST | Resolve the domain, validate every resulting IP address and connect only to the validated address, so DNS rebinding can't swap the target after the check. | host validated as a string, then the URL passed unchanged to the client | SEC-II-10 | ssrf#available-protections, ssrf#available-protections_1 |
| SSRF-05 | MUST | Allow only `http`/`https`; reject other schemes (`file`, `gopher`, `dict`, `ftp`, `jar`) and any non-HTTP fetchers on input-derived URLs. | URL scheme not checked; generic `URL.openStream()` / `urllib.request.urlopen` on input | SEC-II-10 | ssrf#overview-of-a-ssrf-common-flow, ssrf#available-protections_1 |
| SSRF-06 | MUST | When any external destination must be allowed, block internal and reserved targets after normalizing the address: cloud metadata addresses and names, loopback, private (RFC 1918) and link-local ranges, IPv6 unique-local, link-local and multicast, IPv4-mapped and NAT64 forms. Deny-lists are a last resort; prefer allowlists. | no check on resolved IP; check on the raw string only; `169.254.169.254` not blocked | SEC-II-10 | ssrf#deny-list-last-resort, ssrf#case-2-application-can-send-requests-to-any-external-ip-address-or-domain-name, ssrf#available-protections_1 |
| SSRF-07 | SHOULD | When destinations can't be allowlisted, require proof of legitimacy (a random token the target must receive) and build the request only from validated values. | webhook registration without verification token | SEC-II-10 | ssrf#available-protections_1 |
| SSRF-08 | MUST | Reject a URL whose host isn't read identically by every parser in play (the validator and the HTTP client). | validation with one URL parser, request with another; manual string splitting of URLs | SEC-II-10 | ssrf#available-protections, ssrf#challenges-in-blocking-urls-at-application-layer |

## OWASP Top 10:2025 A05 Injection (A05)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| A05-01 | REVIEW | User-supplied data is not validated, filtered or sanitized. | see IV elements | SEC-II-01 | a05#description |
| A05-02 | REVIEW | Dynamic queries or non-parameterized calls without context-aware escaping are used directly in the interpreter; hostile data is concatenated into queries, commands or stored procedures. | see SQL/INJ elements | SEC-II-02 | a05#description |
| A05-03 | REVIEW | Unsanitized data is used in ORM search parameters to extract extra records. | user-controlled filter fields/operators passed to ORM query builders | SEC-II-02 | a05#description |
| A05-04 | MUST | Prefer a safe API, a parameterized interface or an ORM; parameterized stored procedures can still inject via `EXECUTE IMMEDIATE`/`exec()`. | see QP/SQL-03 | SEC-II-03 | a05#how-to-prevent |
| A05-05 | MUST | Use positive server-side input validation (not a complete defense). | see IV-01…03 | SEC-II-01 | a05#how-to-prevent |
| A05-06 | MUST | Escape residual dynamic queries with interpreter-specific syntax; SQL structure names can't be escaped, so user-supplied structure names are dangerous. | see SQL-04 | SEC-II-03 | a05#how-to-prevent |
| A05-07 | REVIEW | NoSQL, OS command, LDAP and Expression Language/OGNL injection follow the same pattern. | EL/OGNL/SpEL evaluation of input; NoSQL operator injection | SEC-II-04 | a05#description |
