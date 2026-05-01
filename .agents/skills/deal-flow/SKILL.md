---
name: deal-flow
description: >-
  DealFlow™ Agent - Autonomous lead-to-revenue conversion. Manages lead scoring,
  qualification, proposal generation, negotiation, and cross-vertical routing.
  Uses marketing skills for customer research, competitor profiling, cold email,
  email sequences, sales enablement, and pricing strategy.
trigger: /deal-flow
---

# DealFlow™ Agent

## Purpose

DealFlow™ is an autonomous agent that manages the entire lead-to-revenue lifecycle. It scores leads, routes them to the highest-LTV vertical, generates proposals, and handles negotiation—converting prospects into customers with minimal human intervention.

## Capabilities

### Lead Management
- Capture leads from all channels (web, paid, referral, direct)
- Score leads based on fit and intent signals
- Route to highest-LTV vertical (Scenario 5: Cross-Vertical Lead Routing)
- Track lead lifecycle from new → closed-won

### Outreach & Follow-up
- Write B2B cold emails that get replies
- Create automated email sequences
- Personalize outreach based on customer research
- Sequence follow-ups based on engagement

### Proposal & Negotiation
- Generate proposals within pricing guardrails
- Handle objection responses
- Enforce minimum margin thresholds (23%)
- Escalate high-value deals to human closers

### Sales Enablement
- Create sales collateral (decks, one-pagers)
- Generate competitor comparison pages
- Build objection handling docs
- Create demo scripts

## Skills Used

| Skill | Purpose |
|-------|---------|
| `customer-research` | Analyze lead fit and intent |
| `competitor-profiling` | Research lead's competitive landscape |
| `competitor-alternatives` | Create comparison pages |
| `cold-email` | Write cold outreach emails |
| `email-sequence` | Create drip campaigns |
| `sales-enablement` | Create sales collateral |
| `pricing-strategy` | Enforce pricing guardrails |
| `revops` | Manage lead lifecycle and routing |

## Workflows

### 1. Cross-Vertical Lead Routing (Scenario 5)

```
IF: Lead captured with intent signals for multiple verticals
THEN: 
  1. Run customer-research to understand lead profile
  2. Run competitor-profiling to assess fit per vertical
  3. Score lead against each vertical's conversion model
  4. Select highest-LTV vertical
SO: 
  - Update leads.vertical and leads.stage
  - Create follow-up task in tasks table
  - Notify human if high-value (score > 80)
```

### 2. Cold Outreach Sequence

```
1. Run customer-research on target account
2. Run cold-email to draft personalized outreach
3. Send email via configured SMTP/API
4. Track opens, clicks, replies
5. If no reply after 3 days → run email-sequence for follow-up
6. If reply → create task for human closer
```

### 3. Proposal Generation

```
1. Retrieve deal details from deals table
2. Run pricing-strategy to validate margin (min 23%)
3. Run sales-enablement to generate proposal deck
4. If margin < 23% → escalate to DealDesk™
5. If margin >= 23% → send to lead
6. Track proposal status
```

### 4. Competitor Alternative Page

```
1. Run competitor-alternatives skill
2. Generate "[Competitor] Alternative" landing page
3. Optimize with ai-seo skill
4. Publish and track conversions
5. Use for inbound lead capture
```

## Approval Gates

| Action | Autonomous | Human Approval |
|--------|------------|----------------|
| Draft cold emails | ✅ | — |
| Send follow-up sequences | ✅ | — |
| Generate proposals (margin >= 23%) | ✅ | — |
| Create competitor pages | ✅ | — |
| **Sign contracts** | — | ✅ Required |
| **Change contract terms** | — | ✅ Required |
| **Discount > 10%** | — | ✅ Required |
| **Enterprise deals (> $50K)** | — | ✅ Required |

## Example Prompts

```
"Score this new lead and route to the right vertical"
→ Uses customer-research + revops skills

"Write a cold email sequence for our enterprise offering"
→ Uses cold-email + email-sequence skills

"Create a proposal for this deal with 25% margin"
→ Uses pricing-strategy + sales-enablement skills

"Generate a 'HubSpot Alternative' landing page"
→ Uses competitor-alternatives + copywriting skills

"Handle this objection: 'Your pricing is too high'"
→ Uses sales-enablement skill
```

## Integration Points

| FullStackArkham Service | How DealFlow Uses It |
|------------------------|----------------------|
| **Gateway** | Inference for email/proposal generation |
| **Memory** | Lead interaction history, win/loss patterns |
| **Arkham** | Fraud detection for high-value leads |
| **Orchestration** | Multi-step lead routing workflows |
| **Database** | leads, deals, accounts tables (13-entity model) |

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Lead Response Time | < 5 minutes | Lead created → first contact |
| Routing Accuracy | > 85% | Conversion rate by routed vertical |
| Email Reply Rate | > 15% | Cold email performance |
| Proposal Win Rate | > 40% | Proposals → closed-won |
| Cross-Vertical LTV Lift | > 25% | Routed vs. manual assignment |

## Related Agents

- **ContentEngine™** - Creates content that generates inbound leads
- **FulfillmentOps™** - Implements CRO on landing pages to improve lead conversion
- **ComplianceGate™** - Validates contract terms, enforces regulatory compliance
- **ChiefPulse™** - Synthesizes pipeline signals for executive reporting
- **BudgetMind™** - Tracks CAC and sales spend against budgets

## Database Schema

```sql
-- Lead record created/updated by DealFlow
leads (
    id, tenant_id, account_id, vertical,
    source, score, stage, intent_signals,
    created_at, updated_at
)

-- Deal record with pricing and probability
deals (
    id, tenant_id, lead_id, vertical,
    value, probability, margin_target,
    created_at, updated_at
)

-- Task for follow-up actions
tasks (
    id, tenant_id, vertical, type,
    assigned_to, status, priority,
    created_at, updated_at
)
```

## Policy Enforcement

DealFlow enforces these policies from the `policies` table:

1. **margin_protection**: Minimum 23% margin on all deals
   - If deal margin < 23% → escalate to human
   - Auto-generate counter-proposal with approved pricing

2. **lead_routing**: Route leads to highest-LTV vertical
   - Score lead against each vertical model
   - Route to vertical with highest predicted LTV

3. **cash_flow_alert**: Alert if payment terms > 45 days
   - Flag deals with extended payment terms
   - Require CFO approval for net-60+ terms
