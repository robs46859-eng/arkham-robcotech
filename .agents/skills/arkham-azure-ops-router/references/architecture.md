# Architecture References

Primary docs:
- `ARCHITECTURE.md`
- `docs/operations/ARKHAM_MAINTENANCE_PLAN.md`
- `docs/operations/ORCHESTRATION_DIRECTIVE.md`

Relevant architecture surfaces for Azure operations:
- Frontend app: `apps/web`
- API ingress: `services/gateway`
- Workflow control plane: `services/orchestration`
- Security service: `services/arkham`
- Memory service: `services/memory`
- Cache service: `services/semantic-cache`
- Billing service: `services/billing`
- First hardening vertical: `services/media-commerce`

Deployment control surfaces:
- `scripts/deploy-bot.sh`
- `scripts/aca_env_secrets_agent.py`
- `infra/docker/postgres/init.sql`
- `infra/docker/postgres/init-verticals.sql`
