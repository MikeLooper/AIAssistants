# Checklist — Dependency Management

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| DEP-01 | Dependencies are version-pinned (exact version or narrow range), not left floating (`*`, `latest`) | Warning | fallback rubric |
| DEP-02 | A lock file exists and is committed (`packages.lock.json`, `pom.xml` with pinned versions, `poetry.lock`/`requirements.txt` with pins) | Warning | fallback rubric |
| DEP-03 | No dependency has a known, unpatched vulnerability reported by an analyzer or manifest inspection | Error | fallback rubric |
| DEP-04 | No dependency targets an end-of-life runtime/framework version | Error | fallback rubric |
| DEP-05 | A license inventory or SBOM is present | Information | fallback rubric |
| DEP-06 | Dependency licenses are compatible with the project's stated license (if known) | Warning | fallback rubric |
