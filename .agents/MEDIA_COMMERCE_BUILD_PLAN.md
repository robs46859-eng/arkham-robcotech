# Media-Commerce Vertical Build Plan

**Created:** 2026-04-28  
**Status:** Cycle 3 Complete (MediaCommerce EPC)  
**Next:** Cycle 4 (ContentEngine Generation)

---

## Build Order (8 Verticals)

### ✅ Cycle 1: DealFlow™ (COMPLETE)
**Status:** Production-ready  
**What:** Lead scoring, cross-vertical routing, proposal generation  
**Why First:** Central to Scenario 5, fits 13-entity model, deterministic logic  
**Files:** `services/orchestration/app/tasks/deal_flow.py`  
**Tests:** 29 passing (cumulative: 69)

### ✅ Cycle 2: FulfillmentOps™ (COMPLETE)
**Status:** Production-ready  
**What:** CRO optimization, A/B testing, analytics tracking  
**Why Second:** Completes content loop (create → optimize → measure), no external dependencies  
**Target Files:** `services/orchestration/app/tasks/fulfillment_ops.py`  
**Executors:** 3 created (PageOptimization, ABTestSetup, AnalyticsTracking)  
**Workflows:** 3 registered (page_cro_optimization, ab_test_lifecycle, analytics_tracking_setup)  
**Tests:** 17 passing (cumulative: 69)

### ✅ Cycle 3: MediaCommerce™ (COMPLETE)
**Status:** Production-ready  
**What:** EPC monitoring, auto-optimization, affiliate placement, content repurposing  
**Why Third:** Core differentiator (algorithmic relevance arbitrage), depends on content assets existing  
**Target Files:** `services/orchestration/app/tasks/media_commerce.py`  
**Executors:** 4 created (EPCMonitoring, ContentAutoOptimize, AffiliatePlacement, ContentRepurpose)  
**Workflows:** 3 registered (epc_monitoring_loop, affiliate_optimization, content_repurposing)  
**Tests:** 23 passing (cumulative: 69)

### 🔄 Cycle 4: ContentEngine™ (NEXT)
**Status:** Not started  
**What:** Content strategy, generation, AI-SEO, programmatic SEO  
**Why Fourth:** Content creation is the source of the media-commerce loop  
**Target Files:** `services/orchestration/app/tasks/content_engine.py`  
**Estimated:** 2.5 hours (model inference adds complexity)

### 📋 Cycle 3: MediaCommerce™
**Status:** Not started  
**What:** EPC monitoring, auto-optimization, content repurposing  
**Why Third:** Core differentiator (algorithmic relevance arbitrage), depends on content assets existing  
**Target Files:** `services/orchestration/app/tasks/media_commerce.py`

### 📋 Cycle 4: ContentEngine™
**Status:** Not started  
**What:** Content strategy, generation, SEO optimization  
**Why Fourth:** Content creation feeds MediaCommerce optimization loop  
**Target Files:** `services/orchestration/app/tasks/content_engine.py`

### 📋 Cycle 5: ChiefPulse™
**Status:** Not started  
**What:** Executive aggregation, anomaly detection, approval queue  
**Why Fifth:** Needs other agents producing data to aggregate  
**Target Files:** `services/orchestration/app/tasks/chief_pulse.py`

### 📋 Cycle 6: ComplianceGate™
**Status:** Not started  
**What:** SEO audits, policy enforcement, churn prevention  
**Why Sixth:** Cross-cutting concern, needs content/leads/deals to enforce against  
**Target Files:** `services/orchestration/app/tasks/compliance_gate.py`

### 📋 Cycle 7: BudgetMind™
**Status:** Not started  
**What:** Budget tracking, unit economics, vendor management  
**Why Seventh:** Needs ledger/revenue data from other verticals  
**Target Files:** `services/orchestration/app/tasks/budget_mind.py`

### 📋 Cycle 8: BoardReady™
**Status:** Not started  
**What:** Board deck generation, investor updates, data room  
**Why Last:** Aggregates all other agents' performance data  
**Target Files:** `services/orchestration/app/tasks/board_ready.py`

---

## Agent Outlines

### FulfillmentOps™ Agent (Cycle 2)

**Purpose:** Autonomous delivery and conversion optimization

**Capabilities:**
- Page CRO (landing pages, marketing pages)
- Form optimization (signup, lead capture, onboarding)
- A/B test setup and monitoring
- Analytics event tracking
- Churn prevention flows

