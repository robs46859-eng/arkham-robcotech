# Arkham Launch List

**Domain:** `robcotech.pro`

## Required Documents

- Architecture: [ARCHITECTURE.md](./ARCHITECTURE.md)
- Existing deployment references:
  `FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md`
  `DEPLOYMENT_PLAN.md`
  `LAUNCH_TODAY.md`

## Full Deploy Checklist

### Code and Repo

- [x] Create the new GitHub repo `robs46859-eng/robarkham`.
- [x] Repoint local `origin` from `stack-arkham` to `robs46859-eng/robarkham`.
- [ ] Confirm the default branch and protection rules.
- [ ] Verify the production branch passes tests and builds.

### Infrastructure

- [x] Confirm the active deployment target and runtime. (Azure Container Apps)
- [x] Provision frontend host. (Vercel/Netlify referenced in script)
- [x] Provision backend container runtime. (Azure Container Apps - fullstackarkham-env)
- [ ] Provision PostgreSQL.
- [ ] Provision Redis.
- [ ] Provision secret storage.
- [ ] Provision logging, metrics, and alerting.

### Configuration and Secrets

- [x] Set production database credentials.
- [x] Set production Redis connection values.
- [ ] Set `JWT_SECRET`.
- [ ] Set all provider API keys.
- [ ] Set live billing secrets if billing is enabled.
- [x] Set `APP_DOMAIN=https://robcotech.pro`.
- [ ] Set API base values for `api.robcotech.pro`.

### Domain and TLS

- [ ] Point `robcotech.pro` to the frontend host.
- [ ] Point `api.robcotech.pro` to the public gateway / ingress.
- [ ] Point `www.robcotech.pro` appropriately.
- [ ] Verify TLS certificates for both frontend and API hosts.

### Data and Runtime Validation

- [ ] Apply database migrations.
- [ ] Verify all critical tables exist.
- [ ] Verify service startup ordering and readiness.
- [ ] Verify worker loop execution.
- [ ] Verify queue processing.
- [ ] Verify internal service-to-service routing.

### App Validation

- [ ] Frontend loads successfully at `https://robcotech.pro`.
- [ ] Public health endpoint passes.
- [ ] Critical API routes respond successfully.
- [ ] Auth flow succeeds.
- [ ] Media-commerce and orchestration flows succeed.
- [ ] Billing flow and webhooks succeed if enabled.

### Launch Operations

- [ ] Prepare rollback plan.
- [ ] Freeze changes during cutover.
- [ ] Run staging smoke tests before production cutover.
- [ ] Run production smoke tests immediately after deploy.
- [ ] Confirm log ingestion and alert routing.

## Exit Criteria

- [ ] `robcotech.pro` is serving production frontend traffic.
- [ ] `api.robcotech.pro` is healthy and reachable.
- [ ] Core workflows succeed end to end.
- [ ] Rollback and monitoring are ready.
