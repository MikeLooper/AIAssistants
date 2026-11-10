# Detection signals — Python (Security: Identity & Access)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). DJ elements apply only when Django is a dependency. Flask and FastAPI defaults are not localized:
report only explicit insecure values there; a missing setting gets a `localized-standard-gap` note, not a finding.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `MIDDLEWARE` without `LoginRequiredMiddleware`, and non-public views without `login_required`/`LoginRequiredMixin` | `settings.py`, views | No deny-by-default | DJ-01, ATZ-02 |
| Admin-like views protected only by `login_required` (no `permission_required`, `PermissionRequiredMixin`, `has_perm`) | views | Missing function-level authorization | DJ-02 |
| `Model.objects.get(pk=...)` returned without filtering by `request.user`/tenant | views, serializers, DRF viewsets | IDOR | ATZ-04 |
| First `PASSWORD_HASHERS` entry `MD5PasswordHasher`, `UnsaltedMD5PasswordHasher` or another non-adaptive hasher | `settings.py` | Weak password storage | DJ-03 |
| `AUTH_PASSWORD_VALIDATORS` absent or `[]` (default is empty) | `settings.py` | No password validation | DJ-04 |
| `SESSION_COOKIE_SECURE` absent or `False` (default `False`) in production settings | `settings.py` | Session cookie without Secure | DJ-05 |
| `CsrfViewMiddleware` removed; `csrf_exempt` on session-authenticated views; `CSRF_COOKIE_SECURE` absent or `False` | `settings.py`, views | Missing CSRF defense | DJ-06 |
| `SESSION_COOKIE_HTTPONLY = False`; `SESSION_COOKIE_SAMESITE = 'None'` or `False` | `settings.py` | Insecure cookie flags | DJ-07 |
| `SESSION_COOKIE_AGE` left at default (2 weeks) on a high-value app; `SESSION_EXPIRE_AT_BROWSER_CLOSE` unset | `settings.py` | Long-lived sessions | DJ-08 |
| `request.session['user_id'] = ...` instead of `auth.login()`; custom logout without `flush()`; password change without `update_session_auth_hash` | views | Session fixation / incomplete logout | DJ-09 |
| `SESSION_ENGINE = '...signed_cookies'` with sensitive values in the session | `settings.py`, views | Client-readable session data | DJ-10 |
| `SESSION_COOKIE_DOMAIN = '.example.com'` | `settings.py` | Overly broad cookie domain | DJ-11 |
| PyJWT `jwt.decode(..., options={"verify_signature": False})`; `jwt.decode` without key; `algorithms` missing or containing `"none"` | token code | Signature not verified | JWT-01 |
| `algorithms` built from `jwt.get_default_algorithms()` or the token header; RS\* and HS\* accepted together | token code | Algorithm confusion | JWT-02 |
| PyJWT decode without `issuer=`/`audience=` arguments (the `verify_iss`/`verify_aud` options do nothing without them); `options={"verify_aud": False}`/`{"verify_exp": False}` | token code | `iss`/`aud`/`exp` not validated | JWT-04, JWT-05, JWT-06 |
| `python-jose`/`authlib` equivalents: `jwt.decode(..., options={"verify_signature": False})`, `claims.validate()` never called | token code | Unverified JWT | JWT-01…06 |
| `hashlib.md5/sha1/sha256(password...)` | user/auth code | Fast hash on password | PWS-01 |
| `passlib`/`argon2-cffi`/`bcrypt` parameters (`rounds`, `time_cost`, `memory_cost`) | auth code, config | Work factor vs. table | PWS-02…05 |
| Flask/FastAPI explicit `SESSION_COOKIE_SECURE=False`, `SESSION_COOKIE_HTTPONLY=False`, `SESSION_COOKIE_SAMESITE=None`; `set_cookie(..., secure=False, httponly=False)` for auth cookies | app config, auth code | Insecure cookie flags | SES-04, SES-05, SES-06 |
| `random`/`uuid.uuid1` used for session IDs, reset tokens or signing secrets (instead of `secrets`) | auth code | Weak randomness | SES-02, JWT-08 |
