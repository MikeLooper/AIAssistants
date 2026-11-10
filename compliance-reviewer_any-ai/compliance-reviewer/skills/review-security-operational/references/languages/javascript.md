# Detection signals — JavaScript/TypeScript (Security: Operational)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). Logger masking defaults (`pino` `redact`, `winston` formats) and `NODE_ENV` behaviour of libraries
aren't localized: judge explicit configuration only, and add a `localized-standard-gap` note when a decision depends
on a default.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| Express app with no final `(err, req, res, next)` handler; handler sending `err.stack`/`err.message` | app setup | Default or leaky error responses | NDO-03, ERR-01 |
| `process.on('uncaughtException'` / `'unhandledRejection'` without `process.exit` | entry point | Process resumed after crash | NDO-01, A10-01 |
| `catch (e) {}`, `.catch(() => {})` with no log or rethrow | any | Swallowed errors | ERR-03, A10-07 |
| Streams/emitters without `.on('error', …)`; async handlers without `next(err)` | handlers | Unhandled errors | NDO-02 |
| `logger.info(req.body)`, `console.log(password)`, `JSON.stringify(user)` into logs | any | Secrets/PII in logs | LOG elements under SEC-OP-03 |
| `` logger.info(`login ${req.body.user}`) `` with no structured fields | any | Log injection risk | LOG elements under SEC-OP-04 |
| `const API_KEY = "sk_…"`, `password: "…"` in `config/*.js`, `.env` with values in the repo | config | Hardcoded secrets | SMG-01, SMG-02 |
| `app.use(errorhandler())` (dev error page) not gated on `NODE_ENV !== 'production'`; `DEBUG=*` in production config | app setup, env files | Debug output in production | SEC-OP-07 elements |
