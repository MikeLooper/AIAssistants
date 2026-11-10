# Runtime lifecycle — Python — localized summary

- Source: devguide.python.org — Status of Python versions (retrieved 2026-11-07)
- Localized: 2026-11-07 · Elements: devguide.python.org 7 (cap 100)
- Level: `LIFECYCLE` — the verdict comes from the date rule in `SKILL.md` (support end vs. reference date), not from a keyword.
- Dates: `YYYY-MM` means the last day of that month.
- Detection (all rows): `requires-python`, `python_requires`, `.python-version`, `runtime.txt`, Poetry `[tool.poetry.dependencies] python`.
  For ranges, evaluate the highest version the range permits (see `SKILL.md`).
- Citation: `Finding.url` = citation base + `#` + anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Source name for `Finding.standard` |
|-----|---------------|------------------------------------|
| pyver | https://devguide.python.org/versions/ | Python Developer's Guide — Status of Python versions |

| ID | Level | Product | Line(s) | Support ends | Status at snapshot | Anchor |
|----|-------|---------|---------|--------------|--------------------|--------|
| PY-01 | LIFECYCLE | Python | 3.16 (main) | 2032-10 | pre-release (feature; first release 2027-10-06) | pyver#supported-versions |
| PY-02 | LIFECYCLE | Python | 3.15 | 2031-10 | bugfix | pyver#supported-versions |
| PY-03 | LIFECYCLE | Python | 3.14 | 2030-10 | bugfix | pyver#supported-versions |
| PY-04 | LIFECYCLE | Python | 3.13 | 2029-10 | security | pyver#supported-versions |
| PY-05 | LIFECYCLE | Python | 3.12 | 2028-10 | security | pyver#supported-versions |
| PY-06 | LIFECYCLE | Python | 3.11 | 2027-10 | security | pyver#supported-versions |
| PY-07 | LIFECYCLE | Python | 3.10 (2026-10-01), 3.9 (2025-10-31), 3.8 (2024-10-07), 3.7 (2023-06-27), 3.6 (2021-12-23), 3.5 (2020-09-30), 3.4 (2019-03-18), 3.3 (2017-09-29), 3.2 (2016-02-20), 3.1 (2012-04-09), 3.0 (2009-06-27), 2.7 (2020-01-01), 2.6 (2013-10-29) | as listed | end of life | pyver#unsupported-versions |
