# OpenAPI Specification — localized summary

- Source site: spec.openapis.org
- Pinned pages: v3.0.4, v3.1.2, v3.2.1 (latest patch of each minor line on 2026-11-07), plus v2.0 for detection only
- Citation base (pick the page that matches the target's `openapi` value; never use `latest`):
  - `3.0.x` → https://spec.openapis.org/oas/v3.0.4.html
  - `3.1.x` → https://spec.openapis.org/oas/v3.1.2.html
  - `3.2.x` → https://spec.openapis.org/oas/v3.2.1.html
  - `swagger: "2.0"` → https://spec.openapis.org/oas/v2.0.html
- Localized: 2026-11-07 · Elements: 43 (cap 100)
- Source name for `Finding.standard`: `OpenAPI Specification`
- Ver column: `all` = same rule in 3.0/3.1/3.2; `differs` = the summary states the per-version rule; `2.0` = Swagger 2.0 only.
- Level `REVIEW` = locally derived review rule (spec ↔ implementation match); it takes the owning check's default severity.

| ID | Level | Requirement (summary) | Ver | Anchor |
|----|-------|-----------------------|-----|--------|
| OAS-01 | REQUIRED | Root `openapi` field holds the OAS version (`3.0.x`/`3.1.x`/`3.2.x`); select the rule set and citation base from it. `swagger: "2.0"` → OAS-43. | all | openapi-object |
| OAS-02 | REQUIRED | `info` with `title` and `version`; `info.version` is the API document's version, not the OAS version. | all | info-object |
| OAS-03 | REQUIRED / MUST | 3.0: `paths` is required. 3.1+: at least one of `paths`, `components`, `webhooks` MUST be present. | differs | openapi-object |
| OAS-04 | MUST / RECOMMENDED | Document is JSON or YAML; field names are case-sensitive; YAML map keys MUST be scalar strings; YAML 1.2 is RECOMMENDED. | all | format |
| OAS-05 | MUST | Fields not defined by the spec are invalid unless they are extensions starting with `x-`. 3.1+: `x-oai-`/`x-oas-` are reserved for the OpenAPI Initiative. | differs | specification-extensions |
| OAS-06 | MUST | `components` map keys match `^[a-zA-Z0-9\.\-_]+$`. | all | components-object |
| OAS-07 | REQUIRED / MUST / SHOULD | Server URL variables are defined in `servers[].variables`, each with a `default`. `enum`: 3.0 SHOULD NOT be empty and default SHOULD be in it; 3.1+ MUST NOT be empty and default MUST be in it. | differs | server-variable-object |
| OAS-08 | MUST | Every `paths` key begins with `/`. | all | paths-object |
| OAS-09 | MUST NOT | Templated paths with the same hierarchy but different template names (e.g. `/pets/{id}` and `/pets/{name}`). | all | path-templating |
| OAS-10 | MUST | Every `{template}` in a path corresponds to an `in: path` parameter at path-item and/or operation level (3.1+: except an empty path item). | all | path-templating |
| OAS-11 | MUST / RECOMMENDED | `operationId` is unique across all operations (case-sensitive); RECOMMENDED to follow common programming naming conventions. | all | operation-object |
| OAS-12 | MUST NOT | Duplicate parameters (same `name` + `in`) within one path-item or operation `parameters` list. | all | operation-object |
| OAS-13 | REQUIRED | Each parameter has `name` and `in` ∈ `query`, `header`, `path`, `cookie`; 3.2 adds `querystring` (not combinable with `in: query` in the same operation). | differs | parameter-object |
| OAS-14 | REQUIRED / MUST | Path parameters declare `required: true`. | all | parameter-object |
| OAS-15 | MUST | A parameter has exactly one of `schema` or `content`; a parameter's `content` map has exactly one entry. | all | parameter-object |
| OAS-16 | SHALL | Header parameters named `Accept`, `Content-Type` or `Authorization` are ignored; describe them via `content`/security schemes instead. | all | parameter-object |
| OAS-17 | REQUIRED / SHALL / SHOULD | `requestBody.content` is required. Bodies on GET/HEAD/DELETE: 3.0 SHALL be ignored by consumers; 3.1 SHOULD be avoided; 3.2 SHOULD be avoided on GET/DELETE. | differs | request-body-object |
| OAS-18 | REQUIRED / SHOULD | 3.0: every operation has `responses`. 3.1+: optional, but a Responses Object has ≥ 1 code; if only one, it SHOULD be the success response. | differs | responses-object |
| OAS-19 | REQUIRED | Response `description` is required in 3.0 and 3.1; optional in 3.2. | differs | response-object |
| OAS-20 | MUST | Status-code keys are strings (quoted in YAML); ranges use `1XX`–`5XX` (uppercase X); an explicit code overrides a range. | all | responses-object |
| OAS-21 | MAY | `default` may describe all responses not declared individually (typically the error shape). | all | responses-object |
| OAS-22 | REVIEW | `content` keys are media types or media-type ranges; for a request matching several keys only the most specific applies. | all | media-type-object |
| OAS-23 | MUST | Schema dialect: 3.0 = OAS subset of JSON Schema, nullability via `nullable`; 3.1+ = JSON Schema 2020-12, nullability via `type: [..., "null"]` (`nullable` is not a 3.1+ keyword). | differs | schema-object |
| OAS-24 | REQUIRED | Every `$ref` resolves. 3.0: other keys beside `$ref` SHALL be ignored. 3.1+: a Reference Object allows only `summary`/`description` siblings. | differs | reference-object |
| OAS-25 | REQUIRED / SHOULD / MUST | `discriminator.propertyName` is set and used with `oneOf`/`anyOf`/`allOf`. 3.0/3.1: the property SHOULD be required. 3.2: it may be optional, but then `defaultMapping` MUST be set. | differs | discriminator-object |
| OAS-26 | SHOULD NOT | `readOnly` properties are not sent in requests; `writeOnly` properties are not sent in responses. | all | schema-object |
| OAS-27 | REVIEW | `type`/`format` values (`int32`, `int64`, `float`, `double`, `date`, `date-time`, `uuid`, `byte`, `binary`, `password`) match the implementation's types. | all | data-types |
| OAS-28 | REVIEW | `required` arrays list exactly the properties the implementation always requires/returns. | all | schema-object |
| OAS-29 | SHOULD | `example`/`examples` values match their schema. | all | example-object |
| OAS-30 | REVIEW | `enum` values in schemas match the implementation's enum values. | all | schema-object |
| OAS-31 | REQUIRED | Each security scheme has a valid `type` (`apiKey`, `http`, `oauth2`, `openIdConnect`; `mutualTLS` 3.1+) with its required fields (`name`+`in`, `scheme`, `flows`, `openIdConnectUrl`). | differs | security-scheme-object |
| OAS-32 | MUST | Security requirement names match declared `securitySchemes`; scope list for oauth2/OIDC. Other types: 3.0 the array MUST be empty; 3.1+ it MAY list role names. | differs | security-requirement-object |
| OAS-33 | REVIEW | Root `security` applies by default and operation `security` overrides it; operations that are public in code use `security: []` (and only those). | all | operation-object |
| OAS-34 | MUST | Tag names in the root `tags` list are unique. | all | tag-object |
| OAS-35 | MUST | In Link Objects, `operationRef` and `operationId` are mutually exclusive and resolve to a real, unique operation. | all | link-object |
| OAS-36 | REVIEW | Operations/parameters/schemas that are deprecated in code carry `deprecated: true`, and vice versa. | all | operation-object |
| OAS-37 | MUST | URL/email fields are well-formed (`termsOfService`, `contact.url`, `contact.email`, `license.url`). 3.1+: `license.identifier` and `license.url` are mutually exclusive. | differs | info-object |
| OAS-38 | REVIEW | Every implemented route + HTTP method appears in `paths`, and every documented path/method exists in code. | all | paths-object |
| OAS-39 | REVIEW | Parameter names, locations (`in`), types and `required` match handler signatures and binding attributes. | all | parameter-object |
| OAS-40 | REVIEW | Request/response schemas match DTO property names (after the serializer naming policy), types, required-ness and nullability. | all | schema-object |
| OAS-41 | REVIEW | Documented response status codes match the codes the handlers actually return (including error paths). | all | responses-object |
| OAS-42 | REVIEW | Documented security matches the auth attributes/middleware applied to each route. | all | security-requirement-object |
| OAS-43 | MAY | Swagger 2.0 (`swagger: "2.0"`; `host`/`basePath`, `definitions`, `in: body`/`formData`, `consumes`/`produces`): check only the OAS-08 … OAS-14 equivalents and recommend migrating to OAS 3.x (Information). | 2.0 | swagger-object |
