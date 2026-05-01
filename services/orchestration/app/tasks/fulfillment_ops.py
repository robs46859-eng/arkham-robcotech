"""
FulfillmentOps task executors.

Bridges horizontal orchestration to FulfillmentOps agent capabilities:
- Page optimization (CRO)
- A/B test setup
- Analytics tracking
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

from app.agents.fulfillment_ops import FulfillmentOpsAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class PageOptimizationExecutor(TaskExecutor):
    """Optimize page for conversions using FulfillmentOps agent."""

    @property
    def task_type(self) -> str:
        return "page_optimization"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        page_id = input_data.get("page_id")
        page_type = input_data.get("page_type", "landing_page")

        if not tenant_id or not page_id:
            return {
                "success": False,
                "error": "tenant_id and page_id are required in workflow input_data",
            }

        agent = FulfillmentOpsAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.optimize_page(
            tenant_id=tenant_id,
            page_id=page_id,
            page_type=page_type,
        )

        logger.info("Page %s optimized for workflow %s", page_id, workflow_id)
        return {
            "success": True,
            "optimization": result,
            "recommendations_count": len(result.get("recommendations", [])),
            "implemented_count": len(result.get("implemented", [])),
        }


class ABTestSetupExecutor(TaskExecutor):
    """Set up A/B test using FulfillmentOps agent."""

    @property
    def task_type(self) -> str:
        return "ab_test_setup"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        page_id = input_data.get("page_id")
        variant_config = input_data.get("variant_config", {})

        if not tenant_id or not page_id:
            return {
                "success": False,
                "error": "tenant_id and page_id are required in workflow input_data",
            }

        if not variant_config:
            return {
                "success": False,
                "error": "variant_config is required in workflow input_data",
            }

        agent = FulfillmentOpsAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.setup_ab_test(
            tenant_id=tenant_id,
            page_id=page_id,
            variant_config=variant_config,
        )

        logger.info("A/B test setup for page %s in workflow %s", page_id, workflow_id)
        return {
            "success": True,
            "test_setup": result,
            "test_id": result.get("test_id"),
            "variants_count": len(result.get("variants", [])),
            "tracking_enabled": result.get("tracking_enabled", False),
        }


class AnalyticsTrackingExecutor(TaskExecutor):
    """Set up analytics tracking using FulfillmentOps agent."""

    @property
    def task_type(self) -> str:
        return "analytics_tracking"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        event_type = input_data.get("event_type")
        tracking_config = input_data.get("tracking_config", {})

        if not tenant_id or not event_type:
            return {
                "success": False,
                "error": "tenant_id and event_type are required in workflow input_data",
            }

        agent = FulfillmentOpsAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.setup_analytics_tracking(
            tenant_id=tenant_id,
            event_type=event_type,
            tracking_config=tracking_config,
        )

        logger.info("Analytics tracking setup for %s in workflow %s", event_type, workflow_id)
        return {
            "success": True,
            "tracking_setup": result,
            "event_type": result.get("event_type"),
            "verified": result.get("verified", False),
        }
