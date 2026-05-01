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

## Blocking Drift

1. residual GCP and GCS references in legacy templates, generated scaffolds, and some docs
2. historical references to `stelar.host` in files that should describe Arkham
3. mixed deployment assumptions across legacy assets and newer Azure-first planning
4. incomplete cleanup between planning-only agents and execution authority

## Current Launch Position

- Azure is the production authority
- orchestration is the execution authority
- planning agents are non-executing
- Graphify is local-only navigation state

## Immediate Priority

1. purge GCS/GCP drift from authoritative docs and app scaffolds
2. align launch docs to `robcotech.pro`
3. align deployment docs to Azure-first operations
4. keep media-commerce thin and orchestration-driven
