---
name: job-search-attributes
description: "Use when the job-search agent needs to turn raw job listing/detail text into the requested attributes (Job Title, Programming Language, Tools, Salary Range), using settings/programminglanguages.txt and settings/tools.txt as the source of truth."
---

# Job Search Attributes Skill

## Objective
Given raw title/detail text for a candidate job (from the `job-search-extraction` skill) and the ordered `attributes` list (from the `job-search-config` skill), produce the `attributes` map for that job.

Recommended built-in helpers:
- `Job Title`: first strong title candidate (header or first meaningful line)
- `Programming Language`: extract technologies from free text using keyword, alias, and delimiter-aware matching
- `Tools`: extract platform, cloud, DevOps, protocol, and lifecycle tooling terms from free text
- `Salary Range`: capture values like `$100,000 - $200,000`, `100K-200K`, `Up to $300K`, `$150K+`

### Programming Language Extraction Logic

When extracting `Programming Language`, scan the combined job text (title, summary, description, requirements) and return all matched technologies as a deduplicated list.

Detection rules:
- Match case-insensitively.
- Support comma-separated, slash-separated, and parenthetical lists.
- Treat punctuation as separators (`/`, `,`, `(`, `)`, `;`, `:`).
- Use word-boundary-safe matching to avoid partial false positives.
- Avoid broad `\bgo\b` language matching; prefer `golang` or an explicit phrase to reduce false positives.

Data-source rules:
- Read `settings/programminglanguages.txt` as the primary source of known programming languages and aliases.
- Preserve the file's order for first-seen output.
- Treat each non-empty, non-comment line as one candidate entry.
- If a line contains a colon, use the part before the colon as the discovery term and the part after the colon as the reporting value.
- If no colon is present, the value is both the discovery term and the reporting value.
- Build the matcher from the configured values rather than from hard-coded language lists in this skill.
- Keep direct canonical names when present and prefer the configured reporting value when available.

Extraction notes:
- If both parent and child ecosystem terms appear, keep both (example: `JavaScript/Node.js` -> `JavaScript`, `Node.js`).
- Return unique outputs in first-seen order.
- Do not require terms to appear in a specific section; requirement and narrative text both count.

### Tools Extraction Logic

When extracting `Tools`, scan the combined job text (title, summary, description, requirements) and return all matched tools as a deduplicated list.

Detection rules:
- Match case-insensitively.
- Support comma-separated, slash-separated, and parenthetical lists.
- Treat punctuation as separators (`/`, `,`, `(`, `)`, `;`, `:`).
- Use word-boundary-safe matching to avoid partial false positives.

Data-source rules:
- Read `settings/tools.txt` as the primary source of known tools and aliases.
- Preserve the file's order for first-seen output.
- Treat each non-empty, non-comment line as one candidate entry.
- If a line contains a colon, use the part before the colon as the discovery term and the part after the colon as the reporting value.
- If no colon is present, the value is both the discovery term and the reporting value.
- Build the matcher from the configured values rather than from hard-coded tool lists in this skill.
- Keep direct canonical names when present and prefer the configured reporting value when available.

Extraction notes:
- Return unique outputs in first-seen order.
- If umbrella and child tools both appear, keep both (example: `AWS` and `EC2`).
- Do not require terms to appear in a specific section; requirement and narrative text both count.

## Output Contract
Return an `attributes` map keyed by the requested `attributes.txt` entries. When present, keep this attribute order:
1. `Job Title`
2. `Programming Language`
3. `Tools`
4. `Salary Range`

Append any additional attributes after these four, preserving original `attributes.txt` order.
