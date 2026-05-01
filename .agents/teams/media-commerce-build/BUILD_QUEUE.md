# Build Queue

## Current Objective
Turn `services/media-commerce` from a scaffolded vertical into one real, horizontal-first workflow slice.

## Priority 1
- Fix local runtime blockers:
  - malformed `docker-compose.yml`
  - media-commerce service boot path

## Priority 2
- Implement `DealFlow.route_lead` as the first real vertical slice
- Keep all inference, workflow, memory, policy, billing, and shared-schema responsibilities horizontal

## Priority 3
- Add smoke coverage for the first slice

## Out of Scope For First Slice
- Full autonomous content lifecycle
- Full executive reporting layer
- Real Azure deployment completion
- Broad multi-agent behavior across all 8 vertical agents
