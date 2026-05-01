# Arkham

**Domain:** [robcotech.pro](https://robcotech.pro)
**API:** `api.robcotech.pro`
**Production Platform:** Azure

Arkham is an Azure-first, multi-vertical platform built around a centralized gateway, durable orchestration, semantic caching, persistent memory, billing, security analysis, and reusable vertical services.

The horizontal core stays authoritative. Vertical layers consume it and add domain-specific UX, data models, and workflow templates.

## Repository Shape

### Core Platform

- `services/gateway`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`
- `services/arkham`

### First Hardening Vertical

- `services/media-commerce`

### Predictive Niche Vertical

- `digital_it_girl`

### Frontend

- `apps/web`
- `apps/admin`
- `apps/docs`

### Shared and Infra

- `packages/`
- `infra/`

### Planning-Only Agents

- `launch-agent`
- `finisher-agent`
- `azure-runner-agent`
- `omni-deployer`

These agent packages are planning and coordination tools. They are not the execution control plane for the product.

## Operating Rules

1. Azure is the authoritative production platform.
2. Orchestration is the authority for workflow execution, retries, checkpoints, and worker control.
3. Vertical services must not reimplement horizontal platform concerns or workflow semantics.
4. `graphify-out/` is a local navigation artifact for operators and agents, not the source of truth.
5. When adding a vertical, update the workspace model, workflow registry, and docs together so the vertical resolves explicitly instead of inheriting SaaS defaults.

## Where To Start

- Architecture overview: `ARCHITECTURE.md`
- Maintenance guidance: `docs/operations/ARKHAM_MAINTENANCE_PLAN.md`
- Execution ownership: `docs/operations/ORCHESTRATION_DIRECTIVE.md`
- Launch checklist: `LAUNCH_LIST.md`
- Current deploy path: `FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md`

## Local Development

```bash
docker-compose up -d
docker-compose logs -f gateway
```

## Production Direction

The active production path is Azure-first:

- frontend on a chosen frontend host
- backend services on Azure container infrastructure
- managed PostgreSQL
- managed Redis
- secure secret management

Legacy GCP-oriented assets may still exist in the repository as historical or alternate material, but they are not the active production target.

Vertical guidance:

- `services/media-commerce` is the current hardening vertical.
- `digital_it_girl` is the current predictive niche vertical.
- both consume Arkham's horizontal services rather than replacing them.
