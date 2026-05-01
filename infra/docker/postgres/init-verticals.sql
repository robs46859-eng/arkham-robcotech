-- ============================================================================
-- 13-ENTITY SHARED DATA MODEL
-- Unified AI Command Center - Media & Commerce Vertical
-- ============================================================================

-- 1. ACCOUNT (Customer/Employer contacts - All businesses)
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    vertical VARCHAR(50) NOT NULL,  -- studio, ecom, saas, staffing, media
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50),  -- client, buyer, subscriber, employer, advertiser
    email VARCHAR(255),
    phone VARCHAR(50),
    status VARCHAR(50) DEFAULT 'active',  -- active, inactive, churned
    ltv DECIMAL(12,2) DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_accounts_tenant ON accounts(tenant_id);
CREATE INDEX idx_accounts_vertical ON accounts(vertical);
CREATE INDEX idx_accounts_type ON accounts(type);
CREATE INDEX idx_accounts_status ON accounts(status);

-- 2. LEAD (Source, score, stage - All businesses)
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    source VARCHAR(100),  -- organic, paid, referral, direct, affiliate
    source_url TEXT,
    score INTEGER DEFAULT 0,  -- 0-100 lead score
    stage VARCHAR(50) DEFAULT 'new',  -- new, contacted, qualified, proposal, negotiation, closed_won, closed_lost
    intent_signals JSONB DEFAULT '[]',  -- Array of detected intent signals
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_leads_tenant ON leads(tenant_id);
CREATE INDEX idx_leads_vertical ON leads(vertical);
CREATE INDEX idx_leads_stage ON leads(stage);
CREATE INDEX idx_leads_score ON leads(score DESC);

-- 3. DEAL (Pricing, probability, contract link - Studio, Staffing, SaaS)
CREATE TABLE IF NOT EXISTS deals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    lead_id UUID REFERENCES leads(id),
    vertical VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    value DECIMAL(12,2),
    probability FLOAT DEFAULT 0,  -- 0-1 probability of closing
    contract_url TEXT,
    margin_target FLOAT DEFAULT 0.23,  -- Target margin (23% minimum)
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_deals_tenant ON deals(tenant_id);
CREATE INDEX idx_deals_lead ON deals(lead_id);
CREATE INDEX idx_deals_vertical ON deals(vertical);

-- 4. ORDER (Cart, SKU, fulfillment status - E-commerce, Media digital products)
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',  -- pending, processing, fulfilled, shipped, delivered, refunded
    total DECIMAL(12,2),
    items JSONB DEFAULT '[]',  -- Array of {sku, quantity, price}
    fulfillment_data JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_orders_tenant ON orders(tenant_id);
CREATE INDEX idx_orders_account ON orders(account_id);
CREATE INDEX idx_orders_status ON orders(status);

-- 5. SUBSCRIPTION (SaaS Access Model - SaaS, Media subscriptions)
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    plan VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active',  -- active, cancelled, expired, past_due
    mrr DECIMAL(12,2) DEFAULT 0,
    start_date DATE,
    end_date DATE,
    cancel_reason TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_tenant ON subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_account ON subscriptions(account_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

-- 6. PROJECT (Facility Onboarding / Creative Projects - Studio, SaaS implementation)
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    account_id UUID REFERENCES accounts(id),
    vertical VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'planning',  -- planning, in_progress, on_hold, completed, cancelled
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_projects_tenant ON projects(tenant_id);
CREATE INDEX idx_projects_account ON projects(account_id);
CREATE INDEX idx_projects_status ON projects(status);

-- 7. PLACEMENT (Deployment Data - Staffing shifts, Media ad placements)
CREATE TABLE IF NOT EXISTS placements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    account_id UUID REFERENCES accounts(id),
    candidate_id UUID,
    vertical VARCHAR(50) NOT NULL,
    type VARCHAR(50),  -- shift, ad_placement, content_placement
    status VARCHAR(50) DEFAULT 'pending',  -- pending, confirmed, active, completed, cancelled
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_placements_tenant ON placements(tenant_id);
CREATE INDEX idx_placements_vertical ON placements(vertical);
CREATE INDEX idx_placements_status ON placements(status);

-- 8. CANDIDATE (Talent Profiles - Staffing clinicians, Media influencers, SaaS trial users)
CREATE TABLE IF NOT EXISTS candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    vertical VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    skills TEXT[],
    experience_years INTEGER,
    score INTEGER DEFAULT 0,  -- Matching score 0-100
    status VARCHAR(50) DEFAULT 'active',  -- active, placed, inactive
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_candidates_tenant ON candidates(tenant_id);
CREATE INDEX idx_candidates_vertical ON candidates(vertical);
CREATE INDEX idx_candidates_score ON candidates(score DESC);
CREATE INDEX idx_candidates_skills ON candidates USING GIN(skills);

-- 9. CONTENT ASSET (Topic, keyword cluster, performance - Media, E-commerce, Studio portfolios)
CREATE TABLE IF NOT EXISTS content_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    vertical VARCHAR(50) NOT NULL,
    type VARCHAR(50),  -- article, video, social, ad, portfolio, job_post, product_desc
    title VARCHAR(255),
    topic VARCHAR(100),
    keywords TEXT[],
    url TEXT,
    status VARCHAR(50) DEFAULT 'draft',  -- draft, published, retired, performing, underperforming
    performance JSONB DEFAULT '{}',  -- {views, clicks, conversions, epc, revenue}
    affiliate_placements JSONB DEFAULT '[]',  -- Array of affiliate links/placements
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_content_assets_tenant ON content_assets(tenant_id);
CREATE INDEX idx_content_assets_vertical ON content_assets(vertical);
CREATE INDEX idx_content_assets_type ON content_assets(type);
CREATE INDEX idx_content_assets_status ON content_assets(status);
CREATE INDEX idx_content_assets_topic ON content_assets(topic);
CREATE INDEX idx_content_assets_keywords ON content_assets USING GIN(keywords);

-- 10. TASK (Work Items - All verticals)
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    vertical VARCHAR(50) NOT NULL,
    type VARCHAR(50),  -- ai_autonomous, human_approval_required, ai_assisted
    status VARCHAR(50) DEFAULT 'pending',  -- pending, in_progress, completed, blocked, cancelled
    assigned_to VARCHAR(100),  -- agent name or human user email
    priority VARCHAR(20) DEFAULT 'medium',  -- low, medium, high, urgent
    due_date TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tasks_tenant ON tasks(tenant_id);
CREATE INDEX idx_tasks_vertical ON tasks(vertical);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_assigned ON tasks(assigned_to);
CREATE INDEX idx_tasks_type ON tasks(type);

-- 11. EVENT (Analytics Events - All verticals)
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    vertical VARCHAR(50) NOT NULL,
    event_type VARCHAR(100),  -- page_view, click, conversion, lead_created, deal_closed, etc.
    account_id UUID,
    lead_id UUID,
    candidate_id UUID,
    content_asset_id UUID,
    event_data JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_events_tenant ON events(tenant_id);
CREATE INDEX idx_events_vertical ON events(vertical);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_created ON events(created_at DESC);

-- 12. LEDGER (Transactions - All verticals)
CREATE TABLE IF NOT EXISTS ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    vertical VARCHAR(50) NOT NULL,
    account_id UUID REFERENCES accounts(id),
    amount DECIMAL(12,2),
    type VARCHAR(50),  -- revenue, cost, refund, adjustment
    description TEXT,
    reference_id UUID,  -- Reference to order/deal/subscription
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ledger_tenant ON ledger(tenant_id);
CREATE INDEX idx_ledger_vertical ON ledger(vertical);
CREATE INDEX idx_ledger_type ON ledger(type);
CREATE INDEX idx_ledger_account ON ledger(account_id);

-- 13. POLICY (Guardrails - All verticals)
CREATE TABLE IF NOT EXISTS policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id),
    vertical VARCHAR(50),  -- NULL = global policy
    name VARCHAR(255) NOT NULL,
    description TEXT,
    rules JSONB NOT NULL,  -- {condition, action, threshold}
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_policies_tenant ON policies(tenant_id);
CREATE INDEX idx_policies_vertical ON policies(vertical);
CREATE INDEX idx_policies_enabled ON policies(enabled);

