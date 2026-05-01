"""
Workflow Worker

Dequeues and executes workflow tasks from the task queue.
Processes tasks step-by-step, checkpointing state between steps.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class WorkflowWorker:
    """
    Workflow Worker - Dequeues and executes workflow tasks

    Responsibilities:
    - Dequeue one task from workflow_tasks queue
    - Load workflow from checkpoint store
    - Skip cancelled/completed workflows
    - Resolve executor from TaskExecutorRegistry
    - Execute task
    - Write step output into workflow state
    - Checkpoint successful step output
    - Enqueue next step if one exists
    - Mark workflow completed when final step finishes
    - Mark workflow failed on executor failure
    """

    def __init__(
        self,
        task_queue,
        checkpoint_store,
        executor_registry,
        flow_registry=None,
        poll_interval: float = 1.0,
    ):
        self.task_queue = task_queue
        self.checkpoint_store = checkpoint_store
        self.executor_registry = executor_registry
        self.flow_registry = flow_registry
        self.poll_interval = poll_interval
        self._running = False

    async def process_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Dequeue and process one task

        Returns:
            Task result dict or None if no tasks available
        """
        # Dequeue next pending task
        task = await self.task_queue.dequeue()
        if not task:
            return None

        task_id = task.get("task_id")
        workflow_id = task.get("workflow_id")
        step_name = task.get("step_name")
        task_type = task.get("task_type")
        step_data = task.get("step_data", {})

        logger.info(
            "Processing task %s (workflow=%s, step=%s, type=%s)",
            task_id,
            workflow_id,
            step_name,
            task_type,
        )

        try:
            # Load workflow from checkpoint store
            workflow = await self.checkpoint_store.get_workflow(workflow_id)
            if not workflow:
                logger.error("Workflow %s not found in checkpoint store", workflow_id)
                await self.task_queue.complete_task(
                    task_id,
                    {
                        "success": False,
                        "error": f"Workflow {workflow_id} not found",
                    },
                )
                return None

            # Skip cancelled/completed workflows
            workflow_status = workflow.get("status")
            if workflow_status in ("completed", "failed", "cancelled"):
                logger.info(
                    "Skipping task for %s workflow %s",
                    workflow_status,
                    workflow_id,
                )
                await self.task_queue.complete_task(
                    task_id,
                    {
                        "success": False,
                        "error": f"Workflow {workflow_id} is {workflow_status}",
                    },
                )
                return None

            # Get executor for task type
            executor = self.executor_registry.get_executor(task_type)
            if not executor:
                error_msg = f"No executor registered for task type: {task_type}"
                logger.error(error_msg)
                await self.task_queue.complete_task(
                    task_id,
                    {"success": False, "error": error_msg},
                )
                await self.checkpoint_store.mark_workflow_failed(
                    workflow_id,
                    error_msg,
                )
                return None

            # Execute task
            workflow_state = workflow.get("workflow_state", {})
            # Executors need the root workflow envelope plus prior step outputs.
            execution_context = {**workflow, **workflow_state}
            result = await executor.execute(
                workflow_id=workflow_id,
                step_name=step_name,
                step_data=step_data,
                workflow_state=execution_context,
            )

            # Check execution result
            if not result.get("success"):
                error_msg = result.get("error", "Unknown executor error")
                logger.error(
                    "Task %s failed: %s",
                    task_id,
                    error_msg,
                )
                await self.task_queue.complete_task(task_id, result)
                await self.checkpoint_store.mark_workflow_failed(
                    workflow_id,
                    error_msg,
                    last_checkpoint={step_name: result},
                )
                return result

            # Save step output to workflow state
            workflow_state[step_name] = result
            await self.checkpoint_store.save_workflow(workflow)

            # Checkpoint successful step output
            await self.checkpoint_store.checkpoint_step(
                workflow_id,
                step_name,
                result,
            )

            # Get flow definition to find next step
            flow_type = workflow.get("workflow_type") or workflow.get("flow_type")
            flow_def = None
            flow_registry = self.flow_registry or getattr(self.checkpoint_store, "flow_registry", None)
            if flow_registry:
                flow_def = flow_registry.get_flow(flow_type)

            if flow_def:
                current_step_index = next(
                    (i for i, s in enumerate(flow_def.steps) if s.name == step_name),
                    -1,
                )

                next_step_index = current_step_index + 1

                if next_step_index < len(flow_def.steps):
                    # Enqueue next step
                    next_step = flow_def.steps[next_step_index]
                    next_task_id = await self.task_queue.enqueue(
                        workflow_id=workflow_id,
                        task_type=next_step.task_type,
                        step_name=next_step.name,
                        step_data=next_step.config,
                    )
                    logger.info(
                        "Enqueued next step %s (task=%s)",
                        next_step.name,
                        next_task_id,
                    )
                else:
                    # All steps complete - mark workflow as completed
                    await self.checkpoint_store.mark_workflow_completed(workflow_id)
                    logger.info("Workflow %s completed successfully", workflow_id)
            else:
                # No flow definition - just mark task complete
                logger.info("Task %s completed (no flow definition for next step)", task_id)

            # Mark task as completed
            await self.task_queue.complete_task(task_id, result)

            logger.info("Task %s completed successfully", task_id)
            return result

        except Exception as exc:
            error_msg = f"Task execution error: {exc}"
            logger.exception("Task %s failed with exception", task_id)

            await self.task_queue.complete_task(
                task_id,
                {"success": False, "error": error_msg},
            )

            if workflow_id:
                await self.checkpoint_store.mark_workflow_failed(
                    workflow_id,
                    error_msg,
                    last_checkpoint={step_name: {"error": error_msg}},
                )

            return {"success": False, "error": error_msg}

    async def drain(self, max_tasks: int = 100) -> Dict[str, Any]:
        """
        Process up to max_tasks from the queue

        Args:
            max_tasks: Maximum number of tasks to process

        Returns:
            Summary of processed tasks
        """
        processed = 0
        successful = 0
        failed = 0

        while processed < max_tasks:
            result = await self.process_next_task()
            if result is None:
                break  # No more tasks

            processed += 1
            if result.get("success"):
                successful += 1
            else:
                failed += 1

        return {
            "processed": processed,
            "successful": successful,
            "failed": failed,
            "stopped": processed < max_tasks,
        }

    async def run_forever(self):
        """
        Run worker loop indefinitely

        Continuously processes tasks with poll_interval between empty dequeues.
        """
        self._running = True
        logger.info("Worker started (poll_interval=%ss)", self.poll_interval)

        while self._running:
            result = await self.process_next_task()

            if result is None:
                # No tasks available, wait before polling again
                await asyncio.sleep(self.poll_interval)

    def stop(self):
        """Stop the worker loop"""
        self._running = False
        logger.info("Worker stopped")


# Import asyncio at module level for run_forever
import asyncio  # noqa: E402
