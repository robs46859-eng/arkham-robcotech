"""
Tests for Workflow Worker

Validates that the worker correctly dequeues and executes tasks.
"""

import asyncio
import sys
from pathlib import Path

import pytest

SERVICE_ROOT = Path(__file__).resolve().parents[1]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from app.worker import WorkflowWorker
from app.queues import TaskQueue
from app.tasks import TaskExecutor, TaskExecutorRegistry


class MockTaskQueue:
    """Mock task queue for testing"""

    def __init__(self, tasks=None):
        self._tasks = tasks or []
        self._dequeue_count = 0

    async def dequeue(self):
        if self._tasks:
            self._dequeue_count += 1
            return self._tasks.pop(0)
        return None

    async def complete_task(self, task_id, output):
        pass

    async def enqueue(self, **kwargs):
        return f"task-{kwargs.get('step_name')}"


class MockCheckpointStore:
    """Mock checkpoint store for testing"""

    def __init__(self, flow_registry=None):
        self._workflows = {}
        self._saved = []
        self._completed = []
        self._failed = []
        self.flow_registry = flow_registry

    async def get_workflow(self, workflow_id):
        return self._workflows.get(workflow_id)

    async def save_workflow(self, workflow):
        self._saved.append(workflow.copy())

    async def checkpoint_step(self, workflow_id, step_name, result):
        pass

    async def mark_workflow_completed(self, workflow_id):
        self._completed.append(workflow_id)

    async def mark_workflow_failed(self, workflow_id, error, last_checkpoint=None):
        self._failed.append({"workflow_id": workflow_id, "error": error})


class MockExecutor(TaskExecutor):
    """Mock executor for testing"""

    def __init__(self, task_type="mock_task", success=True, output=None):
        self._task_type = task_type
        self._success = success
        self._output = output or {"result": "mock_output"}
        self.executed = []

    @property
    def task_type(self) -> str:
        return self._task_type

    async def execute(self, workflow_id, step_name, step_data, workflow_state):
        self.executed.append({
            "workflow_id": workflow_id,
            "step_name": step_name,
            "step_data": step_data,
        })
        return {"success": self._success, **self._output}


class TestWorkflowWorker:
    """Test workflow worker"""

    @pytest.fixture
    def executor_registry(self):
        registry = TaskExecutorRegistry()
        registry.register(MockExecutor())
        return registry

    @pytest.fixture
    def checkpoint_store(self):
        store = MockCheckpointStore()
        return store

    def test_worker_processes_single_task(
        self,
        executor_registry,
        checkpoint_store,
    ):
        """Test worker processes one task successfully"""
        task_queue = MockTaskQueue([
            {
                "task_id": "task-1",
                "workflow_id": "wf-1",
                "step_name": "step_one",
                "task_type": "mock_task",
                "step_data": {},
            }
        ])

        checkpoint_store._workflows["wf-1"] = {
            "workflow_id": "wf-1",
            "flow_type": "test_flow",
            "workflow_state": {},
            "status": "running",
        }

        worker = WorkflowWorker(
            task_queue=task_queue,
            checkpoint_store=checkpoint_store,
            executor_registry=executor_registry,
        )

        result = asyncio.run(worker.process_next_task())

        assert result is not None
        assert result["success"] is True
        assert len(checkpoint_store._saved) == 1

    def test_worker_skips_completed_workflow(
        self,
        executor_registry,
        checkpoint_store,
    ):
        """Test worker skips tasks for completed workflows"""
        task_queue = MockTaskQueue([
            {
                "task_id": "task-1",
                "workflow_id": "wf-completed",
                "step_name": "step_one",
                "task_type": "mock_task",
                "step_data": {},
            }
        ])

        checkpoint_store._workflows["wf-completed"] = {
            "workflow_id": "wf-completed",
            "status": "completed",
        }

        worker = WorkflowWorker(
            task_queue=task_queue,
            checkpoint_store=checkpoint_store,
            executor_registry=executor_registry,
        )

        # Worker returns None when skipping completed workflow
        # but the task is still completed in the queue
        result = asyncio.run(worker.process_next_task())

        # Task was processed (completed with error in queue)
        assert task_queue._dequeue_count == 1

    def test_worker_handles_executor_failure(
        self,
        executor_registry,
        checkpoint_store,
    ):
        """Test worker handles executor failure correctly"""
        # Register failing executor
        failing_executor = MockExecutor(success=False, output={"error": "test error"})
        executor_registry.register(failing_executor)

        task_queue = MockTaskQueue([
            {
                "task_id": "task-1",
                "workflow_id": "wf-2",
                "step_name": "step_one",
                "task_type": "mock_task",
                "step_data": {},
            }
        ])

        checkpoint_store._workflows["wf-2"] = {
            "workflow_id": "wf-2",
            "flow_type": "test_flow",
            "workflow_state": {},
            "status": "running",
        }

        worker = WorkflowWorker(
            task_queue=task_queue,
            checkpoint_store=checkpoint_store,
            executor_registry=executor_registry,
        )

        result = asyncio.run(worker.process_next_task())

        assert result is not None
        assert result["success"] is False
        assert len(checkpoint_store._failed) == 1

    def test_worker_drain_processes_multiple_tasks(
        self,
        executor_registry,
        checkpoint_store,
    ):
        """Test worker drain processes multiple tasks"""
        task_queue = MockTaskQueue([
            {
                "task_id": "task-1",
                "workflow_id": "wf-1",
                "step_name": "step_one",
                "task_type": "mock_task",
                "step_data": {},
            },
            {
                "task_id": "task-2",
                "workflow_id": "wf-2",
                "step_name": "step_one",
                "task_type": "mock_task",
                "step_data": {},
            },
            {
                "task_id": "task-3",
                "workflow_id": "wf-3",
                "step_name": "step_one",
                "task_type": "mock_task",
                "step_data": {},
            },
        ])

        for i in range(1, 4):
            checkpoint_store._workflows[f"wf-{i}"] = {
                "workflow_id": f"wf-{i}",
                "flow_type": "test_flow",
                "workflow_state": {},
                "status": "running",
            }

        worker = WorkflowWorker(
            task_queue=task_queue,
            checkpoint_store=checkpoint_store,
            executor_registry=executor_registry,
        )

        result = asyncio.run(worker.drain(max_tasks=10))

        assert result["processed"] == 3
        assert result["successful"] == 3
        assert result["failed"] == 0