**Executors to Create:**
```
services/orchestration/app/tasks/fulfillment_ops.py
├── PageOptimizationExecutor (task_type: page_optimization)
├── ABTestSetupExecutor (task_type: ab_test_setup)
├── AnalyticsTrackingExecutor (task_type: analytics_tracking)
└── ChurnPreventionExecutor (task_type: churn_prevention)
```

**Workflows to Register:**
```
services/orchestration/app/flows/registry.py
├── page_cro_optimization (3 steps: analyze, generate_variant, implement)
├── ab_test_lifecycle (5 steps: design, implement, monitor, decide, deploy)
└── churn_prevention_flow (4 steps: detect_risk, present_offer, track_response, update_status)
```

**Endpoints to Add:**
```
services/media-commerce/app/main.py
├── POST /api/v1/cro/optimize-page/workflow
├── POST /api/v1/cro/ab-test/workflow
└── POST /api/v1/analytics/track/workflow
```

**Tests to Write:**
- `test_fulfillment_ops_executor.py` (8 tests)
- `test_cro_workflow_submission.py` (2 tests)

---

### MediaCommerce™ Agent (Cycle 3)

**Purpose:** Algorithmic relevance arbitrage engine

**Capabilities:**
- Real-time EPC monitoring
- Auto-optimize content (retire losers, scale winners)
- Affiliate placement optimization
- Content repurposing across formats

**Executors to Create:**
```
services/orchestration/app/tasks/media_commerce.py
├── EPCMonitoringExecutor (task_type: epc_monitoring)
├── ContentAutoOptimizeExecutor (task_type: content_auto_optimize)
├── AffiliatePlacementExecutor (task_type: affiliate_placement)
└── ContentRepurposeExecutor (task_type: content_repurpose)
```

**Workflows to Register:**
```
services/orchestration/app/flows/registry.py
├── epc_monitoring_loop (3 steps: calculate_epc, classify_performance, take_action)
├── affiliate_optimization (4 steps: analyze_placements, swap_underperformers, test_new, log_changes)
└── content_repurposing (5 steps: identify_winners, generate_variations, distribute, track, attribute)
```

---

### ContentEngine™ Agent (Cycle 4)

**Purpose:** Autonomous content creation and SEO

**Capabilities:**
- Content strategy generation
- Multi-format content creation (articles, social, video, ads)
- AI search optimization
- Programmatic SEO at scale

**Executors to Create:**
```
services/orchestration/app/tasks/content_engine.py
├── ContentStrategyExecutor (task_type: content_strategy) - Already exists, enhance
├── ContentGenerationExecutor (task_type: content_generation)
├── AISeoOptimizationExecutor (task_type: ai_seo_optimization)
└── ProgrammaticSeoExecutor (task_type: programmatic_seo)
```

---

### ChiefPulse™ Agent (Cycle 5)

**Purpose:** Executive AI Chief of Staff

**Capabilities:**
- Cross-agent signal synthesis
- Anomaly detection and alerting
- Approval queue management
- Daily executive briefing generation

**Executors to Create:**
```
services/orchestration/app/tasks/chief_pulse.py
├── SignalAggregationExecutor (task_type: signal_aggregation)
├── AnomalyDetectionExecutor (task_type: anomaly_detection)
├── ApprovalQueueExecutor (task_type: approval_queue)
└── ExecutiveBriefingExecutor (task_type: executive_briefing)
```

---

### ComplianceGate™ Agent (Cycle 6)

**Purpose:** Regulatory and risk compliance

**Capabilities:**
- SEO audits (technical, on-page, AI search)
- Schema markup implementation
- ASO compliance (App Store, Google Play)
- Churn prevention flows
- Policy enforcement

**Executors to Create:**
```
services/orchestration/app/tasks/compliance_gate.py
├── SeoAuditExecutor (task_type: seo_audit)
├── SchemaMarkupExecutor (task_type: schema_markup)
├── PolicyEnforcementExecutor (task_type: policy_enforcement)
└── ChurnPreventionExecutor (task_type: churn_prevention)
```

---

### BudgetMind™ Agent (Cycle 7)

**Purpose:** Financial planning and monitoring

**Capabilities:**
- Budget vs actual tracking
- Unit economics calculation (CAC, LTV, payback)
- Vendor consolidation
- Cash flow projection

