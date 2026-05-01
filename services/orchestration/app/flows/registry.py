"""
Flow Registry

Defines and manages workflow types available in the system.
Each flow is a sequence of steps with defined task types.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)


@dataclass
class FlowStep:
    """A single step in a workflow"""
    name: str
    task_type: str
    config: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 300
    retries: int = 3


@dataclass
class FlowDefinition:
    """Definition of a workflow type"""
    flow_type: str
    description: str
    steps: List[FlowStep]
    version: str = "1.0.0"


class FlowRegistry:
    """Registry of available workflow types"""
    
    def __init__(self):
        self._flows: Dict[str, FlowDefinition] = {}
    
    def register(self, flow_def: FlowDefinition):
        """Register a flow definition"""
        self._flows[flow_def.flow_type] = flow_def
        logger.info(f"Registered flow: {flow_def.flow_type}")
    
    def has_flow(self, flow_type: str) -> bool:
        """Check if a flow type exists"""
        return flow_type in self._flows
    
    def get_flow(self, flow_type: str) -> FlowDefinition:
        """Get a flow definition"""
        if flow_type not in self._flows:
            raise ValueError(f"Unknown flow type: {flow_type}")
        return self._flows[flow_type]
    
    def list_flows(self) -> List[Dict[str, str]]:
        """List all registered flows"""
        return [
            {
                "flow_type": flow.flow_type,
                "description": flow.description,
                "steps_count": len(flow.steps),
            }
            for flow in self._flows.values()
        ]
    
    async def register_built_in_flows(self):
        """Register built-in workflow types"""
        
        # BIM Project Analysis Flow
        self.register(FlowDefinition(
            flow_type="bim_project_analysis",
            description="Analyze BIM project and generate status report",
            steps=[
                FlowStep(
                    name="retrieve_project_data",
                    task_type="bim_retrieval",
                    config={"source": "bim_store"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="retrieve_memory_context",
                    task_type="memory_retrieval",
                    config={"scope": "project"},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="run_cheap_classification",
                    task_type="model_inference",
                    config={
                        "model_tier": "cheap",
                        "task": "classification",
                    },
                    timeout=60,
                    retries=3,
                ),
                FlowStep(
                    name="detect_issues",
                    task_type="bim_issue_detection",
                    config={},
                    timeout=120,
                    retries=2,
                ),
                FlowStep(
                    name="evaluate_confidence",
                    task_type="policy_evaluation",
                    config={
                        "confidence_threshold": 0.8,
                        "escalation_policy": "mid_cost",
                    },
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="generate_report",
                    task_type="model_inference",
                    config={
                        "model_tier": "mid_cost",
                        "task": "report_generation",
                        "output_schema": "project_status_report",
                    },
                    timeout=120,
                    retries=3,
                ),
                FlowStep(
                    name="validate_output",
                    task_type="schema_validation",
                    config={"schema": "project_status_report"},
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="write_memory_note",
                    task_type="memory_creation",
                    config={"note_type": "workflow"},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="commit_artifact",
                    task_type="artifact_storage",
                    config={"storage": "object_store"},
                    timeout=60,
                    retries=3,
                ),
            ],
        ))
        
        # IFC Ingestion Flow
        self.register(FlowDefinition(
            flow_type="ifc_ingestion",
            description="Ingest and parse IFC file",
            steps=[
                FlowStep(
                    name="validate_file",
                    task_type="file_validation",
                    config={"allowed_types": [".ifc"]},
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="parse_ifc",
                    task_type="ifc_parsing",
                    config={},
                    timeout=600,
                    retries=2,
                ),
                FlowStep(
                    name="normalize_elements",
                    task_type="data_normalization",
                    config={},
                    timeout=120,
                    retries=2,
                ),
                FlowStep(
                    name="store_elements",
                    task_type="database_insert",
                    config={"table": "bim_elements"},
                    timeout=60,
                    retries=3,
                ),
                FlowStep(
                    name="create_embeddings",
                    task_type="embedding_generation",
                    config={"fields": ["name", "description"]},
                    timeout=120,
                    retries=2,
                ),
            ],
        ))
        
        # Inference Request Flow (gateway-triggered)
        self.register(FlowDefinition(
            flow_type="inference_request",
            description="Route and execute inference request",
            steps=[
                FlowStep(
                    name="check_semantic_cache",
                    task_type="cache_lookup",
                    config={"threshold": 0.95},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="classify_request",
                    task_type="model_inference",
                    config={
                        "model_tier": "cheap",
                        "task": "request_classification",
                    },
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="select_model",
                    task_type="policy_evaluation",
                    config={"policy": "cost_ladder"},
                    timeout=10,
                    retries=1,
                ),
                FlowStep(
                    name="execute_inference",
                    task_type="model_inference",
                    config={},
                    timeout=120,
                    retries=3,
                ),
                FlowStep(
                    name="validate_response",
                    task_type="schema_validation",
                    config={},
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="record_usage",
                    task_type="billing_record",
                    config={},
                    timeout=30,
                    retries=3,
                ),
            ],
        ))

        # Media-Commerce Content Strategy Flow
        self.register(FlowDefinition(
            flow_type="media_content_strategy",
            description="Run horizontal orchestration for a media-commerce content strategy request",
            steps=[
                FlowStep(
                    name="retrieve_memory_context",
                    task_type="memory_retrieval",
                    config={"scope": "tenant_marketing_context"},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="generate_strategy",
                    task_type="content_strategy_generation",
                    config={},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="validate_strategy",
                    task_type="schema_validation",
                    config={"schema": "content_strategy"},
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="store_strategy_artifact",
                    task_type="artifact_storage",
                    config={"storage": "database"},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # DealFlow Lead Routing Flow
        self.register(FlowDefinition(
            flow_type="dealflow_lead_routing",
            description="Route lead to highest-LTV vertical using DealFlow agent",
            steps=[
                FlowStep(
                    name="route_lead",
                    task_type="lead_routing",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="create_routing_task",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "task"},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="log_routing_event",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "event"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # SaaS Pipeline Routing Flow
        self.register(FlowDefinition(
            flow_type="saas_pipeline_routing",
            description="Qualify SaaS demand, route by fit, and create follow-up work",
            steps=[
                FlowStep(
                    name="score_pipeline_intent",
                    task_type="lead_routing",
                    config={"vertical": "saas", "mode": "pipeline"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="evaluate_deal_fit",
                    task_type="policy_evaluation",
                    config={"policy": "saas_pipeline_fit"},
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="create_follow_up_artifact",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "task"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # FulfillmentOps Page CRO Flow
        self.register(FlowDefinition(
            flow_type="page_cro_optimization",
            description="Optimize page for conversions using FulfillmentOps agent",
            steps=[
                FlowStep(
                    name="analyze_page",
                    task_type="page_optimization",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="generate_variant",
                    task_type="model_inference",
                    config={
                        "model_tier": "mid",
                        "task": "cro_copy_generation",
                    },
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="implement_variant",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "content_asset"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # SaaS Signup Conversion Flow
        self.register(FlowDefinition(
            flow_type="saas_signup_conversion",
            description="Analyze signup flow friction and queue SaaS conversion improvements",
            steps=[
                FlowStep(
                    name="review_signup_events",
                    task_type="analytics_tracking",
                    config={"vertical": "saas", "funnel": "signup"},
                    timeout=45,
                    retries=2,
                ),
                FlowStep(
                    name="generate_conversion_actions",
                    task_type="model_inference",
                    config={
                        "model_tier": "mid",
                        "task": "cro_copy_generation",
                        "vertical": "saas",
                    },
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="queue_conversion_work",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "task"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # FulfillmentOps A/B Test Flow
        self.register(FlowDefinition(
            flow_type="ab_test_lifecycle",
            description="Set up and manage A/B test using FulfillmentOps agent",
            steps=[
                FlowStep(
                    name="setup_test",
                    task_type="ab_test_setup",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="setup_tracking",
                    task_type="analytics_tracking",
                    config={},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="monitor_performance",
                    task_type="model_inference",
                    config={
                        "model_tier": "cheap",
                        "task": "ab_test_analysis",
                    },
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="decide_winner",
                    task_type="policy_evaluation",
                    config={
                        "significance_threshold": 0.95,
                        "min_conversions": 100,
                    },
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="deploy_winner",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "content_asset"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # FulfillmentOps Analytics Tracking Flow
        self.register(FlowDefinition(
            flow_type="analytics_tracking_setup",
            description="Set up analytics event tracking using FulfillmentOps agent",
            steps=[
                FlowStep(
                    name="define_event_schema",
                    task_type="analytics_tracking",
                    config={},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="generate_tracking_code",
                    task_type="model_inference",
                    config={
                        "model_tier": "cheap",
                        "task": "tracking_code_generation",
                    },
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="verify_events",
                    task_type="schema_validation",
                    config={"schema": "analytics_event"},
                    timeout=30,
                    retries=1,
                ),
            ],
        ))

        # SaaS Retention Watch Flow
        self.register(FlowDefinition(
            flow_type="saas_retention_watch",
            description="Track SaaS lifecycle risk and prepare retention escalation artifacts",
            steps=[
                FlowStep(
                    name="collect_lifecycle_signals",
                    task_type="analytics_tracking",
                    config={"vertical": "saas", "scope": "retention"},
                    timeout=45,
                    retries=2,
                ),
                FlowStep(
                    name="classify_retention_risk",
                    task_type="policy_evaluation",
                    config={"policy": "saas_retention_risk"},
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="draft_retention_brief",
                    task_type="model_inference",
                    config={
                        "model_tier": "cheap",
                        "task": "report_generation",
                        "output_schema": "retention_watch_brief",
                    },
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="store_retention_brief",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "event"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # MediaCommerce EPC Monitoring Flow
        self.register(FlowDefinition(
            flow_type="epc_monitoring_loop",
            description="Monitor EPC and classify content performance using MediaCommerce agent",
            steps=[
                FlowStep(
                    name="calculate_epc",
                    task_type="epc_monitoring",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="classify_performance",
                    task_type="policy_evaluation",
                    config={
                        "thresholds": {
                            "winner": 10.0,
                            "performer": 5.0,
                            "average": 2.50,
                        },
                    },
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="take_action",
                    task_type="content_auto_optimize",
                    config={},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # MediaCommerce Affiliate Optimization Flow
        self.register(FlowDefinition(
            flow_type="affiliate_optimization",
            description="Optimize affiliate placements based on performance using MediaCommerce agent",
            steps=[
                FlowStep(
                    name="analyze_placements",
                    task_type="epc_monitoring",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="identify_underperformers",
                    task_type="policy_evaluation",
                    config={
                        "min_epc_threshold": 2.50,
                        "min_ctr_threshold": 0.01,
                    },
                    timeout=30,
                    retries=1,
                ),
                FlowStep(
                    name="swap_placements",
                    task_type="affiliate_placement",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="log_changes",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "event"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # MediaCommerce Content Repurposing Flow
        self.register(FlowDefinition(
            flow_type="content_repurposing",
            description="Repurpose top-performing content across formats using MediaCommerce agent",
            steps=[
                FlowStep(
                    name="identify_winners",
                    task_type="epc_monitoring",
                    config={"min_epc": 10.0},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="generate_variations",
                    task_type="content_repurpose",
                    config={"default_formats": ["social", "email", "video"]},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="distribute",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "content_asset"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="track_performance",
                    task_type="analytics_tracking",
                    config={},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="attribute_revenue",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "ledger"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # Media Content Velocity Flow
        self.register(FlowDefinition(
            flow_type="media-content-velocity",
            description="Track content velocity",
            steps=[
                FlowStep(
                    name="analyze_velocity",
                    task_type="media_content_velocity",
                    config={},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # Media EPC Monitor Flow
        self.register(FlowDefinition(
            flow_type="media-epc-monitor",
            description="Monitor EPC",
            steps=[
                FlowStep(
                    name="monitor_epc",
                    task_type="media_epc_monitor",
                    config={},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # ContentEngine Content Generation Flow
        self.register(FlowDefinition(
            flow_type="content_generation_with_quality_gate",
            description="Generate content with MediationAgent quality prediction gate",
            steps=[
                FlowStep(
                    name="predict_quality",
                    task_type="content_quality_prediction",
                    config={},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="get_feedback",
                    task_type="content_engine_feedback",
                    config={},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="generate_content",
                    task_type="content_generation",
                    config={},
                    timeout=120,
                    retries=2,
                ),
                FlowStep(
                    name="optimize_ai_seo",
                    task_type="ai_seo_optimization",
                    config={},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # ChiefPulse Executive Briefing Flow
        self.register(FlowDefinition(
            flow_type="executive_briefing_generation",
            description="Generate executive briefing with signal aggregation and anomaly detection",
            steps=[
                FlowStep(
                    name="aggregate_signals",
                    task_type="signal_aggregation",
                    config={"time_window": "24h"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="detect_anomalies",
                    task_type="anomaly_detection",
                    config={"sensitivity": "medium"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="get_approval_queue",
                    task_type="approval_queue",
                    config={"status_filter": "pending"},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="generate_briefing",
                    task_type="executive_briefing",
                    config={"briefing_type": "daily"},
                    timeout=90,
                    retries=2,
                ),
            ],
        ))

        # Mediation Content Decision Flow
        self.register(FlowDefinition(
            flow_type="content_decision_recording",
            description="Record content approval/rejection and update quality patterns",
            steps=[
                FlowStep(
                    name="record_decision",
                    task_type="record_content_decision",
                    config={},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="analyze_patterns",
                    task_type="content_engine_feedback",
                    config={},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # ChiefPulse Anomaly Response Flow
        self.register(FlowDefinition(
            flow_type="anomaly_response",
            description="Detect anomalies and generate recommended actions",
            steps=[
                FlowStep(
                    name="detect_anomalies",
                    task_type="anomaly_detection",
                    config={"sensitivity": "high"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="aggregate_context",
                    task_type="signal_aggregation",
                    config={"time_window": "1h"},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="generate_briefing",
                    task_type="executive_briefing",
                    config={"briefing_type": "incident"},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # ComplianceGate SEO Audit Flow
        self.register(FlowDefinition(
            flow_type="seo_compliance_audit",
            description="Audit content assets for SEO compliance",
            steps=[
                FlowStep(
                    name="audit_content",
                    task_type="seo_audit",
                    config={},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="generate_recommendations",
                    task_type="model_inference",
                    config={
                        "model_tier": "cheap",
                        "task": "seo_recommendations",
                    },
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # ComplianceGate Policy Enforcement Flow
        self.register(FlowDefinition(
            flow_type="policy_enforcement",
            description="Enforce policy compliance with case law references",
            steps=[
                FlowStep(
                    name="check_compliance",
                    task_type="policy_enforcement",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="get_compounded_memory_context",
                    task_type="content_engine_feedback",
                    config={},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="enforce_action",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "task"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # ComplianceGate HIPAA Compliance Flow
        self.register(FlowDefinition(
            flow_type="hipaa_compliance_check",
            description="Check HIPAA compliance with case law references",
            steps=[
                FlowStep(
                    name="check_hipaa",
                    task_type="hipaa_compliance",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="reference_case_law",
                    task_type="model_inference",
                    config={
                        "model_tier": "mid",
                        "task": "case_law_lookup",
                    },
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="log_compliance_status",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "event"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # ComplianceGate Security Audit Flow
        self.register(FlowDefinition(
            flow_type="security_compliance_audit",
            description="Security audit against OWASP and SOC2",
            steps=[
                FlowStep(
                    name="security_scan",
                    task_type="security_audit",
                    config={},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="remediate_critical",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "task"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # ComplianceGate Project Code Analysis Flow
        self.register(FlowDefinition(
            flow_type="project_code_analysis",
            description="Analyze entire project build for compliance issues",
            steps=[
                FlowStep(
                    name="analyze_codebase",
                    task_type="project_code_analysis",
                    config={},
                    timeout=300,
                    retries=2,
                ),
                FlowStep(
                    name="generate_fixes",
                    task_type="model_inference",
                    config={
                        "model_tier": "mid",
                        "task": "code_fix_generation",
                    },
                    timeout=120,
                    retries=2,
                ),
                FlowStep(
                    name="apply_critical_fixes",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "code_fix"},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # ComplianceGate Churn Prevention Flow
        self.register(FlowDefinition(
            flow_type="churn_prevention_compliance",
            description="Ensure churn prevention flows comply with GDPR/CCPA",
            steps=[
                FlowStep(
                    name="check_gdpr_ccpa",
                    task_type="churn_prevention_compliance",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="enforce_opt_out",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "preference"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # BudgetMind Budget Monitoring Flow
        self.register(FlowDefinition(
            flow_type="budget_variance_analysis",
            description="Monitor budget vs actual with variance analysis",
            steps=[
                FlowStep(
                    name="monitor_budget",
                    task_type="budget_monitoring",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="get_compounded_context",
                    task_type="content_engine_feedback",
                    config={},
                    timeout=30,
                    retries=2,
                ),
                FlowStep(
                    name="generate_recommendations",
                    task_type="model_inference",
                    config={
                        "model_tier": "mid",
                        "task": "budget_recommendations",
                    },
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # BudgetMind Unit Economics Flow
        self.register(FlowDefinition(
            flow_type="unit_economics_analysis",
            description="Calculate unit economics with benchmark comparison",
            steps=[
                FlowStep(
                    name="calculate_metrics",
                    task_type="unit_economics",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="compare_benchmarks",
                    task_type="model_inference",
                    config={
                        "model_tier": "cheap",
                        "task": "benchmark_comparison",
                    },
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # BudgetMind Cash Flow Projection Flow
        self.register(FlowDefinition(
            flow_type="cash_flow_projection",
            description="13-week cash flow projection with alerts",
            steps=[
                FlowStep(
                    name="project_cash_flow",
                    task_type="cash_flow_projection",
                    config={"weeks": 13},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="check_alerts",
                    task_type="policy_evaluation",
                    config={"min_runway_days": 90},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # BudgetMind Vendor Consolidation Flow
        self.register(FlowDefinition(
            flow_type="vendor_consolidation",
            description="Identify vendor consolidation opportunities",
            steps=[
                FlowStep(
                    name="analyze_vendors",
                    task_type="vendor_consolidation",
                    config={},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="prioritize_opportunities",
                    task_type="model_inference",
                    config={
                        "model_tier": "cheap",
                        "task": "prioritization",
                    },
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # BudgetMind Scenario Planning Flow (Digital Twin Integration)
        self.register(FlowDefinition(
            flow_type="financial_scenario_planning",
            description="Run financial scenarios using digital twin",
            steps=[
                FlowStep(
                    name="run_base_scenario",
                    task_type="scenario_planning",
                    config={"scenario_name": "base"},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="run_upside_scenario",
                    task_type="scenario_planning",
                    config={"scenario_name": "upside"},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="run_downside_scenario",
                    task_type="scenario_planning",
                    config={"scenario_name": "downside"},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="compare_scenarios",
                    task_type="model_inference",
                    config={
                        "model_tier": "mid",
                        "task": "scenario_comparison",
                    },
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # BudgetMind Financial Policy Enforcement Flow
        self.register(FlowDefinition(
            flow_type="financial_policy_enforcement",
            description="Enforce financial policies with compounded memory",
            steps=[
                FlowStep(
                    name="check_compliance",
                    task_type="financial_policy_enforcement",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="enforce_action",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "task"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # BoardReady Board Deck Generation Flow
        self.register(FlowDefinition(
            flow_type="board_deck_generation",
            description="Generate quarterly board deck with all sections",
            steps=[
                FlowStep(
                    name="aggregate_agent_data",
                    task_type="signal_aggregation",
                    config={"time_window": "quarter"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="generate_deck_sections",
                    task_type="board_deck_generation",
                    config={},
                    timeout=120,
                    retries=2,
                ),
                FlowStep(
                    name="validate_completeness",
                    task_type="policy_evaluation",
                    config={"min_completeness": 0.90},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # BoardReady Investor Update Flow
        self.register(FlowDefinition(
            flow_type="investor_update_generation",
            description="Generate monthly investor update communication",
            steps=[
                FlowStep(
                    name="aggregate_monthly_data",
                    task_type="signal_aggregation",
                    config={"time_window": "month"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="generate_update",
                    task_type="investor_update",
                    config={},
                    timeout=90,
                    retries=2,
                ),
            ],
        ))

        # BoardReady Data Room Maintenance Flow
        self.register(FlowDefinition(
            flow_type="data_room_maintenance",
            description="Maintain living data room for due diligence",
            steps=[
                FlowStep(
                    name="scan_documents",
                    task_type="data_room_maintenance",
                    config={},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="flag_stale_missing",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "task"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # BoardReady Due Diligence Response Flow
        self.register(FlowDefinition(
            flow_type="due_diligence_response",
            description="Respond to due diligence request with documents",
            steps=[
                FlowStep(
                    name="gather_documents",
                    task_type="due_diligence_response",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="log_response",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "event"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # BoardReady Exit Preparation Flow
        self.register(FlowDefinition(
            flow_type="exit_preparation",
            description="Prepare exit materials (CIM, valuation tracking)",
            steps=[
                FlowStep(
                    name="calculate_valuation",
                    task_type="exit_preparation",
                    config={},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="check_data_room_readiness",
                    task_type="data_room_maintenance",
                    config={},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # Maternal Health Automated Ingestion Flow (Navigate Integration)
        self.register(FlowDefinition(
            flow_type="maternal_resource_ingestion",
            description="Automated ingestion of maternal resources into Arkham Memory",
            steps=[
                FlowStep(
                    name="ingest_resource",
                    task_type="maternal_resource_ingestion",
                    config={},
                    timeout=120,
                    retries=2,
                ),
                FlowStep(
                    name="verify_entities",
                    task_type="maternal_place_verification",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="store_memory",
                    task_type="memory_creation",
                    config={"note_type": "domain"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # Maternal Place Verification Flow
        self.register(FlowDefinition(
            flow_type="maternal_place_verification_loop",
            description="Verify and score maternal-friendly locations",
            steps=[
                FlowStep(
                    name="verify_place",
                    task_type="maternal_place_verification",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="record_result",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "place_verification"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # Pregnancy Journey Intelligent Reminders Flow
        self.register(FlowDefinition(
            flow_type="pregnancy_journey_advisory",
            description="Generate intelligent advice based on pregnancy milestones",
            steps=[
                FlowStep(
                    name="generate_intelligence",
                    task_type="pregnancy_journey_intelligence",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="log_event",
                    task_type="artifact_storage",
                    config={"storage": "database", "record_type": "journey_milestone"},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # Ecom Inventory Monitor Flow
        self.register(FlowDefinition(
            flow_type="ecom_inventory_monitor",
            description="Monitor ecommerce inventory levels and alert on low stock",
            steps=[
                FlowStep(
                    name="check_inventory",
                    task_type="inventory_monitoring",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="alert_operator",
                    task_type="operator_alert",
                    config={},
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # Ecom Cart Recovery Flow
        self.register(FlowDefinition(
            flow_type="ecom_cart_recovery",
            description="Analyze abandoned carts and generate recovery emails",
            steps=[
                FlowStep(
                    name="analyze_signals",
                    task_type="signal_analysis",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="generate_email",
                    task_type="content_generation",
                    config={"template": "cart_recovery"},
                    timeout=90,
                    retries=2,
                ),
            ],
        ))

        # Digital IT Girl Predictive Niche Flow
        self.register(FlowDefinition(
            flow_type="digital_it_girl_predictive_niche",
            description="Score a niche opportunity and synthesize a Digital IT Girl market brief",
            steps=[
                FlowStep(
                    name="score_segment_opportunity",
                    task_type="niche_opportunity_scoring",
                    config={"vertical": "digital_it_girl"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="synthesize_market_brief",
                    task_type="market_research_synthesis",
                    config={"vertical": "digital_it_girl", "mode": "balanced"},
                    timeout=90,
                    retries=2,
                ),
                FlowStep(
                    name="store_niche_artifact",
                    task_type="artifact_storage",
                    config={
                        "storage": "database",
                        "record_type": "market_brief",
                        "source_step": "synthesize_market_brief",
                        "content_field": "market_brief",
                    },
                    timeout=30,
                    retries=2,
                ),
            ],
        ))

        # Staffing vertical flows
        self.register(FlowDefinition(
            flow_type="staffing-placement-audit",
            description="Audit staffing placement processes",
            steps=[
                FlowStep(
                    name="run_audit",
                    task_type="staffing-placement-audit",
                    config={},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        self.register(FlowDefinition(
            flow_type="staffing-pipeline-velocity",
            description="Monitor staffing pipeline velocity",
            steps=[
                FlowStep(
                    name="measure_velocity",
                    task_type="staffing-pipeline-velocity",
                    config={},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # Studio Delivery Posture Flow
        self.register(FlowDefinition(
            flow_type="studio_delivery_posture",
            description="Audit studio delivery posture and project velocity",
            steps=[
                FlowStep(
                    name="measure_velocity",
                    task_type="studio-project-velocity",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="audit_posture",
                    task_type="studio-delivery-posture",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="summarize_findings",
                    task_type="model_inference",
                    config={"model_tier": "mid", "task": "studio_posture_summary"},
                    timeout=90,
                    retries=2,
                ),
            ],
        ))

        # Studio Project Velocity Flow
        self.register(FlowDefinition(
            flow_type="studio_project_velocity",
            description="Track studio project delivery velocity",
            steps=[
                FlowStep(
                    name="measure_velocity",
                    task_type="studio-project-velocity",
                    config={},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="analyze_trends",
                    task_type="model_inference",
                    config={"model_tier": "cheap", "task": "velocity_trend_analysis"},
                    timeout=60,
                    retries=2,
                ),
            ],
        ))

        # Arkham Project Review Flow
        self.register(FlowDefinition(
            flow_type="arkham_project_review",
            description="Autonomous multi-agent review of Arkham project",
            steps=[
                FlowStep(
                    name="analyze_codebase",
                    task_type="project_code_analysis",
                    config={"audit_type": "full"},
                    timeout=600,
                    retries=1,
                ),
                FlowStep(
                    name="security_audit",
                    task_type="security_audit",
                    config={"deep_scan": True},
                    timeout=300,
                    retries=2,
                ),
                FlowStep(
                    name="policy_compliance",
                    task_type="policy_enforcement",
                    config={"standard": "arkham_v1"},
                    timeout=60,
                    retries=2,
                ),
                FlowStep(
                    name="generate_review_summary",
                    task_type="model_inference",
                    config={
                        "model_tier": "premium",
                        "task": "project_review_synthesis",
                    },
                    timeout=180,
                    retries=2,
                ),
                FlowStep(
                    name="store_review_artifact",
                    task_type="artifact_storage",
                    config={
                        "storage": "database",
                        "record_type": "project_review",
                        "path_template": "reviews/arkham/{timestamp}.json",
                    },
                    timeout=60,
                    retries=3,
                ),
            ],
        ))

        logger.info(f"Registered {len(self._flows)} built-in flows")
