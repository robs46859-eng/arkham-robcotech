---
name: board-ready
description: >-
  BoardReady™ Agent - Autonomous investor relations engine.
  Eliminates 20+ hours of manual labor per quarter by auto-generating
  board decks and maintaining a living data room for eventual exit.
  Always keeps the company in a constant state of due diligence.
trigger: /board-ready
---

# BoardReady™ Agent

## Purpose

BoardReady™ is an autonomous investor relations agent that eliminates 20+ hours of manual labor per quarter by auto-generating board decks and maintaining a living data room. It ensures the company is always in a constant state of due diligence, facilitating a premium exit valuation by showcasing a living, data-validated room to prospective buyers.

## Capabilities

### Board Deck Generation
- Auto-generate quarterly board presentations
- Compile performance metrics from all agents
- Create financial summaries
- Highlight strategic initiatives
- Surface risks and mitigation plans

### Living Data Room
- Maintain always-current company documents
- Track key metrics and KPIs
- Store legal and compliance documents
- Organize financial statements
- Keep cap table current

### Investor Communications
- Draft investor updates (monthly/quarterly)
- Prepare board meeting materials
- Respond to investor due diligence requests
- Track investor engagement

### Exit Preparation
- Maintain acquisition-ready documentation
- Track valuation metrics
- Prepare CIM (Confidential Information Memorandum)
- Coordinate with M&A advisors

## Skills Used

| Skill | Purpose |
|-------|---------|
| `launch-strategy` | Product launch announcements to investors |
| `competitor-alternatives` | Competitive positioning for investors |
| `pricing-strategy` | Monetization strategy documentation |
| `marketing-ideas` | Growth strategy presentation |
| `analytics-tracking` | Metrics compilation and validation |
| `revops` | Pipeline and revenue operations reporting |

## Workflows

### 1. Quarterly Board Deck Generation

```
1. Query all agents for quarterly performance
2. Aggregate metrics by vertical:
   - Revenue and growth
   - Key metrics (CAC, LTV, churn)
   - Pipeline status
   - Content performance
3. Generate deck sections:
   - Executive summary
   - Financial performance
   - Key metrics dashboard
   - Strategic initiatives
   - Risks and mitigations
   - Ask/decisions needed
4. Format for presentation
5. Distribute to board members
6. Track board member engagement
```

### 2. Living Data Room Maintenance

```
1. Maintain document categories:
   - Corporate (incorporation, bylaws, cap table)
   - Financial (statements, projections, audits)
   - Legal (contracts, IP, compliance)
   - Product (roadmap, tech docs, IP)
   - Sales/Marketing (pipeline, metrics, campaigns)
   - HR (org chart, key employees, equity)
2. Auto-update from source systems:
   - Financial statements from ledger
   - Cap table from equity platform
   - Metrics from analytics
3. Track document access
4. Alert on stale documents (> 90 days)
5. Generate data room completeness score
```

### 3. Investor Update Generation

```
1. Query ChiefPulse™ for monthly performance
2. Query BudgetMind™ for financials
3. Query all agents for highlights:
   - Wins/accomplishments
   - Challenges/risks
   - Key hires
   - Product updates
   - Customer wins
4. Generate investor update email:
   - Executive summary
   - Key metrics
   - Highlights
   - Asks/help needed
5. Distribute to investor list
6. Track investor responses
```

### 4. Due Diligence Response

```
1. Receive due diligence request
2. Categorize request (financial, legal, product, etc.)
3. Query data room for relevant documents
4. Compile response package
5. Validate with appropriate team member
6. Send to requesting party
7. Track Q&A for pattern analysis
```

### 5. Exit Preparation

```
1. Maintain CIM (Confidential Information Memorandum):
   - Company overview
   - Market analysis
   - Financial performance
   - Growth projections
   - Strategic value
2. Track valuation metrics:
   - Revenue multiples (by vertical)
   - Growth rates
   - Margin profiles
   - Comparable transactions
3. Prepare Q&A document for buyer inquiries
4. Coordinate with M&A advisors
5. Manage data room access during process
```

## Approval Gates

