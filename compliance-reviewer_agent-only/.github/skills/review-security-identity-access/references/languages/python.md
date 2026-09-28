# Language Guidance — Python (Security)

OWASP has no Python-specific security cheat sheet; use general guidance.

- Use a maintained framework's auth (Django auth, Flask-Login/Flask-Security, FastAPI's `OAuth2PasswordBearer`/`Depends`) rather than custom session handling.
- Password hashing via `passlib`/`argon2-cffi`/Django's built-in hashers, not `hashlib.md5`/`sha1` directly.
- JWT libraries (`PyJWT`, `authlib`) must have `verify_signature`/`verify_exp` enabled — check for `verify=False` or algorithm `none` left in code.
- Session/cookie flags (`SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE`) set appropriately in framework settings.
