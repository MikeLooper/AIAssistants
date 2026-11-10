# Maintenance — Software Quality localized standards

**Maintainers only. Workers never load this file.** Background and design decisions:
`docs/plan_localize-review-software-quality.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1). learn.microsoft.com and martinfowler.com are also used by
other skills; the budgets are separate. Within this skill the two learn.microsoft.com files share one budget.

| Website | Local file(s) | Elements | Cap | Note |
|---|---|---|---|---|
| iso25000.com | iso-25010.md | 40 | 100 | Classification only |
| learn.microsoft.com | azure-architecture.md (20), microsoft-csharp.md (24) | 44 | 100 | 7 pages |
| google.github.io | google-java-style.md (34), google-typescript-style.md (23) | 57 | 100 | TypeScript guide added 2026-11-09 (follow-up F-1, afterplanning WP-12f) |
| peps.python.org | python-peps.md | 23 | 100 | PEP 8: 20, PEP 257: 3 |
| martinfowler.com | fowler-bliki.md | 6 | 100 | 2 bliki pages |
| refactoring.com | fowler-refactoring-catalog.md | 23 | 100 | Remedies only |
| cheatsheetseries.owasp.org | software-quality-rubric.md (reference only) | 0 | 100 | REST Security Cheat Sheet `#preventing-out-of-order-api-execution` @97cb8a3c, cited by SQR-37 (separate from the web-api pin) |
| — (local) | software-quality-rubric.md | 37 | n/a | Rubric v1.1 |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Retired check IDs
  that must never be reused: **DP-03, SQ-07, AP-05, CS-CS-01…05, CS-JV-01…05, CS-PY-01…05**.
- Primary anchor first; list every absorbed anchor so coverage stays auditable.
- Every SQR, AAS, MFB, MSC, GJS, PEP and GTS ID is listed by exactly one active check in `../checklist.md`, and the
  element row's Check column names that check.
- FRC elements are remedy-only (listed once, in parentheses, in the checklist). ISO elements are classification-only
  and never appear in the checklist.
- Levels never change severity: every Finding takes the check's default (plan DEC-13).
- Keep rows to one line (≈ 200 characters where possible). Never reproduce more than a one-line paraphrase of a
  source, and nothing from the book *Refactoring* or the ISO standard text.
- Google Java anchors use the in-text ids `#s<number>-<slug>`. Where the guide keeps a historical alias id next to the
  current one (`s3.2`, `s3.4.2`, `s7.1.3`), use the current one (the one without the `<!-- historical link -->`).

## Rubric thresholds (plan DEC-9)

A threshold change is a rubric edit: bump the rubric version, add a dated line to the localization log, and add a
README Maintenance note if scores may shift. No source refresh is needed.

| Measure | Value | Reason |
|---|---|---|
| Function length (SQR-01) | > 60 logical lines, or > 30 with ≥ 2 jobs | Lenient end of common analyzer defaults; the second clause catches short multi-purpose functions. |
| Cyclomatic complexity (SQR-03) | > 15 | Sonar, Checkstyle, Pylint and .NET CA1502 sit in the 10–25 range; 15 is a middle value for a reading estimate. |
| Nesting (SQR-04) | > 4 | Checkstyle/Pylint-style nesting limits; 4 levels are still readable. |
| Duplicate block (SQR-06) | ≥ 10 lines in ≥ 2 places | Copy-paste detectors commonly start at 10 lines/100 tokens. |
| Class size (SQR-08) | > 500 lines, > 20 public methods, > 10 ctor dependencies | Typical "large class" analyzer limits; 10 dependencies flags constructor over-injection. |
| Parameters (SQR-11) | > 5 | Common analyzer default (Sonar 7, Pylint 5); lenient but reading-confirmed. |
| Inheritance depth (SQR-21) | > 3 project-defined levels | Framework bases excluded so UI/ORM hierarchies don't trigger it. |

## ISO/IEC 25010 2011 → 2023 name map (for readers of older reports)

