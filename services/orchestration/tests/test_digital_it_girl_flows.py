import asyncio
import importlib
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

SERVICE_ROOT = Path(__file__).resolve().parents[1]


def _reload_app_module(module_name: str):
    if str(SERVICE_ROOT) in sys.path:
        sys.path.remove(str(SERVICE_ROOT))
    sys.path.insert(0, str(SERVICE_ROOT))
    for key in list(sys.modules):
        if key == "app" or key.startswith("app."):
            sys.modules.pop(key)
    return importlib.import_module(module_name)


registry_module = _reload_app_module("app.flows.registry")
tasks_module = importlib.import_module("app.tasks.digital_it_girl")
artifact_module = importlib.import_module("app.tasks.artifact")
worker_module = importlib.import_module("app.worker")
task_base_module = importlib.import_module("app.tasks")

FlowRegistry = registry_module.FlowRegistry
MarketResearchSynthesisExecutor = tasks_module.MarketResearchSynthesisExecutor
NicheOpportunityScoringExecutor = tasks_module.NicheOpportunityScoringExecutor
ArtifactStorageExecutor = artifact_module.ArtifactStorageExecutor
WorkflowWorker = worker_module.WorkflowWorker
TaskExecutorRegistry = task_base_module.TaskExecutorRegistry


def test_digital_it_girl_predictive_niche_flow_is_registered():
    registry = FlowRegistry()
    asyncio.run(registry.register_built_in_flows())

    assert registry.has_flow("digital_it_girl_predictive_niche") is True
    flow = registry.get_flow("digital_it_girl_predictive_niche")
    assert [step.name for step in flow.steps] == [
        "score_segment_opportunity",
        "synthesize_market_brief",
        "store_niche_artifact",
    ]
    assert flow.steps[0].task_type == "niche_opportunity_scoring"
    assert flow.steps[1].task_type == "market_research_synthesis"
    assert flow.steps[2].config["source_step"] == "synthesize_market_brief"
    assert flow.steps[2].config["content_field"] == "market_brief"


def test_niche_opportunity_scoring_executor_uses_segment_filters_and_signals():
    executor = NicheOpportunityScoringExecutor()

    result = asyncio.run(
        executor.execute(
            workflow_id="wf-dig-1",
            step_name="score_segment_opportunity",
            step_data={"focus": "hair loss complaints"},
            workflow_state={
                "input_data": {
                    "segment_filters": {
                        "region": "Atlanta",
                        "industry": "Beauty",
                        "demographic": "Working professionals",
                    },
                    "trend_signals": [{"velocity": 4}, {"velocity": "3.5"}],
                    "complaint_signals": [{"severity": 2}, {"severity": "1.5"}],
                    "review_signals": [{"gap_score": 2.5}],
                }
            },
        )
    )

    assert result["success"] is True
    assert result["opportunity_score"] > 54
    assert result["watchlist_tags"] == ["Atlanta", "Beauty", "hair loss complaints"]


