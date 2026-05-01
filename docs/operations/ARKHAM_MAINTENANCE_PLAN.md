# Arkham Maintenance Plan

Generated: 2026-04-29

## Purpose

This document defines the day-to-day maintenance model for the Arkham project.

It assumes:

- Azure is the authoritative production platform
- horizontal services under `services/` are the core operating surface
- `services/media-commerce` is the first real vertical to harden
- agent packages are planning-only and do not directly execute production changes
- `graphify-out/` is a local navigation artifact for each operator or agent

## Operating Model

Arkham should be maintained through four standing lanes:

1. Platform lane
2. Vertical lane
3. Planning lane
4. Documentation and drift lane

Each change should clearly belong to one lane. If a change spans multiple lanes, split the work and document the boundary.

## Lane 1: Platform

Platform is the primary maintenance surface.

The backbone services are:

- `services/gateway`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`
- `services/arkham`

These services own:

- ingress and routing
- workflow execution
- durable state and checkpoints
- memory and retrieval
- caching and invalidation
- billing and monetization correctness
- security analysis, fingerprinting, and audit behavior

### Daily checks

Every maintenance cycle should verify:

1. gateway health, readiness, and upstream service connectivity
2. orchestration queue depth, worker state, checkpoint behavior, and retry behavior
3. semantic-cache health, hit behavior, and invalidation paths
4. memory service availability and retrieval correctness
5. billing service health and Stripe-facing error conditions
6. arkham security service health, event throughput, and fingerprint/audit integrity

### Rules

- No vertical service may reimplement auth, queueing, cache invalidation, retry semantics, or memory persistence.
- Platform fixes take priority over vertical feature expansion.
- Health endpoints and readiness behavior must stay accurate enough for operational automation.

## Lane 2: Vertical

The first hardening vertical is:

- `services/media-commerce`

This service should remain thin with respect to platform concerns.

### Vertical ownership

`services/media-commerce` should own:

- domain entities
- domain-specific business rules
- vertical-facing API behavior
- vertical-specific prompt or agent logic

It should not own:

- workflow engine semantics
- queue implementations
- tenant auth
- cache infrastructure
- shared memory persistence
- security classification
- deployment execution

### Daily review focus

For changes in `services/media-commerce`, verify:

1. workflow execution still routes through orchestration
2. state transitions stay explicit and testable
3. cache use is delegated to semantic-cache rather than improvised locally
4. memory-related state is delegated to the memory service where appropriate
5. vertical models remain stable and do not leak platform responsibilities

## Lane 3: Planning

The planning-only agent packages are:

- `launch-agent`
- `finisher-agent`
- `azure-runner-agent`
- `omni-deployer`

These packages are planning and coordination tools only.

### Rules

- They may inspect repository state.
- They may generate plans, commands, checklists, and review outputs.
- They may recruit or structure subagent work.
- They must not be treated as the system of record for deployment execution.
- They must not become the source of truth for architecture or runtime state.

### Required behavior

- Any mutating command must remain approval-gated.
- Readmes and future docs should clearly state `planning-only`.
- Production execution should happen through approved human workflows, CI, or explicitly authorized operational procedures.

## Lane 4: Documentation and Drift

Arkham recently switched from GCS/GCP-oriented assumptions to Azure as the production authority.

That makes documentation drift a real maintenance risk.

### Highest-priority drift targets

- `README.md`
- `ARCHITECTURE.md`
- `DEPLOYMENT_PLAN.md`
- `FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md`
- `LAUNCH_LIST.md`
- `LAUNCH_STATUS.md`
- `LAUNCH_TODAY.md`

### Required cleanup direction

These should converge toward:

- `docs/architecture/current.md`
- `docs/deployment/azure.md`
- `docs/launch/current.md`
- `docs/launch/history/`

Until then, maintainers should treat conflicting deployment guidance as a defect to be resolved, not merely noted.

## Daily Maintenance Routine

## Morning pass

1. Check platform service health and readiness.
2. Review orchestration worker and queue status.
3. Review recent billing and security failures.
4. Review deployment or environment drift from Azure-first assumptions.

## During feature work

1. Classify the change as platform or vertical before implementation.
2. If the change touches workflow semantics, inspect orchestration first.
3. If the change affects repeated inference behavior, inspect semantic-cache first.
4. If the change affects tenant state, audit ownership across gateway, memory, billing, and arkham security surfaces.

## End-of-day pass

1. Update one authoritative project status path.
2. Record unresolved drift or cross-lane issues.
3. Refresh local graph navigation only if the changed scope is materially different.

## Weekly Maintenance Routine

1. Review orchestration task and executor coverage.
2. Review `services/media-commerce` for boundary creep.
3. Review Azure-specific deployment assumptions for doc and script drift.
4. Review planning agents for prompt or instruction drift.
5. Regenerate local Graphify context only for the active operator's needs.

## Graphify Policy

`graphify-out/` is a local navigation artifact.

It is useful for:

- repo orientation
- operator onboarding
- local impact analysis
- agent navigation

It is not the source of truth for:

- architecture decisions
- deployment state
- production runtime topology

### Rules

- Each operator or agent may regenerate local graph output as needed.
- Graph reports should not replace authoritative docs.
- If Graphify highlights a contradiction, the fix belongs in the repo docs or code, not in the graph artifact.

## Suggested Structural Improvements

1. Move planning agents under a unified `agents/` namespace.
2. Collapse deployment docs into Azure-first canonical paths.
3. Add a short `WORKSPACE_MAP.md` explaining authoritative docs and service ownership.
4. Keep `services/media-commerce` thin and orchestration-driven.
5. Treat orchestration as the central maintenance surface for execution correctness.

## Conclusion

Arkham should be maintained as an Azure-first platform repo whose center of gravity is:

- `services/orchestration`
- `services/gateway`
- `services/semantic-cache`
- `services/memory`
- `services/billing`
- `services/arkham`

The vertical path should harden through `services/media-commerce`, but only as a disciplined consumer of the horizontal platform.

