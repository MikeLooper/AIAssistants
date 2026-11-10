# Detection signals — JavaScript/TypeScript (Security: Identity & Access)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). Passport, NextAuth/Auth.js, `jsonwebtoken`, `jose` and NestJS guard defaults aren't localized: judge
explicit code and settings only, and add a `localized-standard-gap` note when a decision depends on a default.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| Router or app without auth middleware before protected routes; `app.use(passport.authenticate(...))` only on some routers | app setup, routers | No deny-by-default | ATZ-02 |
| Handler loading a record by `req.params.id` without checking the owner or tenant | handlers | IDOR | SEC-IA-02 elements (ATZ, T10) |
| `jwt.verify(token, key)` without `algorithms`; `jwt.decode` used for trust; `ignoreExpiration: true` | auth code | JWT not verified properly | JWT-01 and the other SEC-IA-03 elements |
| `express-session` options: `secure: false`, `httpOnly: false`, no `sameSite`, no `name`, no `store` | app setup | Weak session cookie / memory store | NDA-01, NDA-02, SES-04, SES-05, SES-06 |
| `csurf` dependency; state-changing routes with session auth and no CSRF token | `package.json`, routes | CSRF | NDA-04 |
| Login route without `rate-limiter-flexible`/`express-rate-limit`/lockout | auth routes | Brute force | NDA-03, ATN-12 |
| `bcrypt.hash(pw, <10)`, `crypto.createHash('sha256').update(password)`, `md5(password)` | user code | Weak password hashing | PWS-01 |
| `localStorage.setItem('token', …)`, `sessionStorage` for tokens | front-end files | Token in web storage | SES-17 |
| `req.session.regenerate` absent after login | auth code | No session rotation | SES-11 |
