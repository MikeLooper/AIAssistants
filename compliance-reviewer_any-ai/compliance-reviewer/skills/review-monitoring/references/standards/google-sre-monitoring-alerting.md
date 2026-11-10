# Google SRE — Monitoring and alerting — localized summary

- Source site: sre.google (*Site Reliability Engineering*, 2016; *The Site Reliability Workbook*, 2018)
- Pinned pages: see the page table below (chapter + edition; the pages carry no modification date)
- Citation base: https://sre.google/
- Licence: CC BY-NC-ND 4.0. Rows are summaries in our own words; no tables or passages are copied.
- Localized: 2026-11-08 · Elements: 28 (cap 100)
- Source name for `Finding.standard`: `Google SRE`
- Level: `SHOULD` where the summarized sentence says "should" or "(strongly) recommend/advise", otherwise `REVIEW`. The level never changes severity; severity is the owning check's default.
- Anchor(s): `<page key>#<section anchor>`, primary first. Some anchors carry generated suffixes (e.g. `-g0sEi4`); use them exactly as written.
- Citation URL: citation base + page path + `#` + primary anchor.

| Key | Page path | Book / chapter |
|-----|-----------|----------------|
| mds | sre-book/monitoring-distributed-systems/ | *Site Reliability Engineering* (2016), ch. 6 |
| pa | sre-book/practical-alerting/ | *Site Reliability Engineering* (2016), ch. 10 |
| wb-mon | workbook/monitoring/ | *The Site Reliability Workbook* (2018), ch. 4 |
| wb-slo | workbook/alerting-on-slos/ | *The Site Reliability Workbook* (2018), ch. 5 |

## MON-01 — Alert coverage of key failure conditions

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| SREM-01 | REVIEW | User-facing services are alerted on the four golden signals: latency, traffic, errors, saturation (saturation when *nearly* problematic). | user-facing service | mds#xref_monitoring_golden-signals |
| SREM-02 | REVIEW | Errors include implicit failures (wrong content) and policy failures (too slow); latency of failed requests is tracked separately from successful ones. | user-facing service | mds#errors, mds#latency |
| SREM-03 | REVIEW | Resources with hard limits, or whose use degrades performance past a threshold, have approaching-exhaustion alerts, including predictive ones (e.g. disk full in N hours). | compute/data resources | wb-mon#saturation, mds#saturation |
| SREM-04 | REVIEW | Sudden, severe changes in user request rate are detected by a simple rule. | user-facing service | mds#setting-reasonable-expectations-for-monitoring-o8svcM |
| SREM-05 | SHOULD | Responses from direct dependencies are monitored (latency, response codes, sizes), ideally once in the shared client library. | dependencies | wb-mon#dependencies |

## MON-02 — Alerts and dashboards are defined as code

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| SREM-06 | SHOULD | Monitoring configuration is code in version control with review; intent-based config is preferred over UI- or CRUD-only setup. | always (IaC present) | wb-mon#treat-your-configuration-as-code |
| SREM-07 | REVIEW | Rules are templated and reused across targets instead of copy-pasted, and every service gets a consistent baseline of metrics and dashboards. | monitoring-as-code present | pa#maintaining-the-configuration, wb-mon#encourage-consistency |
| SREM-08 | SHOULD | Alerting logic is tested: config linting, rule unit tests with synthetic series (e.g. `promtool test rules`) and routing tests, preferably in CI. | monitoring-as-code present | wb-mon#testing-alerting-logic, pa#maintaining-the-configuration |
| SREM-09 | SHOULD | Alerting parameters (windows, burn rates) are shared across services or request-class buckets, not hand-tuned per service. | several services alerted | wb-slo#alerting_at_scale |