class _FakeRedisClient:
    def __init__(self):
        self.zadd_calls = []
        self.zunionstore_calls = []
        self.zremrangebyscore_calls = []
        self.zpopmin_calls = []
        self._queued_tasks = {}

    async def zadd(self, queue_name, payload):
        self.zadd_calls.append((queue_name, payload))
        if payload:
            task_data = next(iter(payload.keys()))
            self._queued_tasks.setdefault(queue_name, []).append(task_data)

    async def zunionstore(self, queue_name, sources, aggregate="max"):
        self.zunionstore_calls.append((queue_name, tuple(sources), aggregate))

    async def zremrangebyscore(self, queue_name, minimum, maximum):
        self.zremrangebyscore_calls.append((queue_name, minimum, maximum))

    async def zpopmin(self, queue_name, count=1):
        self.zpopmin_calls.append((queue_name, count))
        queued = self._queued_tasks.get(queue_name, [])
        if not queued:
            return []
        return [(queued.pop(0), 0)]


def test_task_queue_defaults_to_workflow_queue_name():
    queue = TaskQueue("redis://unused")
    fake_client = _FakeRedisClient()
    queue.client = fake_client

    task_id = asyncio.run(
        queue.enqueue(
            task_type="mock_task",
            workflow_id="wf-queue-1",
            step_name="step_one",
            step_data={"sample": True},
        )
    )
    dequeued = asyncio.run(queue.dequeue())
    asyncio.run(queue.complete_task(task_id, {"success": True}))

    assert fake_client.zadd_calls[0][0] == "workflow_tasks"
    assert fake_client.zunionstore_calls[0][0] == "workflow_tasks"
    assert fake_client.zpopmin_calls[0][0] == "workflow_tasks"
    assert dequeued["workflow_id"] == "wf-queue-1"

    def test_worker_stops_when_queue_empty(
        self,
        executor_registry,
        checkpoint_store,
    ):
        """Test worker stops when queue is empty"""
        task_queue = MockTaskQueue([])

        worker = WorkflowWorker(
            task_queue=task_queue,
            checkpoint_store=checkpoint_store,
            executor_registry=executor_registry,
        )

        result = asyncio.run(worker.drain(max_tasks=10))

        assert result["processed"] == 0
        assert result["stopped"] is True
