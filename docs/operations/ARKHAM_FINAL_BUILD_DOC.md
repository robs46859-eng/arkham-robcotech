# Arkham Final Build Document

Generated: 2026-04-29

## Purpose

This document defines the final phased build path for Arkham.

It is intentionally phase-based and does not include a timeline.

Each phase ends with an explicit review and debug gate before the next phase begins.

## Global Rules

1. Azure is the only active production platform.
2. Orchestration is the execution authority for multi-step behavior.
3. Planning-only agents do not own execution.
4. Vertical services must consume the horizontal platform rather than recreate it.
5. Graphify is local navigation state, not a source of truth.

## Phase 0: Repository Truth Cleanup

### Goal

Remove or neutralize conflicting repo guidance before further build work.

### Required work

1. align authoritative docs to Azure-first operations
2. align domain references to `robcotech.pro` and `api.robcotech.pro`
3. mark legacy GCP, GCS, and Cloud Run material as deprecated
4. separate planning-only agent behavior from production execution behavior
5. confirm orchestration and maintenance directives are in place

### Exit criteria

- authoritative repo docs no longer present conflicting production stories
- planning-only agents are clearly labeled
- legacy GCP scaffolds are fenced off as non-authoritative

### Review and debug gate

Review:
- compare `README.md`, `ARCHITECTURE.md`, `DEPLOYMENT_PLAN.md`, and `FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md`
- confirm they all describe the same production model

Debug:
- search for production-facing references to GCS, GCP, Cloud Run, or old domains in authoritative docs
- resolve any remaining contradictions before continuing

## Phase 1: Platform Baseline

### Goal

Establish a trustworthy horizontal platform baseline.

### Required work

1. validate gateway startup and routing assumptions
2. validate orchestration service APIs, workers, queues, and checkpoints
3. validate memory service startup and retrieval paths
4. validate semantic-cache lookup, storage, and invalidation paths
5. validate billing startup and webhook-related dependencies
6. validate arkham security service health and event behavior

### Exit criteria

- platform services start reliably
- health and readiness endpoints are meaningful
- service-to-service dependencies are explicit
- core platform tests pass

### Review and debug gate

Review:
- inspect platform service configs and env ownership
- verify each platform service has a clear responsibility boundary

Debug:
- trace failures from gateway through orchestration, cache, memory, billing, and security
- fix platform instability before touching broader vertical work

## Phase 2: Orchestration Hardening

### Goal

Make orchestration the provable execution authority.

### Required work

1. validate workflow creation and state visibility
2. validate task dispatch and executor registration
3. validate retry behavior and failure handling
4. validate checkpoint persistence and resume behavior
5. validate worker drain and queue processing behavior
6. ensure new multi-step behavior routes through orchestration rather than vertical-local logic

### Exit criteria

- orchestration worker behavior is reliable
- executor registry is accurate
- checkpoint and retry semantics are test-backed
- cross-service workflow issues can be diagnosed from orchestration state

### Review and debug gate

Review:
- inspect `services/orchestration/app/main.py`
- inspect `services/orchestration/app/worker.py`
- inspect `services/orchestration/app/tasks/__init__.py`
- confirm ownership matches `ORCHESTRATION_DIRECTIVE.md`

Debug:
- reproduce stuck, duplicate, missing, or out-of-order work through orchestration tests and manual workflow probes
- no phase advancement until orchestration behavior is understandable and observable

## Phase 3: Media-Commerce Hardening

### Goal

Make `services/media-commerce` the first disciplined vertical.

### Required work

1. stabilize domain entities and input/output contracts
2. route execution through orchestration executors
3. keep cache behavior delegated to semantic-cache
4. keep memory behavior delegated to memory services where appropriate
5. keep security and audit behavior delegated to platform services
6. add or strengthen tests around vertical workflows and executor interaction

### Exit criteria

- media-commerce owns domain logic but not platform semantics
- media-commerce workflows complete through orchestration
- vertical boundaries are documented and testable

### Review and debug gate