## MON-03 — Alert quality and actionability

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| SREM-10 | REVIEW | Paging alerts target symptoms (user-visible impact); cause-based alerts are kept for definite, imminent problems. | alert rules present | mds#symptoms-versus-causes-g0sEi4, mds#tying-these-principles-together-nqsJfw, mds#conclusion-8ksvFj |
| SREM-11 | SHOULD | Every page is urgent and actionable; conditions with a rote, scriptable response are automated rather than paged. | alert rules present | mds#tying-these-principles-together-nqsJfw, mds#gmail-predictable-scriptable-responses-from-humans-BVs1h4SD |
| SREM-12 | REVIEW | Threshold alerts tolerate flapping with a minimum pending duration (≥ 2 evaluation cycles); SLO alerts use windowed burn rates instead of long durations. | alert rules present | pa#alerting, wb-slo#3-incrementing-alert-duration |
| SREM-13 | SHOULD | When an SLO is stated, alerts use multiwindow, multi-burn-rate rules. Starting point for 99.9 %: page at 2 % of budget in 1 h (5 m short window) or 5 % in 6 h (30 m); ticket at 10 % in 3 d (6 h). | stated SLO | wb-slo#6-multiwindow-multi-burn-rate-alerts, wb-slo#5-multiple-burn-rate-alerts |
| SREM-14 | REVIEW | Alert design balances precision, recall, detection time and reset time; low-traffic services use synthetic traffic, grouping or longer windows instead of paging on single failures. | stated SLO or low-traffic service | wb-slo#alerting-considerations, wb-slo#low-traffic-services-and-error-budget-alerting |
| SREM-15 | REVIEW | Alerting metrics are counters or ratios that move sharply only in problem states; latency uses histograms/percentiles, not means. | alert rules present | wb-mon#implementing-purposeful-metrics, wb-mon#calculations, mds#worrying-about-your-tail-or-instrumentation-and-performance-Yms9Ck |
| SREM-16 | REVIEW | Alert notifications carry context (rule, scope, triggering value) and link to a dashboard, runbook or ready-made query. | alert rules present | pa#alerting, wb-mon#intended-changes, wb-mon#keep-logs-as-the-data-source |
| SREM-17 | SHOULD | Paging rules are simple, predictable and represent a clear failure; complex dependency-hierarchy rules are avoided. | alert rules present | mds#as-simple-as-possible-no-simpler-lqskHx, mds#setting-reasonable-expectations-for-monitoring-o8svcM |

## MON-04 — Alert routing and ownership

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| SREM-18 | SHOULD | A severity label routes each alert: pages to on-call, subcritical alerts to a ticket queue, the rest to dashboards only. Email-only alerting is avoided. | alert rules present | pa#alerting, wb-mon#alerts, mds#conclusion-8ksvFj |
| SREM-19 | REVIEW | Routing de-duplicates and groups alerts and inhibits dependent ones (per-node vs global; downstream vs failing dependency), and inhibition ends when the event ends. | alert routing config present | wb-mon#alerts, pa#alerting |
| SREM-20 | REVIEW | Pages go to an on-call rotation, and one issue doesn't page several teams. | alert routing config present | mds#tying-these-principles-together-nqsJfw |

## MON-05 — Dashboards present actionable health

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| SREM-21 | SHOULD | Service dashboards show the four golden signals, with SLI metrics prominent on the landing view. | dashboards present | mds#building-dashboards, wb-mon#metrics-with-purpose |
| SREM-22 | SHOULD | Dashboards surface production changes (build or config version, deploy time) so they can be correlated with incidents. | dashboards present | wb-mon#intended-changes |
| SREM-23 | REVIEW | Served traffic can be broken down by status code, including quota or rate-limit rejections. | dashboards present | wb-mon#status-of-served-traffic |
| SREM-24 | REVIEW | Dashboards use fitting chart types (histograms/heatmaps for latency), a consistent layout across sets, and label-based drill-down. | dashboards present | wb-mon#interfaces |

## MON-06 — Telemetry reaches monitoring from all layers

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| SREM-25 | REVIEW | Black-box probes check user-visible behaviour, including response content, both at the front door and behind the load balancer, to localize failures. | user-facing endpoint | pa#black-box-monitoring, mds#black-box-versus-white-box-q8sJuw |
| SREM-26 | REVIEW | Summary metrics are kept for months, for trend and capacity analysis. Sufficiency only: never fail for keeping more. | telemetry store in IaC | wb-mon#calculations |
| SREM-27 | REVIEW | Collection and rule-evaluation intervals keep alerting data fresh (no more than about 4–5 minutes stale) without needless fine resolution. | scrape/evaluation intervals in config | wb-mon#speed, mds#choosing-an-appropriate-resolution-for-measurements-vJsBsE |
| SREM-28 | SHOULD | A self-hosted monitoring stack separates collection, storage, alerting and dashboards behind stable interfaces, and is run like a production service. | self-hosted monitoring stack in IaC | wb-mon#prefer-loose-coupling, wb-mon#managing_your_monitoring_system |
