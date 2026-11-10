# MDN Web Docs — browser security directives — localized summary

- Source site: developer.mozilla.org (MDN Web Docs, English)
- Localized: 2026-11-09 · Elements: 1 (cap 100)
- Level: `SHOULD` (MDN documents the directive and gives no normative level; it is defense in depth). A failed `SHOULD`
  element scores one level below the check's default (`../../SKILL.md` step 6). Never report its absence as an XSS
  vulnerability: XSS encoding and DOM sinks are judged by `review-security-input-injection` SEC-II-08.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Pinned version | Source name for `Finding.standard` |
|-----|---------------|----------------|------------------------------------|
| rttf | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for | page last modified 2025-12-22 (Baseline 2026, newly available since February 2026) | MDN Web Docs |

## SEC-WA-01 — Content Security Policy

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| MDN-01 | SHOULD | HTML apps whose own scripts write to DOM XSS sinks set `require-trusted-types-for 'script'` in their CSP (with a `trusted-types` policy allowlist), so sinks accept only values created by Trusted Type policies, not strings. | CSP set, but the app's scripts use `innerHTML`, `outerHTML`, `insertAdjacentHTML` or `document.write` and the CSP has no `require-trusted-types-for` | SEC-WA-01 | rttf#syntax, rttf#examples |
