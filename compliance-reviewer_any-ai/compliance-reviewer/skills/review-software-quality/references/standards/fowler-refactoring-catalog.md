# Refactoring catalog (2nd edition) — localized summary, remedies only

- Source site: refactoring.com · Version: online catalog for *Refactoring* 2nd edition (66 entries; 1st-edition
  names are listed there as aliases)
- Citation base: https://refactoring.com/catalog/
- Localized: 2026-11-09 · Elements: 23 (cap 100)
- Source name: Refactoring catalog
- **Remedies only.** FRC elements never fail on their own and never appear in `Finding.standard`. Name them in
  `recommendation`, e.g. "Apply *Extract Function* (FRC-01, https://refactoring.com/catalog/extractFunction.html)".
- Citation: citation base + the page in the last column.

| ID | Refactoring (remedy) | Use for | Check | Page |
|----|----------------------|---------|-------|------|
| FRC-01 | Extract Function (1st ed.: Extract Method) | Long Function (SQR-01) | SQ-01 | extractFunction.html |
| FRC-02 | Split Phase | Mixed abstraction levels (SQR-02) | SQ-01 | splitPhase.html |
| FRC-03 | Decompose Conditional | Complex branches (SQR-03, SQR-05) | SQ-02 | decomposeConditional.html |
| FRC-04 | Consolidate Conditional Expression | Long boolean chains (SQR-05) | SQ-02 | consolidateConditionalExpression.html |
| FRC-05 | Replace Nested Conditional with Guard Clauses | Deep nesting (SQR-04) | SQ-02 | replaceNestedConditionalWithGuardClauses.html |
| FRC-06 | Replace Conditional with Polymorphism | Repeated Switches (SQR-07) | SQ-03 | replaceConditionalWithPolymorphism.html |
| FRC-07 | Replace Inline Code with Function Call | Duplicated Code (SQR-06) | SQ-03 | replaceInlineCodeWithFunctionCall.html |
| FRC-08 | Parameterize Function | Near-duplicate functions (SQR-06) | SQ-03 | parameterizeFunction.html |
| FRC-09 | Extract Class | Large Class, divergent responsibilities (SQR-08, SQR-09) | SQ-04 | extractClass.html |
| FRC-10 | Move Function | Feature Envy, data classes (SQR-10, MFB-06) | SQ-04 | moveFunction.html |
| FRC-11 | Introduce Parameter Object | Long Parameter List, Data Clumps (SQR-11, SQR-12) | SQ-05 | introduceParameterObject.html |
| FRC-12 | Preserve Whole Object | Long Parameter List (SQR-11) | SQ-05 | preserveWholeObject.html |
| FRC-13 | Remove Flag Argument | Flag arguments (SQR-13) | SQ-05 | removeFlagArgument.html |
| FRC-14 | Replace Exception with Precheck | Exceptions as control flow (SQR-15) | SQ-06 | replaceExceptionWithPrecheck.html |
| FRC-15 | Remove Dead Code | Dead or commented-out code (SQR-17, SQR-18) | SQ-08 | removeDeadCode.html |
| FRC-16 | Encapsulate Variable | Global or mutable shared data (SQR-19, SQR-20) | DP-01 | encapsulateVariable.html |
| FRC-17 | Replace Superclass with Delegate | Refused Bequest, deep inheritance (SQR-21, SQR-22) | DP-02 | replaceSuperclassWithDelegate.html |
| FRC-18 | Collapse Hierarchy | Needless hierarchy levels (SQR-21) | DP-02 | collapseHierarchy.html |
| FRC-19 | Remove Middle Man | Pass-through classes (SQR-23, AAS-04) | DP-04 | removeMiddleMan.html |
| FRC-20 | Inline Class | Speculative abstractions (SQR-23, SQR-24) | DP-04 | inlineClass.html |
| FRC-21 | Replace Constructor with Factory Function | Duplicated complex construction (SQR-25) | DP-05 | replaceConstructorWithFactoryFunction.html |
| FRC-22 | Rename Variable / Rename Field / Change Function Declaration | Mysterious Name (SQR-32, MSC-06) | CS-01 | renameVariable.html, renameField.html, changeFunctionDeclaration.html |
| FRC-23 | Replace Magic Literal | Unnamed literals that obscure intent (SQR-32) | CS-01 | replaceMagicLiteral.html |
