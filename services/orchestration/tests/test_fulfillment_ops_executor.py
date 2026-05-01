"""
Tests for FulfillmentOpsExecutors

Validates that FulfillmentOps executors correctly bridge orchestration
to the FulfillmentOps agent.
"""

import asyncio
import sys
from pathlib import Path

import pytest

SERVICE_ROOT = Path(__file__).resolve().parents[1]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from app.tasks.fulfillment_ops import (
    PageOptimizationExecutor,
    ABTestSetupExecutor,
    AnalyticsTrackingExecutor,
)


class TestPageOptimizationExecutor:
    """Test page optimization executor"""

    @pytest.fixture
    def executor(self):
        return PageOptimizationExecutor()

    def test_task_type_is_page_optimization(self, executor):
        assert executor.task_type == "page_optimization"

    def test_execute_optimizes_page_successfully(self, executor):
        """Test executor optimizes page correctly"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "page_id": "page-456",
                "page_type": "landing_page",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="analyze_page",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "optimization" in result
        assert "recommendations_count" in result

    def test_execute_rejects_missing_tenant_id(self, executor):
        """Test executor rejects workflow without tenant_id"""
        workflow_state = {
            "input_data": {
                "page_id": "page-456",
                "page_type": "landing_page",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="analyze_page",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "tenant_id" in result["error"]

    def test_execute_rejects_missing_page_id(self, executor):
        """Test executor rejects workflow without page_id"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "page_type": "landing_page",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="analyze_page",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "page_id" in result["error"]


class TestABTestSetupExecutor:
    """Test A/B test setup executor"""

    @pytest.fixture
    def executor(self):
        return ABTestSetupExecutor()

    def test_task_type_is_ab_test_setup(self, executor):
        assert executor.task_type == "ab_test_setup"

    def test_execute_sets_up_ab_test_successfully(self, executor):
        """Test executor sets up A/B test correctly"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "page_id": "page-456",
                "variant_config": {
                    "variant_a": {"headline": "Original"},
                    "variant_b": {"headline": "New Headline"},
                },
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-456",
                step_name="setup_test",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "test_setup" in result
        assert "variants_count" in result

    def test_execute_rejects_missing_tenant_id(self, executor):
        """Test executor rejects workflow without tenant_id"""
        workflow_state = {
            "input_data": {
                "page_id": "page-456",
                "variant_config": {},
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-456",
                step_name="setup_test",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "tenant_id" in result["error"]

    def test_execute_rejects_missing_page_id(self, executor):
        """Test executor rejects workflow without page_id"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "variant_config": {},
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-456",
                step_name="setup_test",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "page_id" in result["error"]

    def test_execute_rejects_empty_variant_config(self, executor):
        """Test executor rejects workflow without variant_config"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "page_id": "page-456",
                "variant_config": {},
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-456",
                step_name="setup_test",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "variant_config" in result["error"]


class TestAnalyticsTrackingExecutor:
    """Test analytics tracking executor"""

    @pytest.fixture
    def executor(self):
        return AnalyticsTrackingExecutor()

    def test_task_type_is_analytics_tracking(self, executor):
        assert executor.task_type == "analytics_tracking"

    def test_execute_sets_up_tracking_successfully(self, executor):
        """Test executor sets up analytics tracking correctly"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "event_type": "signup_completed",
                "tracking_config": {
                    "properties": ["user_id", "timestamp", "source"],
                },
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-789",
                step_name="define_event_schema",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "tracking_setup" in result
        assert "verified" in result

    def test_execute_rejects_missing_tenant_id(self, executor):
        """Test executor rejects workflow without tenant_id"""
        workflow_state = {
            "input_data": {
                "event_type": "signup_completed",
                "tracking_config": {},
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-789",
                step_name="define_event_schema",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "tenant_id" in result["error"]

    def test_execute_rejects_missing_event_type(self, executor):
        """Test executor rejects workflow without event_type"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "tracking_config": {},
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-789",
                step_name="define_event_schema",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "event_type" in result["error"]
