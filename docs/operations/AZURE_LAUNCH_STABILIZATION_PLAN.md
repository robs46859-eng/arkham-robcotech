# Azure Launch And Stabilization Plan

Generated: 2026-04-29

## Decisions

- Azure is authoritative for frontend and backend production hosting.
- `apps/web` is the only launch frontend.
- `apps/admin` and `apps/docs` are deferred until after core stabilization.
- `robcotech.pro` and `www.robcotech.pro` route to the Azure Container Apps frontend.
- `api.robcotech.pro` routes to the gateway/API ingress.
- Stripe is enabled at launch.
- Hostinger owns DNS for `robcotech.pro`.
- Rollback target is the previous known-good Azure Container Apps revision set.

## Step Outline

1. Freeze launch scope around the horizontal platform and `apps/web`.
2. Confirm branch protection, production branch, and build/test status.
3. Validate the local Docker baseline before production deployment.
4. Provision or verify Azure Container Apps, ACR, PostgreSQL, Redis, Key Vault, logging, metrics, and alerts.
5. Populate required secrets, including database, Redis, JWT, provider keys, and Stripe live keys/webhook secrets.
6. Build and deploy backend platform services to Azure Container Apps.
7. Build and deploy `apps/web` to Azure Container Apps.
8. Snapshot known-good Azure revisions before DNS cutover or risky releases.
9. Generate Hostinger DNS records from live Azure values.
10. Apply Hostinger DNS records manually in hPanel unless a separate approved browser automation flow is used.
11. Poll DNS propagation from the deployment machine.
12. Bind Azure managed certificates and custom domains after DNS validation passes.
13. Run production smoke tests for frontend, API health, auth, orchestration, media-commerce, and Stripe.
14. If smoke tests fail, shift traffic back to the known-good revision snapshot.
15. Stabilize post-launch through daily platform checks and drift control.

## Milestone Checklist

### M1: Scope Locked

- [ ] `apps/web` is confirmed as the only launch frontend.
- [ ] `apps/admin` is explicitly deferred.
- [ ] `apps/docs` is explicitly deferred.
- [ ] Stripe launch mode is confirmed as live.
- [ ] DNS owner and access path are confirmed as Hostinger hPanel.

### M2: Local Baseline

- [ ] `docker-compose.yml` parses.
- [ ] Local platform services start.
- [ ] Gateway health passes.
- [ ] Orchestration worker starts.
- [ ] Queue processing is verified.
- [ ] Frontend can reach API routes locally or through configured service URLs.

### M3: Azure Infrastructure

- [ ] Resource group exists.
- [ ] Azure Container Registry exists.
- [ ] Azure Container Apps environment exists.
- [ ] Managed PostgreSQL exists and is reachable.
- [ ] Managed Redis exists and is reachable.
- [ ] Key Vault exists.
- [ ] Logging, metrics, and alerting are available.

### M4: Secrets And Config

- [ ] Database credentials are set.
- [ ] Redis values are set.
- [ ] `JWT_SECRET` is set.
- [ ] Provider API keys are set.
- [ ] Stripe live secret key is set.
- [ ] Stripe webhook secret is set.
- [ ] `APP_DOMAIN=https://robcotech.pro` is set where required.
- [ ] `API_URL=https://api.robcotech.pro` is set where required.

### M5: Deployment

- [ ] Known-good revision snapshot is captured before deployment.
- [ ] Backend services build and push to ACR.
- [ ] `apps/web` builds and pushes to ACR.
- [ ] Backend services deploy to Azure Container Apps.
- [ ] Frontend deploys to Azure Container Apps.
- [ ] Frontend runtime env is applied.
- [ ] Service readiness checks pass.

### M6: DNS And TLS

- [ ] `scripts/aca_dns_plan.sh --print` produces Hostinger records.
- [ ] Hostinger records are backed up before edits.
- [ ] Hostinger records are applied.
- [ ] `scripts/aca_dns_plan.sh --poll` confirms propagation.
- [ ] `scripts/aca_dns_plan.sh --bind` binds Azure managed certificates.
- [ ] `robcotech.pro` serves HTTPS.
- [ ] `www.robcotech.pro` serves HTTPS.
- [ ] `api.robcotech.pro` serves HTTPS.

### M7: Launch Smoke

- [ ] Frontend loads.
- [ ] API health passes.
- [ ] Auth flow passes.
- [ ] Orchestration workflow creation passes.
- [ ] Worker processing passes.
- [ ] Media-commerce flow passes.
- [ ] Stripe checkout passes.
- [ ] Stripe webhook handling passes.
- [ ] Logs and alerts show expected traffic.

### M8: Rollback Gate

- [ ] `scripts/aca_revision_gate.sh --snapshot` captures known-good revisions.
- [ ] `scripts/aca_revision_gate.sh --smoke` runs production smoke checks.
- [ ] `scripts/aca_revision_gate.sh --gate <snapshot>` is available for automatic rollback on failed smoke.
- [ ] Database migration rollback is documented separately.
- [ ] Stripe dashboard/config rollback is documented separately.
- [ ] DNS restore path through Hostinger DNS history is understood.

### M9: Post-Launch Stabilization

- [ ] Daily gateway health and upstream connectivity checks run.
- [ ] Daily orchestration queue, worker, checkpoint, and retry checks run.
- [ ] Daily semantic-cache checks run.
- [ ] Daily memory retrieval checks run.
- [ ] Daily billing and Stripe error checks run.
- [ ] Daily arkham security event/audit checks run.
- [ ] Deployment/documentation drift is recorded and resolved.

## Automation Commands

```bash
./scripts/deploy-bot.sh --snapshot
./scripts/deploy-bot.sh --deploy
./scripts/deploy-bot.sh --dns
./scripts/aca_dns_plan.sh --poll
./scripts/aca_dns_plan.sh --bind
./scripts/deploy-bot.sh --smoke
./scripts/deploy-bot.sh --rollback
```

For a gated release after a snapshot:

```bash
SNAPSHOT="$(./scripts/aca_revision_gate.sh --snapshot)"
./scripts/deploy-bot.sh --deploy
./scripts/aca_revision_gate.sh --gate "$SNAPSHOT"
```

## Rollback Meaning

Azure Container Apps revisions are immutable deployment snapshots. If a new revision never becomes ready, Azure can keep traffic on the old ready revision. If the new revision starts but fails business smoke tests, Arkham automation must explicitly shift traffic back to the previously captured known-good revision.

This rollback does not automatically reverse database migrations, Stripe dashboard changes, DNS edits, or global secret changes. Those need separate launch-specific rollback steps.
