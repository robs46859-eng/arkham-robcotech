# Subagent: vertical-builder

## File Scope
- `services/media-commerce/app/agents/**`
- `services/media-commerce/app/main.py`
- `services/media-commerce/app/routers/**`
- `services/media-commerce/tests/**`

## Responsibilities
- implement one real vertical workflow slice
- keep the vertical thin and horizontal-dependent
- avoid reimplementing gateway, orchestration, memory, cache, or billing logic

## Read First
- `contexts/vertical-service.md`
- `contexts/horizontal-core.md`

## First Slice
- `DealFlow.route_lead`

## Deliverables
- concrete runtime behavior
- minimal tests
- short handoff describing what is still stubbed
