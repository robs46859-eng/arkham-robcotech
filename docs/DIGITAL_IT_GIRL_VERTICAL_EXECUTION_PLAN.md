# Digital IT Girl Vertical Execution Plan

## Position

Arkham is the horizontal control plane.

Digital IT Girl is a vertical execution layer that consumes Arkham's gateway, orchestration, billing, memory, and safety rails. It is not allowed to become a second platform, a parallel queueing system, or a vertical-owned workflow engine.

That boundary is non-negotiable.

## Goal

Build `digital_it_girl` as a predictive niche intelligence vertical with durable opportunity scoring, repeatable audience segmentation, and operator-grade market research workflows.

This rollout must:

- keep Arkham visibly horizontal and authoritative
- make Digital IT Girl a first-class vertical in workspace state, workflow templates, and orchestration
- replace one-off trend analysis with persistent niche scoring primitives
- create a direct path from audience filters to scored opportunities, research briefs, and export-ready results
- preserve cheap-first execution and escalate to premium synthesis only when the workflow justifies it

## What This Vertical Owns

- niche-specific scoring logic
- audience segment research workflows
- product gap synthesis
- operator-facing workflow templates and dashboard framing
- vertical-specific artifact outputs such as niche briefs, watchlists, and market recommendations

## What This Vertical Does Not Own

- workflow engine semantics
- retries, checkpoints, or worker control
- auth, session, or permission policy
- billing enforcement
- gateway-level provider routing
- a standalone database or shadow service before the horizontal seams are exhausted

## Scope

### In Scope

- add `digital_it_girl` to workspace vertical definitions and bundle definitions
- add Digital IT Girl workflow templates and vertical-specific dashboard semantics
- create a first orchestration flow for predictive niche scoring
- add task executors for:
  - opportunity scoring
  - market research synthesis
- define a durable contract for audience filters:
  - US metro
  - age range
  - gender
  - demographic lens
  - income band
  - industry
  - household type
- return operator-ready outputs:
  - opportunity score
  - trend velocity
  - gap size
  - niche rationale
  - product direction
  - watchlist tags

### Out of Scope

- direct purchasing or ordering
- full external scraper implementation for every source on day one
- a new standalone `services/digital_it_girl` microservice before the orchestration contract proves insufficient
- replacing the existing gateway cost ladder with vertical-local routing logic

## Execution Rule

The first milestone is not a full dashboard rewrite.

The first milestone is a vertical foundation plus one credible orchestration slice that proves the hierarchy:

1. workspace recognizes `digital_it_girl`
2. workflows can submit a Digital IT Girl niche workflow
3. orchestration can score and synthesize a niche brief
4. the result lands as a stored artifact through the horizontal path

## Phases

### Phase 0: Lock The Boundary

Deliverables:

- this plan
- explicit horizontal-versus-vertical ownership language
- initial file ownership map

### Phase 1: Vertical Foundation

Deliverables:

- `digital_it_girl` in workspace vertical definitions
- Digital IT Girl bundle metadata
- Digital IT Girl workflow templates
- Digital IT Girl dashboard framing and vertical metrics labels

Build rule:

- no placeholder naming drift
- no SaaS copy leaking into the Digital IT Girl path
- template and bundle defaults must resolve deterministically

### Phase 2: Predictive Niche Engine Slice

Deliverables:

- orchestration flow registration for Digital IT Girl
- opportunity scoring executor
- market research synthesis executor
- artifact persistence through existing orchestration storage

Build rule:

- scoring must work with structured input even when external systems are unavailable
- research synthesis may call the gateway, but must degrade cleanly
- all outputs must stay explainable and structured

### Phase 3: Product Surface Expansion

Deliverables:

- dashboard and workflows surfaces that speak Digital IT Girl language
- workflow creation defaults that prefer Digital IT Girl templates
- preparation for audience search and CSV export UI

Build rule:

- no shadow API surface
- no hidden write path outside workspace/orchestration routes

### Phase 4: Search Ingestion Hardening

Deliverables:

- branded ingestion interfaces for reviews, mentions, trends, and competitor research
- stronger cost ladder alignment between gateway and orchestration metadata
- source normalization contracts for niche scoring inputs

Build rule:

- cheap-first is mandatory
- premium synthesis is explicit, not accidental

### Phase 5: Review, Verification, Graphify

Deliverables:

- targeted review findings
- green validation for the added vertical slice
- updated Graphify output

## File Ownership

### Vertical Foundation

- `apps/web/src/lib/workspace-types.ts`
- `apps/web/src/lib/workspace-store.server.ts`
- `apps/web/src/app/dashboard/page.tsx`
- `apps/web/src/app/workflows/page.tsx`

### Predictive Niche Flow

- `services/orchestration/app/flows/registry.py`
- `services/orchestration/app/tasks/digital_it_girl.py`
- `services/orchestration/app/tasks/__init__.py`
- `services/orchestration/tests/test_digital_it_girl_flows.py`

## Immediate Build Sequence

1. make Digital IT Girl a first-class workspace vertical
2. register the first predictive niche workflow
3. add scoring and research executors
4. wire Digital IT Girl template defaults in the workflows UI
5. validate and update Graphify
