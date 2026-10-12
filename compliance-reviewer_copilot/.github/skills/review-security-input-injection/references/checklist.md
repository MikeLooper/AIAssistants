# Checklist — Security: Input & Injection

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| SEC-II-01 | All external input is validated with an allow-list approach (type, length, format) before use | Error | https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html |
| SEC-II-02 | No user input is concatenated directly into SQL statements | Error | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html |
| SEC-II-03 | Database access uses parameterized queries/prepared statements or a vetted ORM | Error | https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html |
| SEC-II-04 | Command execution (shell, OS process) never interpolates unsanitized user input | Error | https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html |
| SEC-II-05 | XML parsers disable external entity resolution and DTD processing where not required (XXE prevention) | Error | https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html |
| SEC-II-06 | File uploads validate type/size and store with randomized names outside the web root | Error | https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html |
| SEC-II-07 | Uploaded files are not directly executable from the storage location | Error | https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html |
