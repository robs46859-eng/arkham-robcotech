# DESIGN_SPEC.md

## Overview

Build a launch-focused ADK agent for the `robcotech.pro` project. The agent should understand the local repo layout, generate Azure-first deployment plans for backend and database resources, prepare GitHub push and publish steps, and coordinate a GitHub Pages frontend deployment. It must also generate DNS and hosting relationship updates for `robcotech.pro`, `www.robcotech.pro`, and `api.robcotech.pro`.

## Example Use Cases

1. "Plan a production deployment for robcotech.pro"
   Expected output: ordered launch plan for git push, Azure provisioning, backend deploy, GitHub Pages deploy, and DNS cutover.

2. "Show me the exact Azure commands for backend deploy"
   Expected output: resource group, registry, container apps, PostgreSQL, Redis, and image deployment commands.

3. "Prepare DNS updates for the frontend and API"
   Expected output: GitHub Pages A/CNAME records for the frontend and Azure target records for the API.

4. "Push the current repo and deploy the frontend"
   Expected output: exact commands first, followed by execution only after explicit user approval.

5. "Run a periodic launch review"
   Expected output: recurring review checklist and verification commands for git, Azure, GitHub Pages, DNS, and health endpoints.

## Tools Required

1. Local command execution for git, gh, az, docker, npm, and shell utilities.
2. Repo inspection for status and current remote configuration.
3. Launch plan synthesis using the local architecture and launch docs.
4. Periodic production review planning.

## Constraints & Safety Rules

1. Backend services and databases stay on Azure.
2. Frontend may be deployed to GitHub Pages.
3. The agent must not execute mutating commands until the user explicitly approves the exact command.
4. The agent should prefer project-local paths and the checked-in deployment docs as its source of truth.

## Success Criteria

1. The agent can summarize the project deployment topology.
2. The agent can emit executable Azure, GitHub, and DNS command plans.
3. The agent can run approved commands after confirming them with the user.
4. The agent exposes a stable launch command and a repeatable periodic review path.
