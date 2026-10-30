# Java (Spring Boot)

## Recognizing the layers

The layers are either Maven/Gradle modules (`*-domain`, `*-repository`/`*-persistence`/`*-data`, `*-service`/`*-application`, `*-api`/`*-web`) or packages inside one module (`domain`, `repository`, `service`, `api`/`web`/`controller`). Treat each module or package as the "project" for that layer. Check module dependencies in `pom.xml` / `build.gradle`: service depends on domain and repository, presentation depends on service. Add a missing dependency rather than working around it, and mention it in the summary.

## Files and names

Java interfaces take no `I` prefix, so the interface gets the plain name and the class gets a descriptive prefix. Both still contain the domain name, and both classes end in the required suffix. If the codebase already uses another scheme (for example `I` prefixes or `Impl` suffixes), follow the codebase as long as the class still ends in `Repository` / `Service`.

| Artifact | Default name | Layer |
|---|---|---|
| DTO | `<Domain>Dto` (a `record`) | domain |
| Entity | `<Domain>Entity` (`@Entity`, `@Table(name = "<table>")`) | repository |
| Repository interface | `<Domain>Repository` | repository |
| Repository class | `Jpa<Domain>Repository` or `Jdbc<Domain>Repository` | repository |
| Service interface | `<Domain>Service` | service |
| Service class | `Default<Domain>Service` | service |
| Controller | `<Domain>Controller` (`@RestController`) | presentation |

Put the files in a sub-package named after the domain (`com.pilot.service.supplier`) unless the codebase groups by technical role.

## Data access by technology

**JPA** (`spring-boot-starter-data-jpa`, `EntityManager`, existing `JpaRepository` interfaces):
- The class `Jpa<Domain>Repository` implements `<Domain>Repository` and uses an injected `EntityManager` (or delegates to a package-private Spring Data interface, if the codebase already does that).
- Mark write methods `@Transactional`.

**JDBC** (`JdbcTemplate`, `JdbcClient`, `NamedParameterJdbcTemplate`):
- Keep the table name in `private static final String TABLE_NAME = "<table>";`.
- Use named or positional parameters only; never concatenate values into SQL.

## Registration

Spring can find beans by component scan, but this feature registers them explicitly so each layer has one registration point the next layer calls:

```java
// repository layer
@Configuration
public class RepositoryConfig {
    @Bean
    SupplierRepository supplierRepository(EntityManager entityManager) {
        return new JpaSupplierRepository(entityManager);
    }
}

// service layer: calling the repository registration
@Configuration
@Import(RepositoryConfig.class)
public class ServiceConfig {
    @Bean
    SupplierService supplierService(SupplierRepository supplierRepository) {
        return new DefaultSupplierService(supplierRepository);
    }
}

// presentation layer: calling the service registration
@SpringBootApplication
@Import(ServiceConfig.class)
public class PilotApplication { ... }
```

If such config classes already exist, add `@Bean` methods to them. If the codebase relies only on `@Repository` / `@Service` component scanning and has no config classes, ask the user whether to introduce the config classes or keep component scanning; if they keep component scanning, annotate the new classes and say so in the summary.

## Service and mapping

`Default<Domain>Service` takes `<Domain>Repository` as a constructor parameter (`private final` field). It holds two mapping methods, package-private so tests can reach them: `<Domain>Entity toEntity(<Domain>Dto dto)` and `<Domain>Dto toDto(<Domain>Entity entity)`. Return `Optional<<Domain>Dto>` for single-item reads.

## Controller

Constructor-inject `<Domain>Service`. Use `ResponseEntity<T>` with the status codes in [actions.md](../actions.md). In an existing controller, add the parameter to the existing constructor without removing others.

## Unit tests

These are the standard best practices for this stack. A `unit-tests.instructions.md` file in the repository takes precedence over them (see [testing.md](../testing.md)).

Tests live in `src/test/java` of the module under test, in the same package as the class under test. Follow the framework (JUnit 5 by default with `spring-boot-starter-test`), assertion library (AssertJ) and test-double library (Mockito) already in use; `spring-boot-starter-test` provides all three.

- Repository: `@DataJpaTest` (JPA) or `@JdbcTest` (JDBC) with an embedded H2 database, if the module has H2 as a test dependency or adding it is the only option (name it in the plan). Use `@AutoConfigureTestDatabase` as the existing tests do.
- Service and mapping: plain JUnit tests with a Mockito mock or a hand-written fake of `<Domain>Repository`. The package-private `toEntity` / `toDto` methods are reachable because the test is in the same package.
- Controller: `@WebMvcTest(<Domain>Controller.class)` with `@MockitoBean` (Spring Boot 3.4+) or `@MockBean` for `<Domain>Service`, using `MockMvc` to assert the status codes.
- Registration: a test that loads `ServiceConfig` in an `ApplicationContextRunner` with a mocked `EntityManager` / `JdbcTemplate`, and asserts that the `<Domain>Repository` and `<Domain>Service` beans exist.

Run `mvn test` (or `./gradlew test`).

## Bruno base URL

Use `http://localhost:<server.port>` as `baseUrl`, with `server.port` from `application.properties` / `application.yml` (default `8080`).

## Verify

Run `mvn -q compile` (or `./gradlew compileJava`), then `mvn test` (or `./gradlew test`). Report the result.
