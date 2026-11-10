# The Twelve-Factor App (12factor.net) — localized summary

- Source site: 12factor.net (English pages only) · Version: footer "Written by Adam Wiggins • Last updated 2017";
  each page pinned by the SHA-256 of its extracted text (table below)
- Citation base: https://12factor.net/
- Localized: 2026-11-09 (retrieved 2026-11-09) · Elements: 55 (cap 100)
- Source name for `Finding.standard`: The Twelve-Factor App (12factor.net)
- Level: informational only; severity is the owning check's default.
- Reading rule: modern platform equivalents satisfy an element when they meet its intent (rubric TFR-06 and the
  "Accepted modern equivalents" column). The tool names on the pages (Capistrano, Foreman, Memcached, Vagrant, …) are
  examples, never requirements.
- The pages have **no section anchors** below the factor heading (both ids on each page point at its top). Citation:
  `Finding.url` = citation base + page path, e.g. `https://12factor.net/config`; the element ID in `Finding.standard`
  gives the precision.
- "Service-like" in *Applies when* means the rubric's applicability table doesn't exclude the check for the
  deployable's kind.

| Key | Page path | Text SHA-256 (first 16 hex) |
|-----|-----------|-----------------------------|
| idx | `/` (site root, introduction: applicability provenance only, no elements) | f03929b9938874bb |
| cb | `codebase` | 3e451703fee54f70 |
| dep | `dependencies` | 8d1b16459beb17ac |
| cfg | `config` | ea9d3387e9814032 |
| bs | `backing-services` | eabe1c7b6ac5e3d0 |
| brr | `build-release-run` | d73c40174ab1d2c8 |
| proc | `processes` | 034941af715125b4 |
| port | `port-binding` | d55f90364f8926e1 |
| conc | `concurrency` | 8476d1a0d0358fd2 |
| disp | `disposability` | ccfe65679edb41dc |
| dpp | `dev-prod-parity` | 0ff764560773b1c5 |
| logs | `logs` | 4ebc9229a16ba3a3 |
| adm | `admin-processes` | 2d731c00c3c98032 |

