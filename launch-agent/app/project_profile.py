from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class ProjectProfile:
    agent_name: str
    project_name: str
    domain: str
    api_domain: str
    repo_owner: str
    repo_name: str
    repo_url: str
    repo_root: str
    backend_root: str
    frontend_root: str
    frontend_publish_dir: str
    azure_resource_group: str
    azure_location: str
    azure_container_registry: str
    azure_container_env: str
    azure_postgres_server: str
    azure_redis_name: str
    container_services: list[str] = field(default_factory=list)
    architecture_doc: str = ""
    launch_doc: str = ""
    deployment_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


PROFILE = ProjectProfile(
    agent_name="robarkham_launch_agent",
    project_name="RobArkham",
    domain="robcotech.pro",
    api_domain="api.robcotech.pro",
    repo_owner="robs46859-eng",
    repo_name="robarkham",
    repo_url="https://github.com/robs46859-eng/robarkham.git",
    repo_root="..",
    backend_root="..",
    frontend_root="../apps/web",
    frontend_publish_dir="dist",
    azure_resource_group="robarkham-rg",
    azure_location="eastus",
    azure_container_registry="robarkhamacr",
    azure_container_env="robarkham-env",
    azure_postgres_server="robarkham-postgres",
    azure_redis_name="robarkham-redis",
    container_services=[
        "gateway",
        "billing",
        "semantic-cache",
        "orchestration",
        "memory",
        "arkham",
        "bim_ingestion",
        "media-commerce",
    ],
    architecture_doc="../ARCHITECTURE.md",
    launch_doc="../LAUNCH_LIST.md",
    deployment_refs=[
        "../FULLSTACKARKHAM_DEPLOYMENT_GUIDE.md",
        "../DEPLOYMENT_PLAN.md",
        "../LAUNCH_TODAY.md",
    ],
)
