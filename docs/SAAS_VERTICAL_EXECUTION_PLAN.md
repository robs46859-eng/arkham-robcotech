# SaaS Vertical Execution Plan

## Goal

Build the first productized market vertical on top of the existing Arkham horizontal platform.

The first market vertical is `saas`.

This rollout must:

- preserve the Azure-first deployment story
- keep orchestration as the execution authority
- reuse existing horizontal agents and workflow patterns
- convert the current founder workspace into a SaaS-native command layer
- create a clear implementation path for later `ecommerce`, `media`, `staffing`, and `studio` verticals

## Why SaaS First

SaaS is the fastest path to a coherent market vertical because the current workspace model, integrations, and founder-facing product language already support:

- subscription billing
- investor reporting
- pipeline and demand capture
- onboarding and conversion optimization
- product analytics and customer signals

The core operating loop is:

1. capture demand
2. score and route demand
3. convert through signup or sales motion
4. monitor expansion, churn, and board-facing KPIs
5. feed that state back into founder reporting

## Scope

### In Scope

- add a tenant-level vertical profile for `saas`
- create SaaS-specific dashboard summaries, metrics, and investor targets
- add SaaS-specific project categories, source mapping, and workflow templates
- create a SaaS startup bundle definition and page copy path in the web app
- make the workspace derive meaningful values from user data for SaaS operators
- add vertical-aware workflow submission metadata for orchestration
- add hardening layers for validation, default safety rails, and review coverage

### Out of Scope

- full OAuth sync for every external provider
- new standalone microservices for SaaS
- removal of legacy compatibility aliases in gateway model mapping
- direct replacement of the media-commerce hardening service as the first hardened backend vertical

## Phases

### Phase 0: Spec Lock

Deliverables:

- this execution plan
- phase timing budgets
- stop conditions for subagents

Time budget before update:

- `900000` ms

### Phase 1: Vertical Data Foundation

Deliverables:

- add a SaaS-aware tenant profile and workspace state
- define SaaS bundle metadata
- define SaaS metric derivation rules
- define SaaS-specific workflow templates and source/provider defaults

Work:

- extend workspace types for vertical and bundle concepts
- extend workspace store seed/derivation logic
- add vertical-aware helper functions for metrics and defaults
- ensure future verticals can be registered without rewriting the workspace store

Hardening layer:

- central type-safe registry for vertical definitions
- default fallback behavior when vertical is unset
- permission-aware mutation paths only

Time budget before update:

- `1200000` ms

### Phase 2: SaaS Founder Bundle Product Surface

Deliverables:

- add SaaS bundle packaging to pricing and product surfaces
- add SaaS-specific dashboard, projects, workflows, and settings presentation
- reduce copy further and keep user values real and data-backed

Work:

- wire bundle and vertical labels into the home page and pricing page
- add SaaS-specific shell metadata and page summaries
- map projects to SaaS operating lanes such as pipeline, onboarding, retention, and reporting
- show source cards for SaaS-native providers such as Stripe, HubSpot, Segment, Google, Slack, and finance tools

Hardening layer:

- no layout shift from dynamic header sizes
- bounded empty states
- short copy only, no UI self-description

Time budget before update:

- `1200000` ms

### Phase 3: Workflow and Orchestration Mapping

Deliverables:

- vertical-aware workflow templates for SaaS
- richer metadata passed to orchestration
- deterministic mapping from user data to recommended workflows

Work:

- create SaaS template set such as:
  - `saas-board-cycle`
  - `saas-pipeline-routing`
  - `saas-signup-conversion`
  - `saas-retention-watch`
- attach vertical, bundle, and source-project context to orchestration submissions
- keep orchestration ownership of retries and execution

Hardening layer:

- local fallback if orchestration is unavailable
- no hidden mutation without role permission
- explicit status surfaces for failed or queued flows

Time budget before update:

- `900000` ms

### Phase 4: Review, Debug, and Consistency Pass

Deliverables:

- code review findings
- targeted cleanup patch
- final build verification

Work:

- inspect for type regressions and dead copy
- inspect for permission leaks and unsafe defaults
- inspect for mismatched vertical naming across files

Hardening layer:

- reviewer agent does not implement wide rewrites
- debug agent reports root cause and minimal fix only
- local integration owner resolves final conflicts

Time budget before update:

- `900000` ms

### Phase 5: Closeout

Deliverables:

- green build
- updated graphify output
- concise rollout summary
- explicit next vertical recommendation

Time budget before final handoff:

- `600000` ms

## SaaS Bundle Definition

### SaaS Core

Includes:

- DealFlow
- FulfillmentOps
- BudgetMind
- BoardReady basic

Primary outcomes:

- pipeline clarity
- signup and onboarding conversion
- revenue visibility
- investor reporting cadence

### SaaS Executive

Includes:

- everything in SaaS Core
- ChiefPulse
- ComplianceGate
- BoardReady executive
- ContentEngine support where applicable

Primary outcomes:

- executive anomaly visibility
- approval routing
- retention and expansion visibility
- cleaner board and investor posture

## SaaS Metrics Model

The first implementation should derive or estimate:

- investor readiness
- active opportunities
- onboarding risk items
- retention or churn watch items
- connected source count
- billing/revenue instrumentation coverage
- workflow coverage

Initial source mapping:

- `Stripe` -> revenue and subscription posture
- `HubSpot` and `Salesforce` -> pipeline
- `Segment` -> product activation signals
- `Google` and `Notion` -> reporting context
- `Slack` -> operating signals and approvals
- `QuickBooks` and `Xero` -> finance posture

## Subagent Work Plan

### Worker A: Web Surface

Ownership:

- `apps/web/src/app/page.tsx`
- `apps/web/src/app/pricing/page.tsx`
- `apps/web/src/app/dashboard/page.tsx`
- `apps/web/src/app/projects/page.tsx`
- `apps/web/src/app/workflows/page.tsx`
- `apps/web/src/app/settings/page.tsx`
- `apps/web/src/components/*`

Task:

- implement SaaS-first product and workspace surfaces

Stop conditions:

- stop after bounded patch set
- do not touch workspace store internals
- report changed files explicitly

### Worker B: Workspace and API Model

Ownership:

- `apps/web/src/lib/workspace-types.ts`
- `apps/web/src/lib/workspace-store.server.ts`
- `apps/web/src/app/api/workspace/route.ts`
- `apps/web/src/app/api/workflows/route.ts`
- `apps/web/src/app/api/projects/upload/route.ts`
- `apps/web/src/app/api/integrations/route.ts`
- `apps/web/src/app/api/settings/route.ts`

Task:

- implement vertical registry, SaaS bundle state, SaaS metrics derivation, and vertical-aware workflow metadata

Stop conditions:

- do not redesign frontend copy
- preserve session and permission enforcement
- report changed files explicitly

### Worker C: Debug and Review

Ownership:

- read-only across repo unless a minimal targeted fix is needed after findings

Task:

- review the SaaS rollout for regressions, permission leaks, naming drift, and type issues
- run targeted validation where needed

Stop conditions:

- findings first
- only propose minimal fixes
- do not refactor for style

## Final Handoff Rule

Subagents must stop after their assigned patch or findings pass and hand control back to the integration owner.

They must not:

- retry the same failed approach more than twice
- overwrite another worker's likely ownership area
- expand scope into later verticals
- continue looping on speculative improvements after reporting a concrete result
