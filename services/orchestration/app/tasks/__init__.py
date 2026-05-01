"""
Task Executors

Execute workflow tasks for the orchestration layer.
Each executor handles a specific task type.
"""

import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class TaskExecutor(ABC):
    """Base class for task executors"""
    
    @property
    @abstractmethod
    def task_type(self) -> str:
        """Return the task type this executor handles"""
        pass
    
    @abstractmethod
    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute the task and return output"""
        pass


class TaskExecutorRegistry:
    """Registry of task executors"""
    
    def __init__(self):
        self._executors: Dict[str, TaskExecutor] = {}
    
    def register(self, executor: TaskExecutor):
        """Register an executor"""
        self._executors[executor.task_type] = executor
        logger.info(f"Registered executor: {executor.task_type}")
    
    def get_executor(self, task_type: str) -> Optional[TaskExecutor]:
        """Get executor for task type"""
        return self._executors.get(task_type)
    
    def list_executors(self) -> list[str]:
        """List registered executor types"""
        return list(self._executors.keys())


# Import all executors to register them
from app.tasks.bim import BIMRetrievalExecutor, BIMIssueDetectionExecutor
from app.tasks.memory import MemoryRetrievalExecutor, MemoryCreationExecutor
from app.tasks.inference import ModelInferenceExecutor
from app.tasks.policy import PolicyEvaluationExecutor
from app.tasks.validation import SchemaValidationExecutor
from app.tasks.artifact import ArtifactStorageExecutor
from app.tasks.deal_flow import LeadRoutingExecutor
from app.tasks.media_content import ContentStrategyGenerationExecutor
from app.tasks.fulfillment_ops import (
    PageOptimizationExecutor,
    ABTestSetupExecutor,
    AnalyticsTrackingExecutor,
)
from app.tasks.media_commerce import (
    EPCMonitoringExecutor,
    ContentAutoOptimizeExecutor,
    AffiliatePlacementExecutor,
    ContentRepurposeExecutor,
)
from app.tasks.content_engine import (
    ContentGenerationExecutor,
    AISeoOptimizationExecutor,
    ProgrammaticSeoExecutor,
)
from app.tasks.chief_pulse import (
    SignalAggregationExecutor,
    AnomalyDetectionExecutor,
    ExecutiveBriefingExecutor,
    ApprovalQueueExecutor,
)
from app.tasks.mediation import (
    ContentQualityPredictionExecutor,
    RecordContentDecisionExecutor,
    ContentEngineFeedbackExecutor,
)
from app.tasks.compliance_gate import (
    SeoAuditExecutor,
    PolicyEnforcementExecutor,
    HipaaComplianceExecutor,
    SecurityAuditExecutor,
    ProjectCodeAnalysisExecutor,
    ChurnPreventionComplianceExecutor,
)
from app.tasks.budget_mind import (
    BudgetMonitoringExecutor,
    UnitEconomicsExecutor,
    CashFlowProjectionExecutor,
    VendorConsolidationExecutor,
    ScenarioPlanningExecutor,
    FinancialPolicyEnforcementExecutor,
)
from app.tasks.board_ready import (
    BoardDeckGenerationExecutor,
    InvestorUpdateExecutor,
    DataRoomMaintenanceExecutor,
    DueDiligenceResponseExecutor,
    ExitPreparationExecutor,
)
from app.tasks.maternal_health import (
    MaternalPlaceVerificationExecutor,
    MaternalIngestionExecutor,
    PregnancyJourneyIntelligenceExecutor,
)
from app.tasks.ecommerce import (
    InventoryMonitoringExecutor,
    OperatorAlertExecutor,
    SignalAnalysisExecutor,
)
from app.tasks.digital_it_girl import (
    NicheOpportunityScoringExecutor,
    MarketResearchSynthesisExecutor,
)
from app.tasks.media import (
    MediaContentVelocityExecutor,
    MediaEPCMonitorExecutor,
)
from app.tasks.staffing import (
    StaffingPlacementAuditExecutor,
    StaffingPipelineVelocityExecutor,
)
from app.tasks.studio import (
    StudioDeliveryPostureExecutor,
    StudioProjectVelocityExecutor,
)


def create_executor_registry() -> TaskExecutorRegistry:
    """Create and populate executor registry"""
    registry = TaskExecutorRegistry()

    # BIM executors
    registry.register(BIMRetrievalExecutor())
    registry.register(BIMIssueDetectionExecutor())

    # Memory executors
    registry.register(MemoryRetrievalExecutor())
    registry.register(MemoryCreationExecutor())

    # Inference executors
    registry.register(ModelInferenceExecutor())

    # Policy executors
    registry.register(PolicyEvaluationExecutor())

    # Validation executors
    registry.register(SchemaValidationExecutor())

    # Artifact executors
    registry.register(ArtifactStorageExecutor())

    # Media-commerce vertical executors
    registry.register(LeadRoutingExecutor())
    registry.register(ContentStrategyGenerationExecutor())
    registry.register(PageOptimizationExecutor())
    registry.register(ABTestSetupExecutor())
    registry.register(AnalyticsTrackingExecutor())
    registry.register(EPCMonitoringExecutor())
    registry.register(ContentAutoOptimizeExecutor())
    registry.register(AffiliatePlacementExecutor())
    registry.register(ContentRepurposeExecutor())

    # ContentEngine executors (Cycle 4)
    registry.register(ContentGenerationExecutor())
    registry.register(AISeoOptimizationExecutor())
    registry.register(ProgrammaticSeoExecutor())

    # ChiefPulse executors (Cycle 5)
    registry.register(SignalAggregationExecutor())
    registry.register(AnomalyDetectionExecutor())
    registry.register(ExecutiveBriefingExecutor())
    registry.register(ApprovalQueueExecutor())

    # Mediation executors (Cross-cycle memory)
    registry.register(ContentQualityPredictionExecutor())
    registry.register(RecordContentDecisionExecutor())
    registry.register(ContentEngineFeedbackExecutor())

    # ComplianceGate executors (Cycle 6)
    registry.register(SeoAuditExecutor())
    registry.register(PolicyEnforcementExecutor())
    registry.register(HipaaComplianceExecutor())
    registry.register(SecurityAuditExecutor())
    registry.register(ProjectCodeAnalysisExecutor())
    registry.register(ChurnPreventionComplianceExecutor())

    # BudgetMind executors (Cycle 7)
    registry.register(BudgetMonitoringExecutor())
    registry.register(UnitEconomicsExecutor())
    registry.register(CashFlowProjectionExecutor())
    registry.register(VendorConsolidationExecutor())
    registry.register(ScenarioPlanningExecutor())
    registry.register(FinancialPolicyEnforcementExecutor())

    # BoardReady executors (Cycle 8)
    registry.register(BoardDeckGenerationExecutor())
    registry.register(InvestorUpdateExecutor())
    registry.register(DataRoomMaintenanceExecutor())
    registry.register(DueDiligenceResponseExecutor())
    registry.register(ExitPreparationExecutor())

    # Maternal Health executors (Vertical Integration with Navigate)
    registry.register(MaternalPlaceVerificationExecutor())
    registry.register(MaternalIngestionExecutor())
    registry.register(PregnancyJourneyIntelligenceExecutor())

    # Ecommerce vertical executors
    registry.register(InventoryMonitoringExecutor())
    registry.register(OperatorAlertExecutor())
    registry.register(SignalAnalysisExecutor())

    # Digital IT Girl vertical executors
    registry.register(NicheOpportunityScoringExecutor())
    registry.register(MarketResearchSynthesisExecutor())

    # Media vertical executors
    registry.register(MediaContentVelocityExecutor())
    registry.register(MediaEPCMonitorExecutor())

    # Staffing vertical executors
    registry.register(StaffingPlacementAuditExecutor())
    registry.register(StaffingPipelineVelocityExecutor())

    # Studio vertical executors
    registry.register(StudioDeliveryPostureExecutor())
    registry.register(StudioProjectVelocityExecutor())

    return registry
