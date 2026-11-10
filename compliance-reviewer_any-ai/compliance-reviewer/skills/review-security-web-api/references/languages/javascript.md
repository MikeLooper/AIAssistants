# Detection signals — JavaScript/TypeScript (Security: Web & API)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). Only the Express/helmet defaults stated in `node-web-api.md` (NDW-01, NDW-02) may be relied on;
other frameworks (Fastify, NestJS, Next.js, Koa) and the `cors` package defaults aren't localized: judge explicit values
only and add a `localized-standard-gap` note for a missing header. Browser bundles (React, Angular, Vue) set no response
headers; judge the server or hosting config that serves them.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| Express app without `helmet()` and without its own header middleware | `app.js`, `server.ts`, `index.js` | No security headers (HSTS, nosniff, framing, policy headers) | NDW-01, HDR-03, HDR-01, HST-01 |
| `helmet({ contentSecurityPolicy: false })`, `{ hsts: false }`, `{ frameguard: false }` | app setup | Header explicitly disabled | NDW-01, NDW-04, CSP-01, HST-01, HDR-01 |
| No `app.disable('x-powered-by')` and no helmet | app setup | `X-Powered-By: Express` sent | NDW-02, HDR-15 |
| `res.setHeader('X-Powered-By', …)`, informative `Server` header | middleware | Version-revealing headers | HDR-15, HDR-14 |
| `cors()` with no options, `origin: '*'` or `origin: true` together with `credentials: true`; `origin: req.headers.origin` | app setup | Any-origin or reflected CORS with credentials | H5-01, H5-02, H5-03 |
| `http.createServer(app).listen(80)` as the only listener; no `trust proxy` behind a proxy | server entry | No HTTPS / spoofable protocol detection | NDW-03, TLS-03, TLS-04 |
| `res.send(obj)` for JSON instead of `res.json`, or `res.type('html')` on API data | handlers | Wrong content type | RST-06 |
| `res.sendFile(userPath)` / `res.download` with inline disposition for user uploads | handlers | Inline download of user files | HDR-19 |
| `req.query.token`, `req.query.api_key`, `req.query.password` | handlers | Credentials in URLs | RST-11, RST-12 |
| `app.all(...)` for API routes, or method handlers including `trace` | routes | Any-method handler | RST-02 |
