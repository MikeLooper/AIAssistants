
Create a plan for building an agent, with multiple skills, that will review application source code and determine how well the application complies with standards and best-practices in: architecture, coding, and security.  The plan will be written to a file in the `docs` directory.
- If any part of this plan directive is unclear, interview the user for further details.
- The agent will use related tooling (references, sub-agents, and/or other tools) as needed to minimize context size and maximize flexibility and effectiveness.
- The agent tooling will be source code language-agnostic as much as possible.  Where it is necessary to be language-specific, ensure that the tool structure and the usage instructions are clear.
- Clarify that the agent is pre-approved to browse the links listed in the agent definition (including related tooling), but that other links must be approved by the user.
- After each step of the agent, save the data derived from that step; so that the agent can be re-started in the middle in case it was interrupted before completion.  Save this data in a `transitions` sub-directory.
- While the agent is executing, display a status to the user with the current step and the remaining work until completion.
- Create an agent README that includes the following:
	- The purpose and structure of the agent and related tooling.
	- Usage instructions.
	- How to resume the agent at a specific step after interruption.
	- Best practices in maintaining the agent and related tooling.
- At the end of the agent, create a report, written to the `docs` sub-directory, with a file name including a meaningful name plus the current date/time.
- This agent report will include the following:
	- A summary of the results.
	- The full results of the assessment.
	- Things that were done well.
	- Improvements that are recommended, divided into three categories: Errors, Warnings, and Information.
	- Recommended improvements will include a link to the source of the related standard or guideline, where possible.
- The subjects that will be assessed by the agent are:
1. Software Quality
2. Software Lifecycle
3. Application Design
  - Design Patterns
  - Twelve-Factor App
  - Architecture Patterns
4. API Design
  - OpenAPI
5. Security
  - OWASP Cheat Sheets
6. Implementation
  - Coding standards
  - Testing
  - Observability
  - Dependency management
7. Operations
  - Reliability
  - Performance
  - Disaster recovery
  - Monitoring
  - Cost/Sustainability
  - Mantainability
- Each subject may be split up as needed to minimize the amount of context required and achieve the most effective work accomplished within a skill or related tooling.
- The references listed below should only be loaded by the agent as-needed - to avoid overloading the context.

References:
1. API Design:
	- https://www.openapis.org/
	- https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
		- In this page:
			- The `DO` items are required, and are Errors if not implemented.
			- The `YOU SHOULD` items are recommended but not required, and are Warnings if not implemented.
			- The `YOU MAY` items are suggestions but not required, and are Information if not implemented.
2. Twelve-Factor App:
	- https://12factor.net/
3. Primary OWASP Cheat Sheets:
	- Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
	- Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
	- Content Security Policy Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
	- DotNet Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html
	- Error Handling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
	- File Upload Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
	- HTTP Security Response Headers Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
	- Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html
	- Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
	- JSON Web Token Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html
	- Java Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html
	- Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
	- OAuth 2.0 Protocol Cheatsheet: https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html
	- Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
	- Query Parameterization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
	- REST Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
	- SQL Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
	- Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
	- Secure Code Review Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
	- Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
	- XML Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html
	- Zero Trust Architecture Cheat Shee: https://cheatsheetseries.owasp.org/cheatsheets/Zero_Trust_Architecture_Cheat_Sheet.html
