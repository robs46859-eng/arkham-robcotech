# Stripe & Agent API Integration Guide

## Stripe Integration

### 1. Get Your Stripe API Keys

1. **Sign up for Stripe**: https://stripe.com
2. **Get API Keys**:
   - Go to Stripe Dashboard → Developers → API Keys
   - Copy `Publishable key` and `Secret key`

3. **Create Products & Prices**:

```bash
# In Stripe Dashboard → Products → Add Product

# Basic Plan
Name: FullStackArkham Basic
Price: $29/month
Price ID: price_XXXXX (copy this)

# Pro Plan
Name: FullStackArkham Pro
Price: $99/month
Price ID: price_XXXXX (copy this)

# Enterprise Plan
Name: FullStackArkham Enterprise
Price: $499/month
Price ID: price_XXXXX (copy this)
```

4. **Create Webhook Endpoint**:

```bash
# In Stripe Dashboard → Developers → Webhooks → Add endpoint

URL: https://your-domain.com/api/v1/billing/webhook
Events to send:
  ✓ checkout.session.completed
  ✓ customer.subscription.updated
  ✓ customer.subscription.deleted
  ✓ invoice.payment_succeeded
  ✓ invoice.payment_failed

Signing Secret: whsec_XXXXX (copy this)
```

### 2. Configure Environment Variables

Create `services/billing/.env`:

```bash
STRIPE_SECRET_KEY=sk_test_51ABC...
STRIPE_WEBHOOK_SECRET=whsec_1ABC...
STRIPE_PRICE_ID_BASIC=price_1ABC...
STRIPE_PRICE_ID_PRO=price_1ABC...
STRIPE_PRICE_ID_ENTERPRISE=price_1ABC...
STRIPE_CURRENCY=usd
```

### 3. Update Docker Compose

Add to `docker-compose.yml`:

```yaml
billing:
  build:
    context: ./services/billing
    dockerfile: Dockerfile
  container_name: fullstackarkham-billing
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/fullstackarkham
    - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    - STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}
    - STRIPE_PRICE_ID_BASIC=${STRIPE_PRICE_ID_BASIC}
    - STRIPE_PRICE_ID_PRO=${STRIPE_PRICE_ID_PRO}
    - STRIPE_PRICE_ID_ENTERPRISE=${STRIPE_PRICE_ID_ENTERPRISE}
  ports:
    - "8086:8086"
  depends_on:
    - postgres
```

### 4. Test Stripe Integration

```bash
# Start billing service
docker-compose up -d billing

# Test webhook (use Stripe CLI)
stripe listen --forward-to localhost:8086/api/v1/billing/webhook

# Trigger test event
stripe trigger checkout.session.completed
```

---

## Agent API (MCP Server)

### What is MCP?

Model Context Protocol (MCP) allows AI assistants (Claude, Cursor, Windsurf) to:
- Discover available agents/tools
- Execute agent actions
- Query workflow status

### 1. Install MCP Dependencies

```bash
cd /Users/joeiton/Desktop/FullStackArkham

# Install MCP server package
pip install mcp

# Or add to billing requirements
echo "mcp>=1.0.0" >> services/billing/requirements.txt
```

### 2. Configure AI Assistant

#### For Claude Code:

Edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "fullstackarkham": {
      "command": "python",
      "args": ["-m", "services.mcp_server"],
      "cwd": "/Users/joeiton/Desktop/FullStackArkham",
      "env": {
        "DATABASE_URL": "postgresql://postgres:postgres@localhost:15432/fullstackarkham",
        "GATEWAY_URL": "http://localhost:8080"
      }
    }
  }
}
```

#### For Cursor:

Create `.cursor/settings.json` in project:

```json
{
  "mcp": {
    "servers": {
      "fullstackarkham": {
        "type": "stdio",
        "command": "python",
        "args": ["-m", "services.mcp_server"],
        "cwd": "/Users/joeiton/Desktop/FullStackArkham"
      }
    }
  }
}
```

### 3. Available Agent Tools

Once connected, AI assistants can use:

#### ContentEngine™
- `ContentEngine.create_content_strategy` - Create content strategy
- `ContentEngine.generate_content` - Generate content
- `ContentEngine.optimize_for_ai_seo` - Optimize for AI search

#### DealFlow™
- `DealFlow.score_lead` - Score lead
- `DealFlow.route_lead` - Route to highest-LTV vertical
- `DealFlow.generate_proposal` - Generate proposal

#### MediaCommerce™
- `MediaCommerce.monitor_epc` - Monitor EPC
- `MediaCommerce.auto_optimize_content` - Auto-optimize content
- `MediaCommerce.repurpose_content` - Repurpose content

#### ChiefPulse™
- `ChiefPulse.generate_daily_briefing` - Executive briefing
- `ChiefPulse.get_approval_queue` - Get approval queue
- `ChiefPulse.detect_anomalies` - Detect anomalies

### 4. Test MCP Server

```bash
# Run MCP server locally
cd /Users/joeiton/Desktop/FullStackArkham
python -m services.mcp_server

# In Claude/Cursor, try:
"List available agents"
"Use ContentEngine to create a content strategy for healthcare staffing"
```

---

## API Endpoints Summary

### Billing/Stripe

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/billing/webhook` | POST | Stripe webhook handler |
| `/api/v1/billing/subscribe` | POST | Create subscription |
| `/api/v1/billing/cancel` | POST | Cancel subscription |
| `/api/v1/billing/usage` | POST | Report usage |
| `/api/v1/billing/invoice` | POST | Create invoice |

### Agent API (via MCP)

| Tool | Agent | Purpose |
|------|-------|---------|
| `create_content_strategy` | ContentEngine | Create content strategy |
| `route_lead` | DealFlow | Cross-vertical lead routing |
| `monitor_epc` | MediaCommerce | EPC monitoring |
| `generate_daily_briefing` | ChiefPulse | Executive briefing |

---

## Security Best Practices

### Stripe
1. **Never commit API keys** - Use environment variables only
2. **Verify webhook signatures** - Always validate `stripe-signature` header
3. **Use test mode first** - Test thoroughly before going live
4. **Implement idempotency** - Prevent duplicate charges

### Agent API
1. **Authenticate agent access** - Require API key for agent execution
2. **Rate limit agent calls** - Prevent abuse
3. **Log all agent actions** - Audit trail for compliance
4. **Validate inputs** - Sanitize all tool arguments

---

## Troubleshooting

### Stripe Webhooks Not Working

```bash
# Check webhook logs
stripe logs tail

# Verify signature locally
# Add debug logging to webhooks.py
logger.info(f"Received signature: {stripe_signature}")
logger.info(f"Payload: {payload[:200]}...")
```

### MCP Server Not Connecting

```bash
# Check Python path
which python
python --version

# Test MCP server directly
python -m services.mcp_server

# Check Claude/Cursor logs for connection errors
```

---

## Next Steps

1. **Complete Stripe Setup**
   - [ ] Get API keys from Stripe Dashboard
   - [ ] Create products and prices
   - [ ] Configure webhook endpoint
   - [ ] Update environment variables

2. **Complete MCP Setup**
   - [ ] Install `mcp` package
   - [ ] Configure AI assistant (Claude/Cursor)
   - [ ] Test agent tool execution
   - [ ] Connect to actual agent implementations

3. **Production Deployment**
   - [ ] Switch to live Stripe keys
   - [ ] Configure production webhook URL
   - [ ] Set up monitoring for webhooks
   - [ ] Implement dunning sequence
