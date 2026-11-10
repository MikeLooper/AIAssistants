# Detection signals — C#/.NET (Security: Input & Injection)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). A signal is evidence only when untrusted data reaches it or the setting is explicit (`SKILL.md`
step 3). The only .NET defaults a worker may rely on are those stated in `dotnet-input.md` (NET-07, NET-08, NET-11,
NET-14); for anything else, report explicit values only.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `FromSqlRaw`/`ExecuteSqlRaw`/`SqlQueryRaw` with `$"…"` or `+`; `SqlCommand`/`OleDbCommand` text built by concatenation; Dapper `Query(sql + …)` | repositories, `DbContext` code, services | SQL built from untrusted values | NET-01, NET-07, SQL-01 |
| Home-made `Escape(…)` / `Replace("'", "''")` before building SQL | data access helpers | Manual escaping instead of binding | SQL-05 |
| `SqlCommand` without `Parameters.Add…` next to user values; values "validated" then concatenated | data access | No bind API; validation used instead of binding | QP-02, SQL-06 |
| `OrderBy` strings, `$"ORDER BY {sort}"` or table names from request input | repositories, query builders | Dynamic identifiers not allowlisted | SQL-04, NET-02 |
| `EXEC('…' + @p)`, `sp_executesql` with concatenated text | `*.sql` stored procedures, migrations | Dynamic SQL inside procedures | SQL-03 |
| Connection strings with `User Id=sa`, `db_owner`/admin accounts | `appsettings*.json`, `web.config`, migrations | Over-privileged database account | SQL-07 |
| `XmlReaderSettings { DtdProcessing = DtdProcessing.Parse }`; `XmlUrlResolver` or a non-null `XmlResolver` on `XmlDocument`/`XmlReaderSettings`; `XslCompiledTransform` with `XsltSettings.TrustedXslt` | XML parsing code | DTDs/external resources enabled on untrusted XML | NET-08, NET-05, XML-01, XML-02 |
| Schemas loaded from `xsi:schemaLocation` or an `http://` URL | XML validation code | Untrusted schema source | XML-05 |
| `BinaryFormatter`, `SoapFormatter`, `LosFormatter`, `NetDataContractSerializer`, `ObjectStateFormatter` | serializers, caches, message consumers | Dangerous native deserialization | NET-09, DES-03 |
| Newtonsoft `TypeNameHandling` other than `None` (without a `SerializationBinder`); `JavaScriptTypeResolver`; `Type.GetType(<payload value>)` | JSON settings, `Program.cs`, consumers | Payload selects the type | DES-02, DES-09, NET-04 |
| `Process.Start`/`ProcessStartInfo.Arguments` with request data; `cmd.exe /c`, `powershell -Command` with input | services, controllers | Command injection | NET-15, INJ-04, INJ-05 |
| `CSharpScript.EvaluateAsync`, `DataTable.Compute`, dynamic LINQ strings from input | services | Runtime code/expression evaluation | INJ-03 |
| `DirectorySearcher.Filter` / LDAP filters built by concatenation; `XPathNavigator.Select(… + input)` | directory and XML query code | LDAP/XPath injection | INJ-06 |
| `Html.Raw`, `new HtmlString(`, Blazor `MarkupString` / `@((MarkupString)…)` with user data | `*.cshtml`, `*.razor`, tag helpers | Encoding bypassed | NET-03, XSS-02 |
| Inline `<script>` with `@Model…` or `@Json.Serialize(…)` of user data; `innerHTML` with server values | views, front-end scripts | Wrong-context encoding | NET-13, XSS-04, XSS-09 |
| `<%= … %>` in Web Forms/MVC 5 views relying on `ValidateRequest` | `*.aspx`, `*.ascx`, legacy views | Legacy XSS | NET-06 |
| `IFormFile.FileName` in a storage path (`Path.Combine(dir, file.FileName)`) | upload handlers | Client filename used for storage | NET-10, FU-04 |
| Upload type decided by `IFormFile.ContentType` only; extension check on the raw name | upload handlers | Weak type validation | FU-03, FU-02, FU-01 |
| `MaxRequestBodySize = null`, `[DisableRequestSizeLimit]`, very large `[RequestSizeLimit]`/`MultipartBodyLengthLimit`; `ZipArchive` extracted without size/entry limits | `Program.cs`, controllers, upload code | Unbounded upload size | NET-11, FU-05 |
| Uploads saved under `wwwroot` / content root; `UseStaticFiles` serving the upload folder; links to `/uploads/<name>` | `Program.cs`, upload code, views | Uploads served/executed from storage | NET-12, FU-07, FU-08 |
| MVC/Razor Pages handlers without `[ApiController]` and without `ModelState.IsValid`; `SuppressModelStateInvalidFilter = true` | controllers, pages, `Program.cs` | Validation result ignored | NET-14, IV-07 |
| EF entities bound directly as action parameters | controllers | Mass assignment | IV-07 |
| `new Regex(pattern)` on input without `matchTimeout` or `RegexOptions.NonBacktracking` | validators | ReDoS-prone validation | IV-08 |
| `[StringLength]`/`[Range]`/`[MaxLength]` absent on request DTO strings, numbers and collections | DTOs, view models | Unbounded field rules | IV-02 |
