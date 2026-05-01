# Azure Deploy Bot for FullStackArkham on robcotech.pro

Automated deployment bot for Azure Container Apps.

## What This Bot Does

1. **Validates** all services build correctly
2. **Builds** Docker images for each service
3. **Pushes** to Azure Container Registry (ACR)
4. **Deploys** to Azure Container Apps
5. **Verifies** deployment health
6. **Notifies** on success/failure

## Quick Start

```bash
# Create Azure infrastructure
./scripts/deploy-bot.sh --setup

# Build and deploy services
./scripts/deploy-bot.sh --deploy
```

---

## Files Included

- `scripts/deploy-bot.sh` - Main deployment script
- `.github/workflows/deploy.yml` - GitHub Actions CI/CD
- `deploy-bot/README.md` - Full documentation

---

## Azure Resources Created

| Resource | Purpose |
|----------|---------|
| Container Registry (ACR) | Docker image storage |
| Container Apps Environment | Serverless container hosting |
| Container Apps (8) | One per service |
| PostgreSQL Flexible Server | Database |
| Redis Cache | Caching & queues |
| Key Vault | Secrets management |
| Application Insights | Monitoring |

---

## Prerequisites

1. **Azure CLI** installed
2. **Azure subscription** with owner/contributor access
3. **Docker** installed locally
4. **Git** configured

---

## Setup (One Time)

```bash
# 1. Login to Azure
az login
az account set --subscription YOUR_SUBSCRIPTION_ID

# 2. Run infrastructure setup
./scripts/deploy-bot.sh --setup

# 3. Deploy application
./scripts/deploy-bot.sh --deploy
```

`--setup` does not run Docker Compose. If it fails before any Azure resource is created, check Azure CLI login plus DNS/network access to `login.microsoftonline.com`.

---

## Commands

| Command | Description |
|---------|-------------|
| `./scripts/deploy-bot.sh --setup` | Create Azure resources |
| `./scripts/deploy-bot.sh --deploy` | Build and deploy all services |
| `./scripts/deploy-bot.sh --status` | Check deployment status |
| `./scripts/deploy-bot.sh --logs [service]` | View service logs |
| `./scripts/deploy-bot.sh --rollback` | Rollback to previous version |
| `./scripts/deploy-bot.sh --cleanup` | Delete all Azure resources |

---

## Environment Variables

Set these in Azure Key Vault or as App Settings:

```bash
# Domain
APP_DOMAIN=robcotech.pro

# Stripe (Live)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_BASIC=price_...
STRIPE_PRICE_ID_PRO=price_...
STRIPE_PRICE_ID_ENTERPRISE=price_...

# Database
DATABASE_URL=postgresql://...

# Gateway
ARKHAM_ENDPOINT=http://arkham:8081

# All service URLs
GATEWAY_URL=http://gateway:8080
MEDIA_COMMERCE_URL=http://media-commerce:8087
```

---

## Deployment Flow

```
┌─────────────────────────────────────────────────────────┐
│  1. VALIDATE                                            │
│     ✓ Check Azure login                                 │
│     ✓ Verify Docker running                             │
│     ✓ Verify Azure login token and DNS reachability     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  2. BUILD                                               │
│     ✓ Build all 8 Docker images                         │
│     ✓ Tag with version/timestamp                        │
│     ✓ Run smoke tests                                   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  3. PUSH                                                │
│     ✓ Login to ACR                                      │
│     ✓ Push all images to registry                       │
│     ✓ Tag with git commit SHA                           │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  4. DEPLOY                                              │
│     ✓ Update Container Apps with new images             │
│     ✓ Rolling deployment (zero downtime)                │
│     ✓ Wait for health checks                            │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  5. VERIFY                                              │
│     ✓ Health check all endpoints                        │
│     ✓ Verify DNS (robcotech.pro)                          │
│     ✓ Test Stripe webhook                               │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  6. NOTIFY                                              │
│     ✓ Log deployment summary                            │
│     ✓ Output URLs                                       │
│     ✓ Alert on failures                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Monitoring

After deployment:

```bash
# View all services
./scripts/deploy-bot.sh --status

# View logs for specific service
./scripts/deploy-bot.sh --logs gateway
./scripts/deploy-bot.sh --logs billing
./scripts/deploy-bot.sh --logs media-commerce

# View Application Insights
az monitor app-insights query \
  --app YOUR_APP_INSIGHTS \
  --analytics-query "requests | take 10"
```

---

## Rollback

If deployment fails:

```bash
# Rollback to previous version
./scripts/deploy-bot.sh --rollback

# Re-run the current deploy flow after fixing the issue
./scripts/deploy-bot.sh --deploy
```

---

## URLs After Deploy

| Service | URL |
|---------|-----|
| **Frontend** | https://robcotech.pro |
| **Gateway API** | https://api.robcotech.pro/v1 |
| **Billing Webhooks** | https://api.robcotech.pro/api/v1/billing/webhook |
| **Application Insights** | Azure Portal → Monitor → Application Insights |

---

## Cost Estimate

| Resource | Monthly Cost (Estimated) |
|----------|-------------------------|
| Container Apps (8 × 0.25 vCPU) | ~$60 |
| PostgreSQL (Flexible, Basic) | ~$25 |
| Redis Cache (Basic) | ~$15 |
| Container Registry | ~$5 |
| Application Insights | ~$10 |
| **Total** | **~$115/month** |

---

## Security

- ✅ All secrets in Key Vault
- ✅ Private endpoints for DB/Redis
- ✅ SSL/TLS enforced
- ✅ Network isolation
- ✅ Managed identities

---

## Support

For issues:
1. Check logs: `./scripts/deploy-bot.sh --logs [service]`
2. Check Azure Portal → Container Apps
3. Review Application Insights

---

**Ready to deploy? Run:** `./scripts/deploy-bot.sh --deploy`
