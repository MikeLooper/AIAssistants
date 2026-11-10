# Language Guidance — JavaScript/TypeScript

Load `../standards/google-typescript-style.md` (GTS-01…GTS-23). Its elements are scored under CS-05, CS-04 (GTS-22)
and SQ-06 (GTS-20, GTS-21). Apply "TS" rows to `.ts`/`.tsx` files only. A documented convention (`eslint.config.*`,
`.eslintrc*`, `.prettierrc*`, `biome.json`, `tsconfig.json` `strict`/`noImplicitAny`, `.editorconfig`) prevails over
the guide's defaults. Ignored caught errors on security-relevant paths belong to review-security-operational SEC-OP-02.

Signals:
- Formatter/linter config counts as "formatting enforced" for CS-02: `.prettierrc*`, `prettier` key in `package.json`,
  `eslint.config.*`/`.eslintrc*`, `biome.json`, `dprint.json`.
- Static checking adopted (SQR-36): `tsconfig.json` with `"strict": true` or `"noImplicitAny": true`; inconsistent use
  is widespread `any`, `// @ts-ignore` or `!` assertions in files under that config.
- Project references for dependency-cycle checks: `tsconfig.json` `references`, workspace `package.json`
  (`workspaces`), `pnpm-workspace.yaml`, `nx.json`, `turbo.json`.
