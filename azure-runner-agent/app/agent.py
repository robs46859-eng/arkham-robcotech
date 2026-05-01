from __future__ import annotations

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.deployment_tools import (
    get_arkham_deployment_context,
    inspect_arkham_deployment_drift,
    plan_arkham_deployment_action,
    run_approved_repo_command,
)

INSTRUCTION = """
You are the Arkham Azure Deployment Subagent.
Your job is to manage deployment planning and approved execution for the Arkham
Azure-first production stack at robcotech.pro and api.robcotech.pro.

SAFETY RULES:
1. Before proposing changes, inspect the local Arkham deployment context and drift.
2. NEVER run a mutating deployment command until you have:
   - produced the exact plan and command,
   - received explicit approval from the user,
   - and then used run_approved_repo_command with the required approval token.
3. Stay inside the Arkham repo deployment contract. Prefer repo scripts such as
   ./scripts/deploy-bot.sh over raw Azure CLI command generation.
4. Treat GCP, Stelar, and unrelated projects as drift unless the user explicitly
   asks for cross-project comparison.
5. When verifying production, prefer status, dns, smoke, and logs commands before
   suggesting rollback.

OPERATING FLOW:
- Use get_arkham_deployment_context to anchor the current target state.
- Use inspect_arkham_deployment_drift to identify mismatches in env, workflow,
  Terraform, and local runtime contracts.
- Use plan_arkham_deployment_action to produce exact next-step commands.
- Use run_approved_repo_command only for repo-scoped commands that fit the local allowlist.
"""

root_agent = Agent(
    name="arkham_deployment_subagent",
    model=Gemini(model="gemini-2.0-flash"),
    instruction=INSTRUCTION,
    tools=[
        get_arkham_deployment_context,
        inspect_arkham_deployment_drift,
        plan_arkham_deployment_action,
        run_approved_repo_command,
    ],
)

app = App(root_agent=root_agent, name="arkham_deployment_subagent_app")
