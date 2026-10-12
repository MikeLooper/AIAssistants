# Language Guidance — Python (Security)

OWASP has no Python-specific security cheat sheet; use general guidance.

- Secrets via environment variables (`os.environ`), `python-dotenv` for local dev only, or a secret manager — never committed in `settings.py`/`config.py`.
- Use the `logging` module with parameterized formatting (`logger.info("User %s", user_id)`), not f-strings that could leak secrets into log records.
- Framework debug mode (`DEBUG = True` in Django, `app.debug = True` in Flask) must be off in production so stack traces aren't returned to clients.
