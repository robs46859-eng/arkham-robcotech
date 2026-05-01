-- Resume vertical schema bootstrap after a partial first-run failure.
-- This file is intentionally idempotent for the first-deploy recovery path.

ALTER TABLE policies
    ALTER COLUMN tenant_id DROP NOT NULL;

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

CREATE OR REPLACE VIEW lead_pipeline AS
SELECT
    vertical,
    stage,
    COUNT(*) AS lead_count,
    AVG(score) AS avg_score
FROM leads
GROUP BY vertical, stage
ORDER BY vertical, stage;

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