| 2011 | 2023 |
|---|---|
| Usability | Interaction capability (new sub-characteristics include Inclusivity and Self-descriptiveness) |
| Portability | Flexibility (new sub-characteristic: Scalability) |
| Reliability › Maturity | Reliability › Faultlessness |
| Security | Security (new sub-characteristic: Resistance) |
| — | Safety (new characteristic, ISO-36 … ISO-40) |

## Pins and watch items

- **Azure Architecture Center** (repo `MicrosoftDocs/architecture-center`): `as` ms.date 2025-09-25 @ d1d0ebff1b2a;
  `nt` 2025-08-15 @ 03e41c0834ab; `wqw` 2026-01-06 @ c32bf659d950; `ms` 2025-06-30 @ f69851e7c8b2; `dfe` 2018-08-30 @
  f440454b6512.
- **C#** (repo `dotnet/docs`): `cc` ms.date 2025-01-15 @ 156931bb4ec1 (updated 2026-03-30); `in` ms.date 2025-10-10 @
  6b2c20688c8f (updated 2026-07-14).
- **Google Java Style:** `google/styleguide` `gh-pages`, last commit touching `javaguide.html` 5cfdc38868c8
  (2026-10-28). The page shows no date; renumbered sections need anchor updates.
- **PEPs** (`python/peps`): `peps/pep-0008.rst` @ 5514795ade79 (2025-04-04 00:19 UTC); `peps/pep-0257.rst` @
  f22614f903cd (2024-04-17 11:35 UTC).
- **iso25000.com:** no version shown. SHA-256 prefixes of the raw HTML on 2026-11-09 (the pages also carry a news
  box, so compare the extracted characteristic text, not the raw hash, before concluding there is drift):
  p1 `8da9041a9c790b1b`, p2 `737e2979cfa9cf7e`. Watch for an amendment to ISO/IEC 25010:2023.
- **refactoring.com:** 66 catalog entries on 2026-11-09. Watch for renamed or removed entries.
- **martinfowler.com:** CodeSmell (2006-02-09) and PresentationDomainDataLayering (2015-08-26); confirm they exist.

## Localization log

- **2026-11-09 — planning snapshot.** Found: iso25000.com has no `#maintainability`/`#reliability` anchors and is
  paginated (page 2 = `?start=5`); the page now presents the 2023 model; the Azure patterns catalog doesn't cover
  layering and was never allowlisted (dropped); refactoring.com is a catalog of refactorings, not smells, so FRC
  elements are remedies only and the rubric uses its own smell names with no book attribution (plan DEC-10).
