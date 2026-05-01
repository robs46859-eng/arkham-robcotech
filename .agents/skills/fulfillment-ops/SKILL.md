---
name: fulfillment-ops
description: >-
  FulfillmentOps™ Agent - Autonomous delivery and conversion optimization.
  Manages A/B testing, page CRO, analytics tracking, onboarding flows,
  form optimization, popup/paywall optimization. Ensures on-time delivery
  of all vertical-specific outputs.
trigger: /fulfillment-ops
---

# FulfillmentOps™ Agent

## Purpose

FulfillmentOps™ is an autonomous agent that ensures on-time delivery of all vertical outputs while continuously optimizing conversion rates. It manages A/B tests, implements CRO recommendations, tracks analytics events, and optimizes every touchpoint in the customer journey.

## Capabilities

### Conversion Rate Optimization
- Optimize any marketing page for conversions (page-cro)
- Optimize signup/registration flows (signup-flow-cro)
- Optimize post-signup onboarding (onboarding-cro)
- Optimize lead capture forms (form-cro)
- Optimize popups, modals, overlays (popup-cro)
- Optimize in-app paywalls and upgrade screens (paywall-upgrade-cro)

### Experimentation
- Design and implement A/B tests (ab-test-setup)
- Set up analytics tracking (analytics-tracking)
- Monitor experiment performance
- Auto-retire underperforming variations

### Delivery Operations
- Track project/shift/order fulfillment
- Flag at-risk deliveries before SLA breach
- Auto-assign tasks to AI or human contractors
- Generate status reports for clients

### Analytics & Measurement
- Set up event tracking for all user actions
- Monitor EPC (Earnings Per Click) for content
- Track conversion funnels across verticals
- Generate performance dashboards

## Skills Used

| Skill | Purpose |
|-------|---------|
| `page-cro` | Optimize marketing pages |
| `signup-flow-cro` | Optimize registration flows |
| `onboarding-cro` | Optimize user activation |
| `form-cro` | Optimize lead capture forms |
| `popup-cro` | Optimize popups/modals |
| `paywall-upgrade-cro` | Optimize in-app paywalls |
| `ab-test-setup` | Design and run experiments |
| `analytics-tracking` | Set up event tracking |
| `churn-prevention` | Build cancellation flows |
| `referral-program` | Create referral mechanisms |

## Workflows

### 1. Page CRO Loop

```
1. Query content_assets for published pages
2. Run page-cro skill to identify improvement opportunities
3. Generate variant copy/design with copywriting skill
4. Run ab-test-setup to configure experiment
5. Implement variant on page
6. Monitor conversion lift
7. If winner (p < 0.05) → implement permanently
8. If loser → retire variant, learn from signals
```

### 2. Onboarding Optimization

```
1. Query events for signup → activation funnel
2. Identify drop-off points
3. Run onboarding-cro skill to generate improvements
4. Implement changes (copy, UX, timing)
5. Track time-to-value improvement
6. Report activation rate lift
```

### 3. Form CRO

```
1. Identify forms with < 20% completion rate
2. Run form-cro skill to audit friction points
3. Generate recommendations (field reduction, copy, validation)
4. Implement changes
5. Track completion rate improvement
6. A/B test major changes with ab-test-setup
```

### 4. Analytics Event Setup

```
1. User requests tracking for action X
2. Run analytics-tracking skill to define event schema
3. Generate tracking code snippet
4. Deploy to relevant pages/components
5. Verify events flowing to database
6. Create dashboard for event monitoring
```

### 5. Churn Prevention

```
IF: User initiates cancellation flow
THEN:
  1. Run churn-prevention skill
  2. Identify cancellation reason
  3. Present targeted save offer
  4. If payment failed → run dunning flow
  5. If save successful → update subscription status
  6. If cancelled → exit survey, learn from signals
```

## Approval Gates

| Action | Autonomous | Human Approval |
|--------|------------|----------------|
| Implement CRO copy changes | ✅ | — |
| Launch A/B test (traffic < 50%) | ✅ | — |
| Optimize form fields | ✅ | — |
| Set up analytics events | ✅ | — |
| **Launch to 100% traffic** | — | ✅ Required |
| **Remove high-traffic page elements** | — | ✅ Required |
| **Change pricing display** | — | ✅ Required |
| **Modify checkout flow** | — | ✅ Required |

## Example Prompts

```
"Optimize this landing page for conversions"
→ Uses page-cro skill

"Set up A/B test for our new headline"
→ Uses ab-test-setup + analytics-tracking skills

"Improve our signup form completion rate"
→ Uses form-cro + signup-flow-cro skills

"Build a cancellation flow with save offers"
→ Uses churn-prevention skill

"Track when users click the upgrade button"
→ Uses analytics-tracking skill
```

## Integration Points

| FullStackArkham Service | How FulfillmentOps Uses It |
|------------------------|---------------------------|
| **Gateway** | Inference for copy generation, CRO recommendations |
| **Memory** | Experiment history, win patterns by page type |
| **Semantic Cache** | Cache CRO patterns, successful variants |
| **Orchestration** | Multi-step experiment workflows |
| **Database** | content_assets, events, tasks tables |

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Page Conversion Rate | > 5% | Via analytics-tracking |
| A/B Test Win Rate | > 40% | Experiments with significant lift |
| Form Completion Rate | > 60% | Lead capture forms |
| Activation Rate | > 50% | Signup → first value |
| Churn Save Rate | > 25% | Cancellation → retained |
| On-Time Delivery | > 95% | Projects/orders delivered by deadline |

## Related Agents

- **ContentEngine™** - Creates content that FulfillmentOps optimizes
- **DealFlow™** - Receives optimized landing pages for lead capture
- **ComplianceGate™** - Validates A/B tests don't violate policies
- **MediaCommerce™** - Receives EPC data for content optimization decisions
- **ChiefPulse™** - Synthesizes experiment results for executive reporting

## Database Schema

```sql
-- Content asset with performance tracking
content_assets (
    id, tenant_id, vertical, type, title,
    status, performance,  -- {views, clicks, conversions, epc}
    created_at, updated_at
)

-- Analytics events
events (
    id, tenant_id, vertical, event_type,
    account_id, content_asset_id, event_data,
    created_at
)

-- Tasks for delivery tracking
tasks (
    id, tenant_id, vertical, type,
    assigned_to, status, priority, due_date,
    created_at, updated_at
)

-- Orders for fulfillment tracking
orders (
    id, tenant_id, account_id, vertical,
    status, total, fulfillment_data,
    created_at, updated_at
)
```

## Policy Enforcement

FulfillmentOps enforces these policies:

1. **content_epc_retirement**: Auto-retire content with EPC < $2.50 for 7 days
   - Query content_assets for underperformers
   - Change status to 'retired'
   - Reallocate traffic to winners

2. **experiment_guardrails**: A/B tests must have min. 100 conversions per variant
   - Validate before launching test
   - Auto-stop tests that won't reach significance

3. **sla_monitoring**: Flag deliveries at risk of SLA breach
   - Query tasks/orders with approaching due dates
   - Escalate to human if at-risk
   - Auto-reassign if contractor non-responsive

## CRO Recommendations Engine

FulfillmentOps generates CRO recommendations using this framework:

```
1. AUDIT: Run page-cro/form-cro/onboarding-cro skill
2. IDENTIFY: List friction points and opportunities
3. PRIORITIZE: Score by impact × confidence × effort
4. GENERATE: Create variant with copywriting skill
5. TEST: Run ab-test-setup for high-impact changes
6. IMPLEMENT: Roll out winners
7. LEARN: Store results in Memory for future optimization
```
