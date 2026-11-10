# OWASP identity & access guidance — localized summary

- Sources: cheatsheetseries.owasp.org @ OWASP/CheatSheetSeries (per-sheet commits below);
  top10.owasp.org (A01:2025, A07:2025) @ OWASP/Top10 d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966 (2025-12-24)
- Localized: 2026-11-08 · Elements: cheatsheetseries.owasp.org 80 here + 14 in `aspnetcore-identity.md` = 94 (cap 100);
  top10.owasp.org 16 (cap 100)
- Level: `MUST` where the source says must/must not/never/do not/"is mandatory"/"is required", or states a prohibited
  practice; `SHOULD` for recommendations. Top 10 elements: `MUST` for "How to prevent" bullets, `REVIEW` for
  "Description" weaknesses (`REVIEW` is treated like `MUST`). Severity rules are in `../../SKILL.md`.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.
- Citation preference: framework element (ASP/SPS/DJ) → cheat-sheet element → Top 10 element (cite T10 only when
  nothing more specific fits; otherwise name the T10 ID in the recommendation).

| Key | Citation base | Pinned commit | Source name for `Finding.standard` |
|-----|---------------|---------------|------------------------------------|
| atn | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | 684d6d9d (2026-10-04) | OWASP Authentication Cheat Sheet |
| atz | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | cfd69aab (2026-10-09) | OWASP Authorization Cheat Sheet |
| jwt | https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html | 25d263ce (2026-10-04) | OWASP JSON Web Token Cheat Sheet |
| oau | https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html | 995524d4 (2026-10-03) | OWASP OAuth 2.0 Cheat Sheet |
| ses | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | 757270a2 (2026-11-05) | OWASP Session Management Cheat Sheet |
| pws | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html | 87a1faf1 (2026-10-30) | OWASP Password Storage Cheat Sheet |
| zta | https://cheatsheetseries.owasp.org/cheatsheets/Zero_Trust_Architecture_Cheat_Sheet.html | 67663b74 (2026-10-04) | OWASP Zero Trust Architecture Cheat Sheet |
| a01 | https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/ | d4d000ec (2025-12-24) | OWASP Top 10:2025 A01 |
| a07 | https://top10.owasp.org/2025/A07_2025-Authentication_Failures/ | d4d000ec (2025-12-24) | OWASP Top 10:2025 A07 |

