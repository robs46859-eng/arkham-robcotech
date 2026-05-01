---
name: azure-aca-build-update
description: Use when adding a new service to the FullStackArkham Azure build and deploy flow, changing ports, updating env requirements, extending SQL bootstrap assets, or modifying the service map, ACR build logic, or ACA env wiring used by the repo deployment scripts.
---

# Azure ACA Build Update

Use this skill when the build or deploy system needs to change because the repo changed.

Primary files:
- `scripts/deploy-bot.sh`
- `scripts/aca_env_secrets_agent.py`
- `apps/*/Dockerfile`
- `services/*/Dockerfile`
- `infra/docker/postgres/*.sql`

## Change Checklist

1. Inspect the actual service before editing deploy automation.
Confirm:
- source path
- Dockerfile presence
- listening port inside the container
- required plain env vars
- required secret env vars
- service-to-service dependencies

2. Update the deploy service map.
In this repo the format is:
- `app_name:source_path:container_port`

Do not add only a name. The deploy script uses the path and port.

3. Update ACA env wiring.
If the service needs:
- static env vars: update `APP_SPECS[*].base_plain_env`
- secrets: update `APP_SPECS[*].base_secret_env` or `optional_secret_env`
- dependency URLs: update `dependency_env_keys` and `DEPENDENCY_TARGETS`

4. Update database bootstrap assets only when the schema actually changed.
If a new table or seed is added:
- check idempotency
- check partial-bootstrap recovery
- add or update a resume SQL file when replay would fail on existing objects

5. Keep Azure regions explicit.
- Resource group and ACA env default to the RG location.
- PostgreSQL may use a different location.
- Do not silently collapse them.

6. Keep operator output useful.
If a long-running phase was added:
- emit per-service or per-phase progress
- avoid silent loops that look hung

## Common Edits

- Add a service to `SERVICES`
- Add service secrets and env mappings to `APP_SPECS`
- Add dependency FQDN wiring to `DEPENDENCY_TARGETS`
- Update frontend runtime env if a public URL contract changed
- Update SQL bootstrap plus matching resume SQL

## Validation

After edits, run:
- `bash -n scripts/deploy-bot.sh`
- `python3 -m py_compile scripts/aca_env_secrets_agent.py`

If SQL changed, inspect the new DDL and seed paths for:
- schema/seed mismatches
- missing casts for typed `NULL`
- non-idempotent inserts
- partial-bootstrap replay failures

## References

Read when needed:
- `references/architecture.md`
- `references/graphify.md`
