"""
Mediation task executor.

Bridges horizontal orchestration to MediationAgent capabilities:
- Content quality prediction
- Approval/rejection recording
- Feedback for ContentEngine
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

from app.tasks import TaskExecutor

SERVICE_ROOT = Path(__file__).resolve().parents[2]
MEDIA_COMMERCE_ROOT = SERVICE_ROOT.parent / "media-commerce"
if str(MEDIA_COMMERCE_ROOT) not in sys.path:
    sys.path.insert(0, str(MEDIA_COMMERCE_ROOT))

from app.agents.mediation import MediationAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class ContentQualityPredictionExecutor(TaskExecutor):
    """Predict content quality before generation using MediationAgent."""

    @property
    def task_type(self) -> str:
        return "content_quality_prediction"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        topic = input_data.get("topic")
        content_type = input_data.get("content_type", "article")
        keywords = input_data.get("keywords", [])

        if not tenant_id or not topic:
            return {
                "success": False,
                "error": "tenant_id and topic are required in workflow input_data",
            }

        agent = MediationAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.predict_content_quality(
            tenant_id=tenant_id,
            topic=topic,
            content_type=content_type,
            keywords=keywords,
        )

        logger.info(
            "Quality prediction for '%s': score=%.2f, recommendation=%s",
            topic,
            result["predicted_quality_score"],
            result["recommendation"],
        )

        return {
            "success": True,
            "prediction": result,
            "should_proceed": result["recommendation"] != "block",
            "quality_score": result["predicted_quality_score"],
            "blocking_reason": result.get("blocking_reason"),
        }


class RecordContentDecisionExecutor(TaskExecutor):
    """Record content approval/rejection decision using MediationAgent."""

    @property
    def task_type(self) -> str:
        return "record_content_decision"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        content_id = input_data.get("content_id")
        decision = input_data.get("decision")  # approved, rejected, modified
        decision_reason = input_data.get("decision_reason")
        content_metadata = input_data.get("content_metadata", {})

        if not tenant_id or not content_id or not decision:
            return {
                "success": False,
                "error": "tenant_id, content_id, and decision are required",
            }

        agent = MediationAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.record_content_decision(
            tenant_id=tenant_id,
            content_id=content_id,
            decision=decision,
            decision_reason=decision_reason,
            content_metadata=content_metadata,
        )

        logger.info(
            "Content decision recorded: %s → %s (patterns: %s)",
            content_id,
            decision,
            result["pattern_analysis"]["pattern"],
        )

        return {
            "success": True,
            "decision_recorded": result,
            "pattern_analysis": result["pattern_analysis"],
        }


class ContentEngineFeedbackExecutor(TaskExecutor):
    """Get feedback for ContentEngine improvement using MediationAgent."""

    @property
    def task_type(self) -> str:
        return "content_engine_feedback"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        topic = input_data.get("topic")
        content_type = input_data.get("content_type", "article")

        if not tenant_id or not topic:
            return {
                "success": False,
                "error": "tenant_id and topic are required in workflow input_data",
            }

        agent = MediationAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.get_feedback_for_content_engine(
            tenant_id=tenant_id,
            topic=topic,
            content_type=content_type,
        )

        logger.info(
            "Feedback generated for '%s': %d suggestions, %d patterns to avoid",
            topic,
            len(result.get("suggestions", [])),
            len(result.get("avoid_patterns", [])),
        )

        return {
            "success": True,
            "feedback": result,
            "suggestions": result.get("suggestions", []),
            "avoid_patterns": result.get("avoid_patterns", []),
            "approval_rate": result.get("approval_rate", 0),
        }
