# Django web and API security guidance — localized summary

- Sources: docs.djangoproject.com — Django 6.1 documentation (versioned paths `/en/6.1/`), selected sections only
- Localized: 2026-11-09 · Elements: docs.djangoproject.com 9 (cap 100)
- Applies when language `python` is detected and `Django` is a dependency. PYW-01, -02, -03, -07 and -08 need
  `django.middleware.security.SecurityMiddleware` in `MIDDLEWARE`; PYW-05 needs `XFrameOptionsMiddleware`; PYW-06
  needs `ContentSecurityPolicyMiddleware`. Flask, FastAPI and `django-cors-headers` defaults are **not** localized:
  judge explicit values only, and add `localized-standard-gap: <framework> default for <header> not localized` to
  `notes` for a missing header.
- Level: a vendor element takes the level of the OWASP element it supports, or `SHOULD` when the vendor only
  recommends. **(Default)** marks an element that states API behaviour or a default; cite the OWASP element that is
  violated and name the PYW element in the recommendation. Where vendor guidance is weaker than an OWASP element, the
  OWASP element decides; `Referrer-Policy: same-origin` (the Django default) passes HDR-04, and RST-09's
  `no-referrer` applies only to API responses that never feed Django's CSRF checks. Severity rules are in
  `../../SKILL.md`.
- Defaults stated here are the only Django header, HTTPS and CORS defaults a worker may rely on.
- Anchors: Django pages expose both `s-<slug>` and `<slug>` ids; the `<slug>` form is used. Settings use
  `std-setting-<NAME>`.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Version pin | Source name for `Finding.standard` |
|-----|---------------|-------------|------------------------------------|
| dj-mw | https://docs.djangoproject.com/en/6.1/ref/middleware/ | Django 6.1 (security, clickjacking and CSP middleware only) | Django 6.1 documentation — Middleware |
| dj-set | https://docs.djangoproject.com/en/6.1/ref/settings/ | Django 6.1 (`SECURE_*` and `X_FRAME_OPTIONS` only) | Django 6.1 documentation — Settings |
| dj-cj | https://docs.djangoproject.com/en/6.1/ref/clickjacking/ | Django 6.1 | Django 6.1 documentation — Clickjacking Protection |
| dj-csp | https://docs.djangoproject.com/en/6.1/ref/csp/ | Django 6.1 | Django 6.1 documentation — Content Security Policy |
| dj-sec | https://docs.djangoproject.com/en/6.1/topics/security/ | Django 6.1 (SSL/HTTPS, CORS and CSP sections only) | Django 6.1 documentation — Security in Django |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| PYW-01 | MUST | **(Default)** With `SecurityMiddleware` in `MIDDLEWARE`, `SECURE_CONTENT_TYPE_NOSNIFF` (default `True`) adds `nosniff` to every response that lacks it. Files served directly by the front-end server (e.g. `MEDIA_URL`) need the header there. | `SECURE_CONTENT_TYPE_NOSNIFF = False`; no `SecurityMiddleware` | SEC-WA-03 | dj-set#std-setting-SECURE_CONTENT_TYPE_NOSNIFF, dj-mw#x-content-type-options-nosniff, dj-mw#module-django.middleware.security |
| PYW-02 | MUST | **(Default)** `SECURE_HSTS_SECONDS` defaults to `0` (no HSTS). Set a non-zero value after testing; one year (`31536000`) is common. `SECURE_HSTS_INCLUDE_SUBDOMAINS` (default `False`) and `SECURE_HSTS_PRELOAD` add the directives. | production settings without `SECURE_HSTS_SECONDS` | SEC-WA-02 | dj-mw#http-strict-transport-security, dj-set#std-setting-SECURE_HSTS_SECONDS, dj-set#std-setting-SECURE_HSTS_INCLUDE_SUBDOMAINS |
| PYW-03 | MUST | **(Default)** `SECURE_SSL_REDIRECT` defaults to `False`. Set it to `True` (permanent redirect) unless the front-end server redirects. `SECURE_REDIRECT_EXEMPT` keeps matching URLs on HTTP. | production settings without a redirect; broad `SECURE_REDIRECT_EXEMPT` | SEC-WA-06 | dj-mw#ssl-redirect, dj-set#std-setting-SECURE_SSL_REDIRECT, dj-sec#ssl-https |
| PYW-04 | MUST | Set `SECURE_PROXY_SSL_HEADER` only behind a proxy that controls that header. A wrong setting can cause CSRF vulnerabilities. | the setting with no proxy in the deployment files | SEC-WA-06 | dj-set#std-setting-SECURE_PROXY_SSL_HEADER, dj-sec#ssl-https |
| PYW-05 | MUST | **(Default)** `XFrameOptionsMiddleware` (included by `startproject`) sets `X-Frame-Options` to `X_FRAME_OPTIONS` (default `DENY`). `@xframe_options_exempt` removes it for a view. | middleware removed; `@xframe_options_exempt` on views with forms or actions | SEC-WA-04 | dj-cj#setting-x-frame-options-for-all-responses, dj-cj#setting-x-frame-options-per-view, dj-set#std-setting-X_FRAME_OPTIONS |
| PYW-06 | MUST | **(Default)** Django 6.0+ `ContentSecurityPolicyMiddleware` sends CSP from `SECURE_CSP` (default `{}`, meaning no header) and Report-Only from `SECURE_CSP_REPORT_ONLY`, which alone gives no protection. Use `CSP.NONCE` for nonces, and don't exclude paths from the policy. | no CSP middleware or empty `SECURE_CSP`; Report-Only only; per-view exemptions | SEC-WA-01 | dj-csp#settings, dj-mw#content-security-policy-middleware, dj-set#std-setting-SECURE_CSP, dj-sec#limitations-and-considerations |
| PYW-07 | SHOULD | **(Default)** `SECURE_REFERRER_POLICY` defaults to `'same-origin'`. Don't disable `Referer` completely, because HTTPS CSRF checks need it. | `SECURE_REFERRER_POLICY = None` or `"unsafe-url"` | SEC-WA-11 | dj-set#std-setting-SECURE_REFERRER_POLICY, dj-mw#referrer-policy |
| PYW-08 | SHOULD | **(Default)** `SECURE_CROSS_ORIGIN_OPENER_POLICY` defaults to `'same-origin'`; `None` or `unsafe-none` turns it off. | `SECURE_CROSS_ORIGIN_OPENER_POLICY = None` | SEC-WA-11 | dj-set#std-setting-SECURE_CROSS_ORIGIN_OPENER_POLICY, dj-mw#cross-origin-opener-policy |
| PYW-09 | MUST | **(Default)** Django has no built-in CORS support; CORS headers come only from third-party packages, which aren't localized. | CORS package settings: judge explicit values only; gap note for package defaults | SEC-WA-05 | dj-sec#cross-origin-resource-sharing-cors |
