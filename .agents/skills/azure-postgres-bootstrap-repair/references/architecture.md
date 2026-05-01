# Architecture References

Read first:
- `ARCHITECTURE.md`
- `docs/operations/ARKHAM_MAINTENANCE_PLAN.md`

SQL/bootstrap surfaces:
- `scripts/deploy-bot.sh`
- `infra/docker/postgres/init.sql`
- `infra/docker/postgres/init-resume.sql`
- `infra/docker/postgres/init-verticals.sql`
- `infra/docker/postgres/init-verticals-resume.sql`

Database consumers most likely affected by bootstrap changes:
- `services/gateway`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`
- `services/media-commerce`
