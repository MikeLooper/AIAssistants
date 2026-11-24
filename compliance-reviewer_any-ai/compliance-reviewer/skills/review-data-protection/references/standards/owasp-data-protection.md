# OWASP data-protection guidance — localized summary

- Sources: cheatsheetseries.owasp.org @ OWASP/CheatSheetSeries (per-sheet commits below); top10.owasp.org (A04:2025
  @ OWASP/Top10 d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966, 2025-12-24); owasp.org (API3:2023 @ OWASP/API-Security
  ea77cba533150900a7d0c3822d75c460f52edef1, 2023-06-28; "Information exposure through query strings in URL" @
  OWASP/www-community 01e67c2f2ec4625a2231eb4d3ec67048aa18e7ec, 2025-10-05)
- Localized: 2026-11-24 · Elements: cheatsheetseries.owasp.org 10 (cap 100); top10.owasp.org 5 (cap 100);
  owasp.org 5 (cap 100)
- Level: `MUST` where the source says must/must not/never/do not/always, gives an unqualified imperative, or is a
  Top 10 "How to prevent" bullet; `SHOULD` for should/recommended/"consider"/"advised"; `REVIEW` for a "Description"
  or "Is the API vulnerable?" weakness (treated like `MUST`). Levels are informational: every Finding takes its
  check's default severity (`../../SKILL.md` step 7).
- Scope: the sections listed in the anchors only. The Mass Assignment Cheat Sheet and API3's mass-assignment bullets
  belong to `review-security-input-injection` (SEC-II-01) and are not localized here; key hard-coding belongs to
  SEC-OP-05; local-storage tokens and session IDs belong to `review-security-identity-access`.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Pinned commit | Source name for `Finding.standard` |
|-----|---------------|---------------|------------------------------------|
| cs | https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html | 87a1faf1 (2026-10-30) | OWASP Cryptographic Storage Cheat Sheet |
| upp | https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html | d7951be5 (2026-11-23) | OWASP User Privacy Protection Cheat Sheet |
| h5 | https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html | 3919b1c4 (2026-10-04) | OWASP HTML5 Security Cheat Sheet |
| a04 | https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures/ | d4d000ec (2025-12-24) | OWASP Top 10:2025 A04 |
| bop | https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/ | ea77cba5 (2023-06-28) | OWASP API Security Top 10:2023 API3 |
| qse | https://owasp.org/www-community/vulnerabilities/Information_exposure_through_query_strings_in_url | 01e67c2f (2025-10-05) | OWASP — Information exposure through query strings in URL |

## Cryptographic Storage Cheat Sheet (CSD)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| CSD-01 | SHOULD | Avoid storing sensitive information wherever possible; the best protection is not to store it (card details especially). | full card numbers, CVV or national IDs stored without a business need | DPR-01 | cs#minimize-the-storage-of-sensitive-information |
| CSD-02 | SHOULD | Choose the encryption layer (application, database, filesystem, hardware) from the threat model; disk or hardware encryption doesn't protect against a remote compromise of the server. | sensitive columns stored in plaintext, protected only by disk or volume encryption | DPR-01 | cs#where-to-perform-encryption, cs#architectural-design |
| CSD-03 | SHOULD | Application-level encryption uses AES (≥ 128-bit, ideally 256-bit) in an authenticated mode (GCM/CCM) from a maintained library; CTR/CBC only with separate authentication (Encrypt-then-MAC); no ECB, no custom algorithms; RSA ≥ 2048 bits with OAEP padding. | `CipherMode.ECB`, `AES/ECB/…`, `Cipher.getInstance("AES")`, home-made XOR or Base64 "encryption", RSA without OAEP | DPR-01 | cs#algorithms, cs#cipher-modes, cs#custom-algorithms, cs#random-padding |
| CSD-04 | SHOULD | Keys that encrypt stored data are kept apart from the data (not in the same database), are themselves encrypted by a separate key-encryption key where possible (envelope encryption), and use the platform's key vault, HSM or OS-protected storage where available. | encryption key stored in a table or column next to the ciphertext; key read from the same database it protects | DPR-01 | cs#separation-of-keys-and-data, cs#encrypting-stored-keys, cs#key-storage |
| CSD-05 | SHOULD | Encrypted data is still protected by access control; the application doesn't rely on encrypted URL parameters to protect information. | encrypted or encoded personal data in query strings treated as the protection | DPR-03 | cs#defense-in-depth |