## Authentication Cheat Sheet (ATN)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| ATN-01 | MUST | Sensitive internal accounts (backend, middleware, DB) can't log in through any front-end UI; the internal IdP isn't reused for public access. | service/DB accounts in user store or seed data with UI login enabled | SEC-IA-08 | atn#authentication-solution-and-sensitive-accounts |
| ATN-02 | SHOULD | Enforce a minimum password length: < 8 is weak with MFA, < 15 without MFA. | min-length setting/validator below threshold or absent | SEC-IA-10 | atn#implement-proper-password-strength-controls |
| ATN-03 | SHOULD | Allow at least 64 characters; never silently truncate passwords. | max length < 64; `substring`/truncation before hashing | SEC-IA-10 | atn#implement-proper-password-strength-controls |
| ATN-04 | SHOULD | Allow all characters (Unicode, whitespace); no composition rules (upper/lower/digit/special). | `RequireDigit`/`RequireUppercase`-style rules; regex composition checks | SEC-IA-10 | atn#implement-proper-password-strength-controls |
| ATN-05 | SHOULD | Don't require periodic password changes; rotate on compromise or authenticator change. | password-expiry policy (`PasswordExpiryDays`, max-age jobs) | SEC-IA-10 | atn#implement-proper-password-strength-controls |
| ATN-06 | SHOULD | Block common and previously breached passwords. | no blocklist/breach-check validator on registration/change | SEC-IA-10 | atn#implement-proper-password-strength-controls |
| ATN-07 | SHOULD | Compare passwords with the framework's verify function; otherwise constant-time, typed, length-limited. | `==`/`equals` on hashes; loose comparisons | SEC-IA-07 | atn#compare-password-hashes-using-safe-functions |
| ATN-08 | MUST | Change-password requires an authenticated session and verification of the current password. | change endpoint without current-password check | SEC-IA-10 | atn#change-password-feature |
| ATN-09 | MUST | Login pages and all authenticated pages are reached only over TLS (credential path specifically; site-wide HTTPS is SEC-WA-06). | `http://` login form action/post URL; auth endpoint excluded from HTTPS | SEC-IA-11 | atn#transmit-passwords-only-over-tls-or-other-strong-transport |
| ATN-10 | MUST | Login, password reset/recovery and registration return the same generic message whatever the cause. | "user not found", "invalid password", "account locked" messages | SEC-IA-09 | atn#authentication-responses |
| ATN-11 | SHOULD | Failure cases use the same HTTP status and comparable processing time (no "quick exit"). | early return before hashing when user is missing; 404 vs 401 split | SEC-IA-09 | atn#authentication-responses |
| ATN-12 | SHOULD | Throttle or lock out failed logins per account (not only per IP), with threshold, window and duration; avoid lockout-DoS. | no lockout/throttle configuration on password login | SEC-IA-09 | atn#login-throttling, atn#protect-against-automated-attacks |
| ATN-13 | MUST | No security questions for authentication or re-authentication; verify the full secret, not selected characters. | security-question fields used in login/recovery; partial-password prompts | SEC-IA-10 | atn#security-questions-and-memorable-words |
| ATN-14 | SHOULD | Log all authentication failures, password failures and account lockouts. | auth-failure paths with no log call | SEC-IA-09 | atn#logging-and-monitoring |
| ATN-15 | MUST | OIDC relying parties validate ID tokens: `iss`, `aud`, signature against provider JWKs, `exp`; use maintained libraries and discovery. OpenID 2.0 isn't implemented. | hand-parsed ID token; validation flags off; OpenID 2.0 libraries | SEC-IA-04 | atn#oidc-implementation-guidance, atn#openid-connect-oidc |
| ATN-16 | MUST | Identify federated users by `iss` + `sub`; never auto-link accounts on matching email or username. | lookup by `email`/`preferred_username` claim on external login | SEC-IA-04 | atn#secure-federated-account-linking |
| ATN-17 | SHOULD | Linking/unlinking identities requires an authenticated session; a removed identity no longer grants access. | link endpoint without auth; unlink not enforced | SEC-IA-04 | atn#secure-federated-account-linking |
| ATN-18 | MUST | Device fingerprints, IPs and remembered-device cookies are risk signals, never substitutes for authentication. | IP allowlist or device cookie treated as logged in | SEC-IA-01 | atn#adaptive-or-risk-based-authentication |

## Authorization Cheat Sheet (ATZ)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| ATZ-01 | SHOULD | Least privilege applied horizontally and vertically; roles/permissions no broader than needed. | admin/wildcard permissions granted by default; all users in a privileged role | SEC-IA-08 | atz#enforce-least-privileges |
| ATZ-02 | MUST | Deny by default: unmatched requests are denied; explicit configuration preferred over framework defaults. | no catch-all deny/authenticated rule; opt-in `[Authorize]` only | SEC-IA-01 | atz#deny-by-default |
| ATZ-03 | MUST | Validate permissions on every request through a global mechanism (filters/middleware), not ad hoc per method. | sensitive handler reachable without the shared authz filter | SEC-IA-02 | atz#validate-the-permissions-on-every-request |
| ATZ-04 | MUST | Object-level checks on every request for the specific object; don't rely on unguessable IDs; derive the owner from the authenticated identity where possible (IDOR). | `findById(request.id)` returned without owner/tenant check | SEC-IA-02 | atz#ensure-lookup-ids-are-not-accessible-even-when-guessed-or-cannot-be-tampered-with |
| ATZ-05 | SHOULD | Static resources and cloud-stored files fall under access-control policy. | private files served from public static path or public bucket config | SEC-IA-02 | atz#enforce-authorization-checks-on-static-resources |
| ATZ-06 | MUST | Never rely on client-side access checks; enforce server-side, at the gateway or in serverless functions. | UI hides buttons but API lacks the check | SEC-IA-02 | atz#verify-that-authorization-checks-are-performed-in-the-right-location |
| ATZ-07 | SHOULD | Failed checks are handled centrally and safely: no unstable state, no sensitive detail in errors. | swallowed `AccessDenied` that continues; stack traces on 403 | SEC-IA-02 | atz#exit-safely-when-authorization-checks-fail |
| ATZ-08 | SHOULD | Log access-control failures in a consistent, parseable format. | denial paths with no log call | SEC-IA-09 | atz#implement-appropriate-logging |

