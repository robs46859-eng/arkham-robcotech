# Vertical Service Context

## Service Location
- `services/media-commerce`

## What Already Exists
- FastAPI app in `app/main.py`
- agent class files in `app/agents/*.py`
- copied marketing skills in `app/skills/*`
- SQLAlchemy models in `app/models/entities.py`

## Current Reality
- agent classes are mostly scaffold-level and often return empty structures
- many methods contain `In production, would...` placeholders
- no committed tests exist under `services/media-commerce/tests`

## Best First Implementation Slice
- `DealFlow.route_lead`

Why:
- it is central to Scenario 5
- it fits the 13-entity shared model
- it can emit `tasks` and `events`
- it can stay horizontal-first by using shared contracts instead of ad hoc logic