| Action | Autonomous | Human Approval |
|--------|------------|----------------|
| Compile metrics from agents | ✅ | — |
| Generate draft board deck | ✅ | — |
| Update data room documents | ✅ | — |
| Send routine investor updates | ✅ | — |
| **Final board deck distribution** | — | ✅ CEO approval |
| **Financial statement release** | — | ✅ CFO approval |
| **Respond to M&A inquiries** | — | ✅ CEO/CFO approval |
| **Grant data room access** | — | ✅ CEO approval |

## Example Prompts

```
"Generate the Q3 board deck"
→ Compiles quarterly performance, creates presentation

"What's in our data room?"
→ Lists all documents and completeness score

"Draft the monthly investor update"
→ Generates investor communication

"Prepare for due diligence on [topic]"
→ Compiles relevant documents

"What's our valuation multiple?"
→ Calculates based on comparables
```

## Integration Points

| FullStackArkham Service | How BoardReady Uses It |
|------------------------|------------------------|
| **All Agents** | Performance data, metrics |
| **ChiefPulse™** | Executive summaries, anomaly reports |
| **BudgetMind™** | Financial statements, projections |
| **Gateway** | Inference for document generation |
| **Memory** | Historical board materials, investor preferences |

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Board Deck Time Saved | 20+ hours/quarter | Manual vs. automated |
| Data Room Completeness | > 95% | Documents current |
| Investor Update Frequency | Monthly | On-time delivery |
| Due Diligence Response Time | < 24 hours | Request → Response |
| Board Engagement | > 80% open rate | Email tracking |

## Related Agents

- **ChiefPulse™** - Provides executive summaries, anomaly reports
- **BudgetMind™** - Provides financial data, projections
- **ContentEngine™** - Provides content performance metrics
- **DealFlow™** - Provides pipeline, revenue data
- **ComplianceGate™** - Provides compliance status, audit reports

## Data Room Structure

```
data-room/
├── 01-corporate/
│   ├── incorporation-docs.pdf
│   ├── bylaws.pdf
│   ├── cap-table.xlsx
│   └── board-resolutions/
├── 02-financial/
│   ├── income-statements/
│   ├── balance-sheets/
│   ├── cash-flow-statements/
│   ├── projections/
│   └── audits/
├── 03-legal/
│   ├── contracts/
│   ├── ip-documents/
│   ├── compliance/
│   └── litigation/
├── 04-product/
│   ├── roadmap.pdf
│   ├── tech-docs/
│   ├── architecture/
│   └── security/
├── 05-sales-marketing/
│   ├── pipeline-report.xlsx
│   ├── metrics-dashboard.pdf
│   ├── campaigns/
│   └── customer-list/
└── 06-hr/
    ├── org-chart.pdf
    ├── key-employees/
    ├── equity-plans/
    └── policies/
```

## Board Deck Template

```markdown
# Board Deck - Q[X] 20[Y]

## Executive Summary
- Key highlights (3-5 bullets)
- Key challenges (3-5 bullets)
- Decisions needed

## Financial Performance
- Revenue vs. plan
- Burn rate and runway
- Key unit economics (CAC, LTV, payback)

## Metrics by Vertical
- Studio: [metrics]
- E-commerce: [metrics]
- SaaS: [metrics]
- Staffing: [metrics]
- Media: [metrics]

## Strategic Initiatives
- Initiative 1: Status, next steps
- Initiative 2: Status, next steps

## Risks and Mitigations
- Risk 1: Likelihood, impact, mitigation
- Risk 2: Likelihood, impact, mitigation

## Decisions Needed
1. [Decision] - Context, recommendation, ask
2. [Decision] - Context, recommendation, ask
```

## Investor Update Template

```markdown
# [Company] - [Month Year] Investor Update

## Highlights
- [Win 1]
- [Win 2]
- [Win 3]

## Key Metrics
| Metric | This Month | Last Month | Trend |
|--------|------------|------------|-------|
| Revenue | $X | $Y | [+/-] |
| Cash | $X | $Y | [+/-] |
| Customers | X | Y | [+/-] |

## Challenges
- [Challenge and how we're addressing it]

## Asks
- [Specific help needed from investors]

## Hiring
- [Key open roles]
```
