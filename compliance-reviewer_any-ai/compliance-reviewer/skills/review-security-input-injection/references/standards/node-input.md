# Node.js / Express input and injection guidance — localized summary

- Sources: cheatsheetseries.owasp.org — OWASP Node.js Security Cheat Sheet @ OWASP/CheatSheetSeries
  eeaa1e474bc2ef98119a3de7bafd067f52faf35e (2026-11-05); expressjs.com — Production Best Practices: Security (Express 5.x docs, retrieved 2026-11-09)
- Localized: 2026-11-09 · Elements: cheatsheetseries.owasp.org 5, expressjs.com 1 (prefix `NDI-`; counted in this skill's per-website budgets)
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
| NDI-01 | SHOULD | Request bodies have size limits per content type (`express.json({ limit })`, `express.urlencoded({ limit })`, `raw-body`), and the body is validated against the content type actually parsed. | `express.json()`/`bodyParser.json()` with a raised or unbounded `limit`; parsers registered for any `type` | SEC-II-01 | njs#set-request-size-limits |
| NDI-02 | SHOULD | Input is validated by allowlist before use, with type checks: `req.query`/`req.body` values can be strings, arrays or nested objects (`validator`, schema validators, `express-mongo-sanitize` for MongoDB operators); duplicated parameters are handled (`hpp`). | `req.query.x` used as a string without a type check; `{ $where … }`/`$ne` operators reaching MongoDB queries | SEC-II-01 | njs#perform-input-validation, njs#prevent-http-parameter-pollution |
| NDI-03 | MUST | Redirect targets taken from input are checked against an allowlist of hosts before `res.redirect`. | `res.redirect(req.query.url)`; `res.redirect(req.body.next)` | SEC-II-01 | exsec#prevent-open-redirects |
| NDI-04 | MUST | Output is encoded for its context: `escape-html` covers only HTML text and quoted attributes, not JavaScript, CSS or URL contexts; user HTML is sanitized with DOMPurify or `sanitize-html`; `node-esapi` isn't used. | template output with raw/unescaped tags (`<%- %>`, `{{{ }}}`, `!{}`) on user data; `escape-html` used inside `<script>` or `href` | SEC-II-08 | njs#perform-output-escaping |
| NDI-05 | MUST | `eval()`, `new Function(string)` and `node:vm` aren't used on untrusted input; `child_process.exec` (which runs through a shell) isn't given unvalidated input; file-system paths from input are validated. | `eval(req.body.x)`; `vm.runInNewContext(userCode)`; `` exec(`convert ${req.query.f}`) `` | SEC-II-04 | njs#do-not-use-dangerous-functions |
| NDI-06 | SHOULD | Regular expressions applied to input avoid nested quantifiers and overlapping alternation (ReDoS); patterns are checked with a safe-regex tool. | `new RegExp(userInput)`; patterns like `(a+)+`, `(\w+\s?)*` on request data | SEC-II-01 | njs#stay-away-from-evil-regexes, exsec#do-not-trust-user-input |
