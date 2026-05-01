---
name: arkham-azure-ops-router
description: Use when an agent needs to choose the correct FullStackArkham Azure operations skill by phase, such as build updates, PostgreSQL bootstrap repair, deploy-debug triage, or custom-domain/TLS cutover, and should route to the narrowest workflow instead of mixing concerns.
---

# Arkham Azure Ops Router

Use this skill as the entrypoint for Azure operational work in this repo.

Route to the narrowest matching skill:
- `azure-aca-build-update`
  Use when service paths, ports, Dockerfiles, env vars, secrets, or the deploy pipeline itself need to change.
- `azure-postgres-bootstrap-repair`
  Use when deploy fails in PostgreSQL setup, extension allowlisting, schema bootstrapping, seeds, or resume SQL.
- `azure-aca-deploy-debug`
  Use when the deploy fails or appears stuck and the root cause is not yet clear.
- `azure-aca-custom-domain-cutover`
  Use when DNS, ACA hostname registration, managed certificates, or HTTPS cutover is the focus.

## Routing Rules

1. If the task is before image build or service creation, prefer `azure-aca-build-update`.
2. If the failure mentions `psql`, SQL files, extensions, `tenant_id`, `ON CONFLICT`, or replaying bootstrap, prefer `azure-postgres-bootstrap-repair`.
3. If the failure phase is unclear or spans Docker, Azure CLI, ACR, ACA, and env wiring, start with `azure-aca-deploy-debug`.
4. If ACA services are deployed and the remaining work is DNS, hostnames, certificates, or HTTPS, use `azure-aca-custom-domain-cutover`.

## Authoritative References

- Architecture: `ARCHITECTURE.md`
- Maintenance lane guidance: `docs/operations/ARKHAM_MAINTENANCE_PLAN.md`
- Orchestration ownership: `docs/operations/ORCHESTRATION_DIRECTIVE.md`
- Deploy workflow: `scripts/deploy-bot.sh`
- ACA env/secrets helper: `scripts/aca_env_secrets_agent.py`

## Graphify Guidance

`graphify-out/` is a local navigation artifact, not the source of truth.

When you need Graphify context, search it using concrete repo surfaces rather than browsing cache files blindly.

Useful patterns:
- `rg -n "deploy-bot.sh|aca_env_secrets_agent.py|init.sql|init-verticals.sql" graphify-out -S`
- `rg -n "services/gateway|services/orchestration|apps/web" graphify-out -S`
- `rg -n "hostname bind|containerapp|custom domain|certificate" graphify-out -S`

Also read the skill-specific references before making large changes:
- `references/architecture.md`
- `references/graphify.md`
