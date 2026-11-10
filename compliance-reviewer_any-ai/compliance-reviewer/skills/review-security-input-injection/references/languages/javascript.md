# Detection signals — JavaScript/TypeScript (Security: Input & Injection)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). Node.js parser and framework defaults aren't localized beyond `node-input.md`: report explicit
values only, and add a `localized-standard-gap` note when a decision depends on a default.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `` db.query(`SELECT … ${req.params.id}`) ``, `"… WHERE id = " + id` with `mysql`/`pg`/`sqlite3`; `sequelize.query(sql)` with interpolation; Knex `raw()` / TypeORM `query()` with interpolation | data access | SQL concatenation | SQL-01, SQL-02, A05-02 |
| `pg` `$1` placeholders, `mysql2` `?` with values array, Sequelize/Prisma/TypeORM query builders | data access | Parameterized access (pass) | QP-01 |
| `collection.find(req.body)`; `{ $where: … }` or operators from input reaching MongoDB | data access | NoSQL operator injection | INJ-06, NDI-02 |
| `child_process.exec`/`execSync` with template strings; `spawn(cmd, { shell: true })` | any | Shell injection | INJ-04, NDI-05 |
| `eval`, `new Function`, `vm.runIn*Context`, `setTimeout(string)` on input | any | Code injection | NDI-05 |
| `element.innerHTML =`, `outerHTML`, `insertAdjacentHTML`, `document.write`, React `dangerouslySetInnerHTML`, Vue `v-html`, Angular `[innerHTML]` / `bypassSecurityTrust*` with untrusted data | front-end files | DOM XSS sinks | XSS-08, XSS-09 |
| EJS `<%- %>`, Handlebars `{{{ }}}`, Pug `!{}` / `!=` on user data | templates | Unescaped output | XSS-02, NDI-04 |
| `express.json({ limit: … })` large or missing on upload-heavy routes; `bodyParser` with `limit: Infinity` | app setup | Unbounded bodies | NDI-01, IV-04 |
| `multer` without `limits.fileSize`/`fileFilter`; `file.originalname` used in a path | upload handlers | Upload checks | FU-01, FU-05, FU-06 |
| `res.redirect(req.query.*)` | handlers | Open redirect | NDI-03 |
| `xml2js`/`libxmljs` with `noent: true` or DTD loading on uploads | XML parsing | XXE | XML-01 |
| `node-serialize` `unserialize`, `serialize-javascript` output passed to `eval`, `js-yaml` `load` with unsafe schema on input | deserialization | Unsafe deserialization | DES-01, DES-02 |
| `new RegExp(req.query.q)`; nested quantifiers on input | any | ReDoS | NDI-06 |