| ID | Requirement (summary) | Applies when | Check | Page |
|----|-----------------------|--------------|-------|------|
| TFA-01 | The app is tracked in a version control system. A codebase is one repo, or a set of repos sharing a root commit. | always | TF-01 | cb |
| TFA-02 | One codebase per app. Several apps sharing the same code is a violation. Shared code is factored into libraries consumed through the dependency manager. | ≥ 2 deployables or shared code | TF-01 | cb |
| TFA-03 | Several codebases form a distributed system. Each component is an app that complies with twelve-factor on its own. | multi-repo or multi-component system | TF-01 | cb |
| TFA-04 | All deploys (production, staging, developer machines) run from the same codebase, possibly at different versions. There are no per-deploy copies of the code. | always | TF-01 | cb |
| TFA-05 | The app never relies on implicitly present system-wide packages. It declares all dependencies, completely and exactly, in a manifest. | always | TF-02 | dep |
| TFA-06 | A dependency isolation mechanism is used at run time, so no undeclared dependency leaks in from the surrounding system. | always | TF-02 | dep |
| TFA-07 | Declaration and isolation are always used together. Either one alone is insufficient. | always | TF-02 | dep |
| TFA-08 | The same full dependency specification applies to production and development. | always | TF-02 | dep |
| TFA-09 | A new developer needs only the language runtime and the dependency manager. One deterministic build command sets up everything needed to run the code. | always | TF-02 | dep |
| TFA-10 | The app doesn't rely on implicitly present system tools (for example by shelling out to an image tool or `curl`). Any tool it needs is vendored or declared. | app invokes external executables | TF-02 | dep |
| TFA-11 | Config is everything that varies between deploys: handles to backing services, credentials to external services, and per-deploy values such as the canonical hostname. | service-like | TF-03 | cfg |
| TFA-12 | Config is strictly separated from code. Deploy-varying values are never stored as constants in the code. | service-like | TF-03 | cfg |
| TFA-13 | Litmus test: the codebase could be made open source at any moment without compromising any credential. | service-like | TF-03 | cfg |
| TFA-14 | Internal application config that doesn't vary between deploys (routing, module wiring) isn't "config" and belongs in the code. | service-like | TF-03 | cfg |
| TFA-15 | Config files kept out of version control are better than constants, but they are easy to commit by mistake, scatter across places and formats, and tie config to one language or framework. | config files used | TF-03 | cfg |
| TFA-16 | Config is supplied through environment variables, a language- and OS-agnostic mechanism that changes per deploy without code changes. Platform equivalents count (TFR-06). | service-like | TF-03 | cfg |
| TFA-17 | Config values are granular, independent controls managed per deploy. They aren't batched into named environment groups (development, test, production), which multiply as deploys grow. | service-like | TF-03 | cfg |
| TFA-18 | A backing service is anything the app consumes over the network: datastores, queues, mail, caches, metrics and third-party APIs. | backing services used | TF-04 | bs |
| TFA-19 | The code doesn't distinguish local from third-party services. Both are attached resources reached through a URL or locator plus credentials held in config. | backing services used | TF-04 | bs |
| TFA-20 | Swapping a resource (for example a local database for a managed one, or a mail server for a provider) needs only a config change, no code change. | backing services used | TF-04 | bs |
| TFA-21 | Each distinct backing service is its own resource with its own handle. Two databases are two resources. | ≥ 2 instances of a service type | TF-04 | bs |
| TFA-22 | Resources attach to and detach from a deploy at will, without code changes. They are loosely coupled. | backing services used | TF-04 | bs |
| TFA-23 | The build stage turns a specific commit into an executable bundle: it fetches or vendors dependencies and compiles binaries and assets. | service-like | TF-05 | brr |
| TFA-24 | The release stage combines a build with the deploy's current config into a release ready to execute. | service-like | TF-05 | brr |
| TFA-25 | The run stage launches the app's processes against one selected release. | service-like | TF-05 | brr |
| TFA-26 | Build, release and run are strictly separated. Code can't be changed at run time. | service-like | TF-05 | brr |
| TFA-27 | Every release has a unique ID (a timestamp or an incrementing number). Releases are an append-only ledger and are never changed after creation. Any change creates a new release. | deployment config visible | TF-05 | brr |
| TFA-28 | Release management makes it possible to roll back to a previous release. | deployment config visible | TF-05 | brr |
| TFA-29 | The run stage has as few moving parts as possible. Complexity belongs in the build stage, where a developer sees the errors. | service-like | TF-05 | brr |
| TFA-30 | Processes are stateless and share nothing. Any data that must persist is stored in a stateful backing service. | service-like | TF-06 | proc |
| TFA-31 | Process memory or disk is used only as a brief, single-transaction cache. The app never assumes such cached data is available to a later request or job. | service-like | TF-06 | proc |
| TFA-32 | Assets are compiled in the build stage, not at run time into the process's filesystem. | app serves compiled assets | TF-06 | proc |
| TFA-33 | No sticky sessions. Session state lives in a datastore with time-based expiry, never in process memory with affinity routing. | app has user sessions | TF-06 | proc |
| TFA-34 | The app is self-contained. It doesn't rely on a web server injected at run time (an external servlet container or a server module), but exports HTTP by binding to a port itself. | network service | TF-07 | port |
| TFA-35 | The web server is a library added through dependency declaration and runs inside the app's own process. | network service | TF-07 | port |
| TFA-36 | The contract with the execution environment is binding to a port. A routing layer maps public hostnames to the port-bound processes. | network service | TF-07 | port |
| TFA-37 | Non-HTTP servers export their services by port binding too. One app can become another app's backing service through a URL in the consumer's config. | network service | TF-07 | port |
| TFA-38 | Each type of work is assigned to a process type (for example web and worker). The set of types and the count of each is the process formation. | service-like | TF-08 | conc |
| TFA-39 | Internal threads or async are allowed, but the app also scales horizontally across processes and machines, not only vertically. | service-like | TF-08 | conc |
| TFA-40 | Processes never daemonize or write PID files. The platform's process manager handles output streams, crash restarts and user-initiated restarts and shutdowns. | service-like | TF-08 | conc |
| TFA-41 | Processes are disposable: they can be started or stopped at a moment's notice. | service-like | TF-09 | disp |
| TFA-42 | Startup time is minimal, ideally a few seconds from launch until the process is ready for requests or jobs. | service-like | TF-09 | disp |
| TFA-43 | On SIGTERM a web process shuts down gracefully: it stops listening, lets current requests finish, then exits. Requests are short, and long-polling clients reconnect. | network service | TF-09 | disp |
| TFA-44 | The tools gap is small: development and production use stacks that are as similar as possible. | service-like | TF-10 | dpp |
| TFA-45 | The developer resists lightweight substitutes for backing services in development, even behind adapters. Small incompatibilities break code in production. Adapters are fine for porting, but not as a reason to diverge. | backing services used | TF-10 | dpp |
| TFA-46 | Every deploy (developer, staging, production) uses the same type and version of each backing service. | backing services used | TF-10 | dpp |
| TFA-47 | Local environments approximate production cheaply through packaged services, declarative provisioning and lightweight virtual environments (containers). | backing services used | TF-10 | dpp |
| TFA-48 | Logs are a time-ordered stream of events aggregated from the output of all processes, with no fixed beginning or end. A file is only one output format. | service-like | TF-11 | logs |
| TFA-49 | The app never concerns itself with routing or storing its output stream. It doesn't write or manage log files. | service-like | TF-11 | logs |
| TFA-50 | Each process writes its event stream, unbuffered, to stdout. | service-like | TF-11 | logs |
| TFA-51 | The execution environment captures, collates and routes the streams to their destinations. Those destinations aren't visible to or configurable by the app. | service-like | TF-11 | logs |
| TFA-52 | One-off admin tasks (database migrations, consoles, one-time scripts) run as one-off processes, separate from the regular process formation. | admin tasks exist | TF-12 | adm |
| TFA-53 | One-off processes run in an environment identical to the regular processes: against a release, with the same codebase and config. | admin tasks exist | TF-12 | adm |
| TFA-54 | Admin code ships with the application code, so the two can't drift out of sync. | admin tasks exist | TF-12 | adm |
| TFA-55 | Every process type, admin processes included, uses the same dependency isolation and runtime invocation. | admin tasks exist | TF-12 | adm |
