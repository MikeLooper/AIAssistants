# Django authentication & session guidance — localized summary

- Source: docs.djangoproject.com — Django **6.1** documentation (versioned URLs; `/en/stable/` redirected to `/en/6.1/`
  at snapshot). Setting defaults were read from `ref/settings/` on 2026-11-08.
- Localized: 2026-11-08 · Elements: docs.djangoproject.com 11 (cap 100)
- Applies when `Django` is a dependency. Flask/FastAPI defaults are **not** localized: report only explicit insecure
  settings there, and add a `localized-standard-gap` note for a missing setting.
- Framework elements apply only when that framework is in use; otherwise they don't apply.
- Level: a framework element takes the level of the OWASP element it implements (e.g. a cookie-flag setting implements
  SES-04/SES-05), or `SHOULD` when the vendor only recommends. Severity rules are in `../../SKILL.md`.
- Defaults stated here are the only framework defaults a worker may rely on. Never use remembered defaults.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Source name for `Finding.standard` |
|-----|---------------|------------------------------------|
| auth | https://docs.djangoproject.com/en/6.1/topics/auth/default/ | Django 6.1 documentation |
| pwd | https://docs.djangoproject.com/en/6.1/topics/auth/passwords/ | Django 6.1 documentation |
| sess | https://docs.djangoproject.com/en/6.1/topics/http/sessions/ | Django 6.1 documentation |
| set | https://docs.djangoproject.com/en/6.1/ref/settings/ | Django 6.1 documentation |
| csrf | https://docs.djangoproject.com/en/6.1/ref/csrf/ | Django 6.1 documentation |
| mw | https://docs.djangoproject.com/en/6.1/ref/middleware/ | Django 6.1 documentation |
| dep | https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/ | Django 6.1 documentation |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| DJ-01 | MUST | Protect views by default with `LoginRequiredMiddleware` (public views marked `login_not_required`), or apply `login_required`/`LoginRequiredMixin` to every non-public view. | protected views without decorator/mixin and no `LoginRequiredMiddleware` | SEC-IA-01 | mw#django.contrib.auth.middleware.LoginRequiredMiddleware, auth#limiting-access-to-logged-in-users |
| DJ-02 | MUST | Sensitive actions check permissions (`permission_required`, `PermissionRequiredMixin`, `user.has_perm`), not only login. | admin-like views with `login_required` only | SEC-IA-02 | auth#the-permission-required-decorator, auth#permissions-and-authorization |
| DJ-03 | MUST | The first `PASSWORD_HASHERS` entry is an adaptive hasher (default PBKDF2-SHA256; Argon2 recommended); no MD5/unsalted/SHA1 hasher first. | `MD5PasswordHasher`/`UnsaltedMD5PasswordHasher` first | SEC-IA-06 | pwd#how-django-stores-passwords, pwd#included-hashers |
| DJ-04 | MUST | Configure `AUTH_PASSWORD_VALIDATORS`: the default is **empty (no validation)**. Include `MinimumLengthValidator` (length per ATN-02) and `CommonPasswordValidator`. | setting absent or empty | SEC-IA-10 | pwd#enabling-password-validation, set#auth-password-validators |
| DJ-05 | MUST | Set `SESSION_COOKIE_SECURE = True` (default **`False`**). | setting absent or `False` in production settings | SEC-IA-05 | dep#session-cookie-secure, set#session-cookie-secure |
| DJ-06 | MUST | Keep `CsrfViewMiddleware` enabled and set `CSRF_COOKIE_SECURE = True` (default **`False`**); `csrf_exempt` only on endpoints that don't use cookie auth. | middleware removed; `csrf_exempt` on session-auth views | SEC-IA-05 | csrf#how-it-works, dep#csrf-cookie-secure, set#csrf-cookie-secure |
| DJ-07 | MUST | Keep `SESSION_COOKIE_HTTPONLY = True` (default `True`) and `SESSION_COOKIE_SAMESITE` `'Lax'` (default) or `'Strict'`, never `'None'`/`False`. | `SESSION_COOKIE_HTTPONLY = False`; SameSite `'None'` | SEC-IA-05 | set#session-cookie-httponly, set#session-cookie-samesite |
| DJ-08 | SHOULD | Set `SESSION_COOKIE_AGE` to fit the application's risk (default **1209600 s = 2 weeks**, persistent cookie). | default age on a high-value application | SEC-IA-05 | set#session-cookie-age, sess#browser-length-sessions-vs-persistent-sessions |
| DJ-09 | MUST | Log in with `auth.login()` (cycles the session key) and log out with `auth.logout()` (flushes); custom password-change views call `update_session_auth_hash`; custom session handling calls `cycle_key()` on privilege change. | manual `request.session['user_id'] = …`; custom logout without `flush()` | SEC-IA-05 | auth#how-to-log-a-user-in, auth#how-to-log-a-user-out, auth#session-invalidation-on-password-change |
| DJ-10 | SHOULD | With the `signed_cookies` session engine, session data is client-readable and has no freshness guarantee: store no sensitive data in it. | `SESSION_ENGINE = signed_cookies` with sensitive session values | SEC-IA-05 | sess#using-cookie-based-sessions |
| DJ-11 | SHOULD | Don't widen `SESSION_COOKIE_DOMAIN` to subdomains you don't control (subdomain session fixation). | `SESSION_COOKIE_DOMAIN = ".example.com"` | SEC-IA-05 | sess#session-security, set#session-cookie-domain |
