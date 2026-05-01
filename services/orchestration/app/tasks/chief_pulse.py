"""
ChiefPulse task executors.

Bridges horizontal orchestration to ChiefPulse agent capabilities:
- Signal aggregation across all agents
- Anomaly detection and alerting
- Executive briefing generation
- Approval queue management
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

from app.agents.chief_pulse import ChiefPulseAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class SignalAggregationExecutor(TaskExecutor):
    """Aggregate signals across all agents using ChiefPulse agent."""

    @property
    def task_type(self) -> str:
        return "signal_aggregation"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        time_window = input_data.get("time_window", "24h")
        agents = input_data.get("agents", ["dealflow", "contentengine", "mediacommerce", "fulfillmentops"])

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = ChiefPulseAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.aggregate_signals(
            tenant_id=tenant_id,
            time_window=time_window,
            agents=agents,
        )

        logger.info(
            "Signal aggregation complete for %s: %d signals from %d agents",
            tenant_id,
            result.get("total_signals", 0),
            len(result.get("by_agent", {})),
        )
        return {
            "success": True,
            "aggregation_result": result,
            "total_signals": result.get("total_signals", 0),
            "by_agent": result.get("by_agent", {}),
            "by_vertical": result.get("by_vertical", {}),
            "anomalies_detected": result.get("anomalies", []),
        }


class AnomalyDetectionExecutor(TaskExecutor):
    """Detect anomalies in tenant performance using ChiefPulse agent."""

    @property
    def task_type(self) -> str:
        return "anomaly_detection"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        metrics = input_data.get("metrics", ["revenue", "conversion_rate", "epc", "lead_volume"])
        sensitivity = input_data.get("sensitivity", "medium")  # low, medium, high

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = ChiefPulseAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.detect_anomalies(
            tenant_id=tenant_id,
            metrics=metrics,
            sensitivity=sensitivity,
        )

        logger.info(
            "Anomaly detection complete for %s: %d anomalies found",
            tenant_id,
            len(result.get("anomalies", [])),
        )
        return {
            "success": True,
            "anomaly_result": result,
            "anomalies": result.get("anomalies", []),
            "anomaly_count": len(result.get("anomalies", [])),
            "severity_breakdown": result.get("severity_breakdown", {}),
            "recommended_actions": result.get("recommended_actions", []),
        }


class ExecutiveBriefingExecutor(TaskExecutor):
    """Generate executive briefing using ChiefPulse agent."""

    @property
    def task_type(self) -> str:
        return "executive_briefing"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        executive_id = input_data.get("executive_id")
        briefing_type = input_data.get("briefing_type", "daily")  # daily, weekly, board

        if not tenant_id or not executive_id:
            return {
                "success": False,
                "error": "tenant_id and executive_id are required in workflow input_data",
            }

        agent = ChiefPulseAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.generate_daily_briefing(
            tenant_id=tenant_id,
            executive_id=executive_id,
            briefing_type=briefing_type,
        )

        logger.info(
            "Executive briefing generated for %s (%s)",
            executive_id,
            briefing_type,
        )
        return {
            "success": True,
            "briefing": result,
            "briefing_id": result.get("briefing_id"),
            "briefing_type": briefing_type,
            "sections": list(result.get("sections", {}).keys()),
            "decisions_required": len(result.get("decisions_required", [])),
            "anomalies_highlighted": len(result.get("anomalies", [])),
        }


class ApprovalQueueExecutor(TaskExecutor):
    """Manage approval queue using ChiefPulse agent."""

    @property
    def task_type(self) -> str:
        return "approval_queue"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        executive_id = input_data.get("executive_id")
        status_filter = input_data.get("status_filter", "pending")  # pending, approved, rejected

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = ChiefPulseAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.get_approval_queue(
            tenant_id=tenant_id,
            executive_id=executive_id,
            status_filter=status_filter,
        )

        logger.info(
            "Approval queue retrieved for %s: %d pending items",
            executive_id or tenant_id,
            len(result.get("pending_items", [])),
        )
        return {
            "success": True,
            "queue_result": result,
            "pending_count": len(result.get("pending_items", [])),
            "overdue_count": len(result.get("overdue_items", [])),
            "pending_items": result.get("pending_items", []),
            "priority_breakdown": result.get("priority_breakdown", {}),
        }
