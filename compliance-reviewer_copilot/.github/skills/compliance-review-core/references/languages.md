# Language Detection

## Signals

| Language | Language id | Signals (file globs) |
|----------|-------------|-----------------------|
| C#/.NET | `csharp` | `*.csproj`, `*.sln` |
| Java | `java` | `pom.xml`, `build.gradle`, `build.gradle.kts` |
| Python | `python` | `pyproject.toml`, `requirements.txt`, `setup.py` |

Any other language is treated as `generic` — only the language-agnostic core of each skill applies.

## Loading Convention

Every subject skill that ships per-language guidance follows this rule:

1. Always load `references/checklist.md`.
2. For each language id found during inventory (`01-inventory.json`), also load `references/languages/<id>.md` if that file exists in the skill.
3. If no `languages/` file exists for a detected language, or the repo only has `generic` signals, use the checklist alone.

A repo may contain more than one language (e.g. a Java backend with a Python tooling script). Load every matching language file, not just the first match.
