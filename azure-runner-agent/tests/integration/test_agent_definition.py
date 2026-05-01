import pytest

pytest.importorskip("google.adk.agents")

from app.agent import root_agent


def test_root_agent_is_arkham_specific() -> None:
    assert root_agent.name == "arkham_deployment_subagent"
    assert "robcotech.pro" in root_agent.instruction
    assert "inspect_arkham_deployment_drift" in root_agent.instruction


def test_root_agent_exposes_expected_tools() -> None:
    tool_names = {tool.__name__ for tool in root_agent.tools}
    assert tool_names == {
        "get_arkham_deployment_context",
        "inspect_arkham_deployment_drift",
        "plan_arkham_deployment_action",
        "run_approved_repo_command",
    }
