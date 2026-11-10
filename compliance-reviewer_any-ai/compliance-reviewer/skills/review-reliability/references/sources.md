# Sources — Reliability (localized)

Standards are localized in `references/standards/`. Do not fetch these sources during a review.

| Source | Pinned version | Retrieved | Elements | Local file |
|---|---|---|---|---|
| Azure Well-Architected Framework — Reliability (RE:05 redundancy, RE:06 scaling, RE:07 self-preservation, RE:03 mitigation, design principles) and Azure Architecture Center — Transient fault handling and Background jobs best practices; Retry, Circuit Breaker, Bulkhead, Throttling, Rate Limiting, Queue-Based Load Leveling, Competing Consumers, Idempotent Consumer and Compensating Transaction patterns; Retry Storm antipattern (learn.microsoft.com) | 18 pages (17 content + 1 traceability); `ms.date`, "Last updated" and git commit per page in the file header | 2026-11-08 | 52 / 100 | standards/azure-reliability-resiliency.md |

`languages/*.md` and `reliability-config-signals.md` are local lookup tables of library and configuration signals, not sources; never cite them.

Element levels never change severity: each Finding takes the check's default (see SKILL.md step 11).
