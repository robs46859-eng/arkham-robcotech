---
name: azure-aca-deploy-debug
description: Use when FullStackArkham Azure deployment fails or stalls across Docker, Azure CLI, PostgreSQL bootstrap, Key Vault sync, ACR push, Container Apps creation, env wiring, or custom-domain binding, and an agent needs a stepwise triage workflow instead of guessing.
---

# Azure ACA Deploy Debug

Use this skill when `scripts/deploy-bot.sh` or `scripts/aca_env_secrets_agent.py` fails, stalls, or behaves inconsistently.

Primary files:
- `scripts/deploy-bot.sh`
- `scripts/aca_env_secrets_agent.py`
- `infra/docker/postgres/init.sql`
- `infra/docker/postgres/init-resume.sql`
- `infra/docker/postgres/init-verticals.sql`
- `infra/docker/postgres/init-verticals-resume.sql`

## Debug Order

1. Identify the exact phase.
Common phases:
- prerequisites
- Key Vault sync
- PostgreSQL firewall or extension allowlist
- core SQL bootstrap
- vertical SQL bootstrap
- Docker build
- ACR push
- Container App create or update
- base env and secrets apply
- dependency URL wiring
- custom domain binding

2. Validate the local execution surface first.
Use:
- `bash -n scripts/deploy-bot.sh`
- `python3 -m py_compile scripts/aca_env_secrets_agent.py`
- `docker context show`
- `colima status`

3. Treat Azure CLI version skew as a real failure mode.
Inspect command help on the live machine before patching syntax:
- `az postgres flexible-server firewall-rule create -h`
- `az containerapp hostname bind -h`
- `az containerapp env certificate create -h`

Do not assume a newer Azure CLI syntax just because warnings mention a future change.

4. Treat partial SQL bootstrap as normal after a first failure.
Check whether the deploy should resume instead of replaying:
- core schema sentinel tables: `tenants`, `subscription_plans`
- vertical schema sentinel table: `policies`

Prefer resume SQL over dropping the database.

5. For seed failures, inspect schema and inserts together.
Typical problems:
- insert references a column not present in the table
- nullable seed data conflicts with a `NOT NULL` column
- `ON CONFLICT DO NOTHING` used without a useful uniqueness target
- `VALUES` inference creates bad types for `NULL`

6. For post-deploy “hangs”, inspect whether the process is just quiet.
This repo previously appeared stuck during ACA dependency wiring because the Python helper emitted no per-app progress.
Check:
- whether the foreground process is still active
- whether a terminal status dump came from `Ctrl-T`
- whether one specific app update is blocking

7. For custom domains, separate DNS from ACA binding.
Check both:
- public DNS with `dig`
- ACA hostnames with `az containerapp hostname list`

If hostnames are `Disabled`, the issue is binding or certificate state, not only DNS.

## Repair Principles

- Patch for resumability and idempotency, not just the single current failure.
- Prefer explicit sentinels over destructive resets.
- Add operator-visible progress output where a quiet long-running phase can be mistaken for a hang.
- When a CLI command can vary across versions, detect or inspect support instead of hardcoding the newest form.

## Validation

After repairs, run only the smallest validation that proves the fix:
- shell syntax check for bash scripts
- `py_compile` for Python helpers
- rerun only the blocked phase if possible
- rerun the full deploy only once resume logic is in place

## References

Read when needed:
- `references/architecture.md`
- `references/graphify.md`
