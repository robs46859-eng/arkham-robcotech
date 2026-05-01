# Architecture References

Read first:
- `ARCHITECTURE.md`
- `docs/operations/ARKHAM_MAINTENANCE_PLAN.md`
- `docs/operations/ORCHESTRATION_DIRECTIVE.md`

Horizontal source surfaces:
- `services/gateway`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`
- `services/arkham`

Example hardening vertical:
- `services/media-commerce`
- `services/media-commerce/app/agents`
- `services/media-commerce/app/models`

Operational surfaces:
- `scripts/deploy-bot.sh`
- `scripts/aca_env_secrets_agent.py`
- `infra/docker/postgres/*.sql`
