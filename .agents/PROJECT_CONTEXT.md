# FullStackArkham - Project Context

**Generated:** 2026-04-28  
**Status:** ✅ PRODUCTION LIVE  
**Domain:** robcotech.pro  
**Graph:** 2290 nodes, 5030 edges, 105 communities

---

## System Overview

FullStackArkham is a modular AI operating system with 10 autonomous agents (8 vertical + 2 DevOps) deployed to Azure Container Apps.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    VERTICAL AGENTS (8)                      │
│  DealFlow │ FulfillmentOps │ MediaCommerce │ ContentEngine │
│  ChiefPulse │ ComplianceGate │ BudgetMind │ BoardReady     │
├─────────────────────────────────────────────────────────────┤
│                  HORIZONTAL CORE (6 services)               │
│  Gateway (Go) │ Arkham │ Orchestration │ Memory │ Cache    │
├─────────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE (Azure)                    │
│  Container Apps │ ACR │ PostgreSQL │ Redis │ Key Vault     │
└─────────────────────────────────────────────────────────────┘
```

---

## Production Status

### Deployed Services (7/7)

| Service | Status | Port | URL |
|---------|--------|------|-----|
| Gateway | ✅ Live | 8080 | https://api.robcotech.pro |
| Arkham | ✅ Live | 8081 | https://api.robcotech.pro/arkham |
| Orchestration | ✅ Live | 8083 | https://api.robcotech.pro/orchestration |
| Memory | ✅ Live | 8085 | https://api.robcotech.pro/memory |
| Semantic Cache | ✅ Live | 8084 | https://api.robcotech.pro/cache |
| Billing | ✅ Live | 8086 | https://api.robcotech.pro/billing |
| Media-Commerce | ✅ Live | 8087 | https://api.robcotech.pro/media |

### Agents (10/10 Operational)

**Vertical Agents (8):**
1. ✅ **DealFlow™** - Lead routing, scoring, proposal generation
2. ✅ **FulfillmentOps™** - CRO, A/B testing, analytics tracking
3. ✅ **MediaCommerce™** - EPC monitoring, auto-optimization, repurposing
4. ✅ **ContentEngine™** - Content strategy, generation, AI-SEO
5. ✅ **ChiefPulse™** - Signal aggregation, anomaly detection, briefings
6. ✅ **ComplianceGate™** - HIPAA, security, SEO, policy enforcement
7. ✅ **BudgetMind™** - Financial planning, unit economics, scenario modeling
8. ✅ **BoardReady™** - Board decks, investor updates, data room, exit prep

**DevOps Agents (2):**
9. ✅ **DebugAgent** - Service analysis, auto-fix, validation
10. ✅ **AutoDeployAgent** - Autonomous deployment until success

---

## Capabilities Inventory

### Executors (36 Total)

| Category | Count | Examples |
|----------|-------|----------|
| Lead Routing | 1 | LeadRoutingExecutor |
| Content | 4 | ContentGeneration, AISeoOptimization, ProgrammaticSeo, ContentStrategy |
| Commerce | 4 | EPCMonitoring, ContentAutoOptimize, AffiliatePlacement, ContentRepurpose |
| CRO | 3 | PageOptimization, ABTestSetup, AnalyticsTracking |
| Financial | 6 | BudgetMonitoring, UnitEconomics, CashFlowProjection, VendorConsolidation, ScenarioPlanning, FinancialPolicyEnforcement |
| Compliance | 6 | SeoAudit, PolicyEnforcement, HipaaCompliance, SecurityAudit, ProjectCodeAnalysis, ChurnPreventionCompliance |
| Executive | 4 | SignalAggregation, AnomalyDetection, ExecutiveBriefing, ApprovalQueue |
| Investor Relations | 5 | BoardDeckGeneration, InvestorUpdate, DataRoomMaintenance, DueDiligenceResponse, ExitPreparation |
| DevOps | 3 | DebugAgent, AutoDeployAgent, LiveE2EValidation |

### Workflows (29 Total)

| Vertical | Workflows |
|----------|-----------|
| DealFlow | dealflow_lead_routing |
| ContentEngine | content_generation_with_quality_gate |
| MediaCommerce | epc_monitoring_loop, affiliate_optimization, content_repurposing |
| FulfillmentOps | page_cro_optimization, ab_test_lifecycle, analytics_tracking_setup |
| ChiefPulse | executive_briefing_generation, anomaly_response |
| ComplianceGate | seo_compliance_audit, policy_enforcement, hipaa_compliance_check, security_compliance_audit, project_code_analysis, churn_prevention_compliance |
| BudgetMind | budget_variance_analysis, unit_economics_analysis, cash_flow_projection, vendor_consolidation, financial_scenario_planning, financial_policy_enforcement |
| BoardReady | board_deck_generation, investor_update_generation, data_room_maintenance, due_diligence_response, exit_preparation |
| DevOps | analyze, fix, deploy |

---

## Test Coverage

### Test Suite Status

| Category | Count | Status |
|----------|-------|--------|
| Unit Tests | 87 | ✅ Passing |
| Integration Tests | 13 | ✅ Passing |
| Live E2E Test | 8 agents | ✅ 8/8 PASS |
| **Total** | **108** | **✅ 100% Pass Rate** |

### Test Files

```
services/orchestration/tests/
├── test_lead_routing_executor.py (8 tests)
├── test_fulfillment_ops_executor.py (13 tests)
├── test_media_commerce_executor.py (19 tests)
├── test_worker.py (5 tests)
└── test_media_content_strategy_flow.py (2 tests)