- **2026-11-09 — implementation re-snapshot (step 1).** All Learn `ms.date`/commit pins and PEP last-modified
  dates match the plan. Every Learn and PEP anchor cited exists (including `cc#-and--operators` and
  `in#primary-constructor-parameters`). Google commit pinned (5cfdc38868c8). Google anchor form decided: in-text
  `#s<number>-<slug>` ids (the table-of-contents `#331-…` form also exists but isn't used). All 25 cited
  refactoring.com pages exist. ISO characteristic and sub-characteristic names match the 40 ISO rows.
- **2026-11-09 — files written.** 206 elements; verification: every scored element in exactly one active check,
  every FRC once as a remedy, no ISO ID in the checklist, every anchor present in the snapshot. Every heading and
  numbered section on the pinned pages appears in the coverage map below.
- **2026-11-09 — out-of-order API workflows (afterplanning WP-11, decision D-5).** Software-quality plan C-10
  (decline) is reversed: rubric element SQR-37 added under AP-02 (check count unchanged; README note). It cites the
  OWASP REST Security Cheat Sheet section `preventing-out-of-order-api-execution` at commit
  97cb8a3c4b62104227ba52833ff7842ff1d0c850 (2026-10-14), pinned for this skill in `approved-sources.md`. Per-step
  authorization stays with identity-access SEC-IA-02; the web-api coverage map code **U** now points here.
- **2026-11-09 — JavaScript/TypeScript (afterplanning WP-12f phase 2, follow-up F-1).** `google-typescript-style.md`
  (GTS-01 … GTS-23) from `tsguide.html` at commit 5d6fa5e1d2d33a7b080a6aef4c8e0ee5a9b358aa (2026-10-29), plus
  `../languages/javascript.md`. Rules not localized: formatting details a formatter decides (line wrapping, JSDoc tag
  layout), decorators (framework-defined), return-type-only generics, mapped/conditional types (judgment),
  `@deprecated` (review-maintainability MAINT-05). Anchors from the heading list; confirm on the first refresh.
- **Open:** the sample-repo runs (plan step 8: C# Web API, Java two-module, Python + `.ts`) haven't been done yet.

## Open items

- Plan §10 follow-ups (changes outside this skill): reviewed and closed by `docs/plan_localize-afterplanning-changes.md` on 2026-11-09 (see its Appendix A). Open hand-offs: none.

## `localized-standard-gap` log

Record each gap reported in run notes with date and run ID. Count "no language standard for javascript" (or
typescript) entries separately: they are evidence for follow-up F-1, not a refresh trigger.

| Date | Run | Gap |
|---|---|---|
| — | — | — |

## Coverage map

Every source item is mapped to an element ID or to "not localized — <reason>".

### iso25000.com

All 9 characteristics and 40 sub-characteristics → ISO-01 … ISO-40 (one each, in page order). Not localized: the
quality-in-use model, the ISO 25000-series overview, news and certification items (not the product model), and
ISO/IEC 25023 metrics (not on the page; thresholds come from the rubric).

### learn.microsoft.com — Azure Architecture Center

| Page | Heading (anchor) | Mapping |
|---|---|---|
| as | a-quick-tour-of-the-styles, n-tier, web-queue-worker, microservices | not localized — summaries; each style's own page is localized |
| as | event-driven-architecture, big-data, big-compute | not localized — rare in targets, mostly infrastructure (follow-up F-4) |
| as | architecture-styles-as-constraints | AAS-05, AAS-07 |
| as | consider-challenges-and-benefits | AAS-06 |
| as | related-resources, next-steps | not localized — navigation |
| nt | (introduction, no anchor) | AAS-01, AAS-02 |
| nt | when-to-use-this-architecture, benefits | not localized — style selection, not code constraints |
| nt | challenges | AAS-04 |
| nt | best-practices | AAS-03 (autoscale, caching, messaging, security items: owned by other subjects) |
| nt | n-tier-architecture-on-vms, other-considerations | not localized — infrastructure, network, security (other subjects) |
| nt | next-step, related-resource | not localized — navigation |
| wqw | when-to-use-this-architecture, benefits | not localized — style selection |
| wqw | challenges | AAS-15, AAS-16 |
| wqw | best-practices | not localized — hosting, autoscale, CDN, idempotency (reliability/performance) |
| wqw | web-queue-worker-on-app-service, workflow, other-considerations | not localized — hosting and operations |
| wqw | related-resource | not localized — navigation |
| ms | what-are-microservices, components, benefits | not localized — descriptive |
| ms | challenges | not localized — operational and organizational |
| ms | best-practices | AAS-07, AAS-08, AAS-10, AAS-11, AAS-13, AAS-17, AAS-20 (deployment, observability, resilience items: other subjects) |
| ms | antipatterns-for-microservices | AAS-09, AAS-11, AAS-12, AAS-14 ("configuration inside services": review-twelve-factor) |
| ms | build-a-microservices-architecture, related-resources | not localized — navigation |
| dfe | an-evolutionary-design-is-key-for-continuous-innovation | not localized — introduction |
| dfe | recommendations | AAS-10, AAS-13, AAS-17, AAS-18, AAS-19 (open versioned interfaces: review-api-design; contracts tests: review-testing; independent deployment and fitness functions: review-software-lifecycle) |

### learn.microsoft.com — C#

| Page | Heading (anchor) | Mapping |
|---|---|---|
| cc | tools-and-analyzers | MSC-24 |
| cc | diagnostic-ids | not localized — applies to analyzer authors only |
| cc | language-guidelines | MSC-09, MSC-10, MSC-11 (sample-only `var` and 65-character rules not localized) |
| cc | string-data | MSC-13 |
| cc | constructors-and-initialization | MSC-08, MSC-14 |
| cc | arrays-and-collections | MSC-14 |
| cc | delegates | MSC-15 (full vs concise instantiation syntax not localized — no quality impact) |
| cc | try-catch-and-using-statements-in-exception-handling | MSC-16 |
| cc | -and--operators | MSC-17 |
| cc | new-operator | MSC-14 |
| cc | event-handling | not localized — lambda handlers are a stylistic choice |
| cc | static-members | MSC-18 |
| cc | linq-queries | MSC-19 |
| cc | implicitly-typed-local-variables | MSC-12 |
| cc | file-scoped-namespace-declarations, place-the-using-directives-outside-the-namespace-declaration | MSC-20 |
| cc | style-guidelines, layout-conventions | MSC-21 |
| cc | comment-style | MSC-22, MSC-23 |
| cc | security | not localized — owned by the security subjects |
| in | naming-rules | not localized — compiler-enforced |
| in | naming-conventions | MSC-01 … MSC-06 |
| in | pascal-case | MSC-01, MSC-02 |
| in | camel-case | MSC-03 |
| in | primary-constructor-parameters | MSC-08 |
| in | type-parameter-naming-guidelines | MSC-07 |
| in | extra-naming-conventions | not localized — sample namespace qualification and designer-generated names |

### google.github.io — Google Java Style Guide (94 numbered sections)

| Section(s) | Mapping |
|---|---|
| 1, 1.1, 1.2 | not localized — introduction, not requirements |
| 2 | heading only |
| 2.1 | GJS-01 |
| 2.2, 2.3.1, 2.3.2 | GJS-02 (2.3 heading only) |
| 2.3.3 | not localized — readability judgment call, rarely an issue |
| 3 | heading only |
| 3.1, 3.2 | not localized — license presence owned by no subject; package declaration compiler-enforced |
| 3.3 | heading only |
| 3.3.1 | GJS-03 |
| 3.3.1.1, 3.5, 3.5.1 | not localized — JPMS module imports and declarations are rare |
| 3.3.2, 3.3.3 | GJS-04 |
| 3.3.4 | GJS-05 |
| 3.4 | heading only |
| 3.4.1 | GJS-01 |
| 3.4.2, 3.4.2.1 | GJS-06 |
| 4, 4.1 | heading only |
| 4.1.1 | GJS-07 |
| 4.1.2, 4.1.3 | GJS-08 |
| 4.2 | GJS-09 |
| 4.3 | GJS-10 |
| 4.4 | GJS-11 |
| 4.5 | heading only |
| 4.5.1, 4.5.2 | GJS-12 |
| 4.6 | heading only |
| 4.6.1, 4.6.2, 4.6.3 | GJS-13 |
| 4.7 | GJS-14 |
| 4.8, 4.8.2, 4.8.3, 4.8.4, 4.8.6 | heading only |
| 4.8.1, 4.8.3.1, 4.8.4.1, 4.8.4.4, 4.8.5.1 … 4.8.5.5, 4.8.9 | not localized — formatting minutiae a formatter settles; GJS-13/17/18 cover the substance |
| 4.8.2.1, 4.8.2.2 | GJS-15 |
| 4.8.3.2 | GJS-16 |
| 4.8.4.2, 4.8.4.3 | GJS-17 |
| 4.8.5 | GJS-18 |
| 4.8.6.1, 4.8.6.2 | GJS-19 |
| 4.8.7 | GJS-20 |
| 4.8.8 | GJS-21 |
| 5, 5.2 | heading only |
| 5.1 | GJS-22 |
| 5.2.1 | GJS-23 |
| 5.2.2 | GJS-24 |
| 5.2.3 | GJS-25 |
| 5.2.4 | GJS-26 |
| 5.2.5, 5.2.6, 5.2.7 | GJS-27 |
| 5.2.8 | GJS-28 |
| 5.2.9 | not localized — unnamed variables are too new to judge consistently |
| 5.3 | GJS-29 |
| 6 | heading only |
| 6.1 | GJS-30 |
| 6.2 | not localized — ignored exceptions owned by review-security-operational SEC-OP-02 |
| 6.3 | GJS-31 |
| 6.4 | GJS-32 |
| 7, 7.1 | heading only |
| 7.1.1, 7.1.2, 7.1.3, 7.2 | GJS-34 |
| 7.3, 7.3.1, 7.3.2 | GJS-33 |
| 7.3.4 | not localized — permissive, nothing to fail |

### peps.python.org

| Page | Heading (anchor) | Mapping |
|---|---|---|
| pep8 | introduction, a-foolish-consistency-is-the-hobgoblin-of-little-minds | not localized — the consistency principle is implemented by the team-convention rule (SKILL.md step 4) |
| pep8 | code-lay-out, whitespace-in-expressions-and-statements, naming-conventions, prescriptive-naming-conventions | heading only |
| pep8 | indentation / tabs-or-spaces / maximum-line-length | PEP-01 / PEP-02 / PEP-03 |
| pep8 | should-a-line-break-before-or-after-a-binary-operator / blank-lines / source-file-encoding | PEP-04 / PEP-05 / PEP-06 |
| pep8 | imports / module-level-dunder-names / string-quotes | PEP-07 / PEP-08 / PEP-09 |
| pep8 | pet-peeves, other-recommendations | PEP-10 |
| pep8 | when-to-use-trailing-commas | PEP-11 |
| pep8 | comments, block-comments, inline-comments | PEP-12 |
| pep8 | documentation-strings | not localized here — points to PEP 257 (PEP-21 … PEP-23) |
| pep8 | overriding-principle, descriptive-naming-styles | not localized — descriptive; PEP-14/15 carry the rules |
| pep8 | names-to-avoid, ascii-compatibility | PEP-13 |
| pep8 | package-and-module-names, class-names, type-variable-names, exception-names | PEP-14 |
| pep8 | global-variable-names | not localized — "same as functions" (PEP-15) plus `__all__` (PEP-16) |
| pep8 | function-and-variable-names, function-and-method-arguments, method-names-and-instance-variables, constants | PEP-15 |
| pep8 | designing-for-inheritance, public-and-internal-interfaces | PEP-16 |
| pep8 | programming-recommendations | PEP-17, PEP-18, PEP-19 |
| pep8 | function-annotations, variable-annotations | PEP-20 |
| pep8 | references, copyright | not localized — not requirements |
| pep257 | abstract, rationale | not localized — not requirements |
| pep257 | specification | PEP-22 |
| pep257 | what-is-a-docstring | PEP-21 |
| pep257 | one-line-docstrings | PEP-22 |
| pep257 | multi-line-docstrings | PEP-21, PEP-23 (script usage, package contents, subclass and "override"/"extend" wording not localized — beyond CS-04) |
| pep257 | handling-docstring-indentation, copyright, acknowledgements | not localized — tool behavior or not requirements |
| PEP 484 | — | not localized — offered and not chosen (plan DEC-7); SQR-36 judges adoption |

### martinfowler.com

| Page | Mapping |
|---|---|
| CodeSmell | MFB-05, MFB-06 (anemic objects as a separate concept not localized) |
| PresentationDomainDataLayering | MFB-01 … MFB-04 (team organization, development sequence, Page Objects, test doubles not localized — process or testing) |

### refactoring.com (66 entries)

Localized as remedies (25 pages, 23 elements): changeFunctionDeclaration, renameField, renameVariable (FRC-22);
collapseHierarchy (FRC-18); consolidateConditionalExpression (FRC-04); decomposeConditional (FRC-03);
encapsulateVariable (FRC-16); extractClass (FRC-09); extractFunction (FRC-01); inlineClass (FRC-20);
introduceParameterObject (FRC-11); moveFunction (FRC-10); parameterizeFunction (FRC-08); preserveWholeObject
(FRC-12); removeDeadCode (FRC-15); removeFlagArgument (FRC-13); removeMiddleMan (FRC-19);
replaceConditionalWithPolymorphism (FRC-06); replaceConstructorWithFactoryFunction (FRC-21);
replaceExceptionWithPrecheck (FRC-14); replaceInlineCodeWithFunctionCall (FRC-07); replaceMagicLiteral (FRC-23);
replaceNestedConditionalWithGuardClauses (FRC-05); replaceSuperclassWithDelegate (FRC-17); splitPhase (FRC-02).

Not localized — no rubric element calls for them as a primary remedy (workers may still name them in prose without
an FRC citation): changeReferenceToValue, changeValueToReference, combineFunctionsIntoClass,
combineFunctionsIntoTransform, encapsulateCollection, encapsulateRecord, extractSuperclass, extractVariable,
hideDelegate, inlineFunction, inlineVariable, introduceAssertion, introduceSpecialCase, moveField,
moveStatementsIntoFunction, moveStatementsToCallers, pullUpConstructorBody, pullUpField, pullUpMethod,
pushDownField, pushDownMethod, removeSettingMethod, removeSubclass, replaceCommandWithFunction,
replaceControlFlagWithBreak, replaceDerivedVariableWithQuery, replaceErrorCodeWithException,
replaceFunctionWithCommand, replaceLoopWithPipeline, replaceParameterWithQuery, replacePrimitiveWithObject,
replaceQueryWithParameter, replaceSubclassWithDelegate, replaceTempWithQuery, replaceTypeCodeWithSubclasses,
returnModifiedValue, separateQueryFromModifier, slideStatements, splitLoop, splitVariable, substituteAlgorithm
(41).

## Refresh procedure

1. **Cadence:** every six months. Refresh earlier on any trigger below, or when run notes contain ≥ 3
   `localized-standard-gap` entries for this skill (excluding the expected JS/TS entries, which count toward F-1).
2. **Drift checks:**
   - Learn (Azure styles, C# pages): compare `ms.date` and `git_commit_id` with the pins. On a change, diff the
     headings and the bullets cited by MSC and AAS rows
     (`https://api.github.com/repos/MicrosoftDocs/architecture-center/commits`,
     `https://api.github.com/repos/dotnet/docs/commits`).
   - Google Java Style: `https://api.github.com/repos/google/styleguide/commits?path=javaguide.html&sha=gh-pages`.
     Renumbered sections need anchor updates.
   - PEPs: `https://api.github.com/repos/python/peps/commits?path=peps/pep-0008.rst` (and `pep-0257.rst`).
   - iso25000.com: compare the extracted characteristic text; check for a new ISO edition (re-pin and re-map ISO IDs).
   - refactoring.com: check for renamed or removed entries. martinfowler.com: confirm the two pages still exist.
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep each website ≤ 100 elements
   (google.github.io reserves about 35 for F-1). Update this coverage map, the header pins and dates,
   `../sources.md`, and the URL list in `compliance-review-core/references/approved-sources.md` if a page moves.
4. **Rubric:** threshold and wording changes need no source refresh; log them here with a date and reason.
5. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo).
   - Script-check: every element ID is in exactly one active check of `../checklist.md` (FRC once as a remedy, ISO
     never); every element's Check column matches; every cited anchor exists on its pinned page; every heading or
     numbered section on the pinned pages appears in this coverage map.
   - Run a review against small sample repos (plan step 8) and confirm `validate` passes and `urlsFetched` is empty.
6. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-software-quality` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers and that every element is listed in `../checklist.md` (ISO elements excepted). Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.
