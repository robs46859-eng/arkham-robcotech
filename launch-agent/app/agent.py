from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.project_profile import PROFILE

os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

ROOT = (Path(__file__).resolve().parent / PROFILE.repo_root).resolve()


def _run(command: str, cwd: Path | None = None) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(cwd or ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return json.dumps(
            {
                "ok": True,
                "command": command,
                "cwd": str(cwd or ROOT),
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            },
            indent=2,
        )
    except subprocess.CalledProcessError as exc:
        return json.dumps(
            {
                "ok": False,
                "command": command,
                "cwd": str(cwd or ROOT),
                "stdout": exc.stdout.strip(),
                "stderr": exc.stderr.strip(),
                "returncode": exc.returncode,
            },
            indent=2,
        )


def get_project_profile() -> dict:
    """Return the project deployment profile and fixed hosting policy."""
    data = PROFILE.to_dict()
    data["hosting_policy"] = {
        "backend": "Azure only",
        "database": "Azure only",
        "frontend": "GitHub Pages allowed",
    }
    return data


def inspect_repo_status() -> dict:
    """Inspect current git remote, branch, and worktree status."""
    branch = _run("git branch --show-current")
    remote = _run("git remote -v")
    status = _run("git status --short")
    return {"branch": branch, "remote": remote, "status": status}


def get_agent_commands() -> dict:
    """Return canonical launch, deploy, and review commands for this agent package."""
    agent_root = Path(__file__).resolve().parent.parent
    launch_cmd = f"cd {agent_root} && uv run uvicorn app.fast_api_app:app --reload"
    deploy_cmd = (
        "Use the agent tool `plan_full_launch` first, then execute approved commands via "
        "`run_local_command` for git push, Azure deploy, GitHub Pages deploy, and DNS updates."
    )
    review_cmd = (
        "Use the agent tool `plan_periodic_review` and then run any approved health, git, "
        "or DNS verification commands with `run_local_command`."
    )
    return {
        "launch_command": launch_cmd,
        "deploy_command": deploy_cmd,
        "periodic_review_command": review_cmd,
    }


def read_launch_context() -> dict:
    """Read the local architecture and launch docs the agent should rely on."""
    docs: dict[str, str] = {}
    for rel in [PROFILE.architecture_doc, PROFILE.launch_doc, *PROFILE.deployment_refs]:
        path = (Path(__file__).resolve().parent / rel).resolve()
        if path.exists():
            docs[str(path)] = path.read_text(encoding="utf-8")
    return docs


def plan_git_push(commit_message: str = "Launch agent deployment update") -> dict:
    """Generate the exact git and GitHub commands for publishing current changes."""
    commands = [
        f"git -C {ROOT} status --short",
        f"git -C {ROOT} add .",
        f"git -C {ROOT} commit -m {json.dumps(commit_message)}",
        f"git -C {ROOT} push origin main",
    ]
    return {
        "purpose": "publish current repository state",
        "repo": PROFILE.repo_url,
        "commands": commands,
        "approval_required": True,
    }


def plan_github_pages_deploy(build_command: str = "npm ci && npm run build") -> dict:
    """Generate a GitHub Pages deployment plan for the frontend."""
    frontend = (Path(__file__).resolve().parent / PROFILE.frontend_root).resolve()
    publish_dir = frontend / PROFILE.frontend_publish_dir
    commands = [
        f"cd {frontend} && {build_command}",
        f"printf '%s\\n' '{PROFILE.domain}' > {publish_dir}/CNAME",
        f"gh repo edit {PROFILE.repo_owner}/{PROFILE.repo_name} --homepage https://{PROFILE.domain}",
        f"gh pages deploy {publish_dir} --repo {PROFILE.repo_owner}/{PROFILE.repo_name} --branch gh-pages",
    ]
    dns = {
        "root_a_records": [
            "185.199.108.153",
            "185.199.109.153",
            "185.199.110.153",
            "185.199.111.153",
        ],
        "www_cname": f"{PROFILE.repo_owner}.github.io",
    }
    return {
        "purpose": "deploy frontend to GitHub Pages",
        "frontend_root": str(frontend),
        "publish_dir": str(publish_dir),
        "commands": commands,
        "dns_requirements": dns,
        "approval_required": True,
    }


def plan_azure_backend_deploy(image_tag: str = "latest") -> dict:
    """Generate the Azure-first backend and database deployment commands."""
    backend = (Path(__file__).resolve().parent / PROFILE.backend_root).resolve()
    registry = f"{PROFILE.azure_container_registry}.azurecr.io"
    commands = [
        f"az group create --name {PROFILE.azure_resource_group} --location {PROFILE.azure_location}",
        f"az acr create --resource-group {PROFILE.azure_resource_group} --name {PROFILE.azure_container_registry} --sku Basic",
        f"az containerapp env create --name {PROFILE.azure_container_env} --resource-group {PROFILE.azure_resource_group} --location {PROFILE.azure_location}",
        (
            "az postgres flexible-server create "
            f"--resource-group {PROFILE.azure_resource_group} "
            f"--name {PROFILE.azure_postgres_server} "
            f"--location {PROFILE.azure_location} "
            "--sku-name Standard_B1ms --version 16 "
            "--admin-user postgres --admin-password '<set-secret>'"
        ),
        (
            f"az redis create --name {PROFILE.azure_redis_name} "
            f"--resource-group {PROFILE.azure_resource_group} "
            f"--location {PROFILE.azure_location} --sku Basic --vm-size c0"
        ),
        f"az acr login --name {PROFILE.azure_container_registry}",
    ]
    for service in PROFILE.container_services:
        service_dir = backend / "services" / service
        commands.append(
            f"docker build -t {registry}/{service}:{image_tag} {service_dir}"
        )
        commands.append(f"docker push {registry}/{service}:{image_tag}")
        commands.append(
            "az containerapp create "
            f"--name {PROFILE.project_name.lower()}-{service} "
            f"--resource-group {PROFILE.azure_resource_group} "
            f"--environment {PROFILE.azure_container_env} "
            f"--image {registry}/{service}:{image_tag} "
            "--ingress external --target-port 8080"
        )
    return {
        "purpose": "deploy backend services and data dependencies to Azure",
        "backend_root": str(backend),
        "services": PROFILE.container_services,
        "commands": commands,
        "approval_required": True,
    }


def plan_dns_updates(
    dns_provider: str = "external",
    zone_resource_group: str = "",
    zone_name: str = "",
) -> dict:
    """Generate DNS update instructions for GitHub Pages frontend and Azure API."""
    frontend_target = f"{PROFILE.repo_owner}.github.io"
    api_target = (
        f"{PROFILE.project_name.lower()}-gateway.{PROFILE.azure_location}.azurecontainerapps.io"
    )
    external = {
        "root_domain": {
            "type": "A",
            "host": "@",
            "values": [
                "185.199.108.153",
                "185.199.109.153",
                "185.199.110.153",
                "185.199.111.153",
            ],
        },
        "www": {"type": "CNAME", "host": "www", "value": frontend_target},
        "api": {"type": "CNAME", "host": "api", "value": api_target},
    }
    azure_commands: list[str] = []
    if dns_provider == "azure_dns" and zone_resource_group and zone_name:
        azure_commands = [
            (
                "az network dns record-set cname set-record "
                f"--resource-group {zone_resource_group} --zone-name {zone_name} "
                f"--record-set-name www --cname {frontend_target}"
            ),
            (
                "az network dns record-set cname set-record "
                f"--resource-group {zone_resource_group} --zone-name {zone_name} "
                f"--record-set-name api --cname {api_target}"
            ),
        ]
        for idx, ip in enumerate(external["root_domain"]["values"], start=1):
            azure_commands.append(
                "az network dns record-set a add-record "
                f"--resource-group {zone_resource_group} --zone-name {zone_name} "
                f"--record-set-name @ --ipv4-address {ip}"
            )
    return {
        "purpose": "update frontend and API DNS/hosting relationships",
        "frontend_target": frontend_target,
        "api_target": api_target,
        "external_dns_records": external,
        "azure_dns_commands": azure_commands,
        "approval_required": True,
    }


def plan_full_launch(
    image_tag: str = "latest",
    build_command: str = "npm ci && npm run build",
    dns_provider: str = "external",
    zone_resource_group: str = "",
    zone_name: str = "",
) -> dict:
    """Assemble the full launch sequence for git, Azure, GitHub Pages, and DNS."""
    return {
        "profile": get_project_profile(),
        "steps": [
            {"name": "inspect_repo_status", "details": inspect_repo_status()},
            {"name": "git_push", "details": plan_git_push()},
            {"name": "azure_backend", "details": plan_azure_backend_deploy(image_tag=image_tag)},
            {"name": "github_pages", "details": plan_github_pages_deploy(build_command=build_command)},
            {
                "name": "dns_updates",
                "details": plan_dns_updates(
                    dns_provider=dns_provider,
                    zone_resource_group=zone_resource_group,
                    zone_name=zone_name,
                ),
            },
        ],
    }


def plan_periodic_review(review_interval: str = "weekly") -> dict:
    """Generate a recurring operational review for git, Azure, Pages, DNS, and health."""
    checks = [
        "review git branch, remote, and worktree drift",
        "verify Azure resource group, container apps, PostgreSQL, and Redis health",
        "verify GitHub Pages deployment and custom domain state",
        "verify frontend and API DNS records still point at the intended targets",
        "verify public health endpoints and critical app routes",
        "review deployment docs against current infrastructure and repo reality",
    ]
    commands = [
        f"git -C {ROOT} status --short",
        f"git -C {ROOT} remote -v",
        f"az containerapp list --resource-group {PROFILE.azure_resource_group}",
        f"az postgres flexible-server show --resource-group {PROFILE.azure_resource_group} --name {PROFILE.azure_postgres_server}",
        f"az redis show --resource-group {PROFILE.azure_resource_group} --name {PROFILE.azure_redis_name}",
        f"gh repo view {PROFILE.repo_owner}/{PROFILE.repo_name}",
        f"curl -I https://{PROFILE.domain}",
        f"curl -I https://{PROFILE.api_domain}/health",
    ]
    return {
        "purpose": "periodic production review",
        "interval": review_interval,
        "checks": checks,
        "commands": commands,
        "approval_required": True,
    }


def run_local_command(command: str, working_directory: str = "") -> str:
    """Execute a local command after explicit user approval."""
    cwd = Path(working_directory).resolve() if working_directory else ROOT
    return _run(command, cwd=cwd)


INSTRUCTION = f"""
You are {PROFILE.project_name} Launch Agent.

Model policy:
- Use Gemini 2.0 Flash for reasoning and tool selection.

Operating policy:
- Backend services and databases must stay on Azure.
- Frontend may be deployed to GitHub Pages.
- Always consult the local architecture and launch docs before giving deployment advice.
- For any mutating action, first present the exact command or commands and wait for explicit approval.
- Prefer project-local paths and the configured repo/hosting profile over generic advice.

Primary responsibilities:
1. plan git push and repo publication steps
2. plan Azure backend and database deployment
3. plan GitHub Pages frontend deployment
4. plan DNS and hosting relationship updates
5. expose a clear launch command, deploy path, and periodic review path
6. execute approved commands when the user explicitly authorizes them
"""

root_agent = Agent(
    name=PROFILE.agent_name,
    model=Gemini(
        model="gemini-2.0-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=INSTRUCTION,
    tools=[
        get_project_profile,
        inspect_repo_status,
        get_agent_commands,
        read_launch_context,
        plan_git_push,
        plan_github_pages_deploy,
        plan_azure_backend_deploy,
        plan_dns_updates,
        plan_full_launch,
        plan_periodic_review,
        run_local_command,
    ],
)

app = App(root_agent=root_agent, name=f"{PROFILE.agent_name}_app")