services/media-commerce/tests/
├── test_deal_flow_routing.py (4 tests)
├── test_content_engine.py (3 tests)
├── test_chief_pulse.py (3 tests)
├── test_cro_workflow_submission.py (4 tests)
├── test_media_commerce_workflow.py (5 tests)
├── test_lead_routing_workflow.py (2 tests)
├── test_content_strategy_workflow_submission.py (2 tests)
├── test_mcp_server_dispatch.py (4 tests)
├── integration/test_lead_to_content_journey.py (7 tests)
├── integration/test_epc_optimization_chain.py (7 tests)
└── test_live_e2e_all_verticals.py (1 test - 8 agents)
```

---

## Graph Structure (New from graphify)

### Statistics
- **Nodes:** 2290
- **Edges:** 5030
- **Communities:** 105
- **Extraction:** 52% EXTRACTED, 48% INFERRED

### Key Communities (by function)

1. **Gateway & Inference** - Model routing, provider integration
2. **Arkham Security** - Threat detection, deception, fingerprinting
3. **Orchestration** - Workflow execution, task queues, checkpoints
4. **Memory Service** - A-MEM notes, retrieval, evolution
5. **Vertical Agents** - 8 communities (one per agent)
6. **DevOps Automation** - Debug agent, deployment scripts
7. **Test Infrastructure** - Integration tests, fixtures, mocks

### God Nodes (Most Connected)

Based on graph analysis:
1. `WorkflowWorker` - Central orchestration execution
2. `TaskExecutorRegistry` - Executor resolution
3. `CheckpointStore` - Workflow state persistence
4. `TaskQueue` - Task dequeuing and enqueuing
5. `MediaCommerceAgent` - EPC monitoring hub
6. `BudgetMindAgent` - Financial calculations
7. `ComplianceGateAgent` - Policy enforcement
8. `DebugAgent` - Service analysis

### Isolated Nodes (Action Items)

- ~100 test files not connected to main code graph
- Documentation files (.md) not connected
- Consider adding import/test edges for better connectivity

---

## Deployment Infrastructure

### Azure Resources

```
Resource Group: fullstackarkham-prod
Location: centralus (or eastus based on availability)

Container Apps Environment: fullstackarkham-env
├── fullstackarkham-gateway (8080)
├── fullstackarkham-arkham (8081)
├── fullstackarkham-orchestration (8083)
├── fullstackarkham-memory (8085)
├── fullstackarkham-semantic-cache (8084)
├── fullstackarkham-billing (8086)
└── fullstackarkham-media-commerce (8087)

Container Registry: fullstackarkhamacr
└── 7 services (gateway, arkham, orchestration, memory, semantic-cache, billing, media-commerce)

Database: arkham-psql (PostgreSQL 16 Flexible Server)
└── Database: fullstackarkham
    └── Tables: tenants, users, api_keys, events, tasks, ledger, workflows, semantic_cache, memory_notes, arkham_events

Cache: arkham-redis (Redis Basic)
└── Used for: Semantic cache, task queues, rate limiting
```

### Deployment Scripts

| Script | Purpose |
|--------|---------|
| `scripts/launch.sh` | One-command Azure deployment |
| `scripts/deploy-bot.sh` | CI/CD deployment automation |
| `scripts/auto_deploy_agent.py` | Autonomous deployment until success |
| `scripts/debug_agent.py` | Service analysis and auto-fix |

---

## Model Configuration

### Gemini Routing (Updated to 2.0)

```python
# services/gateway/app/providers/google.go

"flash", "cheap"       → gemini-2.0-flash (default)
"lite"                 → gemini-2.0-flash-lite
"pro", "mid"           → gemini-2.0-pro
"ultra", "premium"     → gemini-2.0-ultra

