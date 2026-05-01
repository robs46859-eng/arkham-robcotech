# Graphify References

Use Graphify as a locator only.

Horizontal node search patterns:
- `rg -n "services/gateway|services/orchestration|services/memory|services/semantic-cache|services/billing|services/arkham" graphify-out -S`

Vertical node search patterns:
- `rg -n "services/media-commerce|app/agents|app/models" graphify-out -S`

Deploy/runtime node search patterns:
- `rg -n "deploy-bot.sh|aca_env_secrets_agent.py|containerapp|postgres|init.sql|init-verticals.sql" graphify-out -S`

Agent hierarchy node search patterns:
- `rg -n "deal_flow|content_engine|fulfillment_ops|compliance_gate|budget_mind|board_ready|chief_pulse|media_commerce" graphify-out -S`
