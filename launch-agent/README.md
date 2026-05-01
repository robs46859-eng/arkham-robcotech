# RobArkham Launch Agent

ADK launch agent for `robcotech.pro`.

## Purpose

This agent is specialized for:

1. planning and approving Azure-first backend deployment
2. planning git push and repo publication steps
3. coordinating GitHub Pages frontend deployment
4. generating DNS cutover steps for frontend and API domains

## Runtime Model

- Model: `gemini-2.0-flash`
- Backend and database target: Azure
- Frontend target: GitHub Pages

## Usage

```bash
cd arkham/launch-agent
uv run uvicorn app.fast_api_app:app --reload
```

## Launch Command

```bash
cd /Users/joeiton/Desktop/gemini428ew/arkham/launch-agent
uv run uvicorn app.fast_api_app:app --reload
```

## Deploy Path

Ask the agent to run:

- `plan_full_launch`
- `plan_azure_backend_deploy`
- `plan_github_pages_deploy`
- `plan_dns_updates`

Then approve exact commands before execution with `run_local_command`.

## Periodic Review

Ask the agent to run:

- `plan_periodic_review`

Recommended cadence: weekly, and again after every production deployment.

The agent is intentionally approval-gated. It should present exact commands before it runs any modifying action.

## Operating Rule

This package is planning-only. It may inspect and plan, but it is not the production execution authority.
