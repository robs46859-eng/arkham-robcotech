# Arkham Launch Day Plan

**Domain:** `robcotech.pro`
**Status:** Not ready for cutover until cleanup completes
**Date:** 2026-04-29

## Immediate Priorities

1. finish Azure-first documentation cleanup
2. remove or neutralize legacy GCS and GCP assumptions
3. validate local stack and orchestration health
4. confirm production env and secret ownership

## Pre-Cutover Validation

Run before any production launch:

```bash
python3 -m pytest services/orchestration/tests/ services/media-commerce/tests/ --tb=short -q
docker-compose build
docker-compose up -d
```

Minimum checks:

- gateway health
- orchestration health
- worker loop behavior
- billing health
- media-commerce workflow success

## Launch Preconditions

- `robcotech.pro` frontend path is finalized
- `api.robcotech.pro` gateway path is finalized
- production database and redis are provisioned
- required secrets are set
- orchestration flows are validated
- rollback is documented

## Do Not Launch If

- docs still point operators to a competing platform path
- critical services fail health checks
- worker or queue behavior is unstable
- media-commerce depends on local workflow logic outside orchestration
