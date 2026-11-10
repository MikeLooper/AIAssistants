# Detection signals — Python (Security: Operational)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only on concrete code or an explicit setting (`SKILL.md` step 4). The only
Python defaults a worker may rely on are those stated in `python-operational.md` (PYO-01, PYO-03, PYO-05, PYO-08).
Flask, FastAPI, `python-dotenv`, structlog and loguru defaults are not localized: report explicit values only, and add
a `localized-standard-gap` note for a missing setting.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `DEBUG = True` in production settings; `DEBUG = os.environ.get("DEBUG", True)`-style truthy defaults | `settings*.py`, env templates | Production debug mode (always Error) | PYO-01 |
| Flask `app.run(debug=True)`, `app.debug = True`, `FLASK_DEBUG=1` in production config | app factory, Dockerfile, env files | Debug mode (Flask defaults not localized: add a gap note for missing settings) | ERR-04 |
| One `settings.py` with development values and no per-environment split | `settings*.py` | Environments not separated | SCR-02, SCR-01 |
| Literal `SECRET_KEY = "…"` | `settings*.py` | Hardcoded Django key | PYO-02 |
| Committed `.env` with real values; literal passwords/API keys in `settings*.py`/`config.py` | repository root, settings | Hardcoded secrets (`python-dotenv` itself is not a finding) | SMG-01 |
| Production settings with no `LOGGING` and no `ADMINS` | `settings*.py` | Server errors not logged anywhere visible | PYO-05 |
| `AdminEmailHandler` with `include_html: True` | `LOGGING` | Locals and settings mailed | PYO-04 |
| Login, password-change or payment views without `@sensitive_variables`/`@sensitive_post_parameters` | `views.py` | Secrets in error reports | PYO-03 |
| `except Exception: pass`, bare `except:` without logging | any code | Swallowed errors | A10-07, LOG-02 |
| `return JsonResponse({"error": str(e)})`, `traceback.format_exc()` in responses | views, API handlers | Error details sent to clients | ERR-02 |
| No `handler500` or error middleware where views return exception details | `urls.py`, middleware | No global generic handler | ERR-01 |
| `logger.info(f"…{x}")`, `logger.info("…%s" % x)`, `.format()` into logger calls | any code | Pre-formatted log messages | PYO-09, LOG-17 |
| Passwords, tokens, `request.headers`, `request.POST`, `request.body` logged | any code | Secrets or sensitive data in logs | LOG-12, LOG-13 |
| `logging.config.fileConfig`/`dictConfig` on paths or data from requests or uploads | any code | Untrusted logging configuration | PYO-06 |
| `logging.config.listen(` without `verify` | any code | Configuration via `eval()` | PYO-07 |
| Custom handlers that re-raise from `emit()`; `logging.raiseExceptions = True` set in production code | logging modules | Logging failures break the app | PYO-08, LOG-20 |
| `FileHandler` without rotation; `RotatingFileHandler(maxBytes=0)`; log files under `STATIC_ROOT`/`MEDIA_ROOT` | `LOGGING`, logging modules | Unbounded or web-accessible log files | LOG-21, LOG-22 |
| `SysLogHandler` over UDP or `HTTPHandler` with `secure=False` across networks | `LOGGING` | Logs in plaintext transit | LOG-24 |
| Security events written with `print` | admin, export, management commands | Not using the logging framework | LOG-11 |
| Permission checks that `return True` in `except` | permissions, decorators, middleware | Fail open | A10-05 |
| Multi-step ORM writes without `transaction.atomic()` | services, views | No rollback for part-way writes | A10-03, SCR-03 |
| File handles, sockets or locks without `with`/`finally` | any code | Resources not released on exceptions | A10-06 |
