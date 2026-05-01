---
name: vertical-automation-hierarchy
description: Use when a higher-level model needs a control hierarchy to build an entire Arkham vertical, create the needed automations, call the right agents in the right order, and plug the vertical into the defined horizontal platform without blurring ownership boundaries.
---

# Vertical Automation Hierarchy

Use this skill as the control specification for building a full vertical on top of the Arkham horizontal platform.

Do not treat the vertical as a new platform.
Keep horizontal and vertical ownership explicit at all times.

## Horizontal Boundary

The horizontal platform remains authoritative for:
- ingress and API mediation: `services/gateway`
- workflow lifecycle, queues, checkpoints, retries, worker control: `services/orchestration`
- durable memory and retrieval: `services/memory`
- repeated inference cache: `services/semantic-cache`
- billing and monetization correctness: `services/billing`
- security classification, deception, audit behavior: `services/arkham`

The vertical may consume these services.
It must not recreate them.

## Vertical Boundary

The vertical owns:
- domain entities and schemas
- domain APIs
- domain automations and policies
- task payload construction
- skill selection for domain work
- interpretation of workflow outputs

The vertical does not own:
- generic workflow execution
- checkpointing
- retry engines
- queue implementations
- generic auth
- generic billing
- platform cache or memory internals

## Hierarchy

1. Vertical Director
The higher-level model uses this node as the top controller.
Responsibilities:
- define the vertical scope
- keep horizontal and vertical boundaries intact
- sequence the build phases
- call the narrow execution agents below
- stop boundary creep early

2. Horizontal Contract Agent
Use when the vertical must plug into existing platform surfaces.
Responsibilities:
- map the vertical to gateway, orchestration, memory, semantic-cache, billing, and arkham
- define service contracts and dependency URLs
- ensure the vertical routes execution through orchestration executors

3. Domain Model Agent
Responsibilities:
- define tenant-scoped entities
- extend SQL bootstrap safely
- add vertical tables, indexes, views, and seed policies
- preserve idempotency and resume behavior

4. Workflow and Automation Agent
Responsibilities:
- turn domain behaviors into orchestration-driven workflows
- define tasks, policies, trigger conditions, and approval gates
- register domain execution through orchestration-owned seams

5. Vertical Capability Agent
Responsibilities:
- define the domain agents used inside the vertical
- map business capabilities to the right agent modules and skills
- keep agent boundaries coherent

6. Runtime Integration Agent
Responsibilities:
- wire env vars, secrets, and inter-service URLs
- update deploy/build surfaces only as required by the new vertical
- preserve ACA, ACR, PostgreSQL, and Key Vault assumptions

7. Validation Agent
Responsibilities:
- verify schema bootstrap
- verify workflow execution
- verify service health and dependency wiring
- verify domain outcomes and approval gates

## Default Domain-Agent Stack

When building a commercial/operational vertical similar to `media-commerce`, prefer this stack:
- `deal-flow` for lead-to-revenue and routing logic
- `content-engine` for content/programmatic generation
- `fulfillment-ops` for delivery, CRO, and execution follow-through
- `compliance-gate` for policy/compliance workflows
- `budget-mind` for spend, unit economics, and margin policies
- `board-ready` for executive and investor reporting outputs
- `chief-pulse` for cross-agent synthesis and escalation

Only keep agents that match the vertical.
Do not force all of them into every vertical.

## Build Phases

1. Scope
- define the vertical objective
- define domain entities
- define what remains horizontal

2. Contract
- define integration points with gateway, orchestration, memory, cache, billing, security
- define required URLs, secrets, and auth assumptions

3. Data
- add or extend bootstrap SQL
- add resume SQL if replay can fail after partial first-run
- define seed policies carefully

4. Automation
- define workflow triggers
- define orchestration task seams
- define approval-gated vs autonomous actions

5. Agent Layer
- add or update vertical agent modules
- map each agent to its domain skills

6. Runtime
- update deploy/build/env wiring
- ensure ACA and SQL initialization still validate

7. Validation
- run targeted checks first
- then run full vertical smoke tests

## Required Routing

Use these existing skills when the phase matches:
- `arkham-azure-ops-router` for Azure operational routing
- `azure-aca-build-update` for build/deploy changes
- `azure-postgres-bootstrap-repair` for SQL/bootstrap failures
- `azure-aca-deploy-debug` for deploy triage
- `azure-aca-custom-domain-cutover` for DNS/TLS cutover

## Assets

Read when needed:
- `assets/media-commerce-hierarchy.yaml`
- `assets/staffing-operations-hierarchy.yaml`
- `assets/vertical-template.yaml`
- `references/architecture.md`
- `references/graphify.md`
