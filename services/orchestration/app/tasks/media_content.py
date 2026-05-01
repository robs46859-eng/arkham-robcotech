"""
Media-commerce task executors.

These executors bridge the horizontal orchestration layer to bounded,
deterministic media-commerce agent capabilities.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict

from app.tasks import TaskExecutor

SERVICE_ROOT = Path(__file__).resolve().parents[2]
MEDIA_COMMERCE_ROOT = SERVICE_ROOT.parent / "media-commerce"
if str(MEDIA_COMMERCE_ROOT) not in sys.path:
    sys.path.insert(0, str(MEDIA_COMMERCE_ROOT))

from app.agents.content_engine import ContentEngineAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class ContentStrategyGenerationExecutor(TaskExecutor):
    """Generate a deterministic content strategy through the media-commerce vertical agent."""

    @property
    def task_type(self) -> str:
        return "content_strategy_generation"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        vertical = input_data.get("vertical")
        topic = input_data.get("topic")
        goals = input_data.get("goals", [])

        if not tenant_id or not vertical or not topic:
            return {
                "success": False,
                "error": "tenant_id, vertical, and topic are required in workflow input_data",
            }

        agent = ContentEngineAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        strategy = await agent.create_content_strategy(
            tenant_id=tenant_id,
            vertical=vertical,
            topic=topic,
            goals=goals,
        )

        logger.info("Generated content strategy for workflow %s", workflow_id)
        return {
            "success": True,
            "strategy": strategy,
            "content": strategy,
            "strategy_summary": {
                "topic": strategy["topic"],
                "primary_goal": strategy["primary_goal"],
                "channels": strategy["distribution_channels"],
            },
        }
