# Media-Commerce Build Team

This team is for building the `media-commerce` vertical on top of the `FullStackArkham` horizontal backbone without letting the vertical absorb horizontal responsibilities.

## Goal
- Keep `gateway`, `orchestration`, `memory`, `semantic-cache`, `billing`, and shared schema horizontal.
- Build `services/media-commerce` as a tenant-aware vertical service that consumes those horizontal services.
- Reduce context-token waste by giving each subagent a narrow file scope and a compact context pack.

## Active Subagents
1. `coordinator`
   - Owns sequencing, conflict resolution, and handoffs.
2. `horizontal-integrator`
   - Owns horizontal-core contracts and shared-schema guardrails.
3. `vertical-builder`
   - Owns `services/media-commerce` runtime behavior and tests.
4. `deploy-repair`
   - Owns local runtime and deploy path fixes.
5. `verifier`
   - Owns smoke validation and regression checks.

## Token-Saving Rules
- Each subagent reads only its assigned context file first.
- Each subagent reads only its owned file scope unless explicitly escalated by the coordinator.
- Handoffs must be short:
  - `What changed`
  - `What is blocked`
  - `What the next agent needs`
- Do not reload the whole repo if a context file or handoff already covers the needed facts.

## Handoff Protocol
- Write updates into `handoffs/<agent>.md`.
- Keep each handoff under 20 lines.
- If a subagent touches a shared contract, notify `coordinator` and `horizontal-integrator`.

## Current Recommended Build Order
1. `horizontal-integrator` confirms horizontal seams and schema constraints.
2. `vertical-builder` implements one real end-to-end slice in `services/media-commerce`.
3. `deploy-repair` fixes local runtime blockers so the slice can boot.
4. `verifier` runs smoke checks and reports regressions.

## Current Minimum Slice
- `DealFlow.route_lead`
- Backed by shared `Lead`, `Deal`, `Task`, `Event`, and `Policy` logic
- Exposed through `services/media-commerce/app/main.py`
- Covered by a basic integration or service test
