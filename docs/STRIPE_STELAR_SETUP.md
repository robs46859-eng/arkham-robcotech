# Stripe Setup for robcotech.pro

## Quick Setup (5 minutes)

### 1. Add Your Stripe Keys

Edit `services/billing/.env`:

```bash
# Copy the example file
cp services/billing/.env.example services/billing/.env

# Edit with your keys
nano services/billing/.env
```

**Add your Stripe credentials:**

```bash
# Domain
APP_DOMAIN=robcotech.pro

# Stripe API Keys (from https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET_HERE

# Stripe Price IDs (from https://dashboard.stripe.com/products)
# Use the BASE price ID - yearly is configured as upsell in Stripe
STRIPE_PRICE_ID_BASIC=price_YOUR_BASIC_ID
STRIPE_PRICE_ID_PRO=price_YOUR_PRO_ID
STRIPE_PRICE_ID_ENTERPRISE=price_YOUR_ENTERPRISE_ID

# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/fullstackarkham
```

---

### 2. Configure Yearly Upsell in Stripe

Since you already have yearly prices added as upsells:

1. Go to **https://dashboard.stripe.com/products**
2. Click on each product (Basic, Pro, Enterprise)
3. Verify the yearly pricing is configured
4. Copy the **base Price ID** (the monthly one)

The base Price IDs go in your `.env`:
```bash
STRIPE_PRICE_ID_BASIC=price_1ABC...  # ← Base price ID from Stripe
STRIPE_PRICE_ID_PRO=price_1ABC...
STRIPE_PRICE_ID_ENTERPRISE=price_1ABC...
```

Stripe will handle the monthly/yearly toggle automatically in checkout.

---

### 3. Configure Webhook

1. Go to **https://dashboard.stripe.com/test/webhooks** → **Add endpoint**

2. **Endpoint URL**:
   - For local dev: Use Stripe CLI (see below)
   - For production: `https://robcotech.pro/api/v1/billing/webhook`

3. **Events to send**:
   - ☑ `checkout.session.completed`
   - ☑ `customer.subscription.updated`
   - ☑ `customer.subscription.deleted`
   - ☑ `invoice.payment_succeeded`
   - ☑ `invoice.payment_failed`

4. Click **Add endpoint**

5. **Copy the Signing Secret**: `whsec_1ABC...`

6. Add to `.env`:
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET_HERE
   ```

---

### 4. Restart Billing Service

```bash
cd /Users/joeiton/Desktop/FullStackArkham
docker-compose restart billing
```

---

### 5. Test Checkout

1. **Open pricing page**: `http://localhost:3000/pricing`

2. **Select a plan** (toggle Monthly/Yearly)

3. **Click "Start Trial"**

4. **Verify Stripe Checkout opens** with:
   - Correct plan name
   - Monthly/Yearly toggle visible
   - Correct pricing

---

## Stripe CLI (Local Testing)

### Install

```bash
# macOS
brew install stripe/stripe-cli/stripe
```

### Login

```bash
stripe login
```

### Forward Webhooks

```bash
stripe listen --forward-to localhost:8086/api/v1/billing/webhook
```

### Trigger Test Events

```bash
stripe trigger checkout.session.completed
stripe trigger invoice.payment_succeeded
```

---

## What's Different from Before

**Before (Separate Price IDs):**
- 6 Price IDs (3 plans × 2 cycles)
- Code handled monthly/yearly selection
- More complex settings

**Now (Single Price ID with Upsell):**
- 3 Price IDs (one per plan)
- Stripe handles monthly/yearly in checkout
- Simpler configuration
- Yearly discount configured in Stripe Dashboard

---

## Your Price IDs to Add

Fill these in from your Stripe Dashboard:

```bash
# From: https://dashboard.stripe.com/products

STRIPE_PRICE_ID_BASIC=price______________________
STRIPE_PRICE_ID_PRO=price______________________
STRIPE_PRICE_ID_ENTERPRISE=price______________________

# From: https://dashboard.stripe.com/apikeys
STRIPE_SECRET_KEY=sk_test______________________

# From: https://dashboard.stripe.com/webhooks
STRIPE_WEBHOOK_SECRET=whsec______________________
```

---

## Verify It Works

```bash
# Check billing service logs
docker logs fullstackarkham-billing --tail 20

# Should see:
# INFO: Starting Billing Service
# INFO: All agents initialized
```

Then visit `http://localhost:3000/pricing` and click a plan.

---

## Production (robcotech.pro)

When ready for production:

1. **Switch to Live Mode** in Stripe Dashboard

2. **Get Live Keys**:
   ```bash
   STRIPE_SECRET_KEY=sk_live_...
   STRIPE_WEBHOOK_SECRET=whsec_live_...
   STRIPE_PRICE_ID_BASIC=price_live_...
   STRIPE_PRICE_ID_PRO=price_live_...
   STRIPE_PRICE_ID_ENTERPRISE=price_live_...
   ```

3. **Create Production Webhook**:
   - URL: `https://robcotech.pro/api/v1/billing/webhook`
   - Events: Same 5 events as above

4. **Update Production Environment** with live keys

---

**Questions?** Just share the Price IDs (not secret keys!) and I can help verify the format.