Review:
- inspect `services/media-commerce/app/models/`
- inspect `services/media-commerce/app/agents/`
- inspect `services/orchestration/app/tasks/media_commerce.py`

Debug:
- trace a representative media-commerce workflow from request to result
- resolve any shadow retry, shadow queue, or local workflow behavior before continuing

## Phase 4: Runtime and Environment Integration

### Goal

Make the runtime environment coherent for local and production-style execution.

### Required work

1. validate local compose behavior
2. validate env var ownership per service
3. validate database and redis connectivity assumptions
4. validate secret boundaries and secret naming conventions
5. validate internal service URLs and public route splits

### Exit criteria

- local stack is parseable and bootable
- service env ownership is explicit
- data services connect reliably
- internal and public routing are not mixed accidentally

### Review and debug gate

Review:
- inspect `docker-compose.yml`
- inspect service env requirements and launch docs

Debug:
- run local startup and targeted service health checks
- fix env drift and connectivity drift before any deployment work

## Phase 5: Azure Deployment Path

### Goal

Finalize the active production deployment contract on Azure.

### Required work

1. confirm Azure resource model for backend services
2. confirm image build and registry path
3. confirm PostgreSQL and Redis provisioning path
4. confirm secret injection path
5. confirm API ingress path for `api.robcotech.pro`
6. confirm frontend host for `robcotech.pro`

### Exit criteria

- one Azure deployment story exists
- no authoritative docs point to an alternate active platform
- secrets and runtime dependencies are mappable to the chosen Azure environment

### Review and debug gate

Review:
- inspect deployment scripts and deployment docs together
- verify they describe the same service set and same public routing

Debug:
- resolve any mismatch between scripts, docs, and service assumptions
- do not proceed while two competing deployment stories remain active

## Phase 6: Billing and Public Integration

### Goal

Make public-facing and billing-critical behavior safe to expose.

### Required work

1. validate public API health
2. validate frontend to API interaction
3. validate auth flow assumptions
4. validate billing checkout and webhook behavior if enabled
5. validate public route and TLS assumptions

### Exit criteria

- public routes behave as intended
- billing integration is either validated or explicitly disabled
- public-facing failure modes are diagnosable

### Review and debug gate

Review:
- inspect billing service config and public routing docs
- confirm callback and webhook URLs align to the active domains

Debug:
- run end-to-end checks for public routes and billing flows
- fix public integration defects before moving to launch readiness

## Phase 7: Launch Readiness

### Goal

Confirm Arkham is operationally launchable under the Azure-first model.

### Required work

1. verify platform service health
2. verify orchestration behavior under representative flows
3. verify media-commerce workflow success
4. verify monitoring and logs are accessible
5. verify rollback guidance exists
6. verify docs reflect the actual system being launched

### Exit criteria

- operators can identify the authoritative launch path
- core workflows succeed
- rollback and debugging paths are documented
- no major repo-facing contradictions remain

### Review and debug gate

Review:
- compare launch docs, deployment docs, and maintenance docs
- ensure they all describe the same platform and same responsibilities

Debug:
- run a full smoke pass over platform, orchestration, and primary vertical behavior
- fix any discrepancy between docs and runtime before launch approval

## Phase 8: Post-Launch Stabilization

### Goal

Keep the system maintainable after first launch.

### Required work

1. monitor for drift between docs and runtime
2. monitor orchestration behavior and queue health
3. monitor semantic-cache and billing behavior
4. keep Graphify local and disposable
5. continue deleting or archiving legacy scaffolds that create confusion

### Exit criteria

- maintenance routines are repeatable
- the team can debug failures from the current docs and current code
- legacy artifacts no longer distort operator behavior

### Review and debug gate

Review:
- use `ARKHAM_MAINTENANCE_PLAN.md` as the operating checklist
- inspect whether new changes respect platform versus vertical boundaries

Debug:
- investigate failures through the documented maintenance lanes
- correct structural drift, not just surface symptoms

## Final Rule

Do not advance phases based on optimism.

Advance only when:

- the phase exit criteria are satisfied
- the review step confirms architectural alignment
- the debug step confirms the system is diagnosable

