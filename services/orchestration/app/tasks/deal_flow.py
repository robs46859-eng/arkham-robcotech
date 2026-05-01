"""
DealFlow lead routing executor.

Bridges horizontal orchestration to the DealFlow agent's lead routing capability.
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

from app.agents.deal_flow import DealFlowAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class LeadRoutingExecutor(TaskExecutor):
    """Route lead to highest-LTV vertical using DealFlow agent."""

    @property
    def task_type(self) -> str:
        return "lead_routing"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        lead_id = input_data.get("lead_id")
        intent_signals = input_data.get("intent_signals", [])

        if not tenant_id or not lead_id:
            return {
                "success": False,
                "error": "tenant_id and lead_id are required in workflow input_data",
            }

        if not intent_signals:
            return {
                "success": False,
                "error": "intent_signals must include at least one non-empty signal",
            }

        agent = DealFlowAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        routing_result = await agent.route_lead(
            tenant_id=tenant_id,
            lead_id=lead_id,
            intent_signals=intent_signals,
        )

        logger.info(
            "Lead %s routed to %s (confidence: %.2f, requires_review: %s)",
            lead_id,
            routing_result["routed_vertical"],
            routing_result["confidence"],
            routing_result["requires_review"],
        )

        return {
            "success": True,
            "routing": routing_result,
            "routed_vertical": routing_result["routed_vertical"],
            "confidence": routing_result["confidence"],
            "requires_review": routing_result["requires_review"],
            "lead_stage": routing_result["lead_stage"],
            "next_action": routing_result["next_action"],
        }
