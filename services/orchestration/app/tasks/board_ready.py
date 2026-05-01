"""
BoardReady task executors.

Bridges horizontal orchestration to BoardReady agent capabilities:
- Board deck generation
- Investor update generation
- Data room maintenance
- Due diligence response
- Exit preparation
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

from app.agents.board_ready import BoardReadyAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class BoardDeckGenerationExecutor(TaskExecutor):
    """Generate quarterly board deck using BoardReady agent."""

    @property
    def task_type(self) -> str:
        return "board_deck_generation"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        quarter = input_data.get("quarter", "Q1")
        year = input_data.get("year", 2025)

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BoardReadyAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.generate_board_deck(
            tenant_id=tenant_id,
            quarter=quarter,
            year=year,
        )

        logger.info(
            "Board deck generated for %s - %s: %d sections, %.0f%% complete",
            tenant_id,
            result["period"],
            len(result["sections"]),
            result["completeness_score"] * 100,
        )

        return {
            "success": True,
            "deck_result": result,
            "sections_count": len(result["sections"]),
            "completeness_score": result["completeness_score"],
            "data_sources": result["data_sources"],
        }


class InvestorUpdateExecutor(TaskExecutor):
    """Generate investor update using BoardReady agent."""

    @property
    def task_type(self) -> str:
        return "investor_update"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        month = input_data.get("month", "April")
        year = input_data.get("year", 2025)

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BoardReadyAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.generate_investor_update(
            tenant_id=tenant_id,
            month=month,
            year=year,
        )

        logger.info(
            "Investor update generated for %s - %s: %d highlights, %d asks",
            tenant_id,
            result["period"],
            len(result["highlights"]),
            len(result["asks"]),
        )

        return {
            "success": True,
            "update_result": result,
            "highlights": result["highlights"],
            "metrics": result["metrics"],
            "challenges": result["challenges"],
            "asks": result["asks"],
        }


class DataRoomMaintenanceExecutor(TaskExecutor):
    """Maintain living data room using BoardReady agent."""

    @property
    def task_type(self) -> str:
        return "data_room_maintenance"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BoardReadyAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.maintain_data_room(tenant_id=tenant_id)

        logger.info(
            "Data room maintained for %s: %.0f%% complete, %d stale, %d missing",
            tenant_id,
            result["completeness_score"],
            result["stale_documents"],
            result["missing_documents"],
        )

        return {
            "success": True,
            "data_room_result": result,
            "completeness_score": result["completeness_score"],
            "total_documents": result["total_documents"],
            "stale_count": result["stale_documents"],
            "missing_count": result["missing_documents"],
            "recommendations": result["recommendations"],
        }


class DueDiligenceResponseExecutor(TaskExecutor):
    """Respond to due diligence request using BoardReady agent."""

    @property
    def task_type(self) -> str:
        return "due_diligence_response"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        request_category = input_data.get("category", "financial")
        request_details = input_data.get("details", {})

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BoardReadyAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.respond_to_due_diligence(
            tenant_id=tenant_id,
            request_category=request_category,
            request_details=request_details,
        )

        logger.info(
            "Due diligence response for %s - %s: %d documents",
            tenant_id,
            request_category,
            len(result["documents_provided"]),
        )

        return {
            "success": True,
            "response_result": result,
            "documents_count": len(result["documents_provided"]),
            "documents": result["documents_provided"],
            "additional_context": result["additional_context"],
        }


class ExitPreparationExecutor(TaskExecutor):
    """Prepare exit materials (CIM, valuation) using BoardReady agent."""

    @property
    def task_type(self) -> str:
        return "exit_preparation"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        exit_type = input_data.get("exit_type", "acquisition")

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BoardReadyAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.prepare_exit_materials(
            tenant_id=tenant_id,
            exit_type=exit_type,
        )

        logger.info(
            "Exit materials prepared for %s - %s: valuation $%.1fM",
            tenant_id,
            exit_type,
            result["valuation_estimate"]["recommended"] / 1000000,
        )

        return {
            "success": True,
            "exit_result": result,
            "valuation": result["valuation_estimate"],
            "cim_sections": result["cim_sections"],
            "data_room_readiness": result["data_room_readiness"]["completeness_score"],
            "recommendations": result["recommendations"],
        }
