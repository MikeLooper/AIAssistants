# Checklist — Data Protection

Subject: Data Protection

Each check is evaluated through the elements it lists; every element belongs to exactly one check. Element
definitions, anchors and citation bases are in `standards/`. Every Finding takes its check's default severity
(`../SKILL.md` step 7). These are engineering controls only: no check judges lawful basis, consent or legal
compliance.

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|------------------|----------|--------|
| DPR-01 | Storage | Sensitive personal fields (national IDs, payment card numbers, health and biometric data) are minimized and encrypted, tokenized or hashed at rest at field or store level, with sound algorithms and keys kept apart from the data; no plaintext card numbers | Error | CSD-01, CSD-02, CSD-03, CSD-04, A04-03, A04-04, A04-05, UPP-01, SP122-09, GDPR-05 | CSD, A04, UPP, SP122, GDPR |
| DPR-02 | Exposure | API responses and serializers expose only the properties the caller needs: DTOs, projections or explicit field lists instead of persistence entities, with sensitive fields excluded | Error | BOP-01, BOP-02, BOP-03, BOP-04, SP122-03, SP122-08, GDPR-04, JVD-01, JVD-02, PYD-01, PYD-02 | BOP, SP122, GDPR, JVD, PYD |
| DPR-03 | Exposure | Personal data isn't put in URLs or query strings, `localStorage`/`sessionStorage` or IndexedDB, and sensitive form fields don't invite autofill | Warning | CSD-05, HSP-01, HSP-02, HSP-03, QSE-01, TPS-05 | CSD, HSP, QSE, TPS |
| DPR-04 | Sharing | Personal data sent to third parties (error trackers, analytics, LLM/AI APIs, email/SMS providers, embedded third-party content) is minimized or scrubbed; SDK switches that send user data by default are turned off or restricted | Warning | UPP-02, GDPR-01, TPS-01, TPS-02, TPS-03, TPS-04 | UPP, GDPR, TPS |
| DPR-05 | Non-Production Data | Test fixtures, seed data and samples use synthetic data (reserved domains such as `example.com`, published test card numbers, obviously fake values), not real-looking personal data | Warning | SP122-06, RSV-01 | SP122, RSV |
| DPR-06 | Lifecycle | Personal data has a deletion or anonymization path, and retention is bounded where the code stores it (delete or erase operations, purge jobs, TTLs) | Information | SP122-04, GDPR-02 | SP122, GDPR |
| DPR-07 | Non-Production Data | Scripts and jobs that copy production data to other environments mask, pseudonymize or anonymize personal fields, keeping any re-identification key apart | Warning | SP122-05, SP122-07, GDPR-03 | SP122, GDPR |
| DPR-08 | Governance | Personal-data fields are identified in code (classification attributes or annotations, or a documented data inventory) and classified data gets the controls its class requires | Information | A04-01, A04-02, SP122-01, SP122-02, DND-01, DND-02 | A04, SP122, DND |

Totals: 20 OWASP + 9 NIST + 5 GDPR + 1 RFC 2606 + 5 third-party SDK + 2 DND + 2 JVD + 2 PYD = 46 elements across 8 checks.

## Evidence notes

- **Personal data** means the identifiers and linked data listed in SP122-02. "Sensitive personal data" (DPR-01) is the
  subset whose exposure causes the most harm: national and tax IDs, passport and driver's licence numbers, payment
  card and bank account numbers, health, biometric and precise location data.
- **DPR-01:** fail when an entity, table or document stores sensitive personal data in a plain column with no field
  encryption, value converter, tokenization, hashing or truncation in the files; when full card numbers or CVV are
  stored at all; or when application-level encryption uses ECB, a custom scheme or keys stored beside the data. Store-
  level encryption shown in IaC passes for the store it covers (advanced usage only). Names, emails and phone numbers
  alone don't fail DPR-01.
- **DPR-02:** fail when a controller, route handler, resolver or MCP tool returns a persistence entity or ORM model
  that has personal or internal fields the endpoint doesn't need (password hashes, other users' contact data, internal
  flags), returns `to_json()`/`model_dump()`/`__dict__` of such an object, or when a serializer exposes every model
  field (`fields = '__all__'`, no `@JsonIgnore` on sensitive properties). Input binding (over-posting) is SEC-II-01.
- **DPR-03:** fail on routes, links, redirects or client calls that put personal data (email, phone, name, national
  ID, date of birth) in the path or query string; on `localStorage`/`sessionStorage`/IndexedDB writes of personal
  data; and, as a lower-confidence finding, on sensitive personal input fields without `autocomplete="off"`.
  Credentials and tokens are not judged here.
- **DPR-04:** fail when an error-tracker or analytics SDK is configured to send user data (`SendDefaultPii = true`,
  Sentry `userInfo`/`user_info` left at its default where the files set user identity, request bodies or local
  variables collected on endpoints that handle personal data), or when code sends personal data to an LLM/AI,
  email or SMS API without minimizing it to what the call needs. Telemetry attributes are OBS-10.
- **DPR-05:** fail on real-looking personal data in test, fixture, seed or sample files: Luhn-valid card numbers that
  aren't published test numbers, national-ID shapes, checksum-valid IBANs or emails on non-reserved domains attached
  to person names. Use the payload's `piiCandidates` as a starting point (SKILL.md step 3).
- **DPR-06:** fail (Information) when the files store personal data and show no delete, erase, anonymize or purge
  path for it and no TTL or retention setting. Soft-delete flags that never purge count as no deletion path.
- **DPR-07:** fail when a script or job copies a production database (dump, restore, bacpac, snapshot) into another
  environment without a masking or anonymizing step in the files. N/A when no such script exists.
- **DPR-08:** fail (Information) when the files hold personal data and nothing identifies it (no classification
  attributes, annotations or data inventory document), or when fields are labelled sensitive but handled like any
  other field.
