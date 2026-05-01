import json

from app.base_parameters import DEPLOYMENT_PROFILE
from app.deployment_tools import (
    get_arkham_deployment_context,
    inspect_arkham_deployment_drift,
    plan_arkham_deployment_action,
    run_approved_repo_command,
)


def test_get_arkham_deployment_context_contains_expected_domains() -> None:
    payload = json.loads(get_arkham_deployment_context())
    assert payload["domains"]["app"] == "robcotech.pro"
    assert payload["domains"]["api"] == "api.robcotech.pro"
    assert payload["approval_token"] == DEPLOYMENT_PROFILE.approval_token


def test_inspect_arkham_deployment_drift_detects_known_repo_drift() -> None:
    payload = json.loads(inspect_arkham_deployment_drift())
    issues = {finding["file"]: finding["issue"] for finding in payload["findings"]}
    assert ".env.production" in issues
    assert ".github/workflows/deploy-to-prod.yaml" in issues
    assert "infra/terraform/main.tf" in issues


def test_plan_arkham_deployment_action_for_deploy() -> None:
    payload = json.loads(plan_arkham_deployment_action("deploy"))
    assert payload["action"] == "deploy"
    assert payload["commands"] == ["./scripts/deploy-bot.sh --deploy"]
    assert payload["approval_required"] is True


def test_run_approved_repo_command_requires_token_for_mutation() -> None:
    payload = json.loads(run_approved_repo_command("./scripts/deploy-bot.sh --deploy"))
    assert payload["status"] == "approval_required"


def test_run_approved_repo_command_allows_read_only_checks() -> None:
    payload = json.loads(run_approved_repo_command("docker-compose config -q"))
    assert payload["command_type"] == "read_only"
    assert payload["status"] in {"completed", "failed"}
