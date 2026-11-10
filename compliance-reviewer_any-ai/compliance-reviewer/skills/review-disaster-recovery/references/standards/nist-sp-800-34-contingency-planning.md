# NIST SP 800-34 Rev. 1 — Contingency Planning Guide — localized summary

- Source site: nvlpubs.nist.gov (PDF) / csrc.nist.gov (publication record)
- Pinned version: SP 800-34 Rev. 1, *Contingency Planning Guide for Federal Information Systems*, May 2010 (updated 11/11/2010); PDF 150 pages. CSRC record lists no newer revision and no withdrawal as of 2026-11-08.
- Citation base: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
- Localized: 2026-11-08 · Elements: 25 (cap 100)
- Source name for `Finding.standard`: `NIST SP 800-34 Rev. 1`
- Level: the source's own keyword (`SHOULD`, `MUST`) where the summarized sentence has one, otherwise `REVIEW`. The level never changes severity; each Finding takes the owning check's default.
- Terminology mapping: "offsite / alternate site / alternate facility" = a separate region or failure domain; "backup media" = backup copies; "ISCP" = the DR plan.
- Section: primary section first; put it in `Finding.notes` when citing.
- PDF page: the physical page in the PDF (printed page + 14 for chapters 1–5). Citation URL: citation base + `#page=` + PDF page.

| ID | Level | Requirement (summary) | Applies when | Check | Section | PDF page |
|----|-------|-----------------------|--------------|-------|---------|----------|
| SP34-01 | SHOULD | Back up system data regularly; the backup policy sets minimum frequency and scope (full, incremental, differential) from data criticality and rate of change. | stateful store | DR-01 | §3.4.2, §5.1.2 | 35 |
| SP34-02 | SHOULD | The backup policy states retention period, storage location, retrieval time and who may restore. | backup config/docs | DR-01 | §5.1.2 | 59 |
| SP34-03 | SHOULD | Backups are tested regularly to confirm data can be retrieved without errors or loss, including at the alternate location. | stateful store | DR-02 | §3.4.2 (fn. 25), §5.1.5 | 35 |
| SP34-04 | REVIEW | After recovery, data is validated as complete and current to the last backup, and functionality is validated before normal operations resume. | runbook/restore docs | DR-02 | §4.4 | 55 |
| SP34-05 | SHOULD | MTD, RTO and RPO are determined from a business impact analysis with process owners. | always | DR-03 | §3.2, §3.2.1 | 29 |
| SP34-06 | MUST | RTO is shorter than MTD (reprocessing time must fit inside MTD). | MTD and RTO documented | DR-03 | §3.2.1 | 31 |
| SP34-07 | SHOULD | System resources, components and interdependencies are inventoried, and a recovery-priority hierarchy is set. | always | DR-03 | §3.2.2, §3.2.3 | 33 |
| SP34-08 | REVIEW | The plan's scope states the impact level, RTOs, alternate-site and data-storage capabilities, and its assumptions. | plan exists | DR-03 | §4.1 | 49 |
| SP34-09 | REVIEW | Backup/recovery strategy matches availability impact: low → backup + cold site; moderate → replication + cold/warm site; high → mirroring/replication + hot site. | stated impact/tier | DR-04 | §3.4.1 (Table 3-2) | 34 |
| SP34-10 | SHOULD | Moderate- and high-impact systems have a strategy to run at an alternate facility (region) for an extended period. | stated impact/tier | DR-04 | §3.4.3 | 36 |
| SP34-11 | SHOULD | The alternate-site type (cold, warm, hot) follows MTD and BIA results and may differ per function. | stated impact/tier | DR-04 | §5.1.5 | 62 |
| SP34-12 | REVIEW | The plan is organized in three phases: activation and notification, recovery, reconstitution. | plan exists | DR-05 | Ch. 4 intro, §4.1 | 48 |
| SP34-13 | REVIEW | Activation criteria and notification procedures (who, how, in what order) are documented. | plan exists | DR-05 | §4.2.1, §4.2.2 | 50 |
| SP34-14 | SHOULD | Recovery procedures are stepwise, sequenced by BIA priority, and include escalation and cross-team coordination steps. | plan exists | DR-05 | §4.3.1, §4.3.2 | 53 |
| SP34-15 | SHOULD | Contingency roles and teams are designated, with responsibilities per phase. | plan exists | DR-05 | §4.1 | 49 |
| SP34-16 | SHOULD | Reconstitution ends with a full backup of the recovered system and documented events (actions taken, problems, lessons learned). | plan exists | DR-05 | §4.4 | 56 |
| SP34-17 | SHOULD | Copies of the plan are stored at the alternate location and with the backups; distribution is controlled. | plan exists | DR-05 | §3.6 | 46 |
| SP34-18 | SHOULD | Backups are encrypted, and keys are managed and stored separately from, but accessible to, the backups. | backup config | DR-06 | §5.1.2 | 58 |
| SP34-19 | SHOULD | Backup storage is geographically separate (unlikely to share the same disaster), retrievable within the needed time, and secured to the data's requirements. | backup config | DR-06 | §3.4.2, §5.1.5 | 35 |
| SP34-20 | SHOULD | System software, images, configuration and licence information needed to rebuild are backed up or stored at the alternate location. | IaC/images | DR-07 | §5.1.3 | 60 |
| SP34-21 | REVIEW | Redundancy and failover (high-availability) processes are used where uptime requirements justify them. | stated tier | DR-08 | §5.1.6 | 62 |
| SP34-22 | SHOULD | Plan tests and exercises run periodically and after significant changes, using a test plan with objectives, success criteria and scenario, covering notification, recovery from backup, connectivity, performance on alternate resources and return to normal. | plan exists | DR-09 | §3.5, §3.5.1 | 41 |
| SP34-23 | SHOULD | Exercise depth follows impact: low → tabletop; moderate → functional exercise including restore from backup; high → full-scale exercise including failover to the alternate site and reconstitution. | stated impact/tier | DR-09 | §3.5.4 | 44 |
| SP34-24 | REVIEW | Each test or exercise produces an after-action report, and lessons learned update the plan. | test records | DR-09 | §3.5 | 41 |
| SP34-25 | SHOULD | The plan is reviewed at a defined frequency and after significant changes, with a record of changes. | plan exists | DR-09 | §3.6 | 45 |
