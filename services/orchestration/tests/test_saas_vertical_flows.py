import asyncio
import importlib
import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]


def _load_registry_module():
    if str(SERVICE_ROOT) in sys.path:
        sys.path.remove(str(SERVICE_ROOT))
    sys.path.insert(0, str(SERVICE_ROOT))
    for key in list(sys.modules):
        if key == "app" or key.startswith("app."):
            sys.modules.pop(key)
    return importlib.import_module("app.flows.registry")


registry_module = _load_registry_module()
FlowRegistry = registry_module.FlowRegistry


def test_saas_pipeline_routing_flow_is_registered():
    registry = FlowRegistry()
    asyncio.run(registry.register_built_in_flows())

    assert registry.has_flow("saas_pipeline_routing") is True
    flow = registry.get_flow("saas_pipeline_routing")
    assert [step.name for step in flow.steps] == [
        "score_pipeline_intent",
        "evaluate_deal_fit",
        "create_follow_up_artifact",
    ]
    assert flow.steps[0].task_type == "lead_routing"


def test_saas_signup_conversion_flow_is_registered():
    registry = FlowRegistry()
    asyncio.run(registry.register_built_in_flows())

    assert registry.has_flow("saas_signup_conversion") is True
    flow = registry.get_flow("saas_signup_conversion")
    assert [step.name for step in flow.steps] == [
        "review_signup_events",
        "generate_conversion_actions",
        "queue_conversion_work",
    ]
    assert flow.steps[1].config["vertical"] == "saas"


def test_saas_retention_watch_flow_is_registered():
    registry = FlowRegistry()
    asyncio.run(registry.register_built_in_flows())

    assert registry.has_flow("saas_retention_watch") is True
    flow = registry.get_flow("saas_retention_watch")
    assert [step.name for step in flow.steps] == [
        "collect_lifecycle_signals",
        "classify_retention_risk",
        "draft_retention_brief",
        "store_retention_brief",
    ]
    assert flow.steps[2].config["output_schema"] == "retention_watch_brief"