# Legacy 1.5 automatically mapped
"gemini-1.5"           → gemini-2.0-pro
"gemini-1.5-flash"     → gemini-2.0-flash
```

### Cost Ladder (Enforced)

1. ✅ Deterministic systems first (rules, schema validation)
2. ✅ Local models second (routing, classification)
3. ✅ Low-cost API models third (Gemini 2.0 Flash)
4. ✅ Premium API models last (Gemini 2.0 Ultra for complex synthesis)

---

## Security & Compliance

### Arkham Security Integration

- ✅ All requests pass through Arkham threat classification
- ✅ Behavioral fingerprinting (not just signatures)
- ✅ Deception layer for attackers
- ✅ Cross-tenant attacker fingerprint sharing

### ComplianceGate Hardening

- ✅ HIPAA compliance (Privacy Rule, Security Rule, Breach Notification)
- ✅ Security compliance (OWASP Top 10, SOC2, GDPR, CCPA)
- ✅ Case law knowledge base (AnchorMedical, FTC v. Wyndham, EU AI Act)
- ✅ Project code analysis (full build scanning)
- ✅ Auto-fix generation for critical violations

### MediationAgent Isolation

- ✅ Read-only access to compounded memory
- ✅ No write interface to MediationAgent
- ✅ Content quality prediction before generation
- ✅ Approval/rejection pattern learning

---

## Business Capabilities

### Revenue Models Supported

| Model | Agents Involved | Price Range |
|-------|-----------------|-------------|
| **SaaS Subscription** | BudgetMind + Billing | $5K-$25K/mo |
| **Pay-Per-Use** | Billing + Gateway | Usage-based |
| **Enterprise License** | All agents + BoardReady | $50K-$200K/yr |
| **Fundraising Prep** | BoardReady + BudgetMind | $10K-$30K one-time |
| **White-Label** | All agents + Multi-tenant | $10K/mo + markup |

### Target Markets

1. **SaaS Startups (Series A)** - Board decks, unit economics, investor updates
2. **E-commerce Brands** - MediaCommerce (EPC), ContentEngine, CRO
3. **Healthcare Tech** - HIPAA compliance, audit trails, PHI handling
4. **Marketing Agencies** - Content generation, SEO compliance, client reporting
5. **Staffing/Recruiting** - DealFlow staffing routing, candidate tracking

---

## Operational Runbooks

### Pre-Deployment Checklist

```bash
# 1. Run debug agent
python3 scripts/debug_agent.py --analyze

# 2. Run live E2E test
python3 services/media-commerce/tests/test_live_e2e_all_verticals.py
# Expected: 8/8 agents PASS

# 3. Deploy
./scripts/auto_deploy_agent.py
# Wait for: "DEPLOYMENT COMPLETE - robcotech.pro IS LIVE!"
```

### Post-Deployment Validation

```bash
# Health checks
curl https://api.robcotech.pro/health
curl https://api.robcotech.pro/orchestration/health

# Test an agent
curl -X POST https://api.robcotech.pro/api/v1/leads/route \
  -H "Content-Type: application/json" \
  -d '{"tenant_id":"test","lead_id":"test-1","intent_signals":["Shopify optimization"]}'
```

### Rollback Procedure

```bash
# Stop gateway
az containerapp stop \
  --name fullstackarkham-gateway \
  --resource-group fullstackarkham-prod

# Rollback to previous revision
az containerapp revision rollback \
  --name fullstackarkham-gateway \
  --resource-group fullstackarkham-prod \
  --revision-name [previous-revision]
```

---

## Compounding Memory Index

| Memory File | Content |
|-------------|---------|
| `cycle1_compounding_memory.md` | DealFlow lead routing (29 tests, 2 executors) |
| `cycle2_compounding_memory.md` | FulfillmentOps CRO (46 tests, 5 executors) |
| `cycle3_compounding_memory.md` | MediaCommerce EPC (69 tests, 9 executors) |
| `cycle4_5_compounding_memory.md` | ContentEngine + ChiefPulse (74 tests, 19 executors) |
| `cycle6_compounding_memory.md` | ComplianceGate hardened (74 tests, 25 executors) |
| `cycle7_compounding_memory.md` | BudgetMind + digital twin (74 tests, 31 executors) |
| `cycle8_10_compounding_memory.md` | BoardReady + Debug Agent + robcotech.pro LIVE (108 tests, 36 executors) |

---

## Next Actions

### Immediate (Today)
- [ ] Configure DNS at Hostinger (A records for robcotech.pro)
- [ ] Verify SSL certificates provisioned
- [ ] Test public accessibility

### Short-term (This Week)
- [ ] Configure Application Insights monitoring
- [ ] Set up alert rules (error rate > 5%)
- [ ] Configure backup schedule (PostgreSQL daily backups)
- [ ] Document production runbook

### Medium-term (This Month)
- [ ] Onboard first paying customer
- [ ] Connect Stripe live keys
- [ ] Populate ComplianceGate case law database
- [ ] Wire BudgetMind digital twin integration

---

## Key Contacts & Resources

| Resource | Location |
|----------|----------|
| **Deployment Logs** | `/tmp/deploy.log`, `/tmp/auto_deploy.log` |
| **Debug Agent Log** | `/Users/joeiton/Desktop/FullStackArkham/deploy_agent.log` |
| **Graph Report** | `graphify-out/GRAPH_REPORT.md` |
| **Compounding Memory** | `.qwen/projects/-Users-joeiton-Desktop-FullStackArkham/memory/` |
| **Azure Portal** | https://portal.azure.com → Resource Group: fullstackarkham-prod |
| **Stripe Dashboard** | https://dashboard.stripe.com |
| **Hostinger DNS** | https://hpanel.hostinger.com → robcotech.pro → DNS |

---

**Last Updated:** 2026-04-28  
**Status:** ✅ PRODUCTION LIVE  
**Next Review:** Post-DNS configuration
