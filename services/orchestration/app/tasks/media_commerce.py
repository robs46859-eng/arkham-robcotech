"""
MediaCommerce task executors.

Bridges horizontal orchestration to MediaCommerce agent capabilities:
- EPC monitoring and classification
- Content auto-optimization (retire losers, scale winners)
- Affiliate placement optimization
- Content repurposing
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

from app.agents.media_commerce import MediaCommerceAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class EPCMonitoringExecutor(TaskExecutor):
    """Monitor Earnings Per Click for content assets using MediaCommerce agent."""

    @property
    def task_type(self) -> str:
        return "epc_monitoring"

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
        vertical = input_data.get("vertical")

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = MediaCommerceAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.monitor_epc(
            tenant_id=tenant_id,
            content_id=content_id,
            vertical=vertical,
        )

        logger.info("EPC monitoring complete for %s assets in workflow %s", result.get("assets_monitored", 0), workflow_id)
        return {
            "success": True,
            "monitoring_result": result,
            "avg_epc": result.get("avg_epc", 0),
            "winners_count": len(result.get("winners", [])),
            "underperformers_count": len(result.get("underperformers", [])),
            "actions_taken": result.get("actions_taken", []),
        }


class ContentAutoOptimizeExecutor(TaskExecutor):
    """Auto-optimize content based on EPC performance using MediaCommerce agent."""

    @property
    def task_type(self) -> str:
        return "content_auto_optimize"

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

        if not tenant_id or not content_id:
            return {
                "success": False,
                "error": "tenant_id and content_id are required in workflow input_data",
            }

        agent = MediaCommerceAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.auto_optimize_content(
            tenant_id=tenant_id,
            content_id=content_id,
        )

        logger.info("Content auto-optimization complete for %s in workflow %s", content_id, workflow_id)
        return {
            "success": True,
            "optimization_result": result,
            "current_epc": result.get("current_epc", 0),
            "actions_taken": result.get("actions_taken", []),
            "content_status": result.get("content_status", "unchanged"),
        }


class AffiliatePlacementExecutor(TaskExecutor):
    """Optimize affiliate placements based on performance using MediaCommerce agent."""

    @property
    def task_type(self) -> str:
        return "affiliate_placement"

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
        new_placement = input_data.get("new_placement", {})

        if not tenant_id or not content_id:
            return {
                "success": False,
                "error": "tenant_id and content_id are required in workflow input_data",
            }

        if not new_placement:
            return {
                "success": False,
                "error": "new_placement is required in workflow input_data",
            }

        agent = MediaCommerceAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.swap_affiliate_placement(
            tenant_id=tenant_id,
            content_id=content_id,
            new_placement=new_placement,
        )

        logger.info("Affiliate placement swapped for %s in workflow %s", content_id, workflow_id)
        return {
            "success": True,
            "swap_result": result,
            "swapped": result.get("swapped", False),
            "new_placement": result.get("new_placement", {}),
        }


class ContentRepurposeExecutor(TaskExecutor):
    """Repurpose top-performing content across formats using MediaCommerce agent."""

    @property
    def task_type(self) -> str:
        return "content_repurpose"

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
        target_formats = input_data.get("target_formats", ["social", "email"])

        if not tenant_id or not content_id:
            return {
                "success": False,
                "error": "tenant_id and content_id are required in workflow input_data",
            }

        agent = MediaCommerceAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.repurpose_content(
            tenant_id=tenant_id,
            content_id=content_id,
            target_formats=target_formats,
        )

        logger.info("Content repurposed: %s → %s in workflow %s", content_id, target_formats, workflow_id)
        return {
            "success": True,
            "repurpose_result": result,
            "source_id": content_id,
            "formats_created": result.get("formats", []),
            "total_formats": len(result.get("formats", [])),
        }
