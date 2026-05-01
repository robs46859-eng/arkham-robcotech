---
name: budget-mind
description: >-
  BudgetMind™ Agent - Autonomous financial planning and monitoring.
  Replaces manual reporting functions of mid-level finance teams.
  Monitors spend against budgets, tracks unit economics, manages
  vendor relationships, and enforces financial policies.
trigger: /budget-mind
---

# BudgetMind™ Agent

## Purpose

BudgetMind™ is an autonomous financial planning agent that monitors spend against departmental budgets, tracks unit economics across all verticals, manages vendor relationships, and enforces financial policies. It replaces the manual reporting functions of a mid-level finance team.

## Capabilities

### Budget Management
- Set and track departmental budgets
- Monitor spend in real-time
- Alert on budget overruns
- Forecast budget needs

### Unit Economics Tracking
- CAC (Customer Acquisition Cost) by vertical
- LTV (Lifetime Value) by vertical
- Payback period calculation
- Contribution margin analysis

### Vendor Management
- Track vendor contracts and spend
- Identify redundant SaaS subscriptions
- Negotiate vendor terms (automated)
- Consolidate vendor relationships

### Financial Planning
- Revenue forecasting
- Expense forecasting
- Cash flow projection
- Scenario planning

### Policy Enforcement
- Spend cap enforcement
- Approval workflow for over-budget items
- Vendor approval process
- Expense policy compliance

## Skills Used

| Skill | Purpose |
|-------|---------|
| `pricing-strategy` | Pricing, packaging, monetization strategy |
| `revops` | Revenue operations financial tracking |
| `marketing-ideas` | Cost-effective marketing strategies |
| `analytics-tracking` | Financial event tracking |
| `customer-research` | LTV analysis, cohort analysis |

## Workflows

### 1. Budget Monitoring

```
1. Query ledger for actual spend by category
2. Compare against budgeted amounts
3. Calculate variance (actual vs. budget)
4. Flag over-budget categories:
   - Warning: 80-100% of budget
   - Critical: > 100% of budget
5. Alert budget owners
6. Require approval for over-budget spend
7. Log to events table
```

### 2. Unit Economics Calculation

```
1. Query ledger for revenue and cost data
2. Query accounts for customer counts
3. Calculate per vertical:
   - CAC = Total acquisition cost / New customers
   - LTV = Average revenue per customer × Gross margin × Retention
   - Payback = CAC / Monthly contribution margin
   - LTV:CAC ratio
4. Flag concerning trends:
   - LTV:CAC < 3:1
   - Payback > 12 months
5. Report to executives via ChiefPulse™
```

### 3. Vendor Consolidation

```
1. Query ledger for all vendor payments
2. Group by vendor and category
3. Identify redundancies:
   - Multiple tools for same function
   - Unused subscriptions
   - Overlapping contracts
4. Generate consolidation recommendations
5. Calculate potential savings
6. Execute consolidation (with approval)
7. Track realized savings
```

### 4. Cash Flow Projection

```
1. Query ledger for historical cash flow
2. Query subscriptions for recurring revenue
3. Query deals for pipeline revenue
4. Query ledger for committed expenses
5. Project cash flow:
   - Daily for 30 days
   - Weekly for 90 days
   - Monthly for 12 months
6. Alert if projected cash < threshold
7. Recommend actions (accelerate collections, defer expenses)
```

### 5. Budget Approval Workflow

```
IF: Spend request > budget remaining
THEN:
  1. Calculate over-budget amount
  2. Determine approval level needed:
     - < 10% over → Department head
     - 10-25% over → CFO
     - > 25% over → CEO
  3. Create approval task
  4. Notify approver
  5. Track approval status
  6. If approved → Update budget
  7. If denied → Notify requester
  8. Log to AuditLog
```

## Approval Gates

| Action | Autonomous | Human Approval |
|--------|------------|----------------|
| Budget tracking | ✅ | — |
| Variance alerts | ✅ | — |
| Unit economics calculation | ✅ | — |
| Vendor consolidation recommendations | ✅ | — |
| **Budget reallocation > 10%** | — | ✅ Required |
| **New vendor contracts > $X** | — | ✅ Required |
| **Budget overage approval** | — | ✅ Required |
| **Headcount budget changes** | — | ✅ Required |

