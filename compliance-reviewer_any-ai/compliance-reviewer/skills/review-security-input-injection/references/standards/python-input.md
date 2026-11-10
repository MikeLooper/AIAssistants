# Python / Django input & injection guidance — localized summary

- Sources: docs.python.org — Python 3.15 documentation (3.15.2 at localization); docs.djangoproject.com — Django 6.1
  documentation (selected sections/settings only)
- Localized: 2026-11-08 · Elements: 10 — docs.python.org 4 (cap 100); docs.djangoproject.com 6 (cap 100)
- Applies when language `python` is detected. Django elements (PY-05 … PY-10) apply when `Django` is a dependency;
  CPython standard-library elements (PY-01 … PY-04) always.
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element it supports
  and name the PY element in the recommendation. Where vendor guidance is weaker than an OWASP element, the OWASP
  element decides. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only Python defaults a worker may rely on. lxml, PyYAML, Flask/Jinja2, FastAPI/Pydantic
  and SQLAlchemy defaults are **not** localized: report only explicit insecure settings there, and add a
  `localized-standard-gap` note for a missing setting. Standard-library XML parsing alone is not an XXE finding (PY-04).
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| pxml | https://docs.python.org/3.15/library/xml.html | Python 3.15 | Python 3.15 docs — xml |
| psub | https://docs.python.org/3.15/library/subprocess.html | Python 3.15 | Python 3.15 docs — subprocess |
| ppkl | https://docs.python.org/3.15/library/pickle.html | Python 3.15 | Python 3.15 docs — pickle |
| psql | https://docs.python.org/3.15/library/sqlite3.html | Python 3.15 | Python 3.15 docs — sqlite3 |
| dsec | https://docs.djangoproject.com/en/6.1/topics/security/ | Django 6.1 | Django 6.1 docs — Security in Django |
| dsql | https://docs.djangoproject.com/en/6.1/topics/db/sql/ | Django 6.1 | Django 6.1 docs — Performing raw SQL queries |
| dqs | https://docs.djangoproject.com/en/6.1/ref/models/querysets/ | Django 6.1 | Django 6.1 docs — QuerySet API |
| dset | https://docs.djangoproject.com/en/6.1/ref/settings/ | Django 6.1 | Django 6.1 docs — Settings |
| dtpl | https://docs.djangoproject.com/en/6.1/ref/templates/builtins/ | Django 6.1 | Django 6.1 docs — Built-in template tags and filters |
| dutl | https://docs.djangoproject.com/en/6.1/ref/utils/ | Django 6.1 | Django 6.1 docs — Django Utils |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| PY-01 | MUST | (Default) `subprocess` doesn't invoke a shell by default; with `shell=True` the application must quote all whitespace and metacharacters, so untrusted data with `shell=True` fails INJ-04. | `subprocess.run(f"… {v}", shell=True)`; `os.system(cmd + v)` | SEC-II-04 | psub#security-considerations |
| PY-02 | MUST | `pickle` isn't secure: only unpickle trusted data. | `pickle.loads` on request/cache/queue data | SEC-II-09 | ppkl#module-pickle |
| PY-03 | MUST | DB-API: bind values with placeholders (`?`, `:name`); never build SQL with string formatting. | `cursor.execute(f"… {v}")`; `%`-formatting into SQL | SEC-II-02 | psql#sqlite3-placeholders |
| PY-04 | MUST | (Default) Stdlib XML parsers use Expat, which doesn't access local files or the network by default; Expat < 2.7.2 is open to billion-laughs, quadratic-blowup and large-token attacks, and `xmlrpc` to decompression bombs. Stdlib parsing alone isn't an XXE finding. | explicit external-entity handlers/features enabled; `xmlrpc` server on untrusted input; pinned old Expat | SEC-II-05 | pxml#xml-vulnerabilities |
| PY-05 | MUST | (Default) QuerySets are parameterized. With `raw()`, `cursor.execute()`, `extra()` and `RawSQL`, pass parameters separately; never use string formatting or quote placeholders (`'%s'`). `extra()` is a last-resort API. | `Model.objects.raw(f"…")`; `.extra(where=["x='%s'" % v])`; `'%s'` in SQL | SEC-II-02 | dsql#passing-parameters-into-raw, dsql#executing-custom-sql-directly, dsec#sql-injection-protection, dqs#extra |
| PY-06 | MUST | (Default) Templates auto-escape HTML. `{% autoescape off %}`, `\|safe`, `mark_safe`, `is_safe` filters and unquoted attribute variables (`class={{ v }}`) with untrusted data are XSS; escaping is HTML-only. | `mark_safe(user_input)`; `{{ comment\|safe }}`; `<x attr={{ v }}>` | SEC-II-08 | dsec#cross-site-scripting-xss-protection, dtpl#safe, dtpl#autoescape, dutl#django.utils.safestring.mark_safe |
| PY-07 | MUST | Never trust user-controlled data: validate it with forms (or serializers) before use. | views reading `request.GET/POST` directly into logic without a form | SEC-II-01 | dsec#always-sanitize-user-input |
| PY-08 | MUST | (Default) `DATA_UPLOAD_MAX_MEMORY_SIZE` = 2,621,440 bytes, `DATA_UPLOAD_MAX_NUMBER_FIELDS` = 1000, `DATA_UPLOAD_MAX_NUMBER_FILES` = 100; `None` disables a check. Also limit upload size at the web server (SHOULD). | any of these set to `None` or very large | SEC-II-06 | dset#data-upload-max-memory-size, dset#data-upload-max-number-fields, dset#data-upload-max-number-files, dsec#user-uploaded-content, dsec#form-submissions |
| PY-09 | MUST | Uploaded media must not be executed by the server (e.g. `mod_php` on media); serve media from a separate top-level/second-level domain and allowlist served extensions (SHOULD); `ImageField`/Pillow doesn't stop HTML disguised as PNG. | `MEDIA_URL` on the app's own domain serving user uploads; executable handlers on media dirs | SEC-II-07 | dsec#user-uploaded-content |
| PY-10 | MUST | (Default) `FILE_UPLOAD_PERMISSIONS` defaults to `0o644`; explicit executable modes fail FU-09. | `FILE_UPLOAD_PERMISSIONS = 0o755` | SEC-II-07 | dset#file-upload-permissions |
