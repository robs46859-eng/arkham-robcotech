# FullStackArkham Vertical Build Coordination

## Objective
Build the `media-commerce` vertical on top of the FullStackArkham horizontal core without duplicating platform responsibilities.

## Horizontal Core To Preserve
- `services/gateway`: inference, model routing, policy entrypoint
- `services/orchestration`: workflow execution and task runners
- `services/memory`: historical context and notes
- `services/semantic-cache`: repeat request caching
- `services/billing`: usage metering by tenant, vertical, and agent
- `services/arkham`: security, fraud, abuse controls

## Vertical Boundary
Vertical-specific work belongs under:
- `services/media-commerce/app/agents`
- `services/media-commerce/app/main.py`
- `services/media-commerce/app/models`
- `services/media-commerce/tests`

The vertical should consume the horizontal core, not reimplement it.

## Working Lanes
### Lane A: Horizontal Integration
- Ownership: read-only analysis
- Focus: integration points, workflow seams, schema fit, minimum viable vertical slice

### Lane B: Vertical Runtime
- Ownership: `services/media-commerce/app/agents`, `services/media-commerce/app/main.py`, `services/media-commerce/tests`
- Focus: replace one placeholder path with a real end-to-end implementation and tests

### Lane C: Local/Deploy Repair
- Ownership: `docker-compose.yml`, `scripts/deploy-bot.sh`, deployment docs as needed
- Focus: fix compose blocker, improve deploy-bot failure clarity, keep runtime path truthful

## Current Known Truths
- `.agents/skills` exists with 8 top-level vertical agent skill wrappers
- `marketingskills/skills` contains 40 imported marketing skills
- `services/media-commerce/app/skills` contains copied skill folders
- `services/media-commerce/app/agents` exists but most agent methods are still placeholders
- `services/mcp_server.py` exposes agent tools but still returns mock execution
- `docker-compose.yml` has a malformed `media-commerce` entry under `networks`
- `scripts/deploy-bot.sh --setup` fails on Azure DNS/auth resolution, not on Docker Compose

## Build Rule
Prioritize one real vertical slice over broad placeholder completion.

Recommended first slice:
- `DealFlow.route_lead` or `ContentEngine.create_content_strategy`
- backed by shared models and horizontal workflows
- with tests
- with audit/event/task hooks where practical
