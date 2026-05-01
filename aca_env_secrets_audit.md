# ACA Env/Secrets Audit

- `.env.production` exists at `/Users/joeiton/Desktop/arkham-robcotech/.env.production`.
- `.env.production` currently looks like a template, not a live secret source.
- `scripts/launch.sh` is deprecated; the supported Azure flow is `scripts/deploy-bot.sh` with Key Vault-backed secret storage.
- Service settings default many production connections to `localhost`, so ACA env wiring is mandatory.
- Missing external production inputs: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, STRIPE_PRICE_ID_BASIC, STRIPE_PRICE_ID_PRO, STRIPE_PRICE_ID_ENTERPRISE, APPLICATIONINSIGHTS_CONNECTION_STRING.

## Key Vault
- `postgres-admin-user`: present
- `postgres-admin-password`: present
- `database-url-core`: present
- `database-url-bim`: present
- `redis-url`: present
- `redis-password`: present
- `jwt-secret`: present
- `stripe-secret-key`: present
- `stripe-webhook-secret`: present
- `stripe-price-id-basic`: present
- `stripe-price-id-pro`: present
- `stripe-price-id-enterprise`: present
- `applicationinsights-connection-string`: missing
