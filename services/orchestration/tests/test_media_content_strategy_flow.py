import asyncio
import importlib
import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]


def _load_orchestration_modules():
    if str(SERVICE_ROOT) in sys.path:
        sys.path.remove(str(SERVICE_ROOT))
    sys.path.insert(0, str(SERVICE_ROOT))
    for key in list(sys.modules):
        if key == "app" or key.startswith("app."):
            sys.modules.pop(key)
    registry_module = importlib.import_module("app.flows.registry")
    main_module = importlib.import_module("app.main")
    return registry_module, main_module


registry_module, main_module = _load_orchestration_modules()
FlowRegistry = registry_module.FlowRegistry
WorkflowStartRequest = main_module.WorkflowStartRequest
app = main_module.app
start_workflow = main_module.start_workflow


class FakeCheckpointStore:
    def __init__(self):
        self.saved = []

    async def save_workflow(self, workflow):
        self.saved.append(workflow.copy())


class FakeTaskQueue:
    def __init__(self):
        self.enqueued = []

    async def enqueue(self, **kwargs):
        self.enqueued.append(kwargs)
        return "task-1"


def test_media_content_strategy_flow_is_registered():
    registry = FlowRegistry()
    asyncio.run(registry.register_built_in_flows())

    assert registry.has_flow("media_content_strategy") is True
    flow = registry.get_flow("media_content_strategy")
    assert flow.description
    assert [step.name for step in flow.steps] == [
        "retrieve_memory_context",
        "generate_strategy",
        "validate_strategy",
        "store_strategy_artifact",
    ]
    assert flow.steps[1].task_type == "content_strategy_generation"


def test_start_workflow_enqueues_first_media_content_strategy_step():
    registry = FlowRegistry()
    asyncio.run(registry.register_built_in_flows())
    checkpoint_store = FakeCheckpointStore()
    task_queue = FakeTaskQueue()

    app.state.flow_registry = registry
    app.state.checkpoint_store = checkpoint_store
    app.state.task_queue = task_queue

    response = asyncio.run(
        start_workflow(
            WorkflowStartRequest(
                workflow_type="media_content_strategy",
                tenant_id="tenant-123",
                input_data={
                    "tenant_id": "tenant-123",
                    "vertical": "media",
                    "topic": "affiliate content optimization",
                    "goals": ["revenue", "awareness"],
                },
                metadata={"source_service": "media-commerce"},
            )
        )
    )

    assert response.status == "running"
    assert response.current_step == "retrieve_memory_context"
    assert len(checkpoint_store.saved) == 2
    assert task_queue.enqueued[0]["task_type"] == "memory_retrieval"
    assert task_queue.enqueued[0]["step_name"] == "retrieve_memory_context"
