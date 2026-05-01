"""
Tests for MediaCommerceExecutors

Validates that MediaCommerce executors correctly bridge orchestration
to the MediaCommerce agent.
"""

import asyncio
import sys
from pathlib import Path

import pytest

SERVICE_ROOT = Path(__file__).resolve().parents[1]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from app.tasks.media_commerce import (
    EPCMonitoringExecutor,
    ContentAutoOptimizeExecutor,
    AffiliatePlacementExecutor,
    ContentRepurposeExecutor,
)


class TestEPCMonitoringExecutor:
    """Test EPC monitoring executor"""

    @pytest.fixture
    def executor(self):
        return EPCMonitoringExecutor()

    def test_task_type_is_epc_monitoring(self, executor):
        assert executor.task_type == "epc_monitoring"

    def test_execute_monitors_epc_successfully(self, executor):
        """Test executor monitors EPC correctly"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "vertical": "media",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="calculate_epc",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "monitoring_result" in result
        assert "avg_epc" in result

    def test_execute_rejects_missing_tenant_id(self, executor):
        """Test executor rejects workflow without tenant_id"""
        workflow_state = {
            "input_data": {
                "vertical": "media",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-123",
                step_name="calculate_epc",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "tenant_id" in result["error"]

    def test_execute_monitors_specific_content(self, executor):
        """Test executor monitors EPC for specific content"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "content_id": "content-456",
                "vertical": "media",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-456",
                step_name="calculate_epc",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "monitoring_result" in result


class TestContentAutoOptimizeExecutor:
    """Test content auto-optimization executor"""

    @pytest.fixture
    def executor(self):
        return ContentAutoOptimizeExecutor()

    def test_task_type_is_content_auto_optimize(self, executor):
        assert executor.task_type == "content_auto_optimize"

    def test_execute_optimizes_content_successfully(self, executor):
        """Test executor optimizes content correctly"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "content_id": "content-456",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-789",
                step_name="take_action",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "optimization_result" in result
        assert "content_status" in result

    def test_execute_rejects_missing_tenant_id(self, executor):
        """Test executor rejects workflow without tenant_id"""
        workflow_state = {
            "input_data": {
                "content_id": "content-456",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-789",
                step_name="take_action",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "tenant_id" in result["error"]

    def test_execute_rejects_missing_content_id(self, executor):
        """Test executor rejects workflow without content_id"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {},
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-789",
                step_name="take_action",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "content_id" in result["error"]


class TestAffiliatePlacementExecutor:
    """Test affiliate placement executor"""

    @pytest.fixture
    def executor(self):
        return AffiliatePlacementExecutor()

    def test_task_type_is_affiliate_placement(self, executor):
        assert executor.task_type == "affiliate_placement"

    def test_execute_swaps_placement_successfully(self, executor):
        """Test executor swaps affiliate placement correctly"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "content_id": "content-456",
                "new_placement": {
                    "network": "amazon",
                    "offer_id": "B08XYZ123",
                    "placement_url": "https://example.com/placement",
                },
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-aff-123",
                step_name="swap_placements",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "swap_result" in result
        assert result["swap_result"].get("swapped") is True

    def test_execute_rejects_missing_tenant_id(self, executor):
        """Test executor rejects workflow without tenant_id"""
        workflow_state = {
            "input_data": {
                "content_id": "content-456",
                "new_placement": {},
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-aff-123",
                step_name="swap_placements",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "tenant_id" in result["error"]

    def test_execute_rejects_missing_content_id(self, executor):
        """Test executor rejects workflow without content_id"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "new_placement": {},
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-aff-123",
                step_name="swap_placements",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "content_id" in result["error"]

    def test_execute_rejects_empty_new_placement(self, executor):
        """Test executor rejects workflow without new_placement"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "content_id": "content-456",
                "new_placement": {},
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-aff-123",
                step_name="swap_placements",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "new_placement" in result["error"]


class TestContentRepurposeExecutor:
    """Test content repurposing executor"""

    @pytest.fixture
    def executor(self):
        return ContentRepurposeExecutor()

    def test_task_type_is_content_repurpose(self, executor):
        assert executor.task_type == "content_repurpose"

    def test_execute_repurposes_content_successfully(self, executor):
        """Test executor repurposes content correctly"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "content_id": "content-456",
                "target_formats": ["social", "email", "video"],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-repurpose-123",
                step_name="generate_variations",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "repurpose_result" in result
        assert "formats_created" in result
        assert "total_formats" in result

    def test_execute_rejects_missing_tenant_id(self, executor):
        """Test executor rejects workflow without tenant_id"""
        workflow_state = {
            "input_data": {
                "content_id": "content-456",
                "target_formats": ["social"],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-repurpose-123",
                step_name="generate_variations",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "tenant_id" in result["error"]

    def test_execute_rejects_missing_content_id(self, executor):
        """Test executor rejects workflow without content_id"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "target_formats": ["social"],
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-repurpose-123",
                step_name="generate_variations",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is False
        assert "content_id" in result["error"]

    def test_execute_uses_default_formats(self, executor):
        """Test executor uses default formats when not specified"""
        workflow_state = {
            "tenant_id": "tenant-123",
            "input_data": {
                "content_id": "content-456",
            },
        }

        result = asyncio.run(
            executor.execute(
                workflow_id="wf-test-repurpose-123",
                step_name="generate_variations",
                step_data={},
                workflow_state=workflow_state,
            )
        )

        assert result["success"] is True
        assert "repurpose_result" in result
