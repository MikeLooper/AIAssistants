# Node.js / Express web and API security guidance — localized summary

- Sources: cheatsheetseries.owasp.org — OWASP Node.js Security Cheat Sheet @ OWASP/CheatSheetSeries
  eeaa1e474bc2ef98119a3de7bafd067f52faf35e (2026-11-05); expressjs.com — Production Best Practices: Security (Express 5.x docs, retrieved 2026-11-09)
- Localized: 2026-11-09 · Elements: cheatsheetseries.owasp.org 2, expressjs.com 3 (prefix `NDW-`; counted in this skill's per-website budgets)
- Applies when language `javascript` is detected and the code runs on Node.js (server code, not browser bundles);
  Express rows need `express` as a dependency. Express/helmet defaults are localized only as stated in NDW-01 and NDW-02.
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
| NDW-01 | SHOULD (Default) | `app.use(helmet())` sets, by default: `Content-Security-Policy`, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`, `Origin-Agent-Cluster`, `Referrer-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-DNS-Prefetch-Control`, `X-Download-Options`, `X-Frame-Options`, `X-Permitted-Cross-Domain-Policies`; removes `X-Powered-By`; sets `X-XSS-Protection: 0`. Each header can be reconfigured or disabled. | no `helmet` in an Express app that sets none of these headers itself; `helmet({ <header>: false })` | SEC-WA-11 | exsec#use-helmet, njs#use-appropriate-security-headers |
| NDW-02 | MUST (Default) | Express sends `X-Powered-By: Express` unless it is disabled (`app.disable('x-powered-by')`) or removed by helmet; default 404 and error responses are replaced by custom handlers. | Express app without `app.disable('x-powered-by')` and without helmet | SEC-WA-07 | exsec#reduce-fingerprinting, njs#use-appropriate-security-headers |
| NDW-03 | SHOULD | Apps handling sensitive data use TLS, typically terminated at a reverse proxy; behind a proxy, `app.set('trust proxy', …)` is set so secure cookies and protocol detection work. | `http.createServer(app)` as the only listener with no proxy/TLS config in scope | SEC-WA-06 | exsec#use-tls, exsec#dont-use-the-default-session-cookie-name |
| NDW-04 | SHOULD | A Content-Security-Policy is configured (helmet `contentSecurityPolicy` directives) and checked with a CSP evaluator. | `helmet({ contentSecurityPolicy: false })`; directives with `'unsafe-inline'` for scripts | SEC-WA-01 | njs#use-appropriate-security-headers |
| NDW-05 | SHOULD | Sensitive responses disable client caching (`nocache` middleware or equivalent `Cache-Control: no-store`). | authenticated JSON or file responses without `no-store` | SEC-WA-08 | njs#use-appropriate-security-headers |