## JSON Web Token Cheat Sheet (JWT)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| JWT-01 | MUST | Reject unsecured JWTs (`alg: none`); never decode without verifying the signature. | `verify_signature: False`, `algorithms` incl. `none`, `jwt.decode` without key, `parseUnsecuredClaims` | SEC-IA-03 | jwt#unsecured-jwts |
| JWT-02 | MUST | Hardcode accepted algorithms; don't mix public-key and MAC algorithms; key type matches the algorithm (key confusion). | algorithm taken from header; `get_default_algorithms()`; RS* and HS* accepted together | SEC-IA-03 | jwt#key-type-confusion |
| JWT-03 | MUST | Don't trust keys named in the header (`jwk`, `jku`, `x5u`, `x5c`) unless chained to the issuer's trust anchor; prefer pinned keys or the issuer's `jwks_uri`; sanitize `kid`. | key resolver fetching `jku`/`x5u`; embedded `jwk` used to verify | SEC-IA-03 | jwt#trusting-key-material-named-in-the-token-header |
| JWT-04 | MUST | Validate `iss` exactly (or against an allowlist); select the key set bound to that issuer, never a union of issuers' keys. | `ValidateIssuer = false`; multi-tenant key lookup by `kid` across tenants | SEC-IA-03 | jwt#issuer-and-audience-confusion |
| JWT-05 | MUST | Require the recipient's own identifier in `aud`; reject tokens missing `iss`/`aud` where the deployment relies on them. | `ValidateAudience = false`; no audience configured; `verify_aud: False` | SEC-IA-03 | jwt#issuer-and-audience-confusion |
| JWT-06 | MUST | Enforce `exp` and `nbf` validity. | `ValidateLifetime = false`; `verify_exp: False`; tokens issued without `exp` | SEC-IA-03 | jwt#claims |
| JWT-07 | SHOULD | Prevent token-type confusion: validate `typ` (e.g. `at+jwt`) or use mutually exclusive validation rules for ID, access and reset tokens. | ID token accepted as API bearer; one key + same claims for reset and access tokens | SEC-IA-03 | jwt#cross-jwt-and-token-type-confusion |
| JWT-08 | MUST | HMAC secrets come from a CSPRNG, are ≥ the output size (256/384/512 bits) with ≥ 160 bits entropy, aren't passwords, and are unique per issuer–audience pair. | short/human-readable signing secret; same secret for several audiences | SEC-IA-03 | jwt#mac |
| JWT-09 | SHOULD | Prefer EdDSA, ES\* or PS\* (RS\* "not recommended"); don't reuse signing keys for encryption; never publish private keys. | RS256 chosen for new issuer; key pair shared with encryption | SEC-IA-03 | jwt#public-key-signatures |
| JWT-10 | SHOULD | JWTs used as sessions need a revocation design; denylists key on `jti` + `iss`, never on the raw token or its hash; prefer plain server sessions. | JWT session with no logout revocation; denylist keyed on `sha256(token)` | SEC-IA-03 | jwt#not-using-jwts, jwt#jwt-denylist |
| JWT-11 | SHOULD | Signed JWTs aren't confidential: keep sensitive data/PII out of claims (opaque reference or nested JWE: sign then encrypt, allowlisted `alg`/`enc`, no `zip`). | PII, secrets or internal data in claims | SEC-IA-03 | jwt#signed-jwts-are-not-confidential, jwt#using-jwe |

