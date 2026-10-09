# Language Guidance — Python (Security)

OWASP has no Python-specific security cheat sheet; use general guidance.

- Use the ORM's parameter binding (Django ORM, SQLAlchemy `text()` with bound params) — flag any f-string/`%`-formatted SQL passed to `cursor.execute`.
- `defusedxml` (or `lxml` with `resolve_entities=False`) instead of the stdlib `xml.etree.ElementTree`/`xml.dom.minidom` for untrusted XML.
- File uploads validated for content-type/size (e.g. Django's `FileField` validators, FastAPI `UploadFile` checks) and stored with generated names outside any static-serving directory.
