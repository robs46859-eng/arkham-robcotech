# Horizontal Core Context

## Preserve These Services As Horizontal
- `services/gateway`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`
- `services/arkham`

## Preserve These Responsibilities As Horizontal
- inference provider routing
- policy enforcement framework
- workflow execution engine
- cross-run memory
- semantic caching
- usage metering and billing
- security and fraud controls

## Vertical Must Consume, Not Reimplement
- gateway calls for model work
- orchestration flows for multi-step execution
- shared `tasks` / `events` / `ledger` concepts
- billing by tenant, vertical, and agent

## Current Shared-Model Anchor
- `infra/docker/postgres/init-verticals.sql`
- `services/media-commerce/app/models/entities.py`

## Known Constraint
The vertical already has a 13-entity model and should continue using it as the contract instead of inventing vertical-only tables first.