## OAuth 2.0 Cheat Sheet (OAU)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| OAU-01 | MUST | Clients and authorization servers expose no open redirectors (forwarding to URIs from query parameters). | `redirect(request.query.returnUrl)` without allowlist | SEC-IA-04 | oau#oauth-20-essential-basics |
| OAU-02 | MUST | CSRF protection in the flow: PKCE, the OIDC `nonce`, or a one-time `state` bound to the user agent. | no `state`/`nonce`/PKCE; static `state` value | SEC-IA-04 | oau#oauth-20-essential-basics |
| OAU-03 | SHOULD | Clients talking to several authorization servers defend against mix-up (`iss` parameter or distinct redirect URIs). | several providers sharing one callback with no `iss` check | SEC-IA-04 | oau#oauth-20-essential-basics |
| OAU-04 | MUST | Use the authorization code grant with PKCE for all client types (SPA and native included), with a challenge method that doesn't expose the verifier (S256). | public client without PKCE; `code_challenge_method=plain` | SEC-IA-04 | oau#pkce-proof-key-for-code-exchange-mechanism, oau#implicit-grant-deprecated-do-not-use |
| OAU-05 | MUST | The implicit grant (`response_type=token`) isn't used; access tokens never travel via the front channel. | `response_type=token` / `id_token token`; token read from URL fragment | SEC-IA-04 | oau#implicit-grant-deprecated-do-not-use |
| OAU-06 | MUST | The resource owner password credentials grant isn't used. | `grant_type=password` | SEC-IA-04 | oau#resource-owner-password-credentials-grant |
| OAU-07 | MUST | Access tokens are audience-restricted (ideally one resource server); each resource server verifies audience and resource/action per request. | API accepts any token from the issuer; no audience/scope check | SEC-IA-04 | oau#access-token-privilege-restriction |
| OAU-08 | SHOULD | Token privileges (scopes) restricted to the minimum the client needs. | clients requesting broad/admin scopes they don't use | SEC-IA-08 | oau#access-token-privilege-restriction |
| OAU-09 | SHOULD | Refresh tokens are sender-constrained (DPoP/mTLS) or rotated on use. | long-lived refresh tokens reused indefinitely; rotation disabled | SEC-IA-11 | oau#token-replay-prevention |
| OAU-10 | SHOULD | Confidential clients authenticate, preferably with asymmetric methods (`private_key_jwt`, mTLS). | public-client config for a server app; shared secret where asymmetric is available | SEC-IA-04 | oau#client-authentication |
| OAU-11 | MUST | No `http` redirect URIs (except native loopback); authorization responses never over unencrypted connections. | `http://` redirect/callback URIs in client registration | SEC-IA-04 | oau#other-recommendations |

## Session Management Cheat Sheet (SES)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| SES-01 | SHOULD | Use the framework's built-in session management, kept updated and hardened, instead of a home-made one. | custom session table/token scheme alongside an available framework session | SEC-IA-07 | ses#built-in-session-management-implementations |
| SES-02 | MUST | Custom session IDs come from a CSPRNG (≥ 64 bits entropy; ≥ 128 bits if self-generated), are fully random and carry no meaning or PII. | `Random`/`Math.random`/`uuid1`/sequential IDs; user data encoded in the ID | SEC-IA-05 | ses#session-id-entropy, ses#session-id-content-or-value |
| SES-03 | MUST | Session IDs are exchanged only in cookies; IDs in URLs or parameters aren't accepted. | cookieless sessions; `;jsessionid=`; session ID query parameter | SEC-IA-05 | ses#used-vs-accepted-session-id-exchange-mechanisms |
| SES-04 | MUST | Session cookies set `Secure`. | cookie options without Secure / `SecurePolicy` not Always | SEC-IA-05 | ses#secure-attribute |
| SES-05 | MUST | Session cookies set `HttpOnly`. | `HttpOnly = false` | SEC-IA-05 | ses#httponly-attribute |
| SES-06 | MUST | Session cookies set `SameSite=Strict` (preferred) or `Lax` explicitly; never `None` without `Secure`; don't rely on the browser default. | `SameSite=None`; no SameSite set | SEC-IA-05 | ses#samesite-attribute |
| SES-07 | MUST | Cookie-authenticated state-changing requests keep a CSRF token defense; SameSite isn't a replacement (DEC-7). | CSRF disabled with cookie/session auth; state change on GET | SEC-IA-05 | ses#samesite-attribute |
| SES-08 | SHOULD | Use the `__Host-` prefix for session cookies (`__Secure-` only when subdomains must share). | session cookie without prefix | SEC-IA-05 | ses#cookie-name-prefixes |
| SES-09 | SHOULD | Don't set `Domain` (or keep it narrow); keep `Path` as restrictive as possible. | `Domain=.example.com` on session cookie | SEC-IA-05 | ses#domain-and-path-attributes |
| SES-10 | SHOULD | Prefer non-persistent auth cookies unless persistence is needed; enforce expiry on the server. | long `Max-Age`/`Expires` on session cookie by default | SEC-IA-05 | ses#expire-and-max-age-attributes |
| SES-11 | MUST | Renew the session ID after login and any privilege change (password change, role switch); destroy the old ID. | login without regeneration; fixation protection disabled | SEC-IA-05 | ses#renew-the-session-id-after-any-privilege-level-change |
| SES-12 | MUST | Strict session management: never accept a session ID the server didn't generate. | session created from a client-supplied ID | SEC-IA-05 | ses#session-id-generation-and-verification-permissive-and-strict-session-management |
| SES-13 | MUST | Enforce an idle timeout server-side (guide: 2–5 min high-value, 15–30 min low-risk). | no idle timeout; timeout tracked only client-side | SEC-IA-05 | ses#idle-timeout, ses#session-expiration |
| SES-14 | SHOULD | Enforce an absolute timeout regardless of activity (e.g. 4–8 h for a workday app). | sliding expiration only, no maximum lifetime | SEC-IA-05 | ses#absolute-timeout |
| SES-15 | MUST | Logout invalidates the session server-side, including IDs from rotations or grace periods; deleting the cookie or a browser-close handler isn't enough. | logout that only clears the cookie; `beforeunload` logout | SEC-IA-05 | ses#logout-button, ses#limits-of-logout-on-browser-close |
| SES-16 | SHOULD | `Cache-Control: no-store` on responses carrying session IDs or sensitive session data; `Clear-Site-Data` on logout. | auth/account responses cacheable | SEC-IA-11 | ses#web-content-caching-and-clear-site-data |
| SES-17 | MUST | Never store session IDs, JWTs, refresh tokens or other credentials in `localStorage`/`sessionStorage`; use HttpOnly cookies or a BFF. | `localStorage.setItem('token', …)`, `sessionStorage` auth state | SEC-IA-11 | ses#the-localstorage-api |

