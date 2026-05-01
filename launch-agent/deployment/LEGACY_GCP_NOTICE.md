# Legacy GCP and Cloud Run Notice

This deployment subtree was generated from an older Google-oriented ADK deployment scaffold.

It is not the active Arkham production deployment path.

## Deprecated Assumptions

The files under this subtree include legacy assumptions such as:

- Cloud Run deployment
- GCS-backed telemetry
- BigQuery-oriented telemetry tables
- Google-specific CI and Terraform wiring

## Current Rule

Arkham production operations are Azure-first.

The `launch-agent` package is also planning-only and is not the production execution authority.

## How To Use This Directory

- historical reference only
- alternate scaffold source only
- do not use as the current deployment contract

