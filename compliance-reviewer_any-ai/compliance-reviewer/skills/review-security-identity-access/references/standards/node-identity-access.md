# Node.js / Express identity and access guidance — localized summary

- Sources: cheatsheetseries.owasp.org — OWASP Node.js Security Cheat Sheet @ OWASP/CheatSheetSeries
  eeaa1e474bc2ef98119a3de7bafd067f52faf35e (2026-11-05); expressjs.com — Production Best Practices: Security (Express 5.x docs, retrieved 2026-11-09)
- Localized: 2026-11-09 · Elements: cheatsheetseries.owasp.org 3, expressjs.com 2 (prefix `NDA-`; counted in this skill's per-website budgets)
- Applies when language `javascript` is detected and the code runs on Node.js (server code, not browser bundles);
  Express rows need `express` as a dependency. 
- Level: `MUST` where the source says must/must not/never/do not or gives an unqualified imperative; `SHOULD` for
  should/recommended/encouraged/"consider". **(Default)** marks an element that states library behaviour or a default;
  cite the OWASP element that is violated and name this element in the recommendation. Defaults stated here are the
  only Node.js/Express defaults a worker may rely on. Severity rules are in `../../SKILL.md`.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Pinned version | Source name for `Finding.standard` |
|-----|---------------|----------------|------------------------------------|
| njs | https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html | eeaa1e47 (2026-11-05) | OWASP Node.js Security Cheat Sheet |
| exsec | https://expressjs.com/en/advanced/best-practice-security.html | page at retrieval 2026-11-09 (Express 5.x docs) | Express — Production Best Practices: Security |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| NDA-01 | SHOULD | Session cookies set `httpOnly`, `secure` and `sameSite` (`express-session`/`cookie-session` `cookie` options) and don't use the default session cookie name; `trust proxy` is set when TLS terminates at a proxy. | `session({ cookie: { secure: false } })`; no `name` (default `connect.sid`); `httpOnly: false` | SEC-IA-05 | njs#set-cookie-flags-appropriately, exsec#set-cookie-security-options, exsec#dont-use-the-default-session-cookie-name |
| NDA-02 | MUST (Default) | `express-session`'s default in-memory store isn't designed for production; production uses a shared session store. `cookie-session` keeps the whole session in a client-visible cookie, so it holds only small, non-sensitive data. | `session({ … })` with no `store` in production code; tokens or roles kept in `cookie-session` | SEC-IA-05 | exsec#use-cookies-securely |
| NDA-03 | SHOULD | Login is protected against brute force: blocking by consecutive failures per username+IP and by total failures per IP over a long period (`rate-limiter-flexible`, `express-brute`, account lockout). | login route with no limiter or lockout | SEC-IA-09 | exsec#prevent-brute-force-attacks-against-authorization, njs#take-precautions-against-brute-forcing |
| NDA-04 | MUST | Cookie-authenticated state changes use the framework's CSRF defence or maintained token middleware; the archived `csurf` package isn't used, and `SameSite` isn't the only mitigation. | `csurf` in `dependencies`; POST/PUT/DELETE routes behind session auth with no CSRF token check | SEC-IA-05 | njs#use-anti-csrf-tokens |
| NDA-05 | SHOULD | Access is granted by least privilege through roles or ACLs checked on the server (e.g. role middleware on each protected router). | admin routes guarded only by a client-side flag | SEC-IA-02 | njs#use-access-control-lists |
