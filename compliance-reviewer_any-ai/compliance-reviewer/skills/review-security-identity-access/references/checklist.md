# Checklist — Security: Identity & Access

Subject: Security

Elements are defined in `standards/` (ATN/ATZ/JWT/OAU/SES/PWS/ZTA/T10 in `owasp-identity-access.md`; ASP in
`aspnetcore-identity.md`; SPS in `spring-security.md`; DJ in `django-auth.md`). Every element belongs to exactly one
check. Framework elements (ASP/SPS/DJ) apply only when that framework is in use. Severity of a failed element follows
`SKILL.md` (SHOULD elements one level lower; listed exceptions always Error).

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|------------------|----------|--------|
| SEC-IA-01 | Identity & Access | Endpoints are protected by default (deny-by-default / fallback policy / catch-all rule), public endpoints are explicitly allowed, and authentication is enforced server-side, not by network or device signals | Error | ATN-18, ATZ-02, T10-01, ASP-09, SPS-01, SPS-02, DJ-01 | ATN, ATZ, T10, ASP, SPS, DJ |
| SEC-IA-02 | Identity & Access | Authorization is checked server-side on every request for every sensitive function **and object** (no IDOR, no client-only checks, static resources covered, failures handled safely) | Error | ATZ-03…07, T10-02…05, ASP-10, ASP-11, SPS-03…05, DJ-02, NDA-05 | ATZ, T10, ASP, SPS, DJ, NDA |
| SEC-IA-03 | Identity & Access | JWTs are verified before trust: signature with an allowlisted algorithm and trusted key (never `none` or header-supplied keys), `iss`, `aud`, `exp`/`nbf`, token type; strong secrets; no sensitive claims; short lifetimes | Error | JWT-01…11, T10-07, T10-14, SPS-11, SPS-12 | JWT, T10, SPS |
| SEC-IA-04 | Identity & Access | OAuth 2.0/OIDC flows use authorization code + PKCE (no implicit or password grant), protect against CSRF/mix-up and open redirects, use HTTPS redirect URIs, audience-restrict tokens, and validate ID tokens and federated identities (`iss`+`sub`) | Error | ATN-15…17, OAU-01…07, OAU-10, OAU-11, ASP-12, SPS-13 | ATN, OAU, ASP, SPS |
| SEC-IA-05 | Identity & Access | Sessions use secure IDs exchanged only in Secure/HttpOnly/explicit-SameSite cookies, rotate on login and privilege change, expire server-side (idle and absolute), are invalidated on logout, and cookie-authenticated state changes are CSRF-protected | Error | SES-02…15, T10-12, ASP-06…08, ASP-13, ASP-14, SPS-06…08, DJ-05…11, NDA-01, NDA-02, NDA-04 | SES, T10, ASP, SPS, DJ, NDA |
| SEC-IA-06 | Identity & Access | Passwords are stored only with a salted adaptive hash at current parameters (Argon2id, scrypt, bcrypt cost ≥ 10, PBKDF2 ≥ 600k), never plaintext, encrypted or fast-hashed, with an upgrade path | Error | PWS-01…09, T10-15, ASP-04, SPS-09, DJ-03 | PWS, T10, ASP, SPS, DJ |
| SEC-IA-07 | Identity & Access | No home-grown cryptography, hashing, session or authentication schemes for credentials: vetted framework/IdP implementations and safe comparisons are used | Error | ATN-07, SES-01, PWS-10, T10-13, ASP-01 | ATN, SES, PWS, T10, ASP |
| SEC-IA-08 | Identity & Access | Access follows least privilege and explicit verification (Zero Trust): service-to-service calls are authenticated, network location never authorizes, tokens and roles are minimal, sensitive/admin accounts are separated | Warning | ATN-01, ATZ-01, OAU-08, ZTA-01…05 | ATN, ATZ, OAU, ZTA |
| SEC-IA-09 | Identity & Access | Authentication and access-control failures are handled safely: generic responses with the same status and timing (no enumeration), throttling/lockout on login, and failures logged | Warning | ATN-10…12, ATN-14, ATZ-08, T10-06, T10-10, T10-11, ASP-02, ASP-03, NDA-03 | ATN, ATZ, T10, ASP, NDA |
| SEC-IA-10 | Identity & Access | Password policy and credential lifecycle follow current guidance: length-based (≥ 8 with MFA / ≥ 15 without, max ≥ 64), no composition rules or forced rotation, breached/common screening, current password on change, no security questions, no default credentials | Warning (Error for default credentials) | ATN-02…06, ATN-08, ATN-13, T10-08, T10-09, T10-16, ASP-05, SPS-10, DJ-04 | ATN, T10, ASP, SPS, DJ |
| SEC-IA-11 | Identity & Access | Credentials and tokens are protected on the client and in transit: never in `localStorage`/`sessionStorage`, credential paths only over TLS, refresh tokens rotated or sender-constrained, sensitive auth responses not cached | Warning (Error for credentials over plain HTTP) | ATN-09, OAU-09, SES-16, SES-17 | ATN, OAU, SES |
