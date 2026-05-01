# AI Workflows: Studio Vertical

## 1. Studio Project Review
- **Trigger**: New project initialization in Studio.
- **AI Agents Involved**: Architecture Auditor, Security Guardian, ComplianceGate.
- **Expected Output**: Full review of project scaffolding, security audit, and compliance check.

## 2. Delivery Posture Audit
- **Trigger**: Bi-weekly milestone check or manual trigger.
- **AI Agents Involved**: Architecture Auditor, ChiefPulse.
- **Expected Output**: Posture report including risk assessment and milestone confidence.

## 3. Project Velocity Tracking
- **Trigger**: End of sprint or monthly performance review.
- **AI Agents Involved**: BudgetMind, Architecture Auditor.
- **Expected Output**: Throughput analysis, trend report, and bottleneck identification.

## 4. Client-Facing Status Synthesis
- **Trigger**: Weekly client reporting cycle.
- **AI Agents Involved**: BoardReady, ContentEngine.
- **Expected Output**: Professional project status brief for external stakeholders.

---

## Orchestration Steps

```python
# 1. Studio Delivery Posture Workflow
# flow_type: "studio_delivery_posture"
steps = [
    {"name": "measure_velocity", "task_type": "studio-project-velocity"},
    {"name": "audit_posture", "task_type": "studio-delivery-posture"},
    {"name": "summarize_findings", "task_type": "model_inference", "config": {"model_tier": "mid"}}
]

# 2. Studio Project Velocity Workflow
# flow_type: "studio_project_velocity"
steps = [
    {"name": "measure_velocity", "task_type": "studio-project-velocity"},
    {"name": "analyze_trends", "task_type": "model_inference", "config": {"model_tier": "cheap"}}
]
```
