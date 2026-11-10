# Google TypeScript Style Guide — localized summary

- Source site: google.github.io · Version: `google/styleguide` branch `gh-pages`, last commit touching `tsguide.html`
  5d6fa5e1d2d3 (2026-10-29) · single page
- Citation base: https://google.github.io/styleguide/tsguide.html
- Localized: 2026-11-09 · Elements: 23 (google.github.io total with `google-java-style.md`: 57 of 100)
- Source name for `Finding.standard`: Google TypeScript Style Guide
- Level: informational only; severity is the owning check's default.
- **Load only when language `javascript` is detected.** Apply "TS" rows to `.ts`/`.tsx` files only; "TS/JS" rows also
  to `.js`/`.mjs`/`.cjs`/`.jsx` files. A documented team convention (ESLint/Prettier/Biome config, `.editorconfig`,
  `tsconfig.json` settings, a written style guide) prevails over these defaults (SKILL.md), e.g. a Prettier config with
  double quotes passes GTS-11. Generated code is exempt (`#generated-code-mostly-exempt`). `@deprecated` marking is
  judged by `review-maintainability` MAINT-05, not here.
- Anchors: the guide's heading ids (`gts#<id>`); confirm them against the HTML on the first refresh.

| ID | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-----------------------|--------------|-------|-----------|
| GTS-01 | Types, classes, interfaces, enums and decorators use UpperCamelCase; variables, parameters, functions, methods and properties use lowerCamelCase; module-level constants and enum values may use CONSTANT_CASE. | TS/JS | CS-05 | gts#rules-by-identifier-type, gts#identifiers |
| GTS-02 | Names are descriptive; acronyms are treated as words (`loadHttpUrl`); no `opt_` prefixes and no leading or trailing underscores. | TS/JS | CS-05 | gts#identifiers |
| GTS-03 | Variables are declared with `const` by default and `let` when reassigned; `var` is never used; one variable per declaration. | TS/JS | CS-05 | gts#local-variable-declarations |
| GTS-04 | Modules use named exports, not default exports. | TS/JS modules | CS-05 | gts#exports |
| GTS-05 | ES modules are used: no `namespace`, no `require` imports in TypeScript, no `/// <reference>` directives. | TS | CS-05 | gts#imports, gts#source-file-structure |
| GTS-06 | Equality uses `===`/`!==` (except `== null` to cover both null and undefined). | TS/JS | CS-05 | gts#control-structures |
| GTS-07 | `any` is avoided; `unknown` or a specific type is used instead. | TS | CS-05 | gts#any-type |
| GTS-08 | Type and non-null (`!`) assertions are used only with a stated reason; runtime checks are preferred; assertions use `as`, not angle brackets. | TS | CS-05 | gts#type-system, gts#any-type |
| GTS-09 | `@ts-ignore`, `@ts-expect-error` (outside tests) and `@ts-nocheck` aren't used; all files pass type checking. | TS | CS-05 | gts#ts-ignore, gts#typescript-compiler, gts#toolchain-requirements |
| GTS-10 | Type aliases don't include `\|null`/`\|undefined`; optional fields and parameters use `?`. | TS | CS-05 | gts#undefined-and-null |
| GTS-11 | String literals use single quotes; statements end with explicit semicolons (no reliance on automatic semicolon insertion). | TS/JS | CS-05 | gts#primitive-literals, gts#language-features |
| GTS-12 | Control statements always use braced blocks; every `switch` has a `default` case, placed last. | TS/JS | CS-05 | gts#control-structures |
| GTS-13 | `for…in` isn't used on arrays; object iteration filters own properties or uses `Object.keys`/`entries`. | TS/JS | CS-05 | gts#control-structures |
| GTS-14 | No `eval` or `Function(string)`, no `with`, no `debugger` in production code, no wrapper objects (`new String`), no `Array()` constructor, no modification of built-in prototypes. | TS/JS | CS-05 | gts#disallowed-features |
| GTS-15 | Class members don't use the `public` modifier (except non-readonly parameter properties) or `#private` fields; parameter properties are preferred over manual assignment. | TS classes | CS-05 | gts#classes |
| GTS-16 | Getters are pure (no observable side effects); accessors aren't created with `Object.defineProperty`. | TS/JS classes | CS-05 | gts#classes |
| GTS-17 | Named functions use function declarations; function expressions are replaced by arrow functions; `this` is used only in class members or explicitly typed functions. | TS/JS | CS-05 | gts#functions, gts#this |
| GTS-18 | `const enum` isn't used, and enum values aren't coerced to booleans. | TS enums | CS-05 | gts#language-features |
| GTS-19 | Simple array types use `T[]`, complex ones `Array<T>`; interfaces are preferred over object type-literal aliases. | TS | CS-05 | gts#arrayt-type, gts#prefer-interfaces-over-type-literal-aliases |
| GTS-20 | Only `Error` objects (or subclasses) are thrown or used as promise rejection reasons, created with `new`. | TS/JS | SQ-06 | gts#language-features |
| GTS-21 | An empty `catch` block has a comment explaining why ignoring the error is correct. | TS/JS | SQ-06 | gts#language-features |
| GTS-22 | All top-level exports have JSDoc that adds information beyond the name; JSDoc doesn't repeat types already in the TypeScript signature. | TS/JS exported API | CS-04 | gts#document-all-top-level-exports-of-modules, gts#jsdoc-versus-comments, gts#comments-and-documentation |
| GTS-23 | New code follows the file's and directory's established style when the guide is silent; new files use the guide (or the team convention). | TS/JS | CS-05 | gts#consistency, gts#policies |
