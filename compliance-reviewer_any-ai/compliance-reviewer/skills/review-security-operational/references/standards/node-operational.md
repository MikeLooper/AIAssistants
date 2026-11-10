# Node.js / Express operational security guidance — localized summary

- Sources: cheatsheetseries.owasp.org — OWASP Node.js Security Cheat Sheet @ OWASP/CheatSheetSeries
  eeaa1e474bc2ef98119a3de7bafd067f52faf35e (2026-11-05); expressjs.com — Production Best Practices: Security (Express 5.x docs, retrieved 2026-11-09)
- Localized: 2026-11-09 · Elements: cheatsheetseries.owasp.org 5, expressjs.com 1 (prefix `NDO-`; counted in this skill's per-website budgets)
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
| NDO-01 | MUST | A `process.on('uncaughtException')` handler, if present, cleans up, logs the error and exits; the process isn't resumed after an uncaught exception, and stack traces aren't shown to users. | `process.on('uncaughtException', e => console.log(e))` with no exit | SEC-OP-10 | njs#handle-uncaughtexception |
| NDO-02 | SHOULD | `error` events are always listened to on EventEmitters and streams, and async errors are propagated (an `Error` as the first callback argument; Express handlers pass errors to `next(err)`, since Express doesn't catch errors that never reach it). | streams or emitters without `.on('error')`; async route handlers without `try/catch`→`next(err)` or a wrapper on Express 4 | SEC-OP-02 | njs#listen-to-errors-when-using-eventemitter, njs#handle-errors-in-asynchronous-calls |
| NDO-03 | MUST | The default Express 404 and error responses are replaced by custom handlers that return generic messages. | no final `(err, req, res, next)` handler; handler sending `err.stack` or `err.message` | SEC-OP-01 | exsec#reduce-fingerprinting, njs#handle-uncaughtexception |
| NDO-04 | SHOULD | Application activity is logged through a logging library (`winston`, `bunyan`, `pino`) with separate destinations for errors and general logs, not ad-hoc `console.log`. | security-relevant events only in `console.log`; no logger configured | SEC-OP-08 | njs#perform-application-activity-logging |
| NDO-05 | SHOULD | Unused routes, including framework auto-generated REST endpoints (Sails blueprints, Feathers services), are disabled. | Sails `blueprints` actions/rest enabled for models that don't need them | SEC-OP-07 | njs#remove-unnecessary-routes |
