# Python / Django operational security guidance — localized summary

- Sources: docs.djangoproject.com — Django 6.1 documentation (selected pages/settings); docs.python.org — Python 3.15
  documentation (3.15.2 at localization)
- Localized: 2026-11-08 · Elements: 9 — docs.djangoproject.com 5 (cap 100); docs.python.org 4 (cap 100)
- Applies when language `python` is detected. Django elements (PYO-01 … PYO-05) apply when `Django` is a dependency;
  CPython `logging` elements (PYO-06 … PYO-09) always.
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element it supports
  and name the PYO element in the recommendation. Where vendor guidance is weaker than an OWASP element, the OWASP
  element decides. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only Python defaults a worker may rely on. Flask (`debug`, `PROPAGATE_EXCEPTIONS`),
  FastAPI exception handlers, `python-dotenv`, structlog and loguru defaults are **not** localized: report only explicit
  insecure settings there (e.g. `app.run(debug=True)` fails ERR-04), and add a `localized-standard-gap` note for a
  missing setting.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| dj-set | https://docs.djangoproject.com/en/6.1/ref/settings/ | Django 6.1 (`DEBUG` only) | Django 6.1 docs — Settings |
| dj-dep | https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/ | Django 6.1 | Django 6.1 docs — Deployment checklist |
| dj-err | https://docs.djangoproject.com/en/6.1/howto/error-reporting/ | Django 6.1 | Django 6.1 docs — How to manage error reporting |
| dj-log | https://docs.djangoproject.com/en/6.1/topics/logging/ | Django 6.1 | Django 6.1 docs — Logging |
| dj-rlog | https://docs.djangoproject.com/en/6.1/ref/logging/ | Django 6.1 (default configuration only) | Django 6.1 docs — Logging reference |
| py-cfg | https://docs.python.org/3.15/library/logging.config.html | Python 3.15 | Python 3.15 docs — logging.config |
| py-how | https://docs.python.org/3.15/howto/logging.html | Python 3.15 | Python 3.15 docs — Logging HOWTO |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| PYO-01 | MUST | Never run production with `DEBUG = True`. The default is `False`, but `startproject` sets `True`. Debug pages expose tracebacks, environment metadata and settings (only names containing API, KEY, PASS, SECRET, SIGNATURE or TOKEN are hidden), and debug mode keeps every SQL query in memory. | `DEBUG = True` in production settings; `DEBUG` defaulting to `True` from env | SEC-OP-07 | dj-dep#debug, dj-set#debug |
| PYO-02 | MUST | `SECRET_KEY` is a large random value, kept secret, not reused, not committed; load it from an environment variable or file; remove old keys from `SECRET_KEY_FALLBACKS` promptly. | literal `SECRET_KEY = "…"` in settings | SEC-OP-05 | dj-dep#secret-key |
| PYO-03 | SHOULD | **(Default)** Error reports include the full traceback, each frame's local variables and request attributes. Use `sensitive_variables()` and `sensitive_post_parameters()` on views handling passwords, card numbers or similar. | login/payment views without the decorators | SEC-OP-03 | dj-err#filtering-sensitive-information, dj-log#security-implications |
| PYO-04 | SHOULD | Error reports go only to trusted team members and aren't sent unencrypted; avoid `AdminEmailHandler(include_html=True)`, which mails locals and settings. | `include_html: True` in `LOGGING` | SEC-OP-03 | dj-err#filtering-error-reports, dj-log#adminemailhandler |
| PYO-05 | MUST | **(Default)** With `DEBUG = False`, the default config sends `django` ERROR/CRITICAL records only to `AdminEmailHandler` (requires `ADMINS`); the console handler requires `DEBUG = True`. Review `LOGGING` before production. | production settings with no `LOGGING` and no `ADMINS` | SEC-OP-02 | dj-rlog#default-logging-configuration, dj-dep#logging |
| PYO-06 | MUST | Never load logging configuration (`fileConfig`, `dictConfig`) from untrusted sources: it can import and call arbitrary code. | config path or dict taken from request/user input | SEC-OP-09 | py-cfg#security-considerations |
| PYO-07 | SHOULD | Avoid `logging.config.listen()` on hosts with untrusted local users, or pass a `verify` callable: received configuration goes through `eval()`. | `logging.config.listen(` without `verify` | SEC-OP-09 | py-cfg#logging.config.listen |
| PYO-08 | SHOULD | **(Default)** `logging.raiseExceptions` defaults to `True` (handler errors print tracebacks to stderr); set it to `False` in production. Handler errors are otherwise swallowed so logging can't terminate the app. | custom handlers that re-raise from `emit()` | SEC-OP-09 | py-how#exceptions-raised-during-logging |
| PYO-09 | SHOULD | Log variable data as a format string plus arguments (`logger.info("user %s", uid)`), not pre-formatted strings. | f-strings or `%`-formatted strings passed to logger calls | SEC-OP-04 | py-how#logging-variable-data |
