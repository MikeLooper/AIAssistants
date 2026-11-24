# Jackson property exclusion — localized summary

- Sources: github.com — FasterXML/jackson-annotations wiki, "Jackson Annotations" (page text at retrieval 2026-11-24,
  recorded as a text hash in `pins.json`)
- Localized: 2026-11-24 · Elements: github.com 2 (prefix `JVD-`; counted in this skill's per-website budget)
- Applies when language `java` is detected and Jackson (`com.fasterxml.jackson`, Spring Boot's default JSON mapper)
  serializes the response objects.
- Level: `SHOULD` for usage guidance; **(Default)** marks an element that states annotation behaviour. Levels are
  informational: every Finding takes its check's default severity.
- Citation: `Finding.url` = citation base (the wiki page has no stable per-annotation anchors). `Finding.standard` =
  `"<source name> — <element ID>"`.

| Key | Citation base | Pinned version | Source name for `Finding.standard` |
|-----|---------------|----------------|------------------------------------|
| jak | https://github.com/FasterXML/jackson-annotations/wiki/Jackson-Annotations | page at retrieval 2026-11-24 | Jackson Annotations (FasterXML wiki) |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| JVD-01 | SHOULD | **(Default)** Exclude sensitive properties from JSON output with `@JsonIgnore` (on one accessor it removes the whole property; with `@JsonProperty` on the setter the property becomes input-only) or with class-level `@JsonIgnoreProperties({"…"})`; `@JsonIgnore` wins over `@JsonProperty`. | `@Entity` returned from a `@RestController` with password, SSN or internal fields and no `@JsonIgnore` | DPR-02 | jak |
| JVD-02 | SHOULD | **(Default)** `@JsonView` defines the views in which a property is serialized, so one class can expose a restricted public view. | a single entity serialized for public and admin endpoints with no views or DTOs | DPR-02 | jak |
