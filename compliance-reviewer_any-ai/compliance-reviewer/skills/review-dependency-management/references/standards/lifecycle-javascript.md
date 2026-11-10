# Runtime lifecycle — JavaScript/TypeScript (Node.js) — localized summary

- Sources: github.com — `nodejs/Release` `schedule.json` (main branch, retrieved 2026-11-09); expressjs.com — Production
  Best Practices: Security (retrieved 2026-11-09)
- Localized: 2026-11-09 · Elements: github.com 5, expressjs.com 1 (cap 100 each)
- Level: `LIFECYCLE` — the verdict comes from the date rule in `SKILL.md` (support end vs. reference date), not from a keyword.
- Dates are exact days from `schedule.json` (`end`). Odd-numbered Node.js lines are never LTS and end about eight
  months after release.
- Detection (Node.js rows): `engines.node` in `package.json`, `.nvmrc`, `.node-version`, `volta.node` in `package.json`,
  `FROM node:<n>` in a Dockerfile, `runtime`/`linuxFxVersion`/`NODE|<n>` settings in IaC in scope. For ranges
  (`>=18`, `^20 || ^22`), evaluate the highest version the range permits (see `SKILL.md`); `lts/*` and `node` (latest)
  in `.nvmrc` float and are judged by DEP-01, not here.
- Detection (Express row): `express` in `dependencies` with a `2.x`/`3.x` version.
- Citation: `Finding.url` = citation base + `#` + anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Source name for `Finding.standard` |
|-----|---------------|------------------------------------|
| nodesched | https://github.com/nodejs/Release | Node.js Release Working Group — release schedule |
| exsec | https://expressjs.com/en/advanced/best-practice-security.html | Express — Production Best Practices: Security |

| ID | Level | Product | Line(s) | Support ends | Status at snapshot | Anchor |
|----|-------|---------|---------|--------------|--------------------|--------|
| NODE-01 | LIFECYCLE | Node.js | 27 | 2030-04-30 | pre-release (alpha since 2026-10-28; release 2027-04-22) | nodesched#release-schedule |
| NODE-02 | LIFECYCLE | Node.js | 26 (Lithium) | 2029-04-30 | active LTS (since 2026-10-28) | nodesched#release-schedule |
| NODE-03 | LIFECYCLE | Node.js | 24 (Krypton) | 2028-04-30 | maintenance LTS (since 2026-10-20) | nodesched#release-schedule |
| NODE-04 | LIFECYCLE | Node.js | 22 (Jod) | 2027-04-30 | maintenance LTS | nodesched#release-schedule |
| NODE-05 | LIFECYCLE | Node.js | 25 (2026-06-01), 23 (2025-06-01), 21 (2024-06-01), 20 (2026-04-30), 19 (2023-06-01), 18 (2025-04-30), 17 (2022-06-01), 16 (2023-09-11), 15 (2021-06-01), 14 (2023-04-30), 13 (2020-06-01), 12 (2022-04-30), 11 (2019-06-01), 10 (2021-04-30), 9 (2018-06-30), 8 (2019-12-31), 7 (2017-06-30), 6 (2019-04-30), 5 (2016-06-30), 4 (2018-04-30), 0.12 (2016-12-31), 0.10 (2016-10-31), 0.8 (2014-07-31) | as listed | end of life | nodesched#end-of-life-releases |
| EXP-01 | LIFECYCLE | Express | 2.x, 3.x | no longer maintained (no date given) | end of life | exsec#dont-use-deprecated-or-vulnerable-versions-of-express |
