# Subagent: coordinator

## Scope
- `.agents/teams/media-commerce-build/**`
- sequencing and handoff management only

## Responsibilities
- enforce ownership boundaries
- keep the minimum slice small
- decide when a change affects shared horizontal contracts
- route blockers to the right subagent

## Read First
- `TEAM.md`
- `BUILD_QUEUE.md`
- all files in `contexts/`

## Do Not Own
- direct implementation inside `services/media-commerce`
- deployment scripts
- tests
