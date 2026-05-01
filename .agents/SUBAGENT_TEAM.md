# FullStackArkham Subagent Team

## Objective
Build the vertical layer on top of the FullStackArkham horizontal core without duplicating core responsibilities, while keeping each worker's context window as small as possible.

## Active Build Pattern
Horizontal core stays authoritative:

- `services/gateway`
- `services/arkham`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`

Vertical implementation lives primarily in:

- `services/media-commerce`
- `apps/web/src/app/dashboard`
- vertical-specific schema and routing surfaces only where needed

## Shared Context Pack
Every worker should start with only these files unless blocked:

1. `docs/13_ENTITY_VERTICAL_BUILD_PLAN.md`
2. `services/media-commerce/app/models/entities.py`
3. `services/media-commerce/app/main.py`
4. `.agents/SUBAGENT_TEAM.md`

Optional only when relevant:

- `services/mcp_server.py`
- `docker-compose.yml`
- `scripts/deploy-bot.sh`
- `infra/docker/postgres/init-verticals.sql`

## Team Roles
### Architect A
Scope:

- `services/gateway`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`
- `infra/docker/postgres/init-verticals.sql`

Deliverables:

- horizontal integration seams to preserve
- recommended workflow entrypoints
- schema mismatches and core contracts
- minimum next implementation slice

Rules:

- read-only unless explicitly reassigned
- no vertical feature work inside agent files

### Builder B
Scope:

- `services/media-commerce/app/agents`
- `services/media-commerce/app/main.py`
- `services/media-commerce/tests`

Deliverables:

- first real end-to-end vertical slice
- tests for that slice
- no horizontal duplication

Rules:

- prefer one useful workflow over broad placeholder coverage
- call horizontal services or data contracts rather than inventing local substitutes

### Runtime C
Scope:

- `docker-compose.yml`
- `scripts/deploy-bot.sh`
- deployment docs if needed
- runtime wiring needed only to get the vertical running

Deliverables:

- local compose repair
- clearer deploy-bot failure modes
- minimum runtime changes needed for local validation

Rules:

- do not redesign cloud architecture
- do not touch agent business logic

### Coordinator
Scope:

- repo-wide synthesis
- decision log
- handoff compression

Deliverables:

- merge decisions
- next-step ordering
- conflict resolution between lanes

## Context Compression Rules
- Handoffs must be 15 lines or fewer.
- Do not paste whole files into handoffs.
- Report only:
  - changed files
  - exact behavior added or fixed
  - blockers
  - next dependency on another lane
- If a worker needs broader repo context, request one file path or one question, not a full repo reload.

## Ownership Rules
- One worker owns one write scope.
- Never revert another lane’s changes unless explicitly coordinated.
- If a change crosses scopes, stop and hand off rather than editing broadly.

## Recommended Build Order
1. Runtime C fixes compose and local blockers.
2. Architect A confirms horizontal seams and contracts.
3. Builder B implements one real vertical slice against those seams.
4. Coordinator merges findings into the next slice plan.
