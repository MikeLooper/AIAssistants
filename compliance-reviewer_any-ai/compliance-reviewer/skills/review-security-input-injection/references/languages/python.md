# Detection signals — Python (Security: Input & Injection)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only when untrusted data reaches it or the setting is explicit (`SKILL.md`
step 3). The only Python defaults a worker may rely on are those stated in `python-input.md` (PY-01, PY-04, PY-05,
PY-06, PY-08, PY-10). lxml, PyYAML, Flask/Jinja2, FastAPI/Pydantic and SQLAlchemy defaults are not localized: report
explicit values only, and add a `localized-standard-gap` note for a missing setting. Standard-library XML parsing
(`xml.etree`, `xml.dom.minidom`, `xml.sax`) alone is not an XXE finding.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `cursor.execute(f"…")`, `%`/`.format()` into SQL; `sqlite3`/DB-API calls without a parameters argument | data access, scripts | SQL built from untrusted values | PY-03, SQL-01 |
| `Model.objects.raw(f"…")`, `.extra(where=[… % v])`, `RawSQL(f"…")`, quoted `'%s'` placeholders | Django models, managers, views | Raw SQL misuse | PY-05, SQL-01 |
| SQLAlchemy `text(f"…")` / `session.execute(f"…")` | repositories | SQL built from untrusted values | SQL-01 |
| `order_by(request.GET[…])` or table names from input | views, query helpers | Unallowlisted identifiers | SQL-04 |
| `DATABASES` `USER` = `postgres`/`root`/`sa` | `settings.py`, env templates | Over-privileged database account | SQL-07 |
| `subprocess.*(…, shell=True)` with input; `os.system`, `os.popen` with input | services, tasks | Command injection | PY-01, INJ-04, INJ-05 |
| `eval`, `exec`, `compile` on input; `render_template_string(input)` | views, services | Code/template injection | INJ-03 |
| `ldap3`/`python-ldap` filters or `lxml` XPath built by concatenation; Mongo `$where`/raw JSON queries from input | directory, XML, NoSQL code | LDAP/XPath/NoSQL injection | INJ-06 |
| `pickle.load(s)`, `shelve`, `marshal` on external data | caches, consumers, views | Unsafe deserialization | PY-02, DES-01 |
| `jsonpickle.decode`, `yaml.load(…, Loader=yaml.Loader/UnsafeLoader/FullLoader)`, `yaml.unsafe_load` | config loaders, consumers | Unsafe deserialization | DES-04 |
| `xml.sax` with `feature_external_ges` enabled; custom `EntityResolver` fetching URLs; `xmlrpc.server` exposed to untrusted callers | XML code, RPC servers | External entities / decompression bombs | PY-04, XML-01, XML-02 |
| lxml `etree.XMLParser(resolve_entities=True, no_network=False, huge_tree=True, recover=True)` (explicit values only) | XML code | Insecure parser options | XML-01, XML-02, XML-03 |
| `mark_safe(`, `\|safe`, `{% autoescape off %}`, `format_html` with pre-formatted user strings, unquoted `{{ }}` in attributes | templates, template tags, views | Encoding bypassed | PY-06, XSS-02, XSS-03 |
| Flask/Jinja2 `Markup(input)`, `\|safe`, `autoescape=False` | templates, views | Escape hatch (Flask/Jinja2 not localized; note gap for defaults) | XSS-02 |
| User data inside `<script>` blocks without `json_script`/`escapejs` | templates | Wrong-context encoding | XSS-04 |
| Views reading `request.POST[…]`/`request.GET[…]` into logic without a `Form`/serializer | views | Missing validation | PY-07, IV-01 |
| `ModelForm` with `fields = "__all__"` or `exclude` on sensitive models | forms | Mass assignment | IV-07 |
| `DATA_UPLOAD_MAX_MEMORY_SIZE`, `DATA_UPLOAD_MAX_NUMBER_FIELDS` or `DATA_UPLOAD_MAX_NUMBER_FILES` set to `None` or very large | `settings.py` | Request/upload limits removed | PY-08, FU-05 |
| `FILE_UPLOAD_PERMISSIONS` with execute bits (e.g. `0o755`) | `settings.py` | Executable uploads | PY-10, FU-09 |
| `MEDIA_URL` on the application's own domain; web server handlers (`mod_php`, CGI) active on `MEDIA_ROOT` | `settings.py`, server config | Uploads served as active content | PY-09, FU-07 |
| `uploaded_file.name` used in the storage path; type decided by `content_type` only | upload views, storage code | Client filename/type trusted | FU-04, FU-03 |
| `zipfile.extractall` without size/entry checks | import/upload code | Zip bomb | FU-05 |
| `re.match` used for full validation instead of `re.fullmatch`; nested quantifiers on unbounded input | validators | Partial match / ReDoS | IV-08 |
