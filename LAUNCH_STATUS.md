# Arkham Launch Status

**Domain:** `robcotech.pro`
**API Domain:** `api.robcotech.pro`
**Date:** 2026-04-29
**Status:** In cleanup and alignment

## Current State

Arkham has:

- a strong horizontal service layout
- orchestration and worker infrastructure
- a first real vertical in `services/media-commerce`
- multiple planning-only agent packages

Arkham does not yet have a fully clean, single-source production story throughout the repository.

## Blocking Drift (RESOLVED)

1. Purged: GCP and GCS references have been removed from templates, scaffolds, and docs.
2. Aligned: Domain references standardized to `robcotech.pro`.
3. Standardized: Deployment path consolidated to Azure-first authority.
4. Clarified: Planning agents remain planning-only; Orchestration owns execution.

## Current Launch Position

- Azure is the production authority
- orchestration is the execution authority
- planning agents are non-executing
- Graphify is local-only navigation state

## Immediate Priority

1. Finalize DNS cutover for `robcotech.pro`
2. Complete Azure Container Apps deployment validation
3. Verify vertical flow orchestration
4. keep media-commerce thin and orchestration-driven
