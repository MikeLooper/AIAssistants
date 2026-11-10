# Azure Architecture Center: architecture styles and "Design for change" — localized summary

- Source site: learn.microsoft.com · Repo `MicrosoftDocs/architecture-center` (locale-less URLs) · pins per page below
- Citation base: https://learn.microsoft.com/azure/architecture/guide/
- Localized: 2026-11-09 · Elements: 20 (learn.microsoft.com budget shared with `microsoft-csharp.md`: 44 of 100)
- Source name for `Finding.standard`: Azure Architecture Center
- Level: informational only; severity is the owning check's default.
- The N-tier layer rules sit in the page introduction, which has no anchor: those rows cite `nt` without a fragment.

| Key | Page path | Pin |
|-----|-----------|-----|
| as | `architecture-styles/` | ms.date 2025-09-25; commit d1d0ebff1b2a |
| nt | `architecture-styles/n-tier` | ms.date 2025-08-15; commit 03e41c0834ab |
| wqw | `architecture-styles/web-queue-worker` | ms.date 2026-01-06; commit c32bf659d950 |
| ms | `architecture-styles/microservices` | ms.date 2025-06-30; commit f69851e7c8b2 |
| dfe | `design-principles/design-for-evolution` | ms.date 2018-08-30; commit f440454b6512 |

| ID | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-----------------------|--------------|-------|-----------|
| AAS-01 | Each layer has one responsibility. A higher layer may use a lower layer, but a lower layer never uses a higher one. | layered code | AP-03 | nt |
| AAS-02 | In a closed-layer design a layer calls only the next layer down. Skipping layers (open layers) is a deliberate, documented choice because it adds coupling. | layered code | AP-01 | nt |
| AAS-03 | The data tier is accessed only from the middle (business) tier. | layered code | AP-01 | nt#best-practices |
| AAS-04 | A middle tier that only passes CRUD calls through adds latency and complexity without value. | layered code | DP-04 | nt#challenges |
| AAS-05 | A chosen architecture style constrains which elements exist and how they may relate. Code that only superficially conforms loses the style's benefits. | ≥ 2 deployable units | AP-07 | as#architecture-styles-as-constraints |
| AAS-06 | Architectural complexity matches the domain. Too little structure produces a "big ball of mud" with unmanaged dependencies. | ≥ 2 modules | AP-04 | as#consider-challenges-and-benefits |
| AAS-07 | Each service implements a single business capability within a bounded context, and services aren't overly granular. | microservices | AP-07 | ms#best-practices, as#architecture-styles-as-constraints |
| AAS-08 | Data is private to the owning service: no shared database schemas or direct access to another service's store. | microservices | AP-07 | ms#best-practices |
| AAS-09 | Services don't share common domain libraries or code that couples their release cycles. | microservices | AP-07 | ms#antipatterns-for-microservices |
| AAS-10 | Gateways handle routing and infrastructure only. They contain no domain knowledge or business rules. | gateway/BFF code in scope | AP-02 | ms#best-practices, dfe#recommendations |
| AAS-11 | Database entities aren't used as events or API payloads. Contracts model the domain, not the internal implementation. | ≥ 2 deployable units | AP-07 | ms#antipatterns-for-microservices, ms#best-practices |
| AAS-12 | Security logic such as token validation isn't embedded in each service's business code. It's offloaded to a dedicated component, gateway or middleware. | ≥ 2 handlers or services | AP-06 | ms#antipatterns-for-microservices |
| AAS-13 | Cross-cutting concerns are offloaded to a separate component (gateway, sidecar, shared middleware) so they evolve without touching every consumer. | ≥ 2 handlers or services | AP-06 | dfe#recommendations, ms#best-practices |
| AAS-14 | Common infrastructure tasks are abstracted (framework or library) instead of repeated as error-prone code in each service. | ≥ 2 handlers or services | AP-06 | ms#antipatterns-for-microservices |
| AAS-15 | Web front end and worker communicate through the queue. Shared data schemas or code modules between them create hidden dependencies. | web + worker in scope | AP-07 | wqw#challenges |
| AAS-16 | The front end and worker don't grow into large monolithic components. | web + worker in scope | AP-04 | wqw#challenges |
| AAS-17 | High cohesion and loose coupling: functionality that changes together lives together, and needing coordinated updates across modules shows low cohesion. | ≥ 2 modules | AP-04 | dfe#recommendations, ms#best-practices |
| AAS-18 | Domain knowledge is encapsulated in the module or service that owns it. Clients don't each enforce the business rules. | layered code | AP-02 | dfe#recommendations |
| AAS-19 | Infrastructure (messaging, persistence) is abstracted away from domain logic. | layered code | AP-02 | dfe#recommendations |
| AAS-20 | Overly chatty communication between two modules or services signals tight coupling and low cohesion. (The latency impact is performance's concern.) | ≥ 2 modules | AP-04 | ms#best-practices |
