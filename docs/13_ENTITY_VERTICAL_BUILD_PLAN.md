# Unified AI Command Center - 13 Entity Vertical Build Plan

**Vertical Name:** `stack-arkham/media-commerce`
**Based On:** marketingskills (40 marketing agent skills)
**Target:** Scenario 5 - Cross-Vertical Lead Routing

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UNIFIED AI COMMAND CENTER                            │
│                         (Agent's Cockpit)                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ ContentEng  │  │  DealFlow   │  │ FulfillOps  │  │ Compliance  │   │
│  │   Agent     │  │   Agent     │  │   Agent     │  │   Agent     │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                │                │                │           │
│         └────────────────┴────────────────┴────────────────┘           │
│                              │                                          │
│                     ┌────────▼────────┐                                 │
│                     │  13-Entity DB   │                                 │
│                     │  Shared Layer   │                                 │
│                     └────────┬────────┘                                 │
│                              │                                          │
│         ┌────────────────────┼────────────────────┐                     │
│         │                    │                    │                     │
│    ┌────▼────┐        ┌─────▼─────┐       ┌──────▼──────┐             │
│    │ Studio  │        │ E-commerce│       │    SaaS     │             │
│    │ Vertical│        │  Vertical │       │   Vertical  │             │
│    └─────────┘        └───────────┘       └─────────────┘             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 13-Entity Shared Data Model

### Entity Schema (PostgreSQL)

```sql
-- 1. Account (Customer/Employer contacts)
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vertical VARCHAR(50) NOT NULL,  -- studio, ecom, saas, staffing, media
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50),  -- client, buyer, subscriber, employer
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Lead (Source, score, stage)
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    source VARCHAR(100),
    score INTEGER DEFAULT 0,
    stage VARCHAR(50) DEFAULT 'new',  -- new, qualified, proposal, negotiation, closed_won, closed_lost
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Deal (Pricing, probability, contract link)
CREATE TABLE deals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    vertical VARCHAR(50) NOT NULL,
    value DECIMAL(12,2),
    probability FLOAT DEFAULT 0,
    contract_url TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Order (Cart, SKU, fulfillment status)
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',  -- pending, processing, fulfilled, shipped, delivered
    total DECIMAL(12,2),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Subscription (SaaS Access Model)
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    plan VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active',
    start_date DATE,
    end_date DATE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Project (Facility Onboarding / Creative Projects)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'planning',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Placement (Deployment Data)
CREATE TABLE placements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Candidate (Talent Profiles / Influencers / Trial Users)
CREATE TABLE candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vertical VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    skills TEXT[],
    score INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. ContentAsset (Topic, keyword cluster, performance)
CREATE TABLE content_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vertical VARCHAR(50) NOT NULL,
    type VARCHAR(50),  -- article, video, social, ad, portfolio, job_post
    title VARCHAR(255),
    topic VARCHAR(100),
    keywords TEXT[],
    performance JSONB DEFAULT '{}',  -- {views, clicks, conversions, epc}
    status VARCHAR(50) DEFAULT 'draft',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Task (Work Items)
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vertical VARCHAR(50) NOT NULL,
    type VARCHAR(50),  -- ai_autonomous, human_approval_required, ai_assisted
    status VARCHAR(50) DEFAULT 'pending',
    assigned_to VARCHAR(100),  -- agent name or human user
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Event (Analytics Events)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vertical VARCHAR(50) NOT NULL,
    event_type VARCHAR(100),
    account_id UUID,
    candidate_id UUID,
    content_asset_id UUID,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. Ledger (Transactions)
CREATE TABLE ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vertical VARCHAR(50) NOT NULL,
    account_id UUID REFERENCES accounts(id),
    amount DECIMAL(12,2),
    type VARCHAR(50),  -- revenue, cost, refund
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 13. Policy (Guardrails)
CREATE TABLE policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vertical VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    rules JSONB NOT NULL,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Agent Architecture

### Primary Agents (4)

| Agent | Purpose | Marketing Skills Used |
|-------|---------|----------------------|
| **ContentEngine™** | Content creation, SEO, distribution | content-strategy, copywriting, ai-seo, programmatic-seo, social-content, ad-creative, video, image |
| **DealFlow™** | Lead-to-revenue conversion | customer-research, competitor-profiling, cold-email, email-sequence, sales-enablement, pricing-strategy |
| **FulfillmentOps™** | Delivery & fulfillment | analytics-tracking, ab-test-setup, page-cro, signup-flow-cro, onboarding-cro, form-cro, popup-cro, paywall-upgrade-cro |
| **ComplianceGate™** | Regulatory & risk | seo-audit, schema-markup, aso-audit, churn-prevention, revops |

### Supporting Agents (5)

| Agent | Purpose | Marketing Skills Used |
|-------|---------|----------------------|
| **ChiefPulse™** | Signal synthesis | marketing-ideas, marketing-psychology |
| **BudgetMind™** | Financial planning | pricing-strategy, revops |
| **BoardReady™** | Investor relations | launch-strategy, competitor-alternatives |
| **TalentMatch™** | Candidate/influencer matching | customer-research, competitor-profiling |
| **MediaCommerce™** | Algorithmic relevance arbitrage | ai-seo, programmatic-seo, paid-ads, ad-creative, referral-program, free-tool-strategy, lead-magnets |

---

## Scenario 5: Cross-Vertical Lead Routing Implementation

```
IF: Lead captured with intent signals for multiple verticals
THEN: Score against each vertical's conversion model
SO: Route to highest-LTV vertical, create tasks for follow-up
```

### Implementation Steps

1. **Lead Capture Endpoint** (`POST /api/v1/leads`)
   - Accepts lead data with intent signals
   - Stores in `leads` table with `vertical = null`

2. **Scoring Engine** (ContentEngine Agent)
   - Runs lead through each vertical's scoring model
   - Uses `customer-research` skill for intent analysis
   - Uses `competitor-profiling` for fit analysis

3. **Routing Logic** (DealFlow Agent)
   - Selects highest-score vertical
   - Updates `leads.vertical` and `leads.stage`
   - Creates follow-up task in `tasks` table

4. **Notification** (ChiefPulse Agent)
   - Logs event to `events` table
   - Notifies human if high-value lead

---

## Media-to-Commerce Engine Implementation

### Workflow Loop

```
1. KEYWORD CLUSTERING (ai-seo + programmatic-seo)
   → AI identifies high-intent, low-competition topics

2. DRAFT (ContentEngine + copywriting + content-strategy)
   → Generates article/video/script

3. PUBLISH (FulfillmentOps)
   → Auto-publishes to channels, creates content_asset record

4. MONITOR (analytics-tracking)
   → Tracks EPC in real-time, stores in content_assets.performance

5. OPTIMIZE (MediaCommerce Agent)
   → IF EPC < threshold: Auto-swap affiliate placement
   → IF EPC > threshold: Create variations via ad-creative

6. REPURPOSE (ContentEngine + social-content + video)
   → Top performers → Email, Social, Paid ads
   → Underperformers → Retire, learn from signals
```

---

## File Structure

```
FullStackArkham/
├── services/
│   └── media-commerce/          # New vertical service
│       ├── app/
│       │   ├── main.py          # FastAPI entry point
│       │   ├── agents/
│       │   │   ├── content_engine.py
│       │   │   ├── deal_flow.py
│       │   │   ├── fulfillment_ops.py
│       │   │   ├── compliance_gate.py
│       │   │   ├── chief_pulse.py
│       │   │   ├── budget_mind.py
│       │   │   ├── board_ready.py
│       │   │   ├── talent_match.py
│       │   │   └── media_commerce.py
│       │   ├── skills/          # Copied from marketingskills
│       │   │   ├── product-marketing-context/
│       │   │   ├── content-strategy/
│       │   │   ├── copywriting/
│       │   │   ├── ai-seo/
│       │   │   └── ... (all 40 skills)
│       │   ├── models/          # SQLAlchemy models for 13 entities
│       │   ├── routers/
│       │   │   ├── leads.py
│       │   │   ├── content.py
│       │   │   ├── analytics.py
│       │   └── settings.py
│       ├── tests/
│       ├── Dockerfile
│       └── pyproject.toml
├── apps/
│   └── web/
│       └── src/
│           └── app/
│               └── dashboard/   # Executive Overview UI
│                   ├── page.tsx
│                   ├── leads/
│                   ├── revenue/
│                   ├── operations/
│                   ├── finance/
│                   └── risk/
├── infra/
│   ├── docker/
│   │   └── postgres/
│   │       └── init-verticals.sql  # 13-entity schema
│   └── k8s/
│       └── media-commerce-deployment.yaml
└── docs/
    ├── AGENTS.md              # Agent documentation
    └── SKILLS/                # Agent skill files
        ├── content-engine/
        ├── deal-flow/
        ├── fulfillment-ops/
        └── ...
```

---

## Build Phases

### Phase 1: Foundation (Days 1-3)
- [ ] Create 13-entity database schema
- [ ] Set up media-commerce service skeleton
- [ ] Copy marketing skills to service
- [ ] Create base agent classes

### Phase 2: ContentEngine Agent (Days 4-7)
- [ ] Implement content-strategy skill integration
- [ ] Implement copywriting skill integration
- [ ] Implement ai-seo + programmatic-seo
- [ ] Create ContentAsset CRUD endpoints

### Phase 3: DealFlow Agent (Days 8-10)
- [ ] Implement customer-research skill
- [ ] Implement cold-email + email-sequence
- [ ] Implement lead scoring logic
- [ ] Create cross-vertical routing (Scenario 5)

### Phase 4: FulfillmentOps Agent (Days 11-14)
- [ ] Implement page-cro + ab-test-setup
- [ ] Implement analytics-tracking
- [ ] Create CRO recommendation engine

### Phase 5: MediaCommerce Engine (Days 15-18)
- [ ] Implement EPC tracking
- [ ] Implement auto-optimization logic
- [ ] Implement repurposing workflow

### Phase 6: Executive Dashboard (Days 19-21)
- [ ] Build Next.js dashboard UI
- [ ] Implement real-time data feeds
- [ ] Create approval queue UI

---

## Agent Skill Files

Each agent gets a SKILL.md file in `.agents/skills/`:

```
.agents/
└── skills/
    ├── content-engine/
    │   └── SKILL.md
    ├── deal-flow/
    │   └── SKILL.md
    ├── fulfillment-ops/
    │   └── SKILL.md
    └── ...
```

Each SKILL.md includes:
- Agent purpose and capabilities
- Which marketing skills it uses
- Example prompts and workflows
- Approval gate configuration

---

## Integration with FullStackArkham Backbone

| FullStackArkham Service | How Media-Commerce Uses It |
|------------------------|---------------------------|
| **Gateway** | Inference for content generation, lead scoring |
| **Arkham** | Fraud detection for leads, account security |
| **Orchestration** | Workflow execution for all agent actions |
| **Memory (A-MEM)** | Cross-vertical learning, content performance history |
| **Semantic Cache** | Cache SEO queries, content recommendations |
| **Billing** | Usage metering per vertical, per agent |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Content EPC | > $5.00 | Real-time via analytics-tracking |
| Lead Routing Accuracy | > 85% | Conversion rate by routed vertical |
| Autonomous Task % | > 60% | Tasks completed without human approval |
| Cross-Vertical LTV Lift | > 25% | LTV comparison: routed vs. manual |

---

*This plan integrates 40 marketing skills as autonomous agents within the FullStackArkham backbone, targeting Scenario 5 (Cross-Vertical Lead Routing) and the Media-to-Commerce Engine.*