## Password Storage Cheat Sheet (PWS)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| PWS-01 | MUST | Never store passwords in plaintext or with reversible encryption, or with fast hashes (MD5, SHA-1, SHA-256). The only exception is a documented need to replay a credential to a legacy system. | `md5(password)`, `SHA256.HashData(pwd)`, AES-encrypted password column | SEC-IA-06 | pws#introduction, pws#hashing-vs-encryption |
| PWS-02 | SHOULD | Prefer Argon2id, minimum m=19 MiB, t=2, p=1 (or an equivalent row: 46/1, 12/3, 9/4, 7/5). | Argon2 params below table; Argon2i/Argon2d variant | SEC-IA-06 | pws#argon2id |
| PWS-03 | SHOULD | scrypt when Argon2id is unavailable: N=2^17, r=8, p=1 (or equivalent rows). | scrypt N/r/p below table | SEC-IA-06 | pws#scrypt |
| PWS-04 | MUST | bcrypt (legacy only) uses work factor ≥ 10 and a 72-byte input limit; pre-hashing only as `bcrypt(base64(hmac-sha384(pwd, pepper)))`. | cost < 10; raw SHA pre-hash; no length limit | SEC-IA-06 | pws#bcrypt, pws#input-limits-of-bcrypt, pws#pre-hashing-passwords-with-bcrypt |
| PWS-05 | SHOULD | PBKDF2 (when FIPS-140 is required) uses HMAC-SHA256 ≥ 600,000, HMAC-SHA512 ≥ 220,000 iterations; HMAC-SHA1 only for legacy. | iteration count below threshold; SHA1 for new systems | SEC-IA-06 | pws#pbkdf2 |
| PWS-06 | MUST | Each password has a unique random salt (libraries usually manage it). | fixed/global salt; salt from username | SEC-IA-06 | pws#salting |
| PWS-07 | SHOULD | A pepper, if used, is stored apart from the password database (vault/HSM). | pepper in same DB/table or in source | SEC-IA-06 | pws#peppering |
| PWS-08 | SHOULD | Store algorithm and parameters with the hash (e.g. PHC string) so work factors can rise; upgrade legacy hashes at next login. | bare hash column with no algorithm id; no rehash-on-login path | SEC-IA-06 | pws#upgrading-the-work-factor, pws#upgrading-legacy-hashes |
| PWS-09 | SHOULD | Hashing accepts the full Unicode range and NUL bytes; no entropy reduction before hashing. | lowercasing/ASCII-folding passwords before hashing | SEC-IA-06 | pws#international-characters |
| PWS-10 | MUST | Use the language's or framework's built-in password hashing; no home-grown hashing schemes. | custom salt+hash loops; hand-rolled KDF | SEC-IA-07 | pws#introduction |

## Zero Trust Architecture Cheat Sheet (ZTA)

