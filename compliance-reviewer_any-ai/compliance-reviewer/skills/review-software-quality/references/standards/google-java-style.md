# Google Java Style Guide — localized summary

- Source site: google.github.io · Version: `google/styleguide` branch `gh-pages`, last commit touching
  `javaguide.html` 5cfdc38868c8 (2026-10-28) · single page
- Citation base: https://google.github.io/styleguide/javaguide.html
- Localized: 2026-11-09 · Elements: 34 (cap 100; about 35 reserved for a TypeScript guide, follow-up F-1)
- Source name for `Finding.standard`: Google Java Style Guide
- Level: informational only (the guide uses "must"/"should" loosely); severity is the owning check's default.
- **Load only when Java is detected; apply only to `.java` files.** A documented team convention (Checkstyle,
  Spotless/google-java-format config, `.editorconfig`, written style guide) prevails over these defaults
  (SKILL.md), e.g. 4-space indentation enforced by `checkstyle.xml` passes GJS-09.
- Anchors: the guide's in-text section ids (`#s<number>-<slug>`); historical alias ids are not used.

| ID | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-----------------------|--------------|-------|-----------|
| GJS-01 | The file name is the top-level class name plus `.java`, with exactly one top-level class per file. | Java | CS-05 | gjs#s2.1-file-name, gjs#s3.4.1-one-top-level-class |
| GJS-02 | UTF-8 source. The only whitespace character is ASCII space (no tabs). Escape sequences are used instead of octal or Unicode escapes for special characters. | Java | CS-05 | gjs#s2.2-file-encoding, gjs#s2.3.1-whitespace-characters, gjs#s2.3.2-special-escape-sequences |
| GJS-03 | No wildcard imports, static or otherwise. | Java imports | CS-05 | gjs#s3.3.1-wildcard-imports |
| GJS-04 | Imports aren't line-wrapped. Static imports come in one block and non-static in another, each in ASCII order. | Java imports | CS-05 | gjs#s3.3.2-import-line-wrapping, gjs#s3.3.3-import-ordering-and-spacing |
| GJS-05 | No static import for static nested classes. | Java imports | CS-05 | gjs#s3.3.4-import-class-not-static |
| GJS-06 | Class members follow a logical order, and overloads are never split. | Java classes | CS-05 | gjs#s3.4.2-ordering-class-contents, gjs#s3.4.2.1-overloads-never-split |
| GJS-07 | Braces are used with `if`/`else`/`for`/`do`/`while` even for single statements. | Java | CS-05 | gjs#s4.1.1-braces-always-used |
| GJS-08 | K&R ("Egyptian") braces for non-empty blocks; empty blocks may be concise. | Java | CS-05 | gjs#s4.1.2-blocks-k-r-style, gjs#s4.1.3-braces-empty-blocks |
| GJS-09 | Block indentation is +2 spaces (or the documented team convention). | Java | CS-05 | gjs#s4.2-block-indentation |
| GJS-10 | One statement per line. | Java | CS-05 | gjs#s4.3-one-statement-per-line |
| GJS-11 | Column limit is 100 (or the documented convention). | Java | CS-05 | gjs#s4.4-column-limit |
| GJS-12 | Line-wrapping breaks before non-assignment operators, and continuation lines are indented at least +4. | Java | CS-05 | gjs#s4.5.1-line-wrapping-where-to-break, gjs#s4.5.2-line-wrapping-indent |
| GJS-13 | Vertical and horizontal whitespace follow the guide. Horizontal alignment is never required. | Java | CS-05 | gjs#s4.6.1-vertical-whitespace, gjs#s4.6.2-horizontal-whitespace, gjs#s4.6.3-horizontal-alignment |
| GJS-14 | Optional grouping parentheses are used where they aid readability. | Java | CS-05 | gjs#s4.7-grouping-parentheses |
| GJS-15 | One variable per declaration. Locals are declared close to first use. | Java | CS-05 | gjs#s4.8.2.1-variables-per-declaration, gjs#s4.8.2.2-variables-limited-scope |
| GJS-16 | No C-style array declarations (`String args[]`). | Java | CS-05 | gjs#s4.8.3.2-array-declarations |
| GJS-17 | Switch: fall-through is commented, and switches are exhaustive or have a `default`. | Java switch | CS-05 | gjs#s4.8.4.2-switch-fall-through, gjs#s4.8.4.3-switch-default |
| GJS-18 | Annotation placement follows the guide (type-use next to type; class/method annotations one per line). | Java annotations | CS-05 | gjs#s4.8.5-annotations |
| GJS-19 | Block comments use `/* … */` or `//` style consistently. TODO comments follow the `TODO: <bug link or context> - <explanation>` form (tracking is MAINT-04). | Java comments | CS-05 | gjs#s4.8.6.1-block-comment-style, gjs#s4.8.6.2-todo-comments |
| GJS-20 | Modifiers appear in the order the Java Language Specification recommends. | Java | CS-05 | gjs#s4.8.7-modifiers |
| GJS-21 | `long` literals use an uppercase `L` suffix. | Java | CS-05 | gjs#s4.8.8-numeric-literals |
| GJS-22 | Identifiers use only ASCII letters and digits (underscores only where the guide allows). No prefixes or suffixes such as `mName`, `s_name` or `name_`. | Java | CS-05 | gjs#s5.1-identifier-names |
| GJS-23 | Package names are all lowercase with no underscores. | Java | CS-05 | gjs#s5.2.1-package-names |
| GJS-24 | Class names are UpperCamelCase nouns, and test classes end in `Test`. | Java | CS-05 | gjs#s5.2.2-class-names |
| GJS-25 | Method names are lowerCamelCase, usually verbs. | Java | CS-05 | gjs#s5.2.3-method-names |
| GJS-26 | Constants (static final, deeply immutable) use `CONSTANT_CASE`. | Java | CS-05 | gjs#s5.2.4-constant-names |
| GJS-27 | Non-constant fields, parameters and locals are lowerCamelCase. No one-character parameter names in public methods. | Java | CS-05 | gjs#s5.2.5-non-constant-field-names, gjs#s5.2.6-parameter-names, gjs#s5.2.7-local-variable-names |
| GJS-28 | Type variables are a single capital letter (optionally plus a digit) or a class-style name plus `T`. | Java generics | CS-05 | gjs#s5.2.8-type-variable-names |
| GJS-29 | Camel case treats acronyms as words (`XmlHttpRequest`, not `XMLHTTPRequest`). | Java | CS-05 | gjs#s5.3-camel-case |
| GJS-30 | `@Override` is always used where legal. | Java | CS-05 | gjs#s6.1-override-annotation |
| GJS-31 | Static members are qualified with the class name, not an instance. | Java | CS-05 | gjs#s6.3-static-members |
| GJS-32 | Finalizers (`Object.finalize`) aren't used. | Java | CS-05 | gjs#s6.4-finalizers |
| GJS-33 | Javadoc is present on every public class and every public or protected member, except self-explanatory members and overrides. | public Java API | CS-04 | gjs#s7.3-javadoc-where-required, gjs#s7.3.1-javadoc-exception-self-explanatory, gjs#s7.3.2-javadoc-exception-overrides |
| GJS-34 | Javadoc follows the general form: a summary fragment, paragraphs, and block tags in standard order with no empty descriptions. | Javadoc present | CS-04 | gjs#s7.1.1-javadoc-multi-line, gjs#s7.1.2-javadoc-paragraphs, gjs#s7.1.3-javadoc-block-tags, gjs#s7.2-summary-fragment |

Page key `gjs` = the citation base.
