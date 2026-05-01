# Arkham Deployment Guide

## Goal

Deploy Arkham into a coherent Azure-first production stack with one authoritative deployment story, explicit frontend and API routing, validated secrets flow, and working orchestration.

## Active Path

Use this sequence:

1. repair and validate the local Docker baseline
2. standardize the backend deployment on Azure
3. choose and commit the frontend hosting contract
4. complete public routing for `robcotech.pro` and `api.robcotech.pro`
5. validate orchestration, billing, and media-commerce flows end to end

## Current Guidance

Azure is the active production platform.

Legacy GCP- and GCS-oriented assets may still exist in the repository, but they are deprecated for current operations and should not be used as the primary production path.

## Step 1: Local Validation

Before trusting deployment, verify:

- `docker-compose.yml` parses and starts
- service URLs are internally consistent
- required health endpoints return success
- orchestration workers and queues behave correctly
- frontend can reach required API routes

Priority services:

- `gateway`
- `arkham`
- `billing`
- `orchestration`
- `memory`
- `semantic-cache`
- `bim_ingestion`
- `media-commerce`

## Step 2: Azure Infrastructure

The production target must provide:

- backend container runtime
- image registry
- managed PostgreSQL
- managed Redis
- secret storage
- logging, metrics, and alerting

Document the real Azure resource names in the live deployment workflow and keep them aligned with:

- `scripts/deploy-bot.sh`
- `scripts/launch.sh`
- `LAUNCH_LIST.md`

## Step 3: Frontend and API Split

Recommended public routing:

- `https://robcotech.pro` -> frontend
- `https://www.robcotech.pro` -> frontend alias
- `https://api.robcotech.pro` -> gateway/API ingress

Internal service-to-service traffic should remain private where possible.

## Step 4: Secrets and Runtime Configuration

Required secret categories include:

- database connection values
- redis connection values
- JWT secret
- model provider keys
- Stripe secret and webhook values
- domain and API base values

Every service should have a clear split between:

- required secrets
- required non-secret env vars
- optional env vars

## Step 5: Orchestration Validation

Production is not ready unless orchestration is healthy.

Validate:

- workflow creation
- task dispatch
- worker processing
- checkpoint persistence
- retry behavior
- queue draining
- workflow status visibility

See also:

- `docs/operations/ORCHESTRATION_DIRECTIVE.md`
- `docs/operations/ARKHAM_MAINTENANCE_PLAN.md`

## Step 6: Media-Commerce Validation

`services/media-commerce` is the first hardening vertical.

It must remain a client of the horizontal platform.

Validate that:

- execution routes through orchestration executors
- vertical logic does not own retry or checkpoint semantics
- cache behavior remains delegated to semantic-cache
- security and audit behavior remains delegated to the proper platform services

## Step 7: Launch Readiness

Minimum production readiness:

1. frontend loads correctly
2. gateway health is stable
3. core API routes respond
4. orchestration flows succeed
5. billing flow and webhooks succeed if enabled
6. logs and alerts are accessible
7. rollback is documented

## Legacy Asset Policy

If the repository still contains:

- GCP Terraform
- GKE manifests
- GCS telemetry references
- Cloud Run scaffolding

those assets should be treated as deprecated or alternate until deliberately updated and reintroduced.
