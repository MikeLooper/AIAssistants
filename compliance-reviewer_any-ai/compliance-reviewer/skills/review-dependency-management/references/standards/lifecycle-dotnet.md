# Runtime lifecycle — .NET — localized summary

- Sources: dotnet.microsoft.com .NET support policy (data: `releases-index.json`, retrieved 2026-11-07);
  learn.microsoft.com .NET Framework lifecycle (retrieved 2026-11-07)
- Localized: 2026-11-07 · Elements: dotnet.microsoft.com 6; learn.microsoft.com 5 (cap 100 each)
- Level: `LIFECYCLE` — the verdict comes from the date rule in `SKILL.md` (support end vs. reference date), not from a keyword.
- Dates are ISO `YYYY-MM-DD` (US Pacific end-of-support day as published).
- Citation: `Finding.url` = citation base + `#` + anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Source name for `Finding.standard` |
|-----|---------------|------------------------------------|
| dotnet | https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core | Microsoft .NET Support Policy |
| netfx | https://learn.microsoft.com/lifecycle/products/microsoft-net-framework | Microsoft .NET Framework Lifecycle |

## .NET (NET)

| ID | Level | Product | Line(s) | Support ends | Status at snapshot | Detection | Anchor |
|----|-------|---------|---------|--------------|--------------------|-----------|--------|
| NET-01 | LIFECYCLE | .NET | 11.0 (STS) | not published | pre-release (go-live RC3); GA expected 2026-11 | `net11.0*` TFM, SDK 11.0 | dotnet#previews |
| NET-02 | LIFECYCLE | .NET | 10.0 (LTS) | 2028-11-14 | active | `net10.0*` TFM, SDK 10.0 | dotnet#lifecycle |
| NET-03 | LIFECYCLE | .NET | 9.0 (STS) | 2026-11-10 | maintenance | `net9.0*` TFM, SDK 9.0 | dotnet#lifecycle |
| NET-04 | LIFECYCLE | .NET | 8.0 (LTS) | 2026-11-10 | maintenance | `net8.0*` TFM, SDK 8.0 | dotnet#lifecycle |
| NET-05 | LIFECYCLE | .NET / .NET Core | 7.0 (2024-05-14), 6.0 (2024-11-12), 5.0 (2022-05-10), Core 3.1 (2022-12-13), 3.0 (2020-03-03), 2.2 (2019-12-23), 2.1 (2021-08-21), 2.0 (2018-10-01), 1.1, 1.0 (2019-06-27) | as listed (latest 2024-11-12) | end of life | `net7.0*`…`net5.0*` TFM, `netcoreapp*` | dotnet#lifecycle |
| NET-06 | LIFECYCLE | Packages versioned with .NET | `Microsoft.AspNetCore.*`, `Microsoft.EntityFrameworkCore.*`, `Microsoft.Extensions.*` at major N | same as .NET N (NET-01…05) | — | package version major | dotnet#whats-covered |

## .NET Framework (NFX)

| ID | Level | Product | Line(s) | Support ends | Status at snapshot | Detection | Anchor |
|----|-------|---------|---------|--------------|--------------------|-----------|--------|
| NFX-01 | LIFECYCLE | .NET Framework | 4.8.1, 4.8 | with the host OS (no fixed date) | supported | `net48`, `net481`, `v4.8*` | netfx#support-dates |
| NFX-02 | LIFECYCLE | .NET Framework | 4.7.2, 4.7.1, 4.7 | with the host OS (no fixed date) | supported | `net47*`, `v4.7*` | netfx#support-dates |
| NFX-03 | LIFECYCLE | .NET Framework | 4.6.2 | 2027-01-12 | supported | `net462`, `v4.6.2` | netfx#support-dates |
| NFX-04 | LIFECYCLE | .NET Framework | 3.5 SP1 | 2029-01-09 | supported | `net35`, `v3.5` | netfx#support-dates |
| NFX-05 | LIFECYCLE | .NET Framework | 4.6.1, 4.6, 4.5.2 (2022-04-26); 4.5.1, 4.5, 4.0 (2016-01-12); 3.0, 2.0 (2011-07-12) | as listed | end of life | `net461`…`net20`, `v4.6.1`…`v2.0` | netfx#support-dates |

`netstandard*` is a specification, not a runtime, and is never end-of-life.
