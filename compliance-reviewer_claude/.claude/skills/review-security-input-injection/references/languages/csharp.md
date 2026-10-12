# Language Guidance — C#/.NET (Security)

Reference: OWASP .NET Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html

- Entity Framework/Dapper with parameterized queries; flag raw `SqlCommand` string concatenation or `FromSqlRaw` with interpolated strings.
- `XmlReaderSettings.DtdProcessing = DtdProcessing.Prohibit` and `XmlResolver = null` for XML parsing.
- File uploads validated via `IFormFile` content-type/size checks, stored via `Path.GetRandomFileName()` outside `wwwroot`.
