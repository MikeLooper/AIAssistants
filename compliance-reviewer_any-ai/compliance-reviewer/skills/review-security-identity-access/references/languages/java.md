# Detection signals — Java (Security: Identity & Access)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). SPS elements apply only when Spring Security is a dependency. Spring Boot
`server.servlet.session.cookie.*` defaults are not localized: report only explicit insecure values.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `authorizeHttpRequests` without a final `anyRequest()` rule, or `anyRequest().permitAll()`; legacy `authorizeRequests`/`WebSecurityConfigurerAdapter` with the same gaps | `SecurityFilterChain` beans, security config classes | No deny-by-default | SPS-01, ATZ-02 |
| `WebSecurityCustomizer` / `web.ignoring()` for paths | security config | Paths outside the filter chain | SPS-02 |
| `@PreAuthorize`/`@PostAuthorize` without `@EnableMethodSecurity` (or legacy `@EnableGlobalMethodSecurity(prePostEnabled = true)`); `@Secured` without `securedEnabled = true`; `@RolesAllowed` without `jsr250Enabled = true` | config classes, services | Method security inert | SPS-03 |
| Repository `findById(id)` returned from a controller without owner/tenant check, `@PostAuthorize` or `#id` expression | controllers, services | IDOR | SPS-04, ATZ-04 |
| `csrf(c -> c.disable())` / `.csrf().disable()` with form login or session cookies | security config | Missing CSRF defense | SPS-08, SES-07 |
| `sessionFixation(f -> f.none())` / `.sessionFixation().none()` | security config | Session fixation | SPS-06, SES-11 |
| Custom servlet login that sets session attributes without `request.changeSessionId()` | login controllers/filters | No session ID renewal | SES-11 |
| GET logout handler; `invalidateHttpSession(false)`; logout that only clears cookies | security config, controllers | Incomplete logout | SPS-07, SES-15 |
| `NoOpPasswordEncoder`, `{noop}` prefixes, `User.withDefaultPasswordEncoder()`, `StandardPasswordEncoder`, `Md5PasswordEncoder`, `MessageDigest` on passwords | config, user services, seed data | Weak password storage | SPS-09, PWS-01 |
| `new BCryptPasswordEncoder(n)` with `n < 10`; `Pbkdf2PasswordEncoder` with low iterations | config | Weak work factor | PWS-04, PWS-05 |
| Registration/change-password flow without `CompromisedPasswordChecker` | account services | No breached-password check | SPS-10 |
| `spring.security.oauth2.resourceserver.jwt.*` with no `audiences` and no `AudienceValidator` | `application*.yml`/`.properties`, decoder beans | `aud` not validated | SPS-11, JWT-05 |
| `NimbusJwtDecoder` with `setJwtValidator(...)` that replaces the defaults; broad `jws-algorithms`; shared `SecretKey` across services | decoder beans | Weakened JWT validation | SPS-12, JWT-02 |
| jjwt `Jwts.parser()` without `verifyWith`/`setSigningKey`; `parseUnsecuredClaims`; auth0 `JWT.decode(...)` used as verification | token services, filters | Signature not verified | JWT-01 |
| `requireProofKey(false)` on a client registration; `authorization-grant-type: password` or implicit | OAuth2 client config | Weak OAuth flow | SPS-13, OAU-04, OAU-06 |
| `http://` `issuer-uri`, `jwk-set-uri` or `redirect-uri` | `application*.yml`/`.properties` | Tokens over plain HTTP | OAU-11 |