Only code- and config-visible guidance is localized; organizational, device and network-platform controls are not.

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| ZTA-01 | MUST | All communication is authenticated and encrypted whatever the network location; internal service calls aren't trusted because they're internal. | internal endpoints with no auth "because private network"; service clients without credentials | SEC-IA-08 | zta#2-all-communication-is-secured-regardless-of-network-location |
| ZTA-02 | MUST | Access is granted per session and per resource with least privilege; authorization for one resource doesn't grant another; sessions are re-evaluated and revoked when policy no longer permits. | one token/role grants access to all services; no revocation path | SEC-IA-08 | zta#3-access-to-resources-is-granted-on-a-per-session-basis, zta#6-all-authentication-and-authorization-is-dynamic-and-strictly-enforced |
| ZTA-03 | SHOULD | No permanent admin rights; admin accounts separate from regular accounts; just-in-time elevation. | everyday accounts holding admin role; seeded permanent admins | SEC-IA-08 | zta#access-controls, zta#managing-user-accounts |
| ZTA-04 | SHOULD | API gateways authenticate every API call, including service-to-service. | gateway routes with auth disabled | SEC-IA-08 | zta#securing-applications |
| ZTA-05 | MUST | Network position (VPN, segment, IP range) never authorizes access by itself; a WAF doesn't replace application authorization. | IP-range checks used as authorization; "trusted subnet" bypass | SEC-IA-08 | zta#network-controls, zta#technical-mistakes |

## OWASP Top 10:2025 A01 and A07 (T10)

Traceability elements. Cite only when no cheat-sheet or framework element covers the evidence.

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| T10-01 | MUST | Except for public resources, deny by default. | no catch-all deny | SEC-IA-01 | a01#how-to-prevent |
| T10-02 | MUST | Implement access control once and reuse it; prefer declarative toolkits. | duplicated hand-written checks per handler | SEC-IA-02 | a01#how-to-prevent |
| T10-03 | MUST | Enforce record ownership instead of allowing CRUD on any record. | queries not scoped by owner/tenant | SEC-IA-02 | a01#how-to-prevent, a01#description |
| T10-04 | REVIEW | No API missing access control for POST/PUT/DELETE; no force-browsing to authenticated or privileged pages. | write endpoints without authz; admin routes only hidden | SEC-IA-02 | a01#description |
| T10-05 | REVIEW | Access-control metadata (JWT, cookie, hidden field) can't be tampered with or replayed to elevate privileges. | role read from client-editable cookie/field | SEC-IA-02 | a01#description |
| T10-06 | MUST | Log access-control failures; alert admins on repeated failures. | no logging on 403 paths | SEC-IA-09 | a01#how-to-prevent |
| T10-07 | MUST | Stateless JWTs are short-lived; longer access uses refresh tokens and OAuth revocation. | access-token lifetime of days/months | SEC-IA-03 | a01#how-to-prevent |
| T10-08 | MUST | Don't ship or deploy default credentials, particularly for admin users. | seeded `admin/admin`, default passwords in config/migrations | SEC-IA-10 | a07#how-to-prevent |
| T10-09 | MUST | Check new/changed passwords against weak and breached lists; align policy with NIST 800-63B; don't force rotation unless breach is suspected. | no weak/breached check; forced periodic rotation | SEC-IA-10 | a07#how-to-prevent |
| T10-10 | MUST | Registration, recovery and API pathways use the same messages for all outcomes (no account enumeration). | distinct "email exists" responses | SEC-IA-09 | a07#how-to-prevent |
| T10-11 | MUST | Limit or increasingly delay failed logins without creating a DoS; log failures and alert on attacks. | unlimited login attempts | SEC-IA-09 | a07#how-to-prevent |
| T10-12 | MUST | Use a server-side, built-in session manager: new high-entropy ID after login, never in the URL, secure cookie, invalidated on logout, idle and absolute timeout. | custom session handling breaking any of these | SEC-IA-05 | a07#how-to-prevent |
| T10-13 | MUST | Prefer a premade, well-trusted system for authentication, identity and session management. | hand-built auth stack where a framework/IdP is available | SEC-IA-07 | a07#how-to-prevent |
| T10-14 | MUST | Verify the intended use of credentials: validate JWT `aud`, `iss` and scopes. | token accepted without audience/issuer/scope checks | SEC-IA-03 | a07#how-to-prevent, a07#description |
| T10-15 | REVIEW | No plaintext, encrypted or weakly hashed password stores. | as PWS-01 | SEC-IA-06 | a07#description |
| T10-16 | REVIEW | No knowledge-based answers in credential recovery. | security questions in reset flow | SEC-IA-10 | a07#description |
