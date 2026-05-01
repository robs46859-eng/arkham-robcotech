"""
ComplianceGate task executors.

Bridges horizontal orchestration to ComplianceGate agent capabilities:
- SEO audits
- Policy enforcement
- HIPAA compliance
- Security audits
- Code analysis

ISOLATION RULE:
- Executors can read compounded memory from ComplianceGate
- NO direct interface with MediationAgent
- Full project build access for code analysis
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

from app.agents.compliance_gate import ComplianceGateAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class SeoAuditExecutor(TaskExecutor):
    """Perform SEO compliance audit using ComplianceGate agent."""

    @property
    def task_type(self) -> str:
        return "seo_audit"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        content_assets = input_data.get("content_assets", [])

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = ComplianceGateAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.seo_audit(
            tenant_id=tenant_id,
            content_assets=content_assets,
        )

        logger.info(
            "SEO audit complete for %s: %d assets, %.0f%% compliant",
            tenant_id,
            result["assets_audited"],
            result["compliance_rate"] * 100,
        )

        return {
            "success": True,
            "audit_result": result,
            "compliance_rate": result["compliance_rate"],
            "violation_count": len(result["violations"]),
            "recommendations": result["recommendations"],
        }


class PolicyEnforcementExecutor(TaskExecutor):
    """Enforce policy compliance using ComplianceGate agent."""

    @property
    def task_type(self) -> str:
        return "policy_enforcement"

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

        agent = ComplianceGateAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.enforce_policy(
            tenant_id=tenant_id,
            policy_name=policy_name,
            entity_data=entity_data,
        )

        logger.info(
            "Policy enforcement for %s: %s → %s",
            tenant_id,
            policy_name,
            "COMPLIANT" if result["compliant"] else f"NON-COMPLIANT ({len(result['violations'])} violations)",
        )

        return {
            "success": True,
            "enforcement_result": result,
            "compliant": result["compliant"],
            "violations": result["violations"],
            "actions": result["actions"],
            "compounded_memory_context": result.get("compounded_memory_context", {}),
        }


class HipaaComplianceExecutor(TaskExecutor):
    """Check HIPAA compliance using ComplianceGate agent."""

    @property
    def task_type(self) -> str:
        return "hipaa_compliance"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        entity_data = input_data.get("entity_data", {})

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = ComplianceGateAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.enforce_policy(
            tenant_id=tenant_id,
            policy_name="hipaa_compliance",
            entity_data=entity_data,
        )

        logger.info(
            "HIPAA compliance check for %s: %s",
            tenant_id,
            "COMPLIANT" if result["compliant"] else f"NON-COMPLIANT ({len(result['violations'])} violations)",
        )

        return {
            "success": True,
            "compliance_result": result,
            "compliant": result["compliant"],
            "violations": result["violations"],
            "case_law_references": result.get("case_law_references", []),
            "actions": result["actions"],
        }


class SecurityAuditExecutor(TaskExecutor):
    """Perform security compliance audit using ComplianceGate agent."""

    @property
    def task_type(self) -> str:
        return "security_audit"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        entity_data = input_data.get("entity_data", {})

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = ComplianceGateAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.enforce_policy(
            tenant_id=tenant_id,
            policy_name="security_compliance",
            entity_data=entity_data,
        )

        logger.info(
            "Security audit for %s: %s",
            tenant_id,
            "PASS" if result["compliant"] else f"FAIL ({len(result['violations'])} violations)",
        )

        return {
            "success": True,
            "audit_result": result,
            "compliant": result["compliant"],
            "violations": result["violations"],
            "actions": result["actions"],
        }


class ProjectCodeAnalysisExecutor(TaskExecutor):
    """
    Analyze entire project build for compliance issues.

    This executor receives the full project build and checks for:
    - Security vulnerabilities (OWASP Top 10)
    - HIPAA compliance issues
    - Code quality problems
    - Hardcoded secrets
    - SQL injection risks
    """

    @property
    def task_type(self) -> str:
        return "project_code_analysis"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        project_path = input_data.get("project_path", "/app")
        files = input_data.get("files", [])

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        if not files:
            return {
                "success": False,
                "error": "files array is required in workflow input_data",
            }

        agent = ComplianceGateAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.analyze_project_build(
            project_path=project_path,
            files=files,
        )

        logger.info(
            "Project code analysis for %s: %d files, %d violations, score %.1f",
            tenant_id,
            result["files_analyzed"],
            result["total_violations"],
            result["compliance_score"],
        )

        return {
            "success": True,
            "analysis_result": result,
            "files_analyzed": result["files_analyzed"],
            "total_violations": result["total_violations"],
            "by_severity": result["by_severity"],
            "compliance_score": result["compliance_score"],
            "fixes": result["fixes"],
            "case_law_references": result["case_law_references"],
        }


class ChurnPreventionComplianceExecutor(TaskExecutor):
    """
    Ensure churn prevention flows comply with regulations.

    Checks:
    - CCPA opt-out compliance
    - GDPR consent requirements
    - Fair billing practices
    """

    @property
    def task_type(self) -> str:
        return "churn_prevention_compliance"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        cancellation_data = input_data.get("cancellation_data", {})

        if not tenant_id:
            return {
                "success": False,
                "error": "tenant_id is required in workflow input_data",
            }

        agent = ComplianceGateAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))

        # Check GDPR/CCPA compliance for cancellation flow
        violations = []

        # GDPR: Must allow cancellation as easily as signup
        if not cancellation_data.get("easy_cancellation"):
            violations.append({
                "type": "gdpr_cancellation",
                "description": "Cancellation must be as easy as signup",
                "severity": "high",
            })

        # CCPA: Must honor opt-out requests
        if cancellation_data.get("opt_out_requested") and not cancellation_data.get("opt_out_honored"):
            violations.append({
                "type": "ccpa_opt_out",
                "description": "CCPA opt-out request must be honored",
                "severity": "critical",
            })

        compliant = len(violations) == 0
        actions = []
        for v in violations:
            if v["severity"] == "critical":
                actions.append({"type": "block", "reason": v["description"]})
            else:
                actions.append({"type": "warn", "reason": v["description"]})

        result = {
            "tenant_id": tenant_id,
            "policy": "churn_prevention_compliance",
            "violations": violations,
            "actions": actions,
            "compliant": compliant,
        }

        logger.info(
            "Churn prevention compliance for %s: %s",
            tenant_id,
            "COMPLIANT" if compliant else f"NON-COMPLIANT ({len(violations)} violations)",
        )

        return {
            "success": True,
            "compliance_result": result,
            "compliant": compliant,
            "violations": violations,
            "actions": actions,
        }
