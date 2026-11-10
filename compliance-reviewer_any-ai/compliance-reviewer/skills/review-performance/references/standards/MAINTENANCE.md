# Maintenance — Performance localized standards

**Maintainers only. Workers never load this file.** Background and design decisions: `docs/plan_localize-review-performance.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1).

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| learn.microsoft.com (azure/well-architected + azure/architecture) | azure-performance-efficiency.md | 53 (51 active; AZPE-47/48 retired) | 100 | 19 pages: 7 WAF (1 checklist, traceability) + 12 Architecture Center (1 antipattern catalog, traceability). Both doc sets share **one** budget (plan DEC-6). 18 elements have a WAF primary page, 35 an Architecture Center primary page. |

`../languages/*.md` and `../performance-config-signals.md` are local lookup tables, not source summaries. They aren't counted against any budget and aren't refreshed from these sources.

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. The prefix `AZPE-` is skill-specific (plan DEC-6) so it can't be confused with the WAF prefixes `WAF-` (cost), `WAFR-` (DR), `WAFM-` (monitoring) and `WAFO-` (observability).
- Level: every element is `REVIEW` (no normative keywords in either doc set). The level never changes severity (`SKILL.md` step 9).
- Primary anchor first; list every absorbed anchor so coverage stays auditable. Bullet-level guidance cites its section anchor.
- **Src** (W/A) is the doc set of the primary anchor's page and decides the source name in `Finding.standard`. If you change an element's primary anchor to the other doc set, update Src.
- Requirement text is generic: Azure product names (Azure Managed Redis, Service Bus, Cosmos DB, App Service) are generalized ("distributed cache", "message queue"). Product-specific setting names belong in the lookup tables.
- Keep rows to one line (≈ 200 characters where possible). Rows are summaries in our own words.
- Every AZPE ID must be listed by exactly one check in `../checklist.md`, and the standards file's `## PERF-xx` section must agree with it.
- Don't add elements for statelessness, session state or sticky sessions (`review-twelve-factor` TF-06; D-6), load or performance tests (`review-testing` TST-12; D-3), retries, backoff, timeouts, circuit breakers or Retry Storm (`review-reliability`), the HTTP API contract (`review-api-design`), instrumentation or telemetry volume (`review-observability`), alerts (`review-monitoring`), autoscale max bounds, over-provisioning or data lifecycle (`review-cost-sustainability`), or cache authentication/TLS (security skills). See plan §4.4 and §10.

## Refresh procedure

1. **Cadence:** quarterly, or when run notes contain ≥ 3 `localized-standard-gap` entries for this skill.
2. **Detect drift:**
   - Re-fetch each pinned page (locale `en-us`) and follow redirects. Compare the final URL, the `ms.date` meta value, the **"Last updated" footer date** (`<local-time datetime=…>`) and the **`git_commit_id` meta value** with the page table in `azure-performance-efficiency.md`. **Don't rely on `ms.date` alone:** several antipattern pages keep `ms.date` 2017-06-05 while their content changed in 2025–2026 (plan defect 9). `ap-nn` and `pat-ca` show no "Last updated" footer, so the commit is their only reliable signal. The `updated_at` meta value is a build timestamp, not a content date; ignore it.
   - If the commit or "Last updated" date changed, diff that page's section text and anchor list. If a redirect is new, update the page path in the standards file and in `compliance-review-core/references/approved-sources.md`.
   - Check the WAF TOC (`https://learn.microsoft.com/azure/well-architected/toc.json`) for new, removed or renamed Performance Efficiency pages.
   - Check the Architecture Center TOC (`https://learn.microsoft.com/azure/architecture/toc.json`) and the antipattern catalog (`antipatterns/`) for new antipatterns or caching guidance.
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep the website ≤ 100 elements. Update the coverage map below, the page metadata and retrieval date in the standards file header, `../sources.md`, and the URL list in `approved-sources.md` if a page moves.
4. **Lookup tables:** when a review logs a `localized-standard-gap` for an unrecognized library, framework or config setting, add it to the matching `../languages/<id>.md` or to `../performance-config-signals.md`. No source refresh is needed.
5. **Verify:**
   - Download the pinned pages into a scratch folder (never into the repo).
   - Script-check: element IDs are contiguous; the checklist mapping rule above holds; no Azure product name appears in a requirement cell; every listed anchor exists as an HTML `id` on its pinned page; every H1–H4 heading `id` on the pinned pages, minus the boilerplate listed below, appears in the coverage map with zero unaccounted.
   - Run a review against small sample repos (plan §9 step 8): (a) ASP.NET Core + EF Core with `new HttpClient()` per call, `.Result`, lazy-loading N+1 and an unbounded `IMemoryCache`; (b) Spring MVC + JPA with blocking JDBC, `findAll()` filtering and `FetchType.EAGER`; (c) FastAPI with `requests` inside `async def`, Celery offloading and a Kubernetes Deployment with `sessionAffinity: ClientIP`. Expect: `validate` passes; `23-review-performance.json` has `urlsFetched: []`; all 8 checks present; citations use pinned URLs, element IDs and the right source name; (b) has AZPE-13 skipped and doesn't fail PERF-02 for blocking JDBC; AZPE-11 is skipped for API-only targets.
6. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-performance` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-08 — initial localization

- Snapshot: planning snapshot (plan DEC-10) and implementation snapshot both 2026-11-08. All 19 pages returned 200; every final URL, `ms.date`, "Last updated" date and `git_commit_id` matches plan §5. `antipatterns/noisy-neighbor/` still redirects to `antipatterns/noisy-neighbor/noisy-neighbor`.
- The two "(record in step 1)" cells: `ap-nn` and `pat-ca` render **no "Last updated" footer** (pattern-style pages). Recorded as "— (no footer)"; the commit is the drift signal for both.
- Page count: plan §1/§2.2 say "18 pages" and §8.6 "17 content pages"; the plan's own page table lists **19** (7 WAF + 12 Architecture Center), of which 17 are content pages and 2 (`pe-check`, `ap`) traceability. `../sources.md` and this file use 19 / 17.
- Script verification: 53 IDs, contiguous; each listed by exactly one check and in the matching `## PERF-xx` section; every element anchor exists as an HTML `id` on its pinned page; no Azure product name in requirement text. Coverage map below accounts for all 208 non-boilerplate H1–H4 anchors on the 19 pages (zero unaccounted).
- Rows checked against the pinned section text. No anchor corrections were needed. Notes (no change to IDs or checks):
  - AZPE-14: the source states that "a single synchronous I/O call can block an entire call chain" and recommends async versions throughout; "waiting on a task, future or promise result" is our concrete reading of that for async-capable stacks (plan DEC-3).
  - AZPE-34: added "(e.g. remote debugging)" from `pe-ops#optimize-monitoring-and-debugging` ("convenience features like remote debugging can also affect performance").
  - AZPE-49: added "(buffer)" to minimum headroom (source strategy "Use a buffer").
  - AZPE-51: compression comes from the "Data compression" bullet and HTTP/2 from the "Network protocols" bullet, both in `pe-code#optimize-infrastructure-performance`.
- Language files and config signals (plan step 4): written from maintainer knowledge, following the precedent of the observability localization (user decision there, 2026-11-08: fetch only uncertain names). Corrections against the plan's §8.3/§8.4 drafts: DRF `max_page_size` is an attribute of a pagination class, not a setting; ingress-nginx `use-gzip` / `use-http2` are ConfigMap keys, not annotations; Front Door affinity (`sessionAffinityState`) and compression settings added; gunicorn/uWSGI multi-process added as multi-instance evidence for process-local caches. **Not fetched** (re-check on the first refresh): `HybridCache` (.NET 9+), `ExecuteUpdateAsync` (EF Core 7+), `[GeneratedRegex]`, `spring.threads.virtual.enabled`, `spring.data.web.pageable.max-page-size`, `spring.web.resources.cache.*`, Django `CONN_HEALTH_CHECKS`, SQLAlchemy `version_id_col`, Front Door `compressionSettings`, Cloud Run `max_instance_request_concurrency`.
- Plan step 8 (sample-repo validation runs) **not yet run** (user decision 2026-11-08: deferred). Run it per refresh step 5 before relying on the new checks, and record the result here.

### 2026-11-09 — statelessness moved to Twelve-Factor (afterplanning WP-6, decision D-6)

- AZPE-47 (stateless instances) and AZPE-48 (session affinity) **retired**: no performance-only aspect is left in the pinned text of `pe-scale#design-application-to-scale` once statelessness is removed, and TF-06 (TFA-30, TFA-33, TFR-12) judges both. PERF-08 now lists AZPE-49–AZPE-53 and no longer mentions stateless instances or sticky sessions. Performance scores before and after aren't directly comparable (README).
- AZPE-11: added "never recommend caching authenticated, per-user or sensitive responses (`no-store`: SEC-WA-08)" (web-api C-8).
- Latency *targets* (PE:01) aren't localized; stated targets are judged only through observability OBS-07 (performance C-5).

## Open items

- Plan §10 follow-ups (changes outside this skill): reviewed and closed by `docs/plan_localize-afterplanning-changes.md` on 2026-11-09 (see its Appendix A). Open hand-offs: none.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Coverage map

Excluded as boilerplate: `ms--in-this-article`, `ms--feedback`, `ms--additional-resources-mobile-heading`, `next-steps`, `related-links`, `related-resources`, `related-guidance`, `performance-efficiency-checklist`, `contributors`.

Reason codes for "not localized":
- **RUNTIME**: "How to detect" / "Example diagnosis" and their subsections: runtime diagnosis with telemetry and load tests (non-goal, plan §3).
- **REL**: retries, Retry Storm, safe queue handling. Owned by `review-reliability` (plan DEC-4, C-3).
- **OBS**: instrumentation, profiling data, cache hit/miss metrics. Owned by `review-observability` (C-5).
- **MON**: performance monitoring and alerting. Owned by `review-monitoring`.
- **COST**: SKU/capacity purchase, autoscale max bounds, archive/purge. Owned by `review-cost-sustainability` (C-7).
- **DR**: backups, geo-replication, cache persistence. Owned by `review-disaster-recovery`.
- **SEC**: cache authentication, TLS, network isolation. Owned by the security skills (C-8).
- **TEST**: load and performance tests: `review-testing` TST-12 (decision D-3, 2026-11-09). Latency *targets* (PE:01) aren't localized; stated targets are judged only through observability OBS-07.
- **OPS**: deployment, upgrade, tooling and database operations; not code performance.
- **ARCH**: architecture or service-selection decision; not verifiable as pass/fail from a repo.
- **PROC**: process or documentation practice (flow identification, profiling, memory-dump debugging).
- **TOOL**: product tutorial content (Azure Managed Redis client specifics, leaderboards, Aspire).
- **AZ**: "Azure facilitation" (Azure-service-specific).
- **BG**: background, problem statement or worked example.
- **PARENT**: page title or parent heading whose substance is in its subsections (mapped separately).
- **TRACE**: traceability only (checklist and catalog pages).

**pe-check** (2)
- `design-review-checklist-for-performance-efficiency` → TRACE
- `checklist` → TRACE

**pe-svc** (14)
- `architecture-strategies-for-selecting-the-right-services` → PARENT
- `understand-workload-requirements` → ARCH
- `understand-services` → ARCH
- `understand-service-limits` → ARCH
- `prefer-platform-features` → ARCH
- `evaluate-infrastructure-requirements` → ARCH
- `evaluate-networking-requirements` → ARCH
- `evaluate-compute-requirements` → ARCH
- `evaluate-load-balancing-requirements` → ARCH
- `evaluate-data-store-requirements` → ARCH
- `evaluate-database-requirements` → ARCH
- `evaluate-storage-requirements` → ARCH
- `evaluate-cache-requirements` → AZPE-52 (cache sizing and service choice: ARCH)
- `azure-facilitation` → AZ

**pe-scale** (13)
- `architecture-strategies-for-optimizing-scaling-and-partitioning` → PARENT
- `optimize-scaling` → PARENT
- `choose-a-scaling-strategy` → ARCH
- `design-infrastructure-to-scale` → AZPE-53 (decoupling, microservices: ARCH)
- `design-application-to-scale` → AZPE-41, AZPE-42, AZPE-44, AZPE-47 (retired), AZPE-48 (retired) — statelessness and affinity: review-twelve-factor TF-06 (dynamic service discovery: ARCH)
- `configure-scaling` → AZPE-49 ("constrain autoscaling" max bounds: COST; service scaling boundaries: ARCH)
- `test-scaling` → TEST
- `partition-workload` → PARENT
- `understand-partitioning` → ARCH
- `plan-partitioning` → ARCH
- `implement-partitioning` → ARCH
- `test-and-optimize-partitioning` → TEST
- `azure-facilitation` → AZ

**pe-code** (11)
- `architecture-strategies-for-optimizing-code-and-infrastructure` → PARENT
- `optimize-code-performance` → PARENT
- `instrument-your-code` → OBS
- `identify-hot-paths` → PROC (replaced by the static hot-path rule, `SKILL.md` step 3)
- `optimize-code-logic` → AZPE-27, AZPE-30, AZPE-31, AZPE-32, AZPE-34 ("performance-optimized SDKs": follow-up candidate; "cross-cutting implementation": ARCH)
- `optimize-memory-management` → AZPE-24, AZPE-32 (memory-dump debugging: PROC)
- `use-concurrency-and-parallelism` → AZPE-13, AZPE-17, AZPE-18, AZPE-42
- `use-connection-pooling` → AZPE-22, AZPE-23
- `optimize-background-jobs` → AZPE-43
- `optimize-infrastructure-performance` → AZPE-35, AZPE-50, AZPE-51, AZPE-52 (streamline, eventual consistency, delegate tasks: ARCH; log collection: OBS/COST)
- `azure-facilitation` → AZ

**pe-data** (19)
- `architecture-strategies-for-optimizing-data-performance` → PARENT
- `profile-data` → PROC
- `monitor-data-performance` → MON
- `partition-data` → ARCH (partition key for document stores: follow-up candidate)
- `optimize-database-queries` → AZPE-01, AZPE-25, AZPE-41
- `optimize-index-performance` → AZPE-40
- `consider-data-compression` → ARCH
- `archive-and-purge-data` → COST
- `optimize-storage-load` → PARENT
- `use-caching` → AZPE-01, AZPE-52
- `use-read-replicas` → ARCH
- `optimize-data-consistency` → ARCH
- `optimize-data-updates` → AZPE-41
- `optimize-data-movement-and-processing` → AZPE-26
- `optimize-storage-design` → PARENT
- `design-for-data-proximity` → ARCH
- `use-polyglot-persistence` → ARCH
- `separate-oltp-and-olap-systems` → ARCH
- `azure-facilitation` → AZ

**pe-crit** (7)
- `architecture-strategies-for-prioritizing-the-performance-of-critical-flows` → PARENT
- `identify-all-flows` → PROC
- `monitor-flow-performance-metrics` → MON
- `identify-critical-flows` → PROC
- `isolate-critical-flows` → AZPE-50 (dedicated capacity per flow: ARCH)
- `optimize-capacity-allocation` → AZPE-45, AZPE-46
- `azure-facilitation` → AZ

**pe-ops** (9)
- `architecture-strategies-for-optimizing-operational-tasks` → PARENT
- `account-for-operational-tasks` → OPS
- `optimize-deployments` → OPS
- `optimize-upgrades` → OPS
- `optimize-tooling` → OPS
- `optimize-database-operations` → OPS
- `optimize-backups` → DR
- `optimize-monitoring-and-debugging` → AZPE-34
- `azure-facilitation` → AZ

**ap** (2)
- `performance-testing-and-antipatterns-for-cloud-applications` → TRACE
- `catalog-of-antipatterns` → TRACE (Retry Storm row: REL)

**ap-bdb** (9)
- `busy-database-antipattern` → PARENT
- `problem-description` → AZPE-38
- `how-to-fix-the-problem` → AZPE-38
- `considerations` → AZPE-38
- `how-to-detect-the-problem` → RUNTIME
- `example-diagnosis` → RUNTIME
- `monitor-the-volume-of-database-activity` → RUNTIME
- `examine-the-work-performed-by-the-database` → RUNTIME
- `implement-the-solution-and-verify-the-result` → RUNTIME

**ap-bfe** (11)
- `busy-front-end-antipattern` → PARENT
- `problem-description` → AZPE-43
- `how-to-fix-the-problem` → AZPE-42, AZPE-44
- `considerations` → AZPE-46 (complexity notes: BG; safe queue handling: REL)
- `how-to-detect-the-problem` → RUNTIME
- `example-diagnosis` → RUNTIME
- `identify-points-of-slowdown` → RUNTIME
- `examine-telemetry-data-and-find-correlations` → RUNTIME
- `perform-load-testing` → RUNTIME
- `review-the-source-code` → RUNTIME
- `implement-the-solution-and-verify-the-result` → RUNTIME

**ap-cio** (13)
- `chatty-io-antipattern` → PARENT
- `problem-description` → PARENT
- `reading-and-writing-individual-records-to-a-database-as-distinct-requests` → AZPE-25, AZPE-26
- `implementing-a-single-logical-operation-as-a-series-of-http-requests` → AZPE-27
- `reading-and-writing-to-a-file-on-disk` → AZPE-28
- `how-to-fix-the-problem` → AZPE-25, AZPE-27, AZPE-28
- `considerations` → AZPE-29, AZPE-41
- `how-to-detect-the-problem` → RUNTIME
- `example-diagnosis` → RUNTIME
- `load-test-the-application` → RUNTIME
- `monitor-the-application` → RUNTIME
- `gather-detailed-data-access-information` → RUNTIME
- `implement-the-solution-and-verify-the-result` → RUNTIME

**ap-ef** (11)
- `extraneous-fetching-antipattern` → PARENT
- `examples-of-extraneous-fetching-antipattern` → AZPE-36
- `how-to-fix-extraneous-fetching-antipattern` → AZPE-35, AZPE-36
- `considerations` → AZPE-35, AZPE-36, AZPE-37
- `how-to-detect-extraneous-fetching-antipattern` → RUNTIME
- `example-diagnosis` → RUNTIME
- `identify-slow-workloads` → RUNTIME
- `correlate-slow-workloads-with-behavioral-patterns` → RUNTIME
- `identify-data-sources-in-slow-workloads` → RUNTIME
- `identify-and-analyze-slow-queries` → RUNTIME
- `implement-the-solution-and-verify-the-result` → RUNTIME

**ap-ii** (10)
- `improper-instantiation-antipattern` → PARENT
- `problem-description` → AZPE-19, AZPE-24
- `how-to-fix-improper-instantiation-antipattern` → AZPE-19, AZPE-20
- `considerations` → AZPE-21, AZPE-22, AZPE-24
- `how-to-detect-improper-instantiation-antipattern` → RUNTIME
- `example-diagnosis` → RUNTIME
- `identify-points-of-slowdown-or-failure` → RUNTIME
- `examine-telemetry-data-and-find-correlations` → RUNTIME
- `performing-load-testing` → RUNTIME
- `implement-the-solution-and-verify-the-result` → RUNTIME

**ap-mp** (12)
- `monolithic-persistence-antipattern` → PARENT
- `context-and-problem` → AZPE-39
- `solution` → AZPE-39
- `problems-and-considerations` → AZPE-39
- `detect-the-problem` → RUNTIME
- `example-diagnosis` → RUNTIME
- `instrument-and-monitor-the-system` → RUNTIME
- `identify-periods-of-poor-performance` → RUNTIME
- `identify-which-data-stores-are-accessed-during-those-periods` → RUNTIME
- `examine-the-telemetry-for-the-data-stores` → RUNTIME
- `identify-resource-contention` → RUNTIME
- `implement-the-solution-and-verify-the-result` → RUNTIME

**ap-nc** (10)
- `no-caching-antipattern` → PARENT
- `examples-of-no-caching-antipattern` → AZPE-01 (BG examples)
- `how-to-fix-the-no-caching-antipattern` → AZPE-01, AZPE-04
- `considerations-for-caching-strategy` → AZPE-02, AZPE-03, AZPE-06, AZPE-10, AZPE-11, AZPE-33 (cache hit/miss instrumentation: OBS)
- `how-to-detect-a-no-caching-antipattern` → RUNTIME
- `example-diagnosis` → RUNTIME
- `instrument-the-application-and-monitor-the-live-system` → RUNTIME
- `load-test-the-application` → RUNTIME
- `examine-data-access-statistics` → RUNTIME
- `implement-the-cache-strategy-solution-and-verify-the-result` → RUNTIME

**ap-nn** (6)
- `context-and-problem` → BG
- `solution` → PARENT
- `actions-that-clients-can-take` → COST (reserved capacity, tiers, single-tenant instances: ARCH)
- `actions-that-service-providers-can-take` → AZPE-37, AZPE-45, AZPE-46 (monitoring: MON; provisioning, rebalancing, QoS: ARCH)
- `considerations` → ARCH
- `how-to-detect-the-problem` → RUNTIME

**ap-sio** (9)
- `synchronous-io-antipattern` → PARENT
- `problem-description` → AZPE-14
- `how-to-fix-the-problem` → AZPE-13, AZPE-14, AZPE-15, AZPE-16
- `considerations` → AZPE-13, AZPE-18
- `how-to-detect-the-problem` → RUNTIME
- `example-diagnosis` → RUNTIME
- `monitor-web-server-performance` → RUNTIME
- `load-test-the-application` → RUNTIME
- `implement-the-solution-and-verify-the-result` → RUNTIME

**bp-cache** (34)
- `caching-guidance` → PARENT
- `caching-in-distributed-applications` → PARENT
- `private-caching` → AZPE-07
- `shared-caching` → AZPE-07
- `considerations-for-using-caching` → PARENT
- `decide-when-to-cache-data` → AZPE-01, AZPE-05
- `determine-how-to-cache-data-effectively` → AZPE-10, AZPE-33
- `keep-the-cache-consistent-on-writes` → AZPE-04
- `cache-highly-dynamic-data` → ARCH (design advice, no pass/fail criterion)
- `manage-data-expiration-in-a-cache` → AZPE-02, AZPE-03
- `invalidate-data-in-a-client-side-cache` → AZPE-11
- `manage-concurrency-in-a-cache` → AZPE-08
- `implement-high-availability-and-scalability-and-improve-performance` → AZPE-05, AZPE-06, AZPE-09
- `caching-and-eventual-consistency` → AZPE-02
- `protect-cached-data` → AZPE-12 (authentication, TLS, isolation: SEC)
- `implement-caching-by-using-azure-managed-redis` → PARENT (TOOL)
- `connect-and-configure-client-applications` → AZPE-19
- `choose-a-net-client-library` → TOOL
- `implement-caching-patterns` → PARENT
- `implement-the-cache-aside-pattern` → AZPE-04 (localized from `pat-ca`; this is the product walkthrough)
- `perform-atomic-and-batch-operations` → AZPE-08, AZPE-09
- `perform-fire-and-forget-cache-operations` → TOOL
- `specify-automatically-expiring-keys` → TOOL (generic expiry rule is AZPE-02)
- `cross-correlate-cached-items` → TOOL
- `find-recently-accessed-items` → TOOL
- `implement-a-leaderboard` → TOOL
- `cache-session-state-and-html-output` → AZPE-47 (retired; review-twelve-factor TF-06)
- `aspnet-core` → AZPE-47 (retired; review-twelve-factor TF-06) (BG example; signals in `../languages/csharp.md`)
- `net-aspire-integration` → TOOL
- `high-availability-scalability-and-partitioning` → DR (cache HA, clustering: ARCH)
- `active-geo-replication` → DR
- `data-persistence` → DR
- `protect-cached-data-in-azure-managed-redis` → SEC
- `serialization-considerations` → ARCH (design advice, no pass/fail criterion)

**pat-ca** (6)
- `context-and-problem` → BG
- `solution` → AZPE-04
- `problems-and-considerations` → AZPE-02, AZPE-03, AZPE-07, AZPE-10, AZPE-12
- `when-to-use-this-pattern` → AZPE-12, AZPE-47
- `workload-design` → TRACE (pillar cross-references)
- `example` → BG (semantic caching for language models: too narrow for a check)