-- Insert default policies
INSERT INTO policies (tenant_id, vertical, name, description, rules)
SELECT *
FROM (
    VALUES
        (NULL::uuid, NULL::varchar(50), 'margin_protection', 'Minimum 23% margin on all deals',
         '{"condition": "deal.margin < 0.23", "action": "escalate_to_human", "threshold": 0.23}'::jsonb),
        (NULL::uuid, NULL::varchar(50), 'content_epc_retirement', 'Auto-retire content with EPC < $2.50 for 7 days',
         '{"condition": "content_asset.epc < 2.50 AND days > 7", "action": "retire_content", "threshold": 2.50}'::jsonb),
        (NULL::uuid, NULL::varchar(50), 'lead_routing', 'Route leads to highest-LTV vertical',
         '{"condition": "lead.vertical IS NULL", "action": "score_and_route", "threshold": 0.7}'::jsonb),
        (NULL::uuid, NULL::varchar(50), 'cash_flow_alert', 'Alert if cash < 45 days operating expenses',
         '{"condition": "cash_runway < 45", "action": "alert_cfo", "threshold": 45}'::jsonb)
) AS seed(tenant_id, vertical, name, description, rules)
WHERE NOT EXISTS (
    SELECT 1
    FROM policies p
    WHERE p.tenant_id IS NOT DISTINCT FROM seed.tenant_id
      AND p.vertical IS NOT DISTINCT FROM seed.vertical
      AND p.name = seed.name
);

-- ============================================================================
-- CROSS-VERTICAL VIEWS
-- ============================================================================

-- Unified revenue view across all verticals
CREATE OR REPLACE VIEW revenue_by_vertical AS
SELECT 
    vertical,
    DATE_TRUNC('month', created_at) AS month,
    SUM(amount) AS revenue,
    COUNT(*) AS transaction_count
FROM ledger
WHERE type = 'revenue'
GROUP BY vertical, DATE_TRUNC('month', created_at)
ORDER BY month DESC, vertical;

-- Lead pipeline across all verticals
CREATE OR REPLACE VIEW lead_pipeline AS
SELECT 
    vertical,
    stage,
    COUNT(*) AS lead_count,
    AVG(score) AS avg_score
FROM leads
GROUP BY vertical, stage
ORDER BY vertical, stage;

-- Content performance across all verticals
CREATE OR REPLACE VIEW content_performance AS
SELECT 
    vertical,
    type,
    status,
    COUNT(*) AS asset_count,
    AVG((performance->>'epc')::FLOAT) AS avg_epc,
    SUM((performance->>'revenue')::DECIMAL) AS total_revenue
FROM content_assets
GROUP BY vertical, type, status
ORDER BY vertical, type;

-- Task completion by agent type
CREATE OR REPLACE VIEW task_completion AS
SELECT 
    type,
    status,
    COUNT(*) AS task_count,
    COUNT(*) FILTER (WHERE status = 'completed') AS completed_count,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'completed') / NULLIF(COUNT(*), 0), 2) AS completion_rate
FROM tasks
GROUP BY type, status
ORDER BY type, status;