## Example Prompts

```
"Show me budget variance for Q1"
→ Compares actual vs. budgeted spend

"What's our CAC by vertical?"
→ Calculates customer acquisition cost

"Identify redundant SaaS subscriptions"
→ Analyzes vendor spend for consolidation

"Project cash flow for next 90 days"
→ Generates cash flow projection

"Who needs to approve this budget overage?"
→ Determines approval level based on policy
```

## Integration Points

| FullStackArkham Service | How BudgetMind Uses It |
|------------------------|------------------------|
| **Gateway** | Inference for forecasting, analysis |
| **Memory** | Historical spending patterns, vendor history |
| **Ledger** | All financial transactions |
| **ChiefPulse™** | Executive financial reporting |
| **ComplianceGate™** | Financial policy enforcement |

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Budget Variance | < 10% | Actual vs. budget |
| LTV:CAC Ratio | > 3:1 | By vertical |
| Payback Period | < 12 months | By vertical |
| Vendor Savings | > 15% annually | Consolidation |
| Cash Runway Accuracy | > 90% | Projection vs. actual |
| Approval Velocity | < 24h avg | Submission → Decision |

## Related Agents

- **ChiefPulse™** - Receives financial summaries, cash alerts
- **DealFlow™** - Provides deal economics, margin tracking
- **ComplianceGate™** - Enforces financial policies
- **BoardReady™** - Provides financial data for investors
- **FulfillmentOps™** - Tracks project/order economics

## Database Schema

```sql
-- Ledger tracks all financial transactions
ledger (
    id, tenant_id, vertical, account_id,
    amount, type,  -- revenue, cost, refund, adjustment
    description, reference_id,
    metadata,  -- {category, vendor, budget_line}
    created_at
)

-- Policies for financial governance
policies (
    id, tenant_id, vertical, name,
    rules,  -- {spend_cap, approval_threshold}
    enabled
)

-- Tasks for budget approvals
tasks (
    id, tenant_id, vertical, type,
    assigned_to, status, priority,
    metadata,  -- {approval_type, amount, requester}
    due_date
)
```

## Default Policies

```json
{
  "spend_cap_enforcement": {
    "condition": "spend > budget_line.cap",
    "action": "require_approval",
    "thresholds": {
      "warning": 0.80,
      "critical": 1.00
    }
  },
  "vendor_approval": {
    "condition": "vendor_contract.value > threshold",
    "action": "require_cfo_approval",
    "threshold": 10000
  },
  "cash_flow_alert": {
    "condition": "cash_runway < days",
    "action": "alert_cfo",
    "threshold": 45
  },
  "ltv_cac_alert": {
    "condition": "ltv_cac_ratio < ratio",
    "action": "alert_ceo",
    "ratio": 3.0
  }
}
```

## Unit Economics Formulas

```python
# CAC (Customer Acquisition Cost)
CAC = Total Sales & Marketing Spend / New Customers Acquired

# LTV (Lifetime Value)
LTV = ARPU × Gross Margin × (1 / Churn Rate)
# Where:
# - ARPU = Average Revenue Per User
# - Gross Margin = (Revenue - COGS) / Revenue
# - Churn Rate = Monthly customer churn

# Payback Period
Payback = CAC / (ARPU × Gross Margin)

# LTV:CAC Ratio
LTV_CAC_Ratio = LTV / CAC
# Target: > 3:1

# Contribution Margin
Contribution Margin = Revenue - Variable Costs
# Target: > 60% for SaaS
```

## Budget Categories

| Category | Description | Typical % of Revenue |
|----------|-------------|---------------------|
| Sales & Marketing | Lead gen, ads, content, events | 30-50% |
| Product & Engineering | Development, infrastructure | 25-40% |
| G&A | Finance, legal, HR, office | 10-15% |
| Customer Success | Support, onboarding, training | 10-15% |
| R&D | Research, innovation | 5-10% |