## Top 10:2025 A04 Cryptographic Failures (A04)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| A04-01 | MUST | Classify and label the data the application processes, stores or transmits; identify which data is sensitive under privacy laws, regulations or business needs. | entities holding personal data with no classification attribute, annotation or data inventory | DPR-08 | a04#how-to-prevent |
| A04-02 | MUST | Apply the security controls each data classification requires. | fields labelled sensitive but stored, returned or shared like any other field | DPR-08 | a04#how-to-prevent |
| A04-03 | MUST | Don't store sensitive data unnecessarily: discard it as soon as possible, or use PCI DSS compliant tokenization or truncation. | full PAN or CVV columns; card data kept after the payment completes | DPR-01 | a04#how-to-prevent |
| A04-04 | MUST | Encrypt all sensitive data at rest. | plaintext national-ID, health or card columns with no field encryption, converter or tokenization | DPR-01 | a04#how-to-prevent |
| A04-05 | MUST | Use well-trusted implementations, authenticated encryption and current algorithms with proper key management; avoid deprecated functions, modes and padding (MD5, SHA-1, CBC, PKCS #1 v1.5) for protecting data. | `MD5`/`SHA1` used to "protect" personal fields; unauthenticated CBC; PKCS #1 v1.5 encryption | DPR-01 | a04#how-to-prevent |

## API Security Top 10:2023 API3 Broken Object Property Level Authorization (BOP)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| BOP-01 | REVIEW | An endpoint is vulnerable when it exposes object properties that are sensitive and shouldn't be read by the caller (formerly "Excessive Data Exposure"). | responses carrying password hashes, internal flags, other users' contact or location data | DPR-02 | bop#is-the-api-vulnerable |
| BOP-02 | MUST | When exposing an object through an endpoint, make sure the caller should have access to every property returned. | one entity returned to every role, with no per-caller shaping | DPR-02 | bop#how-to-prevent |
| BOP-03 | MUST | Avoid generic serialization of whole objects (`to_json()`, `to_string()`); cherry-pick the properties to return. | controller returns the ORM entity; `jsonify(user.__dict__)`; `return Ok(dbContext.Users.ToList())` | DPR-02 | bop#how-to-prevent |
| BOP-04 | SHOULD | Keep returned data structures to the minimum the endpoint's business requirements need, and define and enforce the data returned (schema-based response validation). | list endpoints returning full records; no response models or schemas | DPR-02 | bop#how-to-prevent |

## User Privacy Protection Cheat Sheet (UPP)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| UPP-01 | MUST | Private user data is encrypted in storage, with keys of sufficient length under strict technical and procedural access conditions. (Credential hashing is judged by identity-access.) | private messages, documents or personal profiles stored in plaintext | DPR-01 | upp#strong-cryptography |
| UPP-02 | SHOULD | Applications that embed external third-party content (avatars, signatures, photo attachments, images in HTML email) consider letting users block it, so a third party can't learn users' IP addresses. | user-supplied external image URLs rendered directly in feeds or messages, with no proxy or block option | DPR-04 | upp#prevent-ip-address-leakage |

## HTML5 Security Cheat Sheet — storage and PII input hints (HSP)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| HSP-01 | SHOULD | Don't store sensitive information in `localStorage` (any XSS can read it all); use `sessionStorage` when persistence isn't needed. | `localStorage.setItem('user', JSON.stringify(profile))` with email, phone or address | DPR-03 | h5#local-storage |
| HSP-02 | SHOULD | Don't assume IndexedDB provides confidentiality; avoid storing sensitive data there, or design encryption and key management for device access. | personal records cached in IndexedDB in plaintext | DPR-03 | h5#client-side-databases |
| HSP-03 | SHOULD | Sensitive personal input fields where autofill is inappropriate carry `autocomplete="off"`; it is a hint, not a no-storage guarantee. | national-ID or card inputs without `autocomplete="off"` | DPR-03 | h5#credential-and-personally-identifiable-information-pii-input-hints |

## Information exposure through query strings in URL (QSE)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| QSE-01 | REVIEW | Sensitive data, including personal data such as email addresses, isn't passed in URL query strings: it leaks through Referer headers, web logs, shared systems, browser history and caches, and third-party monitoring, even over HTTPS. | `GET /users?email=…`, `[FromQuery] string email`, links or redirects that carry email, phone or ID values | DPR-03 | qse#description, qse#examples, qse#other-real-world-example |
