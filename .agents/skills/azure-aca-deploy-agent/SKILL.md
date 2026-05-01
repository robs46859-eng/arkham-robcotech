---
name: azure-aca-deploy-agent
description: Use when a repo needs an Azure Container Apps deployment bot with Key Vault-backed env and secret management, Redis/PostgreSQL setup, database initialization, Container Apps wiring, or a reusable deployment skill copied into another project. Also use when building or porting the companion ACA env/secrets agent and deploy scripts across repositories.
---

# Azure ACA Deploy Agent

Use this skill when a project needs the same Azure deployment pattern used in FullStackArkham:
- `scripts/deploy-bot.sh` for setup, build, push, and deploy
- `scripts/aca_env_secrets_agent.py` for Key Vault sync, env/secret exposure audit, and ACA env/secrets application
- a deprecated `scripts/launch.sh` shim that redirects operators to the supported flow

## What To Build

Create or update these repo-local files:
- `scripts/deploy-bot.sh`
- `scripts/aca_env_secrets_agent.py`
- `scripts/launch.sh`

If the target repo already has deploy scripts, adapt them instead of replacing blindly.

## Core Workflow

1. Inspect the target repo first.
Check service directories, Dockerfiles, listening ports, infra scripts, and required runtime env vars.

2. Build a repo-specific service map.
Use `app_name:source_dir:container_port`, not just service names.
Do not assume the public service port equals the container's listening port.

3. Keep Azure regions explicit.
Use the resource group's location for ACA/ACR/Key Vault by default.
Allow PostgreSQL to use a separate location when the subscription restricts the resource-group region.

4. Persist secrets in Key Vault.
The env/secrets agent should generate or sync:
- PostgreSQL admin user/password
- database URLs
- Redis password and URL
- JWT secret
- optional external secrets like Stripe or App Insights

5. Add a repo-local audit.
The env/secrets agent should emit `aca_env_secrets_audit.md` in the repo root and report:
- plaintext secret exposure
- missing required production inputs
- whether Key Vault contains the expected canonical secrets

6. Initialize databases after PostgreSQL is ready.
Create application databases, add a narrow firewall rule for the deploy host, and run SQL initialization through a Dockerized `psql` client if the local machine does not have `psql`.

7. Apply ACA configuration in two phases.
- `base`: registry credentials, secrets, and static env vars
- `dependencies`: inter-service URLs after apps have FQDNs

8. Keep the old one-shot launcher deprecated.
`scripts/launch.sh` should only redirect users to `deploy-bot.sh`.

## Required Deploy-Bot Behaviors

`scripts/deploy-bot.sh` should:
- bootstrap Azure context from cached `az` login
- export `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID`, `AZURE_USER`, `ARM_SUBSCRIPTION_ID`, and `ARM_TENANT_ID`
- resolve the resource-group location
- resolve a safe Key Vault name inside the target resource group
- allow a separate PostgreSQL location and tier/SKU
- load ACR credentials
- create or reuse RG, ACR, ACA env, Redis, Key Vault, and PostgreSQL
- call the ACA env/secrets agent for Key Vault sync and audit
- reconcile the PostgreSQL admin password from Key Vault back onto the server
- initialize databases from repo SQL files
- build images, including any required binary compilation step before Docker build
- push to ACR
- create or update Container Apps
- apply base and dependency ACA env/secrets configuration after deployment

## Required ACA Env/Secrets Agent Behaviors

`scripts/aca_env_secrets_agent.py` should support these subcommands:
- `audit`
- `sync-keyvault`
- `apply-containerapps`

It should:
- read `.env.production` only as an optional input source
- treat placeholders as missing values
- keep canonical secrets in Key Vault
- map repo services to their required env vars and secret refs
- set ACA registry credentials
- set ACA secrets
- set ACA env vars
- resolve dependency URLs from current ACA FQDNs

## Porting Rules

When copying this pattern to another repo:
- update resource names, service map, SQL file paths, and env-var requirements
- inspect each Dockerfile to determine the actual listening port
- inspect each service's settings/config to determine required env vars
- do not assume PostgreSQL can be created in the same region as ACA
- if Key Vault uses RBAC, assign the current operator `Key Vault Secrets Officer` on the vault scope before syncing secrets

## Validation

After building the repo-local scripts:
- run `bash -n scripts/deploy-bot.sh`
- run `bash -n scripts/launch.sh`
- run `python3 -m py_compile scripts/aca_env_secrets_agent.py`
- run the audit subcommand
- if Azure creds are available, run setup and deploy until the remaining blocker is either fixed or reduced to a concrete external issue

## Starter Files

This skill is paired with the live starter files in the source repo:
- `scripts/deploy-bot.sh`
- `scripts/aca_env_secrets_agent.py`
- `scripts/launch.sh`

Use the installer script when you want to copy those files into another repo quickly:
- `scripts/install_assets.sh /path/to/target-repo`

If you copy only the skill folder into another repo, use this skill as the build specification and recreate the three repo-local scripts there.
