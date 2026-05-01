# Arkham - AI Assistant Guide

**Domain:** [robcotech.pro](https://robcotech.pro)
**Repository:** `/Users/joeiton/Desktop/gemini428ew/arkham`
**Production Platform:** Azure

## Project Overview

Arkham is a modular, multi-vertical platform built around:

- centralized gateway and routing
- durable orchestration
- semantic caching
- persistent memory
- billing
- security analysis and audit behavior
- vertical domain services

Current verticals are consumed as product layers on top of the horizontal core, not as separate platforms. `services/media-commerce` is the hardening vertical, and `digital_it_girl` is the predictive niche vertical.

## Repository Structure

```text
arkham/
├── apps/
├── services/
├── packages/
├── infra/
├── docs/
├── launch-agent/
├── finisher-agent/
├── azure-runner-agent/
└── omni-deployer/
```

## Authoritative Rules

1. Azure is the only active production platform.
2. Orchestration owns workflow lifecycle, task dispatch, retries, checkpoints, and worker control.
3. Vertical services must not recreate horizontal platform concerns or queue/workflow semantics.
4. Planning-only agents may inspect and plan, but they do not own execution.
5. `graphify-out/` is a local navigation artifact for each operator or agent.
6. When adding a vertical, update the workspace model, workflow registry, docs, and tests together so the vertical resolves explicitly instead of falling back to SaaS defaults.

## Core Platform Services

- `services/gateway`
- `services/orchestration`
- `services/memory`
- `services/semantic-cache`
- `services/billing`
- `services/arkham`

## First Hardening Vertical

- `services/media-commerce`

This vertical should remain orchestration-driven and platform-dependent rather than platform-like.

## Predictive Niche Vertical

- `digital_it_girl`

This vertical consumes the same horizontal core. It adds niche scoring, market synthesis, and audience segmentation, but it does not own workflow execution or storage primitives.

## Planning-Only Agents

- `launch-agent`
- `finisher-agent`
- `azure-runner-agent`
- `omni-deployer`

These packages may:

- inspect repository state
- generate plans
- structure work
- recommend commands

They must not become the execution control plane.

## Recommended Reading Order

1. `ARCHITECTURE.md`
2. `docs/operations/ARKHAM_MAINTENANCE_PLAN.md`
3. `docs/operations/ORCHESTRATION_DIRECTIVE.md`
4. `LAUNCH_LIST.md`
5. `FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md`

## Graphify Usage

- regenerate locally when needed
- use it for navigation and impact analysis
- do not treat it as the source of truth over code and docs
