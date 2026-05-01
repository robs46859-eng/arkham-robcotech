"""
BudgetMind task executors.

Bridges horizontal orchestration to BudgetMind agent capabilities:
- Budget monitoring with variance analysis
- Unit economics calculation
- Cash flow projection
- Vendor consolidation
- Scenario planning with digital twin

DIGITAL TWIN INTEGRATION:
- Executors can access hardened digital twin from core
- Twin provides market/operational context for scenarios
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

from app.agents.budget_mind import BudgetMindAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class BudgetMonitoringExecutor(TaskExecutor):
    """Monitor budget vs actual with variance analysis using BudgetMind agent."""

    @property
    def task_type(self) -> str:
        return "budget_monitoring"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        department = input_data.get("department")
        period = input_data.get("period", "month")

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BudgetMindAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.monitor_budget(
            tenant_id=tenant_id,
            department=department,
            period=period,
        )

        logger.info(
            "Budget monitoring for %s: $%.0f budgeted, $%.0f actual (%.1f%% variance)",
            tenant_id,
            result["total_budgeted"],
            result["total_actual"],
            result["variance_pct"],
        )

        return {
            "success": True,
            "budget_result": result,
            "variance_pct": result["variance_pct"],
            "over_budget_count": result["over_budget_count"],
            "recommendations": result["recommendations"],
        }


class UnitEconomicsExecutor(TaskExecutor):
    """Calculate unit economics using top-firm formulas (Sequoia/a16z framework)."""

    @property
    def task_type(self) -> str:
        return "unit_economics"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        vertical = input_data.get("vertical", "saas")
        period_months = input_data.get("period_months", 3)

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BudgetMindAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.calculate_unit_economics(
            tenant_id=tenant_id,
            vertical=vertical,
            period_months=period_months,
        )

        logger.info(
            "Unit economics for %s/%s: LTV:CAC=%.1f, Payback=%.1f months",
            tenant_id,
            vertical,
            result["unit_economics"]["ltv_cac_ratio"],
            result["unit_economics"]["payback_months"],
        )

        return {
            "success": True,
            "unit_economics_result": result,
            "metrics": result["unit_economics"],
            "benchmark_comparison": result["benchmarks"],
            "recommendations": result["recommendations"],
        }


class CashFlowProjectionExecutor(TaskExecutor):
    """Project 13-week cash flow using Y Combinator model."""

    @property
    def task_type(self) -> str:
        return "cash_flow_projection"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        weeks = input_data.get("weeks", 13)
        include_scenarios = input_data.get("include_scenarios", True)

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BudgetMindAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.project_cash_flow(
            tenant_id=tenant_id,
            weeks=weeks,
            include_scenarios=include_scenarios,
        )

        logger.info(
            "Cash flow projection for %s: $%.0f → $%.0f (%d weeks)",
            tenant_id,
            result["starting_cash"],
            result["ending_cash"],
            result["projection_weeks"],
        )

        return {
            "success": True,
            "cash_flow_result": result,
            "starting_cash": result["starting_cash"],
            "ending_cash": result["ending_cash"],
            "cash_alerts": result["cash_alerts"],
            "recommendations": result["recommendations"],
        }


class VendorConsolidationExecutor(TaskExecutor):
    """Identify vendor consolidation opportunities using McKinsey framework."""

    @property
    def task_type(self) -> str:
        return "vendor_consolidation"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        category = input_data.get("category")

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BudgetMindAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.consolidate_vendors(
            tenant_id=tenant_id,
            category=category,
        )

        logger.info(
            "Vendor consolidation for %s: %d opportunities, $%.0f potential savings",
            tenant_id,
            len(result["consolidation_opportunities"]),
            result["total_potential_savings"],
        )

        return {
            "success": True,
            "consolidation_result": result,
            "opportunities_count": len(result["consolidation_opportunities"]),
            "potential_savings": result["total_potential_savings"],
            "prioritized_opportunities": result["consolidation_opportunities"],
            "recommendations": result["recommendations"],
        }


class ScenarioPlanningExecutor(TaskExecutor):
    """
    Run financial scenario planning using digital twin.

    DIGITAL TWIN INTEGRATION:
    - Uses hardened digital twin from core for scenario modeling
    - Twin provides market conditions, competitor actions, operational constraints
    """

    @property
    def task_type(self) -> str:
        return "scenario_planning"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        scenario_name = input_data.get("scenario_name", "base")
        assumptions = input_data.get("assumptions", {})
        time_horizon_months = input_data.get("time_horizon_months", 12)

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = BudgetMindAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.run_scenario(
            scenario_name=scenario_name,
            assumptions=assumptions,
            time_horizon_months=time_horizon_months,
        )

        logger.info(
            "Scenario '%s' for %s: Revenue $%.0f, EBITDA $%.0f, Cash $%.0f",
            scenario_name,
            tenant_id,
            result.revenue,
            result.ebitda,
            result.cash_end,
        )

        return {
            "success": True,
            "scenario_result": {
                "scenario_name": result.scenario_name,
                "revenue": result.revenue,
                "expenses": result.expenses,
                "ebitda": result.ebitda,
                "cash_end": result.cash_end,
                "key_assumptions": result.key_assumptions,
                "risks": result.risks,
                "recommendations": result.recommendations,
            },
        }


class FinancialPolicyEnforcementExecutor(TaskExecutor):
    """
    Enforce financial policies with compounded memory context.

    Policies include:
    - Spend cap enforcement
    - Approval thresholds
    - Cash flow alerts
    - Unit economics guardrails
    """

    @property
    def task_type(self) -> str:
        return "financial_policy_enforcement"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        policy_name = input_data.get("policy_name")
        entity_data = input_data.get("entity_data", {})

        if not tenant_id or not policy_name:
            return {
                "success": False,
                "error": "tenant_id and policy_name are required",
            }

        agent = BudgetMindAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))

        # Get compounded memory context
        memory_context = agent._get_compounded_memory_insights()

        # Check policy based on type
        violations = []
        actions = []

        if "spend_cap" in policy_name.lower():
            violations = self._check_spend_cap(entity_data, memory_context)
        elif "cash_flow" in policy_name.lower():
            violations = self._check_cash_flow_policy(entity_data)
        elif "unit_economics" in policy_name.lower():
            violations = self._check_unit_economics_policy(entity_data)

        # Determine actions
        for violation in violations:
            if violation["severity"] == "critical":
                actions.append({"type": "block", "reason": violation["description"]})
            elif violation["severity"] == "high":
                actions.append({"type": "require_approval", "reason": violation["description"]})
            else:
                actions.append({"type": "warn", "reason": violation["description"]})

        result = {
            "tenant_id": tenant_id,
            "policy": policy_name,
            "violations": violations,
            "actions": actions,
            "compliant": len(violations) == 0,
            "compounded_memory_context": memory_context,
        }

        logger.info(
            "Financial policy enforcement for %s/%s: %s",
            tenant_id,
            policy_name,
            "COMPLIANT" if result["compliant"] else f"NON-COMPLIANT ({len(violations)} violations)",
        )

        return {
            "success": True,
            "enforcement_result": result,
            "compliant": result["compliant"],
            "violations": violations,
            "actions": actions,
        }

    def _check_spend_cap(
        self,
        entity_data: Dict,
        memory_context: Dict,
    ) -> List[Dict]:
        """Check spend cap policy"""
        violations = []

        requested = entity_data.get("requested_amount", 0)
        cap = entity_data.get("spend_cap", 0)
        category = entity_data.get("category", "general")

        if requested > cap:
            over_pct = ((requested - cap) / max(1, cap)) * 100
            severity = "critical" if over_pct > 25 else ("high" if over_pct > 10 else "medium")
            violations.append({
                "type": "spend_cap_exceeded",
                "category": category,
                "requested": requested,
                "cap": cap,
                "over_pct": over_pct,
                "severity": severity,
                "description": f"Spend request exceeds cap by {over_pct:.0f}%",
            })

        # Check historical patterns from compounded memory
        rejection_patterns = memory_context.get("rejected_categories", {})
        if category in rejection_patterns and rejection_patterns[category] > 2:
            violations.append({
                "type": "repeat_violation",
                "category": category,
                "severity": "high",
                "description": f"Category '{category}' has {rejection_patterns[category]} prior rejections",
            })

        return violations

    def _check_cash_flow_policy(self, entity_data: Dict) -> List[Dict]:
        """Check cash flow policy"""
        violations = []

        runway_days = entity_data.get("runway_days", 0)
        min_runway = entity_data.get("min_runway_days", 90)

        if runway_days < min_runway:
            severity = "critical" if runway_days < 30 else "high"
            violations.append({
                "type": "insufficient_runway",
                "runway_days": runway_days,
                "min_required": min_runway,
                "severity": severity,
                "description": f"Cash runway ({runway_days} days) below minimum ({min_runway} days)",
            })

        return violations

    def _check_unit_economics_policy(self, entity_data: Dict) -> List[Dict]:
        """Check unit economics policy"""
        violations = []

        ltv_cac = entity_data.get("ltv_cac_ratio", 0)
        min_ltv_cac = entity_data.get("min_ltv_cac", 3.0)

        if ltv_cac < min_ltv_cac:
            severity = "high" if ltv_cac < 2 else "medium"
            violations.append({
                "type": "poor_unit_economics",
                "ltv_cac_ratio": ltv_cac,
                "min_required": min_ltv_cac,
                "severity": severity,
                "description": f"LTV:CAC ratio ({ltv_cac:.1f}:1) below minimum ({min_ltv_cac}:1)",
            })

        return violations
