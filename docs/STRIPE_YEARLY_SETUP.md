# Stripe Setup Checklist - Yearly Pricing

## Step 1: Get Stripe API Keys (2 minutes)

1. Go to https://dashboard.stripe.com/register
2. Verify your email
3. Navigate to **Developers → API keys**
4. Copy these keys:
   - **Publishable key**: `pk_test_...` (for frontend)
   - **Secret key**: `sk_test_...` (for backend)

---

## Step 2: Create Products in Stripe (5 minutes)

Navigate to: **https://dashboard.stripe.com/products** → **Add Product**

### Product 1: Basic Stack

```
Product name: FullStackArkham Basic Stack
Description: Essential agents for content and lead management

Pricing:
  ☑ One-time or subscription → Subscription
  
  Price 1 (Monthly):
    - Amount: $29.00
    - Currency: USD
    - Billing period: Month
  
  Click "Add another price"
  
  Price 2 (Yearly - Discounted):
    - Amount: $199.00
    - Currency: USD
    - Billing period: Year
```

**After creating, copy these Price IDs:**
- Basic Monthly: `price_1ABC...` ← You'll see this in the pricing table
- Basic Yearly: `price_1ABC...` ← You'll see this in the pricing table

---

### Product 2: Pro (Builder) Stack

```
Product name: FullStackArkham Pro (Builder) Stack
Description: Advanced agents for media-commerce orchestration

Pricing:
  Price 1 (Monthly):
    - Amount: $99.00
    - Currency: USD
    - Billing period: Month
  
  Price 2 (Yearly - Discounted):
    - Amount: $599.00
    - Currency: USD
    - Billing period: Year
```

**Copy Price IDs:**
- Pro Monthly: `price_1ABC...`
- Pro Yearly: `price_1ABC...`

---

### Product 3: Enterprise (FULL) Stack

```
Product name: FullStackArkham Enterprise (FULL) Stack
Description: Complete AI operating system with all agents

Pricing:
  Price 1 (Monthly):
    - Amount: $499.00
    - Currency: USD
    - Billing period: Month
  
  Price 2 (Yearly - Discounted):
    - Amount: $2,350.00
    - Currency: USD
    - Billing period: Year
```

**Copy Price IDs:**
- Enterprise Monthly: `price_1ABC...`
- Enterprise Yearly: `price_1ABC...`

---

## Step 3: Create Webhook Endpoint (3 minutes)

1. Navigate to **https://dashboard.stripe.com/test/webhooks** → **Add endpoint**

2. **Endpoint URL**: 
   - For local dev: Use Stripe CLI (see below)
   - For production: `https://your-domain.com/api/v1/billing/webhook`

3. **Events to send** (select these):
   - ☑ `checkout.session.completed`
   - ☑ `customer.subscription.updated`
   - ☑ `customer.subscription.deleted`
   - ☑ `invoice.payment_succeeded`
   - ☑ `invoice.payment_failed`

4. Click **Add endpoint**

5. **Copy the Signing Secret**: `whsec_1ABC...`

---

## Step 4: Update Environment Variables (2 minutes)

Create or update `services/billing/.env`:

```bash
# ==================== STRIPE API KEYS ====================
STRIPE_SECRET_KEY=sk_test_YOUR_ACTUAL_SECRET_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_ACTUAL_WEBHOOK_SECRET_HERE

# ==================== STRIPE PRICE IDs - MONTHLY ====================
STRIPE_PRICE_ID_BASIC_MONTHLY=price_YOUR_BASIC_MONTHLY_PRICE_ID
STRIPE_PRICE_ID_PRO_MONTHLY=price_YOUR_PRO_MONTHLY_PRICE_ID
STRIPE_PRICE_ID_ENTERPRISE_MONTHLY=price_YOUR_ENTERPRISE_MONTHLY_PRICE_ID

# ==================== STRIPE PRICE IDs - YEARLY ====================
STRIPE_PRICE_ID_BASIC_YEARLY=price_YOUR_BASIC_YEARLY_PRICE_ID
STRIPE_PRICE_ID_PRO_YEARLY=price_YOUR_PRO_YEARLY_PRICE_ID
STRIPE_PRICE_ID_ENTERPRISE_YEARLY=price_YOUR_ENTERPRISE_YEARLY_PRICE_ID

# ==================== CONFIGURATION ====================
STRIPE_CURRENCY=usd
STRIPE_YEARLY_TRIAL_DAYS=14

# ==================== DATABASE ====================
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/fullstackarkham
```

