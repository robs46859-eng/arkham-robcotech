# Ecommerce Vertical Execution Plan

## Goal

Build the next productized market vertical on top of the existing Arkham horizontal platform: `ecommerce`.

This rollout must:
- preserve the Azure-first deployment story
- keep orchestration as the execution authority
- reuse existing horizontal agents and workflow patterns
- add an `ecommerce` layer
- create a clear implementation path for later `media`, `staffing`, and `studio` verticals

## Why Ecommerce Next

Ecommerce closely mirrors the revenue and activation patterns established by the SaaS vertical but introduces physical product signals, demand capture across different channels, and unique operational workflows. The core operating loop is:

1. capture demand (Ads, SEO, Social)
2. optimize conversion (Merchandising, CRO)
3. process revenue (Checkout, Shipping, Returns)
4. monitor margins and retention (LTV, CAC, Logistics)
5. feed that state back into founder reporting

## Scope

### In Scope
- define ecommerce-specific bundles (`ecom-starter`, `ecom-growth`)
- create Ecommerce-specific dashboard summaries, metrics (AOV, LTV, CAC), and investor targets
- add Ecommerce-specific project categories, source mapping (Shopify, Meta, Google Ads), and workflow templates
- add vertical-aware workflow submission metadata for orchestration
- add hardening layers for validation, default safety rails, and review coverage

### Out of Scope
- full OAuth sync for every external provider
- new standalone microservices for Ecommerce
- removal of legacy compatibility aliases in gateway model mapping

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
- define Ecommerce bundle metadata (`ecom-starter`, `ecom-growth`)
- define Ecommerce metric derivation rules (ROAS, AOV, Conversion Rate)
- define Ecommerce-specific workflow templates and source/provider defaults

Work:
- extend workspace types for new bundle concepts
- extend workspace store seed/derivation logic
- add vertical-aware helper functions for metrics and defaults
- ensure future verticals can be registered without rewriting the workspace store

Hardening layer:
- central type-safe registry for vertical definitions
- default fallback behavior when vertical is unset
- permission-aware mutation paths only

Time budget before update:
- `1200000` ms

### Phase 2: Product Surface

Deliverables:
- add Ecommerce bundle packaging to pricing and product surfaces
- add Ecommerce-specific dashboard, projects, workflows, and settings presentation

Work:
- wire bundle and vertical labels into the home page and pricing page
- add Ecommerce-specific shell metadata and page summaries
- map projects to Ecommerce operating lanes such as Acquisition, Merchandising, Logistics, and Reporting
- show source cards for Ecommerce-native providers such as Shopify, Klaviyo, Meta, and Amazon

Hardening layer:
- no layout shift from dynamic header sizes
- bounded empty states
- short copy only, no UI self-description

Time budget before update:
- `1200000` ms

### Phase 3: Workflow and Orchestration Mapping

Deliverables:
- vertical-aware workflow templates for Ecommerce
- richer metadata passed to orchestration
- deterministic mapping from user data to recommended workflows

Work:
- create Ecommerce template set such as:
  - `ecom-inventory-monitor`
  - `ecom-cart-recovery`
  - `ecom-ad-spend-optimization`
  - `ecom-merchandising-audit`
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

## Subagent Work Plan

### Worker A: Web Surface (James)
Ownership:
- `apps/web/src/app/page.tsx`
- `apps/web/src/app/pricing/page.tsx`
- `apps/web/src/app/dashboard/page.tsx`
- `apps/web/src/app/projects/page.tsx`
- `apps/web/src/app/workflows/page.tsx`
- `apps/web/src/components/*`

Task:
- implement Ecommerce-first product and workspace surfaces

Stop conditions:
- stop after bounded patch set
- do not touch workspace store internals
- report changed files explicitly

### Worker B: Workspace and API Model (Franklin)
Ownership:
- `apps/web/src/lib/workspace-types.ts`
- `apps/web/src/lib/workspace-store.server.ts`
- `apps/web/src/app/api/workspace/route.ts`
- `services/orchestration/app/flows/registry.py`

Task:
- implement Ecommerce bundle state, metrics derivation, and vertical-aware workflow metadata and orchestration flow registrations

Stop conditions:
- do not redesign frontend copy
- preserve session and permission enforcement
- report changed files explicitly

### Worker C: Debug and Review (Pasteur)
Ownership:
- read-only across repo unless a minimal targeted fix is needed after findings

Task:
- review the Ecommerce rollout for regressions, permission leaks, naming drift, and type issues
- run targeted validation where needed

Stop conditions:
- findings first
- only propose minimal fixes
- do not refactor for style
