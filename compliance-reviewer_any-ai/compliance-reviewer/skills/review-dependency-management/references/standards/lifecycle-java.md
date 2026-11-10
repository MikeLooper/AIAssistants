# Runtime lifecycle — Java — localized summary

- Sources: adoptium.net Eclipse Temurin support / release roadmap (retrieved 2026-11-07);
  spring.io Spring Boot and Spring Framework support (data: `api.spring.io/projects/<project>/generations`, retrieved 2026-11-07)
- Localized: 2026-11-07 · Elements: adoptium.net 8; spring.io 7 (cap 100 each)
- Level: `LIFECYCLE` — the verdict comes from the date rule in `SKILL.md` (support end vs. reference date), not from a keyword.
- Dates: `YYYY-MM` means the last day of that month. Temurin's "at least" dates are read as the date shown.
  "Supported" means community/OSS support. Spring's "Commercial end" column feeds recommendation text only; the verdict uses OSS support end.
- Citation: `Finding.url` = citation base + `#` + anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Source name for `Finding.standard` |
|-----|---------------|------------------------------------|
| temurin | https://adoptium.net/support/ | Eclipse Temurin Support |
| boot | https://spring.io/projects/spring-boot | Spring Support Policy |
| framework | https://spring.io/projects/spring-framework | Spring Support Policy |

## Java — Eclipse Temurin (JDK)

Detection: Maven `<maven.compiler.release>`/`source`/`target`/`<java.version>`, Gradle toolchain / `sourceCompatibility`, `.java-version`.

| ID | Level | Product | Line(s) | Support ends | Status at snapshot | Detection | Anchor |
|----|-------|---------|---------|--------------|--------------------|-----------|--------|
| JDK-01 | LIFECYCLE | Java (Temurin) | 27 | 2027-03 | supported (non-LTS) | release/toolchain 27 | temurin#release-roadmap |
| JDK-02 | LIFECYCLE | Java (Temurin) | 25 (LTS) | 2031-09 (at least) | supported | release/toolchain 25 | temurin#release-roadmap |
| JDK-03 | LIFECYCLE | Java (Temurin) | 21 (LTS) | 2029-12 (at least) | supported | release/toolchain 21 | temurin#release-roadmap |
| JDK-04 | LIFECYCLE | Java (Temurin) | 17 (LTS) | 2027-10 (at least) | supported | release/toolchain 17 | temurin#release-roadmap |
| JDK-05 | LIFECYCLE | Java (Temurin) | 11 (LTS) | 2027-10 (at least) | supported | release/toolchain 11 | temurin#release-roadmap |
| JDK-06 | LIFECYCLE | Java (Temurin) | 8 (LTS) | 2030-12 (at least) | supported | `1.8`, `8` | temurin#release-roadmap |
| JDK-07 | LIFECYCLE | Java (Temurin) | 26 | 2026-09 | end of life | release/toolchain 26 | temurin#release-roadmap |
| JDK-08 | LIFECYCLE | Java (Temurin) | all other non-LTS lines: 24 (2025-09), 23 (2025-03), 22 (2024-09), 20 (2023-09), 19 (2023-03), 18 (2022-09), 16 (2021-09) and older; anything before 8 | as listed (latest 2025-09) | end of life | release/toolchain ≤ 24, not 25/21/17/11/8 | temurin#release-roadmap |

## Spring (SPR)

Detection: Spring Boot — `spring-boot-starter-parent` / `spring-boot-dependencies` BOM / `org.springframework.boot` plugin version.
Spring Framework — explicit `spring-framework-bom` / `spring-core` version (evaluate only when Boot isn't used or the Framework version is overridden).

| ID | Level | Product | Line(s) | OSS support ends | Commercial end | Status at snapshot | Detection | Anchor |
|----|-------|---------|---------|------------------|----------------|--------------------|-----------|--------|
| SPR-01 | LIFECYCLE | Spring Boot | 4.2.x | 2027-12-31 | 2028-12-31 | pre-release (GA 2026-11-30) | Boot version 4.2.x | boot#support |
| SPR-02 | LIFECYCLE | Spring Boot | 4.1.x | 2027-07-31 | 2028-07-31 | supported | Boot version 4.1.x | boot#support |
| SPR-03 | LIFECYCLE | Spring Boot | 4.0.x | 2026-12-31 | 2027-12-31 | supported | Boot version 4.0.x | boot#support |
| SPR-04 | LIFECYCLE | Spring Boot | 3.5.x (2026-06-30), 3.4.x (2025-12-31), 3.3.x (2025-06-30), 3.2.x (2024-12-31), 3.1.x (2024-06-30), 3.0.x (2023-12-31), 2.7.x (2023-06-30), 2.6.x and older (≤ 2022-11-30) | as listed | 3.5 2032-06-30; 3.4 2026-12-31; 3.3 2026-06-30; 2.7 2029-06-30; others ended | end of OSS support | Boot version ≤ 3.5.x | boot#support |
| SPR-05 | LIFECYCLE | Spring Framework | 7.1.x | 2027-12-31 | 2028-12-31 | pre-release (GA 2026-11-30) | Framework version 7.1.x | framework#support |
| SPR-06 | LIFECYCLE | Spring Framework | 7.0.x | 2027-07-31 | 2028-07-31 | supported | Framework version 7.0.x | framework#support |
| SPR-07 | LIFECYCLE | Spring Framework | 6.2.x (2026-06-30), 6.1.x (2025-06-30), 6.0.x (2024-06-30), 5.3.x (2024-08-31), 5.2.x (2021-12-31), 5.1.x and older (2020-12-31) | as listed | 6.x 2032-06-30; 5.2–5.3 2029-06-30; others ended | end of OSS support | Framework version ≤ 6.2.x | framework#support |