---

## Step 5: Test with Stripe CLI (Local Development)

### Install Stripe CLI

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Or download from: https://github.com/stripe/stripe-cli#installation
```

### Login to Stripe CLI

```bash
stripe login
```

### Forward Webhooks Locally

```bash
# In a new terminal, run:
stripe listen --forward-to localhost:8086/api/v1/billing/webhook
```

You'll see output like:
```
> Ready! Your webhook signing secret is whsec_123...
```

### Trigger Test Events

```bash
# Test subscription creation
stripe trigger checkout.session.completed

# Test payment success
stripe trigger invoice.payment_succeeded

# Test payment failure
stripe trigger invoice.payment_failed
```

---

## Step 6: Verify Pricing Display (1 minute)

Visit `http://localhost:3000/pricing` to verify:

- ☑ Monthly/Yearly toggle works
- ☑ Yearly shows correct savings:
  - Basic: 43% off ($199 vs $348/year)
  - Pro: 50% off ($599 vs $1,188/year)
  - Enterprise: 61% off ($2,350 vs $5,988/year)
- ☑ Features list is correct
- ☑ "Most Popular" badge on Pro plan

---

## Step 7: Test Checkout Flow (5 minutes)

1. **Start all services**:
   ```bash
   cd /Users/joeiton/Desktop/FullStackArkham
   docker-compose up -d billing media-commerce
   ```

2. **Open pricing page**: `http://localhost:3000/pricing`

3. **Select Yearly billing** (toggle switch)

4. **Click "Start Yearly Trial"** on Pro plan

5. **Verify checkout creates subscription** with:
   - Correct plan (pro)
   - Correct billing cycle (yearly)
   - 14-day free trial applied
   - Price: $599/year

---

## Step 8: Verify Webhook Handling (2 minutes)

Check billing service logs:

```bash
docker logs fullstackarkham-billing --tail 50
```

You should see:
```
INFO: Verified webhook event: checkout.session.completed
INFO: Created Yearly subscription for Pro (Builder) Stack: sub_1ABC...
```

---

## Troubleshooting

### Price ID Not Found Error

**Problem**: `ValueError: No price ID found for pro/yearly`

**Solution**: Double-check `.env` file:
```bash
# Verify the Price IDs are correct
cat services/billing/.env | grep PRICE_ID

# Restart billing service after changes
docker-compose restart billing
```

### Webhook Signature Failed

**Problem**: `Webhook signature verification failed`

**Solution**: 
1. Make sure `STRIPE_WEBHOOK_SECRET` matches what Stripe CLI shows
2. Restart billing service after updating `.env`

### Pricing Not Showing Correctly

**Problem**: Yearly prices don't match expected ($199, $599, $2,350)

**Solution**: Check `apps/web/src/app/pricing/page.tsx`:
```typescript
const PLANS = {
  basic: { yearly: 199, ... },
  pro: { yearly: 599, ... },
  enterprise: { yearly: 2350, ... },
}
```

---

## Going Live (Production)

When ready for production:

1. **Switch to Live Mode** in Stripe Dashboard (toggle in top-right)

2. **Get Live API Keys**:
   - Live Secret Key: `sk_live_...`
   - Live Webhook Secret: Create new webhook in live mode

3. **Create Live Products** (repeat Step 2 in live mode)

4. **Update Production Environment**:
   ```bash
   STRIPE_SECRET_KEY=sk_live_...
   STRIPE_WEBHOOK_SECRET=whsec_live_...
   STRIPE_PRICE_ID_BASIC_MONTHLY=price_live_...
   # ... etc
   ```

5. **Update Webhook URL** to production domain:
   ```
   https://your-domain.com/api/v1/billing/webhook
   ```

---

## Summary: What You've Set Up

✅ 3 Products with Monthly + Yearly pricing
✅ Yearly discounts (43%, 50%, 61% off)
✅ 14-day free trial for yearly subscriptions
✅ Webhook handling for all subscription events
✅ Pricing page with toggle
✅ Checkout API integration
✅ Dunning sequence for failed payments

**Next**: Customize features list, add customer portal, set up analytics
