from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AzureBoundaries:
    allowed_locations: tuple[str, ...] = ("eastus", "centralus")
    allowed_prefixes: tuple[str, ...] = (
        "arkham-",
        "fullstackarkham",
        "robcotech",
        "api.robcotech.pro",
    )


@dataclass(frozen=True)
class ArkhamDeploymentProfile:
    app_domain: str = "robcotech.pro"
    api_domain: str = "api.robcotech.pro"
    resource_group: str = "fullstackarkham-prod"
    location: str = "eastus"
    postgres_location: str = "centralus"
    acr_name: str = "fullstackarkhamacr"
    container_apps_env: str = "fullstackarkham-env"
    postgres_server_name: str = "arkham-psql"
    redis_name: str = "arkham-redis"
    services: tuple[str, ...] = (
        "web",
        "gateway",
        "arkham",
        "bim-ingestion",
        "orchestration",
        "semantic-cache",
        "memory",
        "billing",
        "media-commerce",
    )
    approval_token: str = "ARKHAM_DEPLOY_APPROVED"
    read_only_command_prefixes: tuple[str, ...] = (
        "docker-compose config -q",
        "./scripts/deploy-bot.sh --status",
        "./scripts/deploy-bot.sh --dns",
        "./scripts/deploy-bot.sh --smoke",
        "./scripts/deploy-bot.sh --logs ",
        "git status --short",
        "git diff --stat --",
    )
    mutating_command_prefixes: tuple[str, ...] = (
        "./scripts/deploy-bot.sh --setup",
        "./scripts/deploy-bot.sh --deploy",
        "./scripts/deploy-bot.sh --snapshot",
        "./scripts/deploy-bot.sh --rollback",
    )
    authoritative_docs: tuple[str, ...] = (
        "README.md",
        "ARCHITECTURE.md",
        "FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md",
        "LAUNCH_STATUS.md",
        "scripts/deploy-bot.sh",
    )


BOUNDARIES = AzureBoundaries()
DEPLOYMENT_PROFILE = ArkhamDeploymentProfile()
