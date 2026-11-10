# Detection signals — Python (Security: Web & API)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only on concrete code or an explicit setting; a missing header follows the
evidence rule in `SKILL.md` step 3. The only Django defaults a worker may rely on are those stated in
`python-web-api.md` (PYW-01 … PYW-03, PYW-05 … PYW-09). Flask, FastAPI and `django-cors-headers` defaults are not
localized: report explicit values only, and add a `localized-standard-gap` note for a missing header.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `MIDDLEWARE` without `django.middleware.security.SecurityMiddleware` | `settings*.py` | nosniff, HSTS, redirect, Referrer-Policy and COOP support off | PYW-01, HDR-03 |
| `MIDDLEWARE` without `django.middleware.clickjacking.XFrameOptionsMiddleware` (HTML apps) | `settings*.py` | No framing protection | PYW-05, HDR-01 |
| `MIDDLEWARE` without `ContentSecurityPolicyMiddleware` (Django ≥ 6.0, HTML apps); `SECURE_CSP` empty; only `SECURE_CSP_REPORT_ONLY` set | `settings*.py` | No enforced CSP | PYW-06, CSP-01 |
| `SECURE_CSP` with `CSP.UNSAFE_INLINE`/`CSP.UNSAFE_EVAL` (or the literal strings) in `script-src` | `settings*.py` | Weak CSP | PYW-06, CSP-05 |
| Production settings without `SECURE_HSTS_SECONDS`, or a value below `31536000`; `SECURE_HSTS_INCLUDE_SUBDOMAINS` absent | `settings*.py` (production module) | Missing or short HSTS | PYW-02, HST-01, HST-02 |
| `SECURE_SSL_REDIRECT` absent or `False` with no front-end redirect in the files; broad `SECURE_REDIRECT_EXEMPT` | `settings*.py`, proxy config | HTTP not redirected | PYW-03, TLS-03 |
| `SECURE_PROXY_SSL_HEADER` set with no proxy in the deployment files | `settings*.py`, `Dockerfile`, compose | Spoofable HTTPS detection | PYW-04 |
| `SECURE_CONTENT_TYPE_NOSNIFF = False` | `settings*.py` | nosniff removed | PYW-01, HDR-03 |
| `X_FRAME_OPTIONS` other than `DENY`/`SAMEORIGIN`; `@xframe_options_exempt` on views with forms or actions | `settings*.py`, views | Framing allowed | PYW-05, HDR-01 |
| `SECURE_REFERRER_POLICY = None` or `"unsafe-url"` | `settings*.py` | Referrer policy off or harmful | PYW-07, HDR-04 |
| `SECURE_CROSS_ORIGIN_OPENER_POLICY = None` or `"unsafe-none"` | `settings*.py` | COOP off | PYW-08, HDR-10 |
| `corsheaders` settings: `CORS_ALLOW_ALL_ORIGINS = True` (or legacy `CORS_ORIGIN_ALLOW_ALL`); `CORS_ALLOW_CREDENTIALS = True` with broad `CORS_ALLOWED_ORIGIN_REGEXES` (explicit values only; gap note for package defaults) | `settings*.py` | Any-origin or credentialed broad CORS | PYW-09, H5-01, H5-02 |
| Views setting `Access-Control-Allow-Origin` from `request.headers["Origin"]`; authorization on `Origin` | views, middleware | Reflected origin; CORS as access control | H5-01, H5-03 |
| `response["X-Powered-By"] = …`; informative `Server` value set | views, middleware | Version-revealing headers | HDR-15, HDR-14 |
| `X-XSS-Protection: 1`, `Expect-CT`, `Public-Key-Pins` set in middleware | middleware | Harmful headers | HDR-02, HDR-08, HDR-18 |
| `request.GET["token"\|"api_key"\|"password"]`; `requests.get(f"...?api_key={key}")` | views, clients | Credentials in URLs | RST-11, RST-12 |
| `HttpResponse(json.dumps(...))` without `content_type="application/json"` (the Django default content type is not localized: gap note unless the files show `text/html`) | views | JSON with wrong type | RST-06 |
| `FileResponse(..., as_attachment=False)` or `HttpResponse(upload.read(), content_type=upload.content_type)` for user files | views | Inline download of user files | HDR-19 |
| `@require_http_methods` absent is **not** evidence (method defaults not localized); explicit `http_method_names` including `trace` is | views | Any-method handler | RST-02 |
| `ssl.SSLContext` with `minimum_version` below `TLSVersion.TLSv1_2` in a server | server code | Legacy TLS | TLS-01 |
| Flask/FastAPI: `CORSMiddleware(allow_origins=["*"], allow_credentials=True)`, `CORS(app, supports_credentials=True)` with `*`; explicit header code | app factory, `main.py` | Any-origin credentialed CORS (judge explicit values; missing headers → gap note) | H5-01, HDR-09 |
