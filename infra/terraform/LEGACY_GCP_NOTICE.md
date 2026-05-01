# Legacy GCP Notice

This directory contains legacy GCP-oriented Terraform for an older Arkham deployment story.

It is not the active production path.

## Current Rule

Arkham is Azure-first for production operations.

Do not treat the files in this directory as authoritative unless the project explicitly decides to revive and modernize this path.

## Why This Notice Exists

This repository previously carried mixed deployment assumptions:

- GKE
- Cloud SQL
- Memorystore
- GCS Terraform backend

Those assumptions now conflict with the active Azure-first model.

## Status

- retained for historical or alternate reference only
- deprecated for active deployment work
- must not override `README.md`, `ARCHITECTURE.md`, `DEPLOYMENT_PLAN.md`, or `FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md`