def test_market_research_synthesis_executor_uses_previous_scoring_result():
    executor = MarketResearchSynthesisExecutor()
    response_payload = {
        "choices": [
            {
                "message": {
                    "content": '{"niche_definition":"beauty niche","ideal_price":"$49"}'
                }
            }
        ]
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json = Mock(return_value=response_payload)

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.post.return_value = mock_response

    with patch("app.tasks.digital_it_girl.httpx.AsyncClient", return_value=mock_client):
        result = asyncio.run(
            executor.execute(
                workflow_id="wf-dig-2",
                step_name="synthesize_market_brief",
                step_data={"mode": "balanced"},
                workflow_state={
                    "input_data": {
                        "segment_filters": {"region": "Seattle", "demographic": "Creators"},
                        "trend_signals": [{"velocity": 6}],
                    },
                    "score_segment_opportunity": {"opportunity_score": 88.4},
                },
            )
        )

    assert result["success"] is True
    assert result["brief_status"] == "ai_synthesized"
    assert "ideal_price" in result["market_brief"]


def test_market_research_synthesis_executor_falls_back_locally():
    executor = MarketResearchSynthesisExecutor()
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.post.side_effect = RuntimeError("gateway offline")

    with patch("app.tasks.digital_it_girl.httpx.AsyncClient", return_value=mock_client):
        result = asyncio.run(
            executor.execute(
                workflow_id="wf-dig-3",
                step_name="synthesize_market_brief",
                step_data={},
                workflow_state={
                    "input_data": {
                        "segment_filters": {"region": "Miami", "demographic": "Parents"},
                    }
                },
            )
        )

    assert result["success"] is True
    assert result["brief_status"] == "local_fallback"
    assert "Miami" in result["market_brief"]


class _FakeConnection:
    def __init__(self):
        self.execute_calls = []

    async def execute(self, query, *args):
        self.execute_calls.append((query, args))


class _FakeAcquire:
    def __init__(self, connection):
        self.connection = connection

    async def __aenter__(self):
        return self.connection

    async def __aexit__(self, exc_type, exc, tb):
        return False


class _FakePool:
    def __init__(self):
        self.connection = _FakeConnection()

    def acquire(self):
        return _FakeAcquire(self.connection)


def test_artifact_storage_executor_persists_database_artifact():
    executor = ArtifactStorageExecutor()
    executor.__class__._database_pool = None
    executor.__class__._database_pool_url = None
    fake_pool = _FakePool()
    fake_asyncpg = Mock()
    fake_asyncpg.create_pool = AsyncMock(return_value=fake_pool)

    with patch.object(artifact_module, "asyncpg", fake_asyncpg):
        result = asyncio.run(
            executor.execute(
                workflow_id="wf-dig-artifact",
                step_name="store_niche_artifact",
                step_data={
                    "storage": "database",
                    "source_step": "synthesize_market_brief",
                    "content_field": "market_brief",
                },
                workflow_state={
                    "tenant_id": "tenant-1",
                    "synthesize_market_brief": {
                        "market_brief": {"ideal_price": "$49", "niche_definition": "beauty niche"}
                    },
                },
            )
        )

    assert result["success"] is True
    assert result["storage_type"] == "database"
    assert "artifact_id" in result
    assert fake_asyncpg.create_pool.await_count == 1
    assert len(fake_pool.connection.execute_calls) == 2


class _MockTaskQueue:
    def __init__(self, tasks=None):
        self._tasks = tasks or []
        self.enqueued = []
        self.completed = []

    async def dequeue(self):
        if self._tasks:
            return self._tasks.pop(0)
        return None

    async def complete_task(self, task_id, output):
        self.completed.append((task_id, output))

    async def enqueue(self, **kwargs):
        self.enqueued.append(kwargs)
        return f"task-{kwargs.get('step_name')}"


class _MockCheckpointStore:
    def __init__(self, workflow, flow_registry):
        self.workflow = workflow
        self.flow_registry = flow_registry
        self.saved = []
        self.completed = []
        self.failed = []
        self.checkpoints = []

    async def get_workflow(self, workflow_id):
        return self.workflow

    async def save_workflow(self, workflow):
        self.saved.append(workflow.copy())

    async def checkpoint_step(self, workflow_id, step_name, result):
        self.checkpoints.append((workflow_id, step_name, result))

    async def mark_workflow_completed(self, workflow_id):
        self.completed.append(workflow_id)

    async def mark_workflow_failed(self, workflow_id, error, last_checkpoint=None):
        self.failed.append((workflow_id, error, last_checkpoint))


class _RecordingExecutor:
    @property
    def task_type(self):
        return "niche_opportunity_scoring"

    def __init__(self):
        self.seen_state = None

    async def execute(self, workflow_id, step_name, step_data, workflow_state):
        self.seen_state = workflow_state
        return {"success": True, "opportunity_score": 81.2}


def test_worker_passes_workflow_envelope_and_enqueues_next_step():
    registry = FlowRegistry()
    asyncio.run(registry.register_built_in_flows())

    executor_registry = TaskExecutorRegistry()
    executor = _RecordingExecutor()
    executor_registry.register(executor)

    task_queue = _MockTaskQueue(
        [
            {
                "task_id": "task-1",
                "workflow_id": "wf-dig-4",
                "step_name": "score_segment_opportunity",
                "task_type": "niche_opportunity_scoring",
                "step_data": {"vertical": "digital_it_girl"},
            }
        ]
    )
    workflow = {
        "id": "wf-dig-4",
        "tenant_id": "tenant-1",
        "workflow_type": "digital_it_girl_predictive_niche",
        "status": "running",
        "workflow_state": {},
        "input_data": {"segment_filters": {"region": "Chicago"}},
        "operational_state": {"retry_count": 0},
    }
    checkpoint_store = _MockCheckpointStore(workflow, registry)

    worker = WorkflowWorker(
        task_queue=task_queue,
        checkpoint_store=checkpoint_store,
        executor_registry=executor_registry,
        flow_registry=registry,
    )

    result = asyncio.run(worker.process_next_task())

    assert result["success"] is True
    assert executor.seen_state["input_data"]["segment_filters"]["region"] == "Chicago"
    assert task_queue.enqueued[0]["step_name"] == "synthesize_market_brief"
