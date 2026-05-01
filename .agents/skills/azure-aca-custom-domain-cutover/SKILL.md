---
name: azure-aca-custom-domain-cutover
description: Use when binding Azure Container Apps custom domains, propagating DNS at Hostinger or another DNS provider, validating asuid or managed-certificate TXT records, or finishing TLS cutover for apex, www, and api hostnames on the FullStackArkham Azure stack.
---

# Azure ACA Custom Domain Cutover

Use this skill for the final DNS and certificate phase after Container Apps are already deployed.

Primary apps in this repo:
- `web` for `robcotech.pro` and `www.robcotech.pro`
- `gateway` for `api.robcotech.pro`

## Workflow

1. Confirm the live ACA FQDNs first.
Use:
- `az containerapp show --resource-group fullstackarkham-prod --name web --query properties.configuration.ingress.fqdn -o tsv`
- `az containerapp show --resource-group fullstackarkham-prod --name gateway --query properties.configuration.ingress.fqdn -o tsv`

2. Print or inspect the repo DNS plan.
Primary script:
- `./scripts/aca_dns_plan.sh --print`

3. Verify public DNS before touching certificates.
Use:
- `dig +short robcotech.pro A`
- `dig +short www.robcotech.pro CNAME`
- `dig +short api.robcotech.pro CNAME`
- `dig +short asuid.robcotech.pro TXT`
- `dig +short asuid.www.robcotech.pro TXT`
- `dig +short asuid.api.robcotech.pro TXT`

4. Add hostnames to the apps.
Use:
- `az containerapp hostname add --resource-group fullstackarkham-prod --name web --hostname robcotech.pro`
- `az containerapp hostname add --resource-group fullstackarkham-prod --name web --hostname www.robcotech.pro`
- `az containerapp hostname add --resource-group fullstackarkham-prod --name gateway --hostname api.robcotech.pro`

5. Bind TLS with the CLI shape supported on the current machine.
First inspect:
- `az containerapp hostname bind -h`
- `az containerapp env certificate create -h`

Preferred rule:
- Use `hostname bind` with `--validation-method HTTP` for apex when supported.
- Use `hostname bind` with `--validation-method CNAME` for subdomains when supported.
- If this CLI requires explicit environment-managed certificates first, create them with `az containerapp env certificate create`, wait for `Succeeded`, then bind with `--certificate`.

6. Verify the ACA hostname state.
Use:
- `az containerapp hostname list --resource-group fullstackarkham-prod --name web -o table`
- `az containerapp hostname list --resource-group fullstackarkham-prod --name gateway -o table`
- `az containerapp env certificate list --resource-group fullstackarkham-prod --name fullstackarkham-env -o table`

7. Verify HTTPS only after hostname binding is enabled.
Use:
- `curl -sSI https://robcotech.pro`
- `curl -sSI https://www.robcotech.pro`
- `curl -sSI https://api.robcotech.pro`

## Triage Rules

- If `hostname list` is empty, the hostnames were never added.
- If hostnames show `Disabled`, DNS may be present but certificate binding is not complete.
- If `curl` returns connection reset, do not assume the app is down. Check hostname binding and certificate provisioning first.
- If only one TXT record is missing, fix that specific hostname instead of reworking all DNS.
- `asuid.www` is commonly forgotten. Check it explicitly.
- Preview managed-certificate flows may emit a TXT token that is different from the `asuid` ownership TXT. Treat the CLI output as authoritative for that specific certificate request.

## Repo-Specific Notes

- The deploy script prints placeholder eastus URLs at the end. Use the actual ACA FQDNs from Azure, not the static summary lines.
- The active deployment workflow is Azure-first. Ignore older GCP-oriented materials.

## References

Read when needed:
- `references/architecture.md`
- `references/graphify.md`
