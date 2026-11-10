# Maintenance — Reliability localized standards

**Maintainers only. Workers never load this file.** Background and design decisions: `docs/plan_localize-review-reliability.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1).

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| learn.microsoft.com (azure/well-architected + azure/architecture) | azure-reliability-resiliency.md | 52 | 100 | 18 pages: 6 WAF (1 checklist, traceability) + 12 Architecture Center. Both doc sets share **one** budget (plan DEC-6). 9 elements have a WAF primary page, 43 an Architecture Center primary page. |

`../languages/*.md` and `../reliability-config-signals.md` are local lookup tables, not source summaries. They aren't counted against any budget and aren't refreshed from these sources.

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. The prefix `AZRL-` is skill-specific (plan DEC-6); `WAF-` (cost), `WAFR-` (DR), `WAFM-` (monitoring), `WAFO-` (observability) and `AZPE-` (performance) are taken.
- Level: every element is `REVIEW` (no normative keywords in either doc set). The level never changes severity (`SKILL.md` step 11).
- Primary anchor first; list every absorbed anchor so coverage stays auditable. Bullet-level guidance cites its section anchor.
- **Src** (W/A) is the doc set of the primary anchor's page and decides the source name in `Finding.standard`. If you change an element's primary anchor to the other doc set, update Src.
- Requirement text is generic: Azure product names (Service Bus, Front Door, API Management, Chaos Studio) are generalized ("message broker", "gateway", "fault injection"). Product-specific setting names belong in the lookup tables.
- Keep rows to one line (≈ 200 characters where possible). Rows are summaries in our own words.
- Every AZRL ID must be listed by exactly one check in `../checklist.md`, and the standards file's `## REL-xx` section must agree with it.
- Don't add elements for client reuse, pool sizing, total concurrency, offloading, autoscale metrics or resource limits (`review-performance`), statelessness, session state or sticky sessions (`review-twelve-factor` TF-06, decision D-6 in `docs/plan_localize-afterplanning-changes.md`), the HTTP contract of the repo's own APIs (`review-api-design`), health-endpoint implementation or retry/breaker telemetry (`review-observability`), alerts (`review-monitoring`), cross-region redundancy, backups or delete protection (`review-disaster-recovery`), over-provisioning or autoscale maximums (`review-cost-sustainability`), or resilience tests (`review-testing` TST-13). Edge DDoS and WAF rules have no owner (README "Known coverage gaps"). See plan §4.4 (DEC-13) and §10.
- Rate limiting: API rate limiting and `429` for request endpoints, including per-client or per-API-key limits and download limits, are judged under AZRL-32. Login throttling stays with `review-security-identity-access` SEC-IA-09. No element change (afterplanning WP-6, 2026-11-09).

## Shared pages

`re-check`, `re-prin` and `re-red` are also pinned by `review-disaster-recovery` (and `re-check` by `review-monitoring` and `review-observability`). When either skill refreshes them, record the new metadata in both `MAINTENANCE.md` files (plan C-7). The cross-region sections of `re-red` are DR's; the in-region sections are mapped here.

## Refresh procedure

1. **Cadence:** quarterly, or when run notes contain ≥ 3 `localized-standard-gap` entries for this skill.
2. **Detect drift:**
   - Re-fetch each pinned page (locale `en-us`) and follow redirects. Compare the final URL, the `ms.date` meta value, the **"Last updated" footer date** (`<local-time datetime=…>`) and the **`git_commit_id` meta value** with the page table in `azure-reliability-resiliency.md`. **Don't rely on `ms.date` alone:** `pat-retry` has no "Last updated" footer and an old `ms.date` (2024-07-18), so its commit is the only reliable signal (plan defect 12).
   - If the commit or "Last updated" date changed, diff that page's section text and anchor list. If a redirect is new, update the page path in the standards file and in `compliance-review-core/references/approved-sources.md`.
   - Check the WAF TOC (`https://learn.microsoft.com/azure/well-architected/toc.json`) for new, removed or renamed Reliability pages and design guides, and whether the `design-guides/handle-transient-faults` / `design-guides/background-jobs` duplicates have diverged from the Architecture Center guides (plan DEC-8).
   - Check the Architecture Center TOC (`https://learn.microsoft.com/azure/architecture/toc.json`) for new resiliency patterns, antipatterns or best-practice guides.
   - For `re-check`, `re-prin` and `re-red`, also update `review-disaster-recovery`'s `MAINTENANCE.md` (see Shared pages).
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep the website ≤ 100 elements. Update the coverage map below, the page metadata and retrieval date in the standards file header, `../sources.md`, and the URL list in `approved-sources.md` if a page moves.
4. **Lookup tables:** when a review logs a `localized-standard-gap` for an unrecognized library, default timeout or config setting, add it to the matching `../languages/<id>.md` or to `../reliability-config-signals.md`. Re-check the default timeouts at each refresh (the localization log lists which values were verified against vendor sources). No source refresh is needed.
5. **Verify:**
   - Download the pinned pages into a scratch folder (never into the repo).
   - Script-check: element IDs are contiguous; the checklist mapping rule above holds; Src matches the primary page; no Azure product name appears in a requirement cell; every listed anchor exists as an HTML `id` on its pinned page; every H1–H4 heading `id` on the pinned pages, minus the boilerplate listed below, appears in the coverage map with zero unaccounted.
   - Run a review against small sample repos (plan §9 step 8): (a) ASP.NET Core with `HttpClient.Timeout = InfiniteTimeSpan`, a `while(true)` retry, a Polly retry around an Azure SDK client, a breaker created per request and Kubernetes `replicas: 1`; (b) Spring Boot with `RestTemplate` defaults, `@Retryable` on a payment POST, Kafka `enable.auto.commit=true` and no IaC; (c) FastAPI + Celery with `requests` without `timeout=`, tenacity without `stop=`, default Celery acks, an SQS queue without a redrive policy and an App Service plan with `capacity: 2` but no health check path. Expect: `validate` passes; `22-review-reliability.json` has `urlsFetched: []`; all 8 checks present; citations use pinned URLs, element IDs and the right source name; (b) has REL-05 and REL-08 N/A; OkHttp/httpx defaults pass AZRL-01 with a note.
6. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-reliability` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-08 — initial localization

- Snapshot: planning snapshot (plan DEC-5) and implementation snapshot both 2026-11-08. All 18 pages returned 200; every final URL, `ms.date`, "Last updated" date and `git_commit_id` matches plan §5. `pat-retry` still renders no "Last updated" footer; recorded as "— (no footer)".
- Redirects found during planning, recorded here and not pinned: `well-architected/reliability/handle-transient-faults` → `well-architected/design-guides/handle-transient-faults`; `well-architected/reliability/background-jobs` → `well-architected/design-guides/background-jobs`; `architecture/best-practices/retry-service-specific` → `azure/reliability/overview`. The two `design-guides/…` pages (2025-02-24) are older near-copies of `bp-tf` and `bp-bg`; per plan DEC-8 the Architecture Center guides are pinned and the design guides are "not pinned (duplicate)". The `reliability/` landing page cited before localization is a link list and is not pinned.
- Page count: 18 pages, of which 17 are content pages and 1 (`re-check`) is traceability.
- Script verification: 52 IDs, contiguous; each listed by exactly one check and in the matching `## REL-xx` section; Src matches the primary page's doc set; every element anchor exists as an HTML `id` on its pinned page; no Azure product name in requirement text. The coverage map below accounts for all 158 non-boilerplate H1–H4 anchors on the 18 pages (zero unaccounted).
- Rows checked against the pinned section text. No anchor corrections were needed. Corrections and notes (no change to IDs or checks):
  - **AZRL-07 reworded.** The plan draft said "Delays grow between attempts … with jitter". `bp-tf#determine-an-appropriate-retry-count-and-interval` says to use exponential back-off with jitter for background operations and immediate or regular-interval retries for interactive operations; `bp-tf#avoid-antipatterns` warns against regular intervals "especially when you have a high number of retry attempts". The row now says background/batch retries use growing delays with jitter and interactive paths may use a few regular-interval retries.
  - AZRL-20: the source (`pat-retry#transaction-consistency`) only says to consider transaction consistency and tune the policy to reduce undo work; "retry the whole transaction unit" is our concrete reading.
  - AZRL-26: the source (`pat-cb#problems-and-considerations`, "Concurrency") says many concurrent instances access the same breaker; "a new breaker per request never trips" is our concrete reading.
  - AZRL-01: `bp-tf` says "Set timeouts on every outbound call before you implement retry logic". The finite-default/infinite split is plan DEC-9, not source text.
- Language files and config signals (plan step 4): written from maintainer knowledge. Per user decision 2026-11-08, only the † values in the plan's §8.3 drafts were checked against vendor sources (raw repository source or official docs, fetched 2026-11-08). All were confirmed:
  - .NET standard resilience handler: total request timeout 30 s, attempt timeout 10 s, break duration 5 s; `DisableForUnsafeHttpMethods()` disables retries for POST, PATCH, PUT, DELETE and CONNECT (learn.microsoft.com `dotnet/core/resilience/http-resilience`).
  - Azure.Core `RetryOptions`: `NetworkTimeout` 100 s, `Mode` Exponential, 3 retries, 0.8 s initial delay, 1 min max delay (azure-sdk-for-net `RetryOptions.cs`).
  - StackExchange.Redis: `connectTimeout` 5000 ms, `syncTimeout` 5000 ms, `asyncTimeout` = `syncTimeout` (`docs/Configuration.md`).
  - Reactor Netty `HttpClient`: `responseTimeout` not specified by default; `CONNECT_TIMEOUT_MILLIS` 30 s (reference docs).
  - Apache HttpClient 5: `ConnectionConfig` connect timeout 3 min, socket timeout unset; `RequestConfig` connection-request timeout 3 min, response timeout unset (master source). The connection-request timeout was added to `languages/java.md`.
  - OpenFeign `Request.Options()`: connect 10 s, read 60 s (master source).
  - aiohttp `ClientTimeout`: `total` 300 s; `sock_connect` is `None` on current master (older releases used 30 s), so only `total` is stated.
  - redis-py: `socket_timeout` `None` by default.
  - azure-core (Python) `ConnectionConfiguration`: connection and read timeouts 300 s.
  - Celery: `task_acks_late` and `task_reject_on_worker_lost` disabled by default (early ack).
  - **Not fetched** (re-check on the first refresh): `HttpClient` 100 s, `SqlClient` 30 s / 15 s, `Grpc.Net.Client` no deadline, `HttpURLConnection` / `java.net.http.HttpClient` no timeout, OkHttp 10 s, JDBC query timeout 0, HikariCP 30 s, `requests` / `urllib` no timeout, httpx 5 s, psycopg no timeouts, SQLAlchemy `pool_timeout` 30 s, botocore 60 s / 60 s, and every name in the Signals tables and `reliability-config-signals.md`.
- Plan step 8 (sample-repo validation runs) **not yet run** (user decision 2026-11-08: deferred, as for `review-performance`). Run it per refresh step 5 before relying on the new checks, and record the result here.

## Open items

- Plan §10 follow-ups (changes outside this skill): reviewed and closed by `docs/plan_localize-afterplanning-changes.md` on 2026-11-09 (see its Appendix A). Open hand-offs: none.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Coverage map

Excluded as boilerplate: `ms--in-this-article`, `ms--feedback`, `ms--additional-resources-mobile-heading`, `next-steps`, `next-step`, `related-links`, `related-link`, `related-resources`, `reliability-checklist`, `workload-design`, `example`. Subsections of an `example` heading (the `pat-cb` flows and components) are listed and mapped to BG.

Reason codes for "not localized":
- **RUNTIME**: Retry Storm "Detect the problem" / "Example diagnosis" and subsections: runtime diagnosis with telemetry (non-goal, plan §3).
- **PERF**: offloading, worker scaling, autoscale metrics, batching and pooling. Owned by `review-performance` (C-3).
- **API**: the HTTP contract of the repo's own APIs (error codes, 429/503, `Retry-After`). Owned by `review-api-design` (C-4).
- **OBS**: logging, metrics and tracing of retries, breakers and duplicates. Owned by `review-observability` (C-5).
- **MON**: alerts, failure detection, scaling and dead-letter monitoring. Owned by `review-monitoring` (C-6).
- **DR**: cross-region redundancy, failover, geo-replication, delete protection. Owned by `review-disaster-recovery` (C-7).
- **COST**: autoscale maximum bounds, over-provisioning. Owned by `review-cost-sustainability` (C-8).
- **TEST**: retry-strategy tests, fault injection and chaos: `review-testing` TST-13 (decision D-3, 2026-11-09).
- **SEC**: background-job security: the security skills. Edge DDoS/WAF controls: no owner (README "Known coverage gaps"; C-10).
- Notes: software-quality AP-05 is retired; resilience patterns are owned here. Process-level SIGTERM handling and startup: twelve-factor TF-09; consumer and job shutdown semantics: REL-07.
- **ARCH**: architecture or design decision without a pass/fail criterion in a repo.
- **PROC**: process or documentation practice (business requirements, FMA documentation, operations).
- **OPT**: optional refinement with no pass/fail criterion (plan §7.2; some are follow-up candidates).
- **PRODUCT**: hosting-product guidance (`bp-bg#hosting-environment` subtree).
- **AZ**: "Azure facilitation" (Azure-service-specific).
- **XREF**: short pointer to guidance that another pinned page covers in full.
- **BG**: background, problem statement, applicability list or worked example.
- **PARENT**: page title or parent heading whose substance is in its subsections (mapped separately).
- **TRACE**: traceability only (checklist page).

A mapping like "AZRL-31 (… : ARCH)" means the section is localized by the listed elements, and the parenthesized parts are deliberately not localized for the stated reason.

**re-check** (2)
- `design-review-checklist-for-reliability` → TRACE
- `checklist` → TRACE

**re-prin** (6)
- `reliability-design-principles` → PARENT
- `design-for-business-requirements` → PROC
- `design-for-resilience` → AZRL-28, AZRL-31 (decoupling and architecture choices: ARCH)
- `design-for-recovery` → AZRL-50 (automated self-healing only; restore and DR parts: DR)
- `design-for-operations` → PROC
- `keep-it-simple` → ARCH

**re-red** (11)
- `architecture-strategies-for-designing-for-redundancy` → PARENT
- `prefer-serverless-and-fully-managed-services-to-reduce-operational-burden` → AZRL-27
- `build-redundancy-into-your-workload-with-multiple-component-instances` → AZRL-27, AZRL-28, AZRL-29, AZRL-49, AZRL-51 (geo-replication: DR; networking, polyglot, partitioning and CQRS bullets: ARCH)
- `use-the-deployment-stamps-pattern-to-streamline-your-redundancy-approach` → ARCH
- `achieve-zero-downtime-through-active-active-redundancy` → DR
- `use-an-active-passive-architecture-design-as-a-cost-effective-dr-approach` → DR
- `distribute-workloads-across-proximate-independent-infrastructure` → AZRL-48
- `strengthen-fault-tolerance-with-geo-distant-deployments` → DR
- `azure-facilitation` → AZRL-49
- `dns-specific-azure-facilitation` → AZ (DNS; DR)
- `apply-delete-protection-to-preserve-redundancy` → DR (WAFR-31)

**re-scale** (11)
- `architecture-strategies-for-designing-a-reliable-scaling-strategy` → PARENT
- `design-according-to-load-patterns` → ARCH
- `adapt-scaling-strategies-to-fit-individual-components-or-flows` → AZRL-43, AZRL-44, AZRL-47
- `choose-the-right-technology` → ARCH
- `automate-scaling` → AZRL-52 (metrics and thresholds: PERF; maximum bounds: COST)
- `choose-appropriate-scale-units` → ARCH
- `optimize-the-scale-unit-initialization-time` → AZRL-52
- `scale-data-stores-using-sharding-and-partitioning` → ARCH
- `monitor-your-scaling-operations` → MON
- `azure-facilitation` → AZ
- `tradeoffs` → BG

**re-sp** (12)
- `architecture-strategies-for-self-healing-and-self-preservation` → PARENT
- `design-for-redundancy` → AZRL-27
- `design-for-self-preservation` → PARENT
- `infrastructure-design-guidance-and-patterns` → AZRL-48, AZRL-52
- `application-design-guidance-and-patterns` → ARCH
- `design-for-self-healing` → AZRL-49
- `infrastructure-design-guidance` → AZRL-50, AZRL-51
- `application-design-guidance` → AZRL-39, AZRL-43 (monitoring-triggered self-healing actions: MON)
- `implement-a-graceful-degradation-mode` → AZRL-31
- `implement-mechanisms-for-handling-transient-faults` → XREF (bp-tf)
- `implement-background-jobs` → XREF (bp-bg); offloading: PERF
- `azure-facilitation` → AZ

**re-fma** (8)
- `architecture-strategies-for-performing-failure-mode-analysis` → PARENT
- `decompose-your-workload` → PROC
- `identify-workload-dependencies` → PROC
- `evaluate-failure-points-in-your-flows` → PROC
- `plan-mitigation-strategies` → AZRL-31
- `implement-failure-detection` → MON
- `document-your-fma-findings` → PROC
- `azure-facilitation` → AZ

**bp-tf** (13)
- `best-practices-for-transient-fault-handling` → PARENT
- `why-do-transient-faults-occur-in-the-cloud` → BG
- `challenges` → BG
- `general-guidelines` → PARENT
- `check-whether-a-built-in-retry-mechanism-exists` → AZRL-05
- `check-whether-retrying-suits-the-operation` → AZRL-08 (error codes for the repo's own APIs: API)
- `determine-an-appropriate-retry-count-and-interval` → AZRL-01, AZRL-02, AZRL-03, AZRL-07, AZRL-09, AZRL-12, AZRL-14
- `avoid-antipatterns` → AZRL-06, AZRL-07, AZRL-10, AZRL-11
- `test-your-retry-strategy-and-implementation` → TEST
- `manage-retry-policy-configurations` → AZRL-13
- `log-and-track-transient-and-nontransient-faults` → OBS / MON
- `manage-operations-that-continually-fail` → AZRL-14, AZRL-21
- `other-considerations` → AZRL-15, AZRL-18 (shared tenants, premium services: ARCH)

**bp-bg** (27)
- `best-practices-for-background-jobs` → PARENT
- `types-of-background-jobs` → BG
- `triggers` → BG
- `event-driven-triggers` → BG
- `schedule-driven-triggers` → BG
- `returning-results` → ARCH
- `design-for-idempotency` → AZRL-36, AZRL-45
- `hosting-environment` → PRODUCT
- `functions` → PRODUCT (hosting-environment subtree)
- `functions-considerations` → PRODUCT (hosting-environment subtree)
- `container-apps` → PRODUCT (hosting-environment subtree)
- `container-apps-considerations` → PRODUCT (hosting-environment subtree)
- `aks` → PRODUCT (hosting-environment subtree)
- `aks-considerations` → PRODUCT (hosting-environment subtree)
- `batch` → PRODUCT (hosting-environment subtree)
- `batch-considerations` → PRODUCT (hosting-environment subtree)
- `virtual-machines` → PRODUCT (hosting-environment subtree)
- `virtual-machines-considerations` → PRODUCT (hosting-environment subtree)
- `app-service-webjobs` → PRODUCT (hosting-environment subtree)
- `app-service-webjobs-considerations` → PRODUCT (hosting-environment subtree)
- `partitioning` → ARCH
- `conflicts` → AZRL-28, AZRL-45
- `coordination` → AZRL-19 (Pipes and Filters, Scheduler Agent Supervisor: ARCH)
- `reliability-considerations` → AZRL-39, AZRL-40, AZRL-41, AZRL-42, AZRL-43, AZRL-44
- `security-considerations` → SEC
- `observability-considerations` → OBS
- `scaling-and-performance-considerations` → PERF

**pat-retry** (10)
- `context-and-problem` → BG
- `solution` → AZRL-05, AZRL-14 (logging: OBS; scale out the service: PERF)
- `retry-strategies` → BG (strategies restated in bp-tf; AZRL-07, AZRL-08)
- `issues-and-considerations` → PARENT
- `impact-on-performance` → AZRL-02, AZRL-12
- `idempotency` → AZRL-15
- `exception-type` → AZRL-08
- `transaction-consistency` → AZRL-20
- `general-guidance` → AZRL-10
- `when-to-use-this-pattern` → AZRL-08

**pat-cb** (9)
- `circuit-breaker-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → AZRL-21, AZRL-22, AZRL-23
- `problems-and-considerations` → AZRL-01, AZRL-02, AZRL-23, AZRL-24, AZRL-25, AZRL-26, AZRL-31 (monitoring: OBS; manual override, replay, failed-operations testing, accelerated breaking, adaptive, multiregion, compute diversification: OPT)
- `when-to-use-this-pattern` → AZRL-21
- `flow-a-closed-state` → BG (example subtree)
- `flow-b-open-state` → BG (example subtree)
- `flow-c-half-open-state` → BG (example subtree)
- `components` → BG (example subtree)

**pat-bh** (5)
- `bulkhead-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → AZRL-30
- `problems-and-considerations` → AZRL-30 (partition granularity, DDD alignment, AI quotas: ARCH; per-partition monitoring: MON)
- `when-to-use-this-pattern` → AZRL-30

**pat-thr** (5)
- `throttling-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → AZRL-32, AZRL-34
- `problems-and-considerations` → AZRL-32, AZRL-33, AZRL-35 (algorithm choice, adaptive limits, cost normalization, priority deferral, carbon-aware use: OPT; edge controls: SEC; 429/Retry-After shape: API)
- `when-to-use-this-pattern` → BG (applicability; reflected in "Applies when")

**pat-rl** (5)
- `rate-limiting-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → AZRL-04, AZRL-34, AZRL-46 (lease partitioning details, release intervals: OPT)
- `problems-and-considerations` → AZRL-09, AZRL-34
- `when-to-use-this-pattern` → BG (applicability; reflected in "Applies when")

**pat-qbll** (5)
- `queue-based-load-leveling-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → PERF (AZPE-42)
- `problems-and-considerations` → AZRL-36, AZRL-39, AZRL-42, AZRL-46, AZRL-47 (reply mechanisms: ARCH; geo-DR: DR; dead-letter depth monitoring: MON)
- `when-to-use-this-pattern` → BG (applicability; reflected in "Applies when")

**pat-cc** (5)
- `competing-consumers-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → AZRL-41
- `problems-and-considerations` → AZRL-39, AZRL-42, AZRL-46 (result handling, messaging-system scaling: ARCH / PERF)
- `when-to-use-this-pattern` → BG (applicability; reflected in "Applies when")

**pat-ic** (11)
- `idempotent-consumer-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → AZRL-36
- `choose-a-stable-deduplication-key` → AZRL-17, AZRL-36
- `decide-where-to-store-processed-keys` → ARCH
- `commit-the-processed-key-and-the-side-effects-atomically` → AZRL-37
- `guard-against-concurrent-duplicates` → AZRL-37
- `handle-side-effects-that-cant-join-the-transaction` → AZRL-38
- `problems-and-considerations` → AZRL-16, AZRL-17, AZRL-36, AZRL-38, AZRL-42 (instrumentation: OBS; messaging frameworks: pass signals in languages/)
- `when-to-use-this-pattern` → BG (applicability; reflected in "Applies when")
- `idempotent-processing-beyond-messaging` → BG

**pat-ct** (5)
- `compensating-transaction-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → AZRL-19
- `problems-and-considerations` → AZRL-04, AZRL-19 (correlation and audit of compensation: OBS)
- `when-to-use-this-pattern` → BG (applicability; reflected in "Applies when")

**ap-rs** (8)
- `retry-storm-antipattern` → PARENT
- `context-and-problem` → AZRL-06
- `solution` → AZRL-05, AZRL-06, AZRL-07, AZRL-09, AZRL-21, AZRL-32, AZRL-33 (abstraction layer: pass signal in config-signals; batching and pooling: PERF)
- `considerations` → AZRL-08
- `detect-the-problem` → RUNTIME
- `example-diagnosis` → RUNTIME
- `identify-patterns-by-using-client-telemetry` → RUNTIME
- `identify-patterns-by-using-server-telemetry` → RUNTIME
