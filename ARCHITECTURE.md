# Arkham Architecture: Multi-Vertical Horizontal Core

**Domain:** `robcotech.pro`
**API Domain:** `api.robcotech.pro`
**Production Platform:** Azure

## System Shape

Arkham is an Azure-first, multi-service platform. It functions as a **horizontal control plane** that powers specialized **market verticals**.

### Core Architecture
- **Horizontal Services:** Orchestration, Billing, Gateway, Memory, Semantic Cache. These services provide the cognitive and operational machinery shared across all verticals.
- **Verticals:** Self-contained bundles (SaaS, Ecommerce, Media, Maternal Health) that define their own metrics, workflow templates, and operating lanes.

### Vertical Integration Pattern
Adding a new vertical follows a strict, repeatable process:
1. **Model Layer:** Register vertical keys, bundles, and metric derivation rules in `apps/web/src/lib/workspace-store.server.ts`.
2. **Gateway:** Add proxy routes for vertical-specific APIs (or directly trigger orchestration flows).
3. **Orchestration:** Register vertical-specific flows and task executors in `services/orchestration/app/flows/registry.py`.
4. **Surface:** Update dashboard/pricing logic to branch on `tenant.vertical`.

This architecture ensures core system integrity while enabling high-velocity vertical deployment.

## Core Components

1. Gateway
   `services/gateway`
   Public ingress, auth, routing, provider coordination, and service mediation.

2. Orchestration
   `services/orchestration`
   Workflow lifecycle, queues, checkpoints, task execution, retries, and worker control.

3. Memory
   `services/memory`
   Persistent memory, retrieval, and context linking.

4. Semantic Cache
   `services/semantic-cache`
   Repeated inference caching, lookup, invalidation, and cost control.

5. Billing
   `services/billing`
   Subscription, checkout, metering, and billing webhooks.

6. Arkham Security
   `services/arkham`
   Threat detection, fingerprinting, deception, and audit behavior.

7. Media Commerce
   `services/media-commerce`
   First hardening vertical for media and commerce workflows.

8. Frontend Applications
   `apps/web`
   Main user-facing frontend.

9. Digital IT Girl
   Predictive niche vertical for opportunity scoring, audience segmentation, and market synthesis.

## Runtime Topology

- Frontend deployed separately from backend services
- Backend services deployed as containers on Azure
- Managed PostgreSQL for persistent state
- Managed Redis for cache and queues
- Secret storage through Azure-native secret management or equivalent secure app settings
- Logs, metrics, and alerts aligned to the Azure production path

## Recommended Public Routing

- `https://robcotech.pro` -> frontend
- `https://www.robcotech.pro` -> frontend alias
- `https://api.robcotech.pro` -> gateway / API ingress

## Execution Authority

Orchestration is the execution control plane for multi-step behavior.

That means:

- vertical services do not own workflow engine semantics
- task execution flows through orchestration executors
- retries, checkpoints, and worker control remain orchestration-owned
- new verticals must resolve explicitly through workspace and workflow metadata rather than inheriting SaaS defaults

See:

- `docs/operations/ARKHAM_MAINTENANCE_PLAN.md`
- `docs/operations/ORCHESTRATION_DIRECTIVE.md`

## Deployment Assets

Active deployment guidance:

- `FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md`
- `DEPLOYMENT_PLAN.md`
- `LAUNCH_LIST.md`
- `LAUNCH_TODAY.md`
- `scripts/deploy-bot.sh`
- `scripts/launch.sh`

Legacy or alternate deployment assets may still exist in the repository, but they are not authoritative unless explicitly promoted again.

## Launch-Critical Dependencies

1. Gateway health and public ingress
2. Database migrations and connectivity
3. Redis and queue processing
4. Frontend to API connectivity
5. Worker loop and orchestration task execution
6. Billing and webhook connectivity if enabled
7. Security eventing and audit visibility

## Current Risks

1. Legacy configuration drift was identified and GCP/GCS references have been purged from the active repository.
2. Several launch and deployment docs previously drifted from the Azure-first production decision.
3. Planning-only agent packages need continued separation from execution authority.
4. Media-commerce must remain a disciplined consumer of the horizontal platform, not a shadow platform.
