# PEP 8 and PEP 257 — localized summary

- Source site: peps.python.org · Repo `python/peps` · pins per page below
- Citation base: https://peps.python.org/
- Localized: 2026-11-09 · Elements: 23 (cap 100)
- Source names for `Finding.standard`: "PEP 8" (PEP-01 … PEP-20), "PEP 257" (PEP-21 … PEP-23)
- Level: informational only (PEP 8 uses "should" loosely and itself puts project consistency first); severity is
  the owning check's default.
- **Load only when Python is detected; apply only to `.py` files.** A documented team convention (Black, Ruff,
  Flake8/Pylint config, `.editorconfig`, written style guide) prevails over these defaults (SKILL.md), e.g. a Black
  line length of 88 passes PEP-03.
- Whether type hints are *required* is not a PEP rule here: SQR-36 judges adoption consistency.

| Key | Page path | Pin |
|-----|-----------|-----|
| pep8 | `pep-0008/` | `peps/pep-0008.rst` @ 5514795ade79, last modified 2025-04-04 00:19 UTC |
| pep257 | `pep-0257/` | `peps/pep-0257.rst` @ f22614f903cd, last modified 2024-04-17 11:35 UTC (Active, Informational) |

| ID | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-----------------------|--------------|-------|-----------|
| PEP-01 | Four spaces per indentation level. Continuation lines are aligned or use a hanging indent. | Python | CS-05 | pep8#indentation |
| PEP-02 | Spaces, not tabs. Never mix them. | Python | CS-05 | pep8#tabs-or-spaces |
| PEP-03 | Lines ≤ 79 characters (docstrings and comments ≤ 72), or a team-agreed limit up to 99, or a documented formatter limit. | Python | CS-05 | pep8#maximum-line-length |
| PEP-04 | Line breaks come before binary operators in new code. | Python | CS-05 | pep8#should-a-line-break-before-or-after-a-binary-operator |
| PEP-05 | Two blank lines around top-level definitions, one between methods. | Python | CS-05 | pep8#blank-lines |
| PEP-06 | Source files use UTF-8 with no encoding declaration. | Python | CS-05 | pep8#source-file-encoding |
| PEP-07 | Imports: one per line, at the top of the file, grouped stdlib / third-party / local, absolute preferred, no wildcard imports. | Python imports | CS-05 | pep8#imports |
| PEP-08 | Module-level dunders (`__all__`, `__version__`) come after the module docstring and before imports. | module dunders present | CS-05 | pep8#module-level-dunder-names |
| PEP-09 | String quote style is consistent within the project. | Python | CS-05 | pep8#string-quotes |
| PEP-10 | No extraneous whitespace (pet peeves). Spacing around operators, keyword arguments and annotations follows the recommendations. | Python | CS-05 | pep8#pet-peeves, pep8#other-recommendations |
| PEP-11 | Trailing commas are used in multi-line collections and are mandatory for one-element tuples. | Python | CS-05 | pep8#when-to-use-trailing-commas |
| PEP-12 | Comments are complete sentences and up to date. Block comments match the code's indentation, and inline comments are sparse and separated by two spaces. | Python comments | CS-05 | pep8#comments, pep8#block-comments, pep8#inline-comments |
| PEP-13 | Never `l`, `O` or `I` as single-character names. Identifiers are ASCII in the standard library and recommended ASCII elsewhere. | Python | CS-05 | pep8#names-to-avoid, pep8#ascii-compatibility |
| PEP-14 | Short lowercase module and package names, CapWords classes and type variables, and exception names ending in `Error`. | Python | CS-05 | pep8#package-and-module-names, pep8#class-names, pep8#type-variable-names, pep8#exception-names |
| PEP-15 | snake_case for functions, methods and variables; `self`/`cls` as first arguments; UPPER_CASE constants. | Python | CS-05 | pep8#function-and-variable-names, pep8#function-and-method-arguments, pep8#method-names-and-instance-variables, pep8#constants |
| PEP-16 | Non-public names start with an underscore, and `__all__` declares the public API. | Python modules | CS-05 | pep8#public-and-internal-interfaces, pep8#designing-for-inheritance |
| PEP-17 | Programming idioms: `is`/`is not` for `None`, `isinstance()` instead of type comparison, `def` instead of assigning a lambda, `startswith`/`endswith` instead of slicing. | Python | CS-05 | pep8#programming-recommendations |
| PEP-18 | Catch specific exceptions; no bare `except:`; keep `try` bodies minimal; derive exceptions from `Exception`. (Swallowed errors: SEC-OP-02.) | Python exception handling | SQ-06 | pep8#programming-recommendations |
| PEP-19 | Return statements are consistent (all return an expression, or none do). `with` or `try`/`finally` ensures cleanup. | Python | CS-05 | pep8#programming-recommendations |
| PEP-20 | Annotations, where used, follow PEP 8 syntax and spacing (`x: int`, `-> str`). Whether they're required is SQR-36. | annotations present | CS-05 | pep8#function-annotations, pep8#variable-annotations |
| PEP-21 | Public modules, functions, classes and methods (including `__init__`) have docstrings. | public Python API | CS-04 | pep257#what-is-a-docstring, pep257#multi-line-docstrings |
| PEP-22 | Docstrings use `"""triple double quotes"""`. One-liners fit on one line as an imperative phrase ending in a period, with no signature repeated. | docstrings present | CS-04 | pep257#specification, pep257#one-line-docstrings |
| PEP-23 | Multi-line docstrings have a summary line, a blank line and a description. Function docstrings cover arguments, return values, side effects and exceptions raised. | docstrings present | CS-04 | pep257#multi-line-docstrings |
