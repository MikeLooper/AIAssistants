# Language Guidance — Python

Reference: PEP 8 — https://peps.python.org/pep-0008/

| id | Check | Default severity |
|----|-------|-------------------|
| CS-PY-01 | snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants | Warning |
| CS-PY-02 | Line length and indentation (4 spaces) follow PEP 8, or a documented formatter (Black) config | Information |
| CS-PY-03 | No bare `except:` clauses; exceptions are caught specifically | Warning |
| CS-PY-04 | Type hints are used on public function signatures where the project has adopted typing | Information |
| CS-PY-05 | Docstrings present on public modules/functions/classes | Information |
