-- Resume core schema bootstrap after a partial first-run failure.
-- This file is intentionally idempotent for the first-deploy recovery path.

-- Insert default tenant (for development)
INSERT INTO tenants (id, name, slug, api_key_hash, plan, quota_monthly)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Default Tenant',
    'default',
    '$2a$10$placeholder_hash_for_dev_api_key',
    'free',
    100000
)
ON CONFLICT (id) DO NOTHING;

-- Insert default API key (for development: fsa_dev_key_12345)
-- In production, this should be properly hashed
INSERT INTO api_keys (tenant_id, name, key_hash, key_prefix, permissions)
SELECT
    '00000000-0000-0000-0000-000000000001',
    'Development Key',
    'placeholder_hash',
    'fsa_dev',
    '["infer", "read", "write", "admin"]'
WHERE NOT EXISTS (
    SELECT 1
    FROM api_keys
    WHERE tenant_id = '00000000-0000-0000-0000-000000000001'
      AND name = 'Development Key'
);

-- ============================================================================
-- SUBSCRIPTION PLANS - Subscription tier definitions
-- ============================================================================

CREATE TABLE IF NOT EXISTS subscription_plans (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price_monthly DECIMAL(10, 2) NOT NULL DEFAULT 0,
    quota_monthly BIGINT NOT NULL DEFAULT 10000,
    features TEXT[] NOT NULL DEFAULT '{}',
    stripe_price_id VARCHAR(100),
    stripe_yearly_price_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Add stripe columns to tenants table
ALTER TABLE tenants ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(100);
ALTER TABLE tenants ADD COLUMN IF NOT EXISTS stripe_subscription_id VARCHAR(100);

-- Add tenant foreign key to billing_records
ALTER TABLE billing_records
    DROP CONSTRAINT IF EXISTS billing_records_tenant_id_fkey,
    ADD CONSTRAINT billing_records_tenant_id_fkey
    FOREIGN KEY (tenant_id) REFERENCES tenants(id);
