from __future__ import annotations

import json
import re
import shlex
import subprocess
from pathlib import Path

from app.base_parameters import DEPLOYMENT_PROFILE

REPO_ROOT = Path(__file__).resolve().parents[2]
APPROVAL_MESSAGE = (
    "This command changes Azure or deployment state. Re-run with "
    f"approval_token={DEPLOYMENT_PROFILE.approval_token!r} after explicit user approval."
)


def _read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _normalize_command(command: str) -> str:
    return re.sub(r"\s+", " ", command.strip())


def _contains_disallowed_shell_features(command: str) -> bool:
    disallowed_tokens = ("&&", "||", ";", "|", "`", "$(")
    return any(token in command for token in disallowed_tokens)


def _match_command_prefix(command: str, prefixes: tuple[str, ...]) -> bool:
    return any(command == prefix or command.startswith(prefix) for prefix in prefixes)


def _classify_command(command: str) -> str:
    normalized = _normalize_command(command)
    if _match_command_prefix(normalized, DEPLOYMENT_PROFILE.read_only_command_prefixes):
        return "read_only"
    if _match_command_prefix(normalized, DEPLOYMENT_PROFILE.mutating_command_prefixes):
        return "mutating"
    return "blocked"


def _arkham_port_findings() -> list[dict[str, str]]:
    compose = _read_text("docker-compose.yml")
    arkham_dockerfile = _read_text("services/arkham/Dockerfile")
    arkham_main = _read_text("services/arkham/app/main.py")

    compose_maps_host_8081 = '"8081:8081"' in compose
    dockerfile_uses_8080 = "--port\", \"8080" in arkham_dockerfile or "EXPOSE 8080" in arkham_dockerfile
    main_uses_8081 = "port=8081" in arkham_main

    findings: list[dict[str, str]] = []
    if compose_maps_host_8081 and dockerfile_uses_8080 and main_uses_8081:
        findings.append(
            {
                "severity": "warning",
                "file": "docker-compose.yml / services/arkham/Dockerfile / services/arkham/app/main.py",
                "issue": "Arkham local port contract is split across 8081 host mapping, 8080 container image defaults, and 8081 app runtime defaults.",
            }
        )
    return findings


def get_arkham_deployment_context() -> str:
    """Return the active Arkham deployment contract from local repo state."""
    payload = {
        "project": "Arkham",
        "deployment_authority": "Azure-first",
        "domains": {
            "app": DEPLOYMENT_PROFILE.app_domain,
            "api": DEPLOYMENT_PROFILE.api_domain,
        },
        "azure_profile": {
            "resource_group": DEPLOYMENT_PROFILE.resource_group,
            "location": DEPLOYMENT_PROFILE.location,
            "postgres_location": DEPLOYMENT_PROFILE.postgres_location,
            "acr_name": DEPLOYMENT_PROFILE.acr_name,
            "container_apps_env": DEPLOYMENT_PROFILE.container_apps_env,
            "postgres_server_name": DEPLOYMENT_PROFILE.postgres_server_name,
            "redis_name": DEPLOYMENT_PROFILE.redis_name,
        },
        "services": list(DEPLOYMENT_PROFILE.services),
        "authoritative_docs": list(DEPLOYMENT_PROFILE.authoritative_docs),
        "active_entrypoint": "./scripts/deploy-bot.sh",
        "approval_token": DEPLOYMENT_PROFILE.approval_token,
    }
    return json.dumps(payload, indent=2)


def inspect_arkham_deployment_drift() -> str:
    """Inspect repo files for deployment drift against the Azure-first Arkham target."""
    findings: list[dict[str, str]] = []

    env_production = _read_text(".env.production")
    if "stelar.host" in env_production:
        findings.append(
            {
                "severity": "high",
                "file": ".env.production",
                "issue": "Production env file still targets stelar.host instead of robcotech.pro.",
            }
        )

    workflow = _read_text(".github/workflows/deploy-to-prod.yaml")
    if "google-github-actions" in workflow or "Cloud Run" in workflow:
        findings.append(
            {
                "severity": "high",
                "file": ".github/workflows/deploy-to-prod.yaml",
                "issue": "Production CI workflow still deploys via Google Cloud tooling instead of the Azure-first path.",
            }
        )

    terraform = _read_text("infra/terraform/main.tf")
    if 'source  = "hashicorp/google"' in terraform or 'backend "gcs"' in terraform:
        findings.append(
            {
                "severity": "high",
                "file": "infra/terraform/main.tf",
                "issue": "Terraform stack is still GCP/GKE/Cloud SQL based.",
            }
        )

    compose = _read_text("docker-compose.yml")
    if "version: '3.8'" in compose:
        findings.append(
            {
                "severity": "low",
                "file": "docker-compose.yml",
                "issue": "Compose file still declares an obsolete version key.",
            }
        )

    findings.extend(_arkham_port_findings())

    summary = {
        "deployment_target": "Azure-first Arkham on robcotech.pro / api.robcotech.pro",
        "findings": findings,
    }
    return json.dumps(summary, indent=2)