**Executors to Create:**
```
services/orchestration/app/tasks/budget_mind.py
├── BudgetMonitoringExecutor (task_type: budget_monitoring)
├── UnitEconomicsExecutor (task_type: unit_economics)
├── VendorConsolidationExecutor (task_type: vendor_consolidation)
└── CashFlowProjectionExecutor (task_type: cash_flow_projection)
```

---

### BoardReady™ Agent (Cycle 8)

**Purpose:** Investor relations and board prep

**Capabilities:**
- Quarterly board deck generation
- Living data room maintenance
- Investor update drafting
- Due diligence response

**Executors to Create:**
```
services/orchestration/app/tasks/board_ready.py
├── BoardDeckGeneratorExecutor (task_type: board_deck_generation)
├── DataRoomMaintenanceExecutor (task_type: data_room_maintenance)
├── InvestorUpdateExecutor (task_type: investor_update)
└── DueDiligenceResponseExecutor (task_type: due_diligence_response)
```

---

## Next Steps (Cycle 2: FulfillmentOps)

### Task List

- [ ] Create `services/orchestration/app/tasks/fulfillment_ops.py`
  - [ ] `PageOptimizationExecutor` - Optimize pages for conversions
  - [ ] `ABTestSetupExecutor` - Design and configure experiments
  - [ ] `AnalyticsTrackingExecutor` - Set up event tracking

- [ ] Register executors in `services/orchestration/app/tasks/__init__.py`

- [ ] Add workflows to `services/orchestration/app/flows/registry.py`
  - [ ] `page_cro_optimization`
  - [ ] `ab_test_lifecycle`
  - [ ] `analytics_tracking_setup`

- [ ] Add endpoints to `services/media-commerce/app/main.py`
  - [ ] `POST /api/v1/cro/optimize-page/workflow`
  - [ ] `POST /api/v1/cro/ab-test/workflow`

- [ ] Create tests
  - [ ] `services/orchestration/tests/test_fulfillment_ops_executor.py`
  - [ ] `services/media-commerce/tests/test_cro_workflow_submission.py`

- [ ] Run verification
  - [ ] `pytest services/orchestration/tests/ services/media-commerce/tests/ -v`
  - [ ] Target: 40+ passing tests

- [ ] Update graph
  - [ ] `graphify update .`

- [ ] Write Cycle 2 compounding memory

### Estimated Timeline

| Task | Time |
|------|------|
| Executor implementation | 45 min |
| Workflow registration | 15 min |
| Endpoint addition | 15 min |
| Test writing | 30 min |
| Verification + graph | 15 min |
| **Total** | **~2 hours** |

---

## Architecture Principles (Carry Forward)

From Cycle 1 compounding memory:

1. **Executor Bridge Pattern** - Orchestration → Agent via TaskExecutor
2. **Deterministic-First Logic** - Pattern matching before model inference
3. **Test Structure** - `asyncio.run()` not pytest-asyncio
4. **Dual Endpoint Strategy** - Direct agent + workflow submission
5. **Horizontal-First** - Vertical consumes, doesn't reimplement

---

## Success Metrics

### Cycle 1 (Baseline)
- 2 hours implementation
- 10 tests written
- 2 executors created
- 29 tests passing total

### Cycle 2 (Target)
- 2 hours implementation
- 10 tests written
- 3 executors created
- 40+ tests passing total

### End of 8 Cycles (Goal)
- ~16 hours total implementation
- ~80 tests written
- ~25 executors created
- 100+ tests passing total
- All 8 agents production-ready

---

## Dependencies

### External
- None (all services run locally via docker-compose)

### Internal
- Horizontal orchestration service (✅ Complete)
- 13-entity data model (✅ Complete)
- Gateway inference routing (✅ Complete)
- Memory service (✅ Complete)
- Semantic cache (✅ Complete)
- Billing service (✅ Complete)
- Arkham security (✅ Complete)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Scope creep | One workflow slice per cycle |
| Test failures | Test-first, run after each change |
| Horizontal leakage | Review against compounding memory anti-patterns |
| Context bloat | Handoffs ≤15 lines, read one file at a time |

---

## References

- Cycle 1 Compounding Memory: `.qwen/projects/-Users-joeiton-Desktop-FullStackArkham/memory/cycle1_compounding_memory.md`
- Agent Skills: `.agents/skills/*/SKILL.md`
- Build Team: `.agents/teams/media-commerce-build/TEAM.md`
- Build Summary: `.agents/MEDIA_COMMERCE_BUILD_SUMMARY.md`
