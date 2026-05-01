# Arkham Deployment Plan

**Domain:** `robcotech.pro`
**API Domain:** `api.robcotech.pro`
**Status:** Azure-first rollout path
**Date:** 2026-04-29

## Objective

Deploy Arkham as an Azure-first production stack with:

- frontend and API split
- containerized backend services
- managed PostgreSQL
- managed Redis
- production secrets handling
- validated orchestration and worker behavior

## Active Production Path

1. Validate the local stack
2. Build and publish backend images
3. Deploy backend services to Azure
4. Configure frontend hosting and public routing
5. Apply database migrations
6. Validate orchestration, billing, and core vertical flows
7. Confirm monitoring, rollback, and launch readiness

## Active Service Set

- `services/gateway`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`
- `services/arkham`
- `services/media-commerce`

## Required Infrastructure

- Azure resource group
- Azure container runtime for backend services
- Azure container registry
- managed PostgreSQL
- managed Redis
- secure secret storage
- monitoring and alerting

## Public Routing

- `robcotech.pro` -> frontend
- `www.robcotech.pro` -> frontend alias
- `api.robcotech.pro` -> gateway

## Validation Gates

Before production cutover:

1. all required service health endpoints return success
2. database migrations apply cleanly
3. orchestration workers process queued work correctly
4. semantic-cache behaves correctly on lookup and invalidation
5. billing routes and webhook handling are validated if enabled
6. media-commerce workflows complete through orchestration-owned execution paths

## Explicit Non-Goals

The repository has been purged of legacy materials. The following are NOT supported:
- GCS-backed telemetry
- GKE deployments
- Cloud Run deployments
- Any GCP-based production stories