def plan_arkham_deployment_action(action: str) -> str:
    """Return the exact Arkham deployment steps and repo commands for an action."""
    normalized = action.strip().lower()
    plans = {
        "setup": {
            "summary": "Provision or reconcile Azure infra, Key Vault secrets, Redis, PostgreSQL, and Container Apps environment.",
            "commands": ["./scripts/deploy-bot.sh --setup"],
            "approval_required": True,
            "checks": [
                "Azure CLI authenticated",
                "Docker daemon running",
                "Key Vault secret inputs available",
            ],
        },
        "deploy": {
            "summary": "Build local container images, push them to ACR, then update all Azure Container Apps.",
            "commands": ["./scripts/deploy-bot.sh --deploy"],
            "approval_required": True,
            "checks": [
                "docker-compose config -q",
                "git diff --stat -- scripts/deploy-bot.sh docker-compose.yml apps/web/next.config.js",
                "./scripts/deploy-bot.sh --snapshot",
            ],
        },
        "verify": {
            "summary": "Check current Azure Container Apps state, DNS plan, and smoke-test production traffic.",
            "commands": [
                "./scripts/deploy-bot.sh --status",
                "./scripts/deploy-bot.sh --dns",
                "./scripts/deploy-bot.sh --smoke",
            ],
            "approval_required": False,
            "checks": ["Inspect unresolved drift before trusting results"],
        },
        "rollback": {
            "summary": "Rollback to the latest known-good Azure Container Apps revision snapshot.",
            "commands": ["./scripts/deploy-bot.sh --rollback"],
            "approval_required": True,
            "checks": ["Confirm the snapshot exists and identify the failed revision"],
        },
        "logs": {
            "summary": "Stream Azure Container Apps logs for one Arkham service.",
            "commands": ["./scripts/deploy-bot.sh --logs <service-name>"],
            "approval_required": False,
            "checks": [f"Service must be one of: {', '.join(DEPLOYMENT_PROFILE.services)}"],
        },
    }

    if normalized not in plans:
        return json.dumps(
            {
                "error": f"Unsupported action: {action}",
                "supported_actions": sorted(plans.keys()),
            },
            indent=2,
        )

    response = {"action": normalized, **plans[normalized]}
    if response["approval_required"]:
        response["approval_token"] = DEPLOYMENT_PROFILE.approval_token
    return json.dumps(response, indent=2)


def run_approved_repo_command(command: str, approval_token: str = "") -> str:
    """
    Run a repo-scoped Arkham deployment or diagnostics command.

    Read-only commands can run immediately. Mutating commands require
    approval_token='ARKHAM_DEPLOY_APPROVED'.
    """
    normalized = _normalize_command(command)
    if _contains_disallowed_shell_features(normalized):
        return json.dumps(
            {
                "status": "blocked",
                "reason": "Shell chaining and redirection features are not allowed.",
                "command": normalized,
            },
            indent=2,
        )

    command_type = _classify_command(normalized)
    if command_type == "blocked":
        return json.dumps(
            {
                "status": "blocked",
                "reason": "Command is outside the Arkham deployment allowlist.",
                "command": normalized,
                "allowed_read_only_prefixes": list(
                    DEPLOYMENT_PROFILE.read_only_command_prefixes
                ),
                "allowed_mutating_prefixes": list(
                    DEPLOYMENT_PROFILE.mutating_command_prefixes
                ),
            },
            indent=2,
        )

    if (
        command_type == "mutating"
        and approval_token != DEPLOYMENT_PROFILE.approval_token
    ):
        return json.dumps(
            {
                "status": "approval_required",
                "command": normalized,
                "message": APPROVAL_MESSAGE,
            },
            indent=2,
        )

    result = subprocess.run(
        shlex.split(normalized),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    payload = {
        "status": "completed" if result.returncode == 0 else "failed",
        "command": normalized,
        "command_type": command_type,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    return json.dumps(payload, indent=2)
