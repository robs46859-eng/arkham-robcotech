"""
Tests for LeadRoutingExecutor

Validates that the lead routing executor correctly bridges orchestration
to the DealFlow agent.
"""

import asyncio
import sys
from pathlib import Path

import pytest

SERVICE_ROOT = Path(__file__).resolve().parents[1]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from app.tasks.deal_flow import LeadRoutingExecutor


class TestLeadRoutingExecutor:
    """Test lead routing executor"""

    @pytest.fixture
    def executor(self):
        return LeadRoutingExecutor()

    def test_task_type_is_lead_routing(self, executor):
        assert executor.task_type == "lead_routing"

    def test_execute_routes_lead_successfully(self, executor):
        """Test executor routes lead to correct vertical"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "lead_id": "lead-456",
                "intent_signals": [
                    "Need nurse staffing support",
                    "Fill shifts urgently",
                    "Credentialing help",
                ],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="route_lead",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert result["routed_vertical"] == "staffing"
        assert result["confidence"] >= 0.5
        assert "lead_stage" in result
        assert "next_action" in result

    def test_execute_rejects_missing_tenant_id(self, executor):
        """Test executor rejects workflow without tenant_id"""
        workflow_state = {
            "input_data": {
                "lead_id": "lead-456",
                "intent_signals": ["test"],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="route_lead",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "tenant_id" in result["error"]

    def test_execute_rejects_missing_lead_id(self, executor):
        """Test executor rejects workflow without lead_id"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "intent_signals": ["test"],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="route_lead",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "lead_id" in result["error"]

    def test_execute_rejects_empty_intent_signals(self, executor):
        """Test executor rejects workflow without intent_signals"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "lead_id": "lead-456",
                "intent_signals": [],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="route_lead",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "intent_signals" in result["error"]

    def test_execute_routes_ecom_lead(self, executor):
        """Test executor routes e-commerce lead correctly"""
        workflow_state = {
            "tenant_id": "tenant-789",
            "input_data": {
                "lead_id": "lead-ecom-123",
                "intent_signals": [
                    "Shopify checkout optimization",
                    "Abandoned cart recovery",
                    "Product feed cleanup",
                ],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-456",
                step_name="route_lead",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert result["routed_vertical"] == "ecom"
        assert result["confidence"] >= 0.6

    def test_execute_routes_saas_lead(self, executor):
        """Test executor routes SaaS lead correctly"""
        workflow_state = {
            "tenant_id": "tenant-saas",
            "input_data": {
                "lead_id": "lead-saas-123",
                "intent_signals": [
                    "API integration needed",
                    "Workflow automation",
                    "Demo request",
                ],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-saas",
                step_name="route_lead",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert result["routed_vertical"] == "saas"
        assert result["confidence"] >= 0.6

    def test_execute_routes_media_lead(self, executor):
        """Test executor routes media lead correctly"""
        workflow_state = {
            "tenant_id": "tenant-media",
            "input_data": {
                "lead_id": "lead-media-123",
                "intent_signals": [
                    "Affiliate program setup",
                    "EPC tracking needed",
                    "Content monetization",
                ],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-media",
                step_name="route_lead",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert result["routed_vertical"] == "media"
        assert result["confidence"] >= 0.6
