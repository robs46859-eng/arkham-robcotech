# Graphify References

`graphify-out/` in this repo is cache-heavy. Treat it as a locator, not a primary document.

Search targets that correspond to the key operational nodes:
- deploy orchestration:
  `rg -n "scripts/deploy-bot.sh|scripts/aca_env_secrets_agent.py" graphify-out -S`
- SQL bootstrap:
  `rg -n "infra/docker/postgres/init.sql|infra/docker/postgres/init-verticals.sql" graphify-out -S`
- frontend and gateway:
  `rg -n "apps/web|services/gateway" graphify-out -S`
- orchestration and vertical boundaries:
  `rg -n "services/orchestration|services/media-commerce" graphify-out -S`
- custom-domain workflow:
  `rg -n "containerapp|hostname|certificate|custom domain" graphify-out -S`
