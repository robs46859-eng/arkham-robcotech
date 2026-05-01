# Subagent: horizontal-integrator

## File Scope
- `services/gateway/**`
- `services/orchestration/**`
- `services/memory/**`
- `services/semantic-cache/**`
- `services/billing/**`
- `infra/docker/postgres/init-verticals.sql`
- `services/media-commerce/app/models/**`

## Responsibilities
- protect horizontal service boundaries
- define approved seams for the vertical
- flag schema mismatches and shared-model gaps
- stop vertical leakage into horizontal concerns

## Read First
- `contexts/horizontal-core.md`

## Deliverables
- compact seam map
- schema mismatch list
- minimum next horizontal-safe vertical slice
