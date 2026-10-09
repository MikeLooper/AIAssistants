# Language Guidance — C#/.NET (Security)

Reference: OWASP .NET Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html

- Use `ASP.NET Core Identity` or a vetted identity provider rather than custom auth.
- Use `[Authorize]` attributes (with policies/roles) on controllers/actions; verify no sensitive endpoint is missing one.
- Data Protection API (`IDataProtector`) for anything needing encryption at rest in-process, not custom crypto.
- Antiforgery tokens (`[ValidateAntiForgeryToken]`) on state-changing form posts.
