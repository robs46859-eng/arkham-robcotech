# Integration Test Plan - Media-Commerce Vertical

**Created:** 2026-04-28  
**Status:** Cycles 1-2 Complete, Integration Tests Needed  
**Goal:** Test workflows end-to-end across DealFlow + FulfillmentOps

---

## Integration Test Strategy

### Why Integration Tests Now

- Cycles 1-2 have 46 unit tests (executor + workflow submission)
- Workflows are siloed in tests (each tested independently)
- Real usage will chain workflows (lead → content → optimize → track)
- Need to verify cross-workflow state handoff

### Test Pyramid

```
                    ┌─────────────┐
                   │   E2E (1)   │  Full user journey
                  ├───────────────┤
                 │  Integration (6) │  Workflow chains
                ├───────────────────┤
               │    Unit (46)      │  Executors + endpoints
              └─────────────────────┘
```

---

## Integration Tests to Create

### Test 1: Lead-to-Content Journey
**File:** `services/media-commerce/tests/test_lead_to_content_journey.py`

**Flow:**
```
1. Lead captured (DealFlow)
   ↓ route_lead workflow
2. Lead routed to vertical (e.g., "media")
   ↓ trigger content creation
3. Content strategy generated (ContentEngine)
   ↓ content published
4. Page CRO applied (FulfillmentOps)
   ↓ tracking configured
5. Analytics events logged
```

**Assertions:**
- Lead routed to correct vertical
- Content strategy created for routed vertical
- CRO recommendations match content type
- Tracking events have correct metadata

---

### Test 2: A/B Test Full Lifecycle
**File:** `services/media-commerce/tests/test_ab_test_lifecycle.py`

**Flow:**
```
1. Setup A/B test (2 variants)
   ↓ tracking configured
2. Simulate events (variant A: 100 conversions, variant B: 150)
   ↓ monitor performance
3. Decide winner (variant B, p < 0.05)
   ↓ deploy winner
4. Verify winner deployed
```

**Assertions:**
- Test setup returns valid test_id
- Tracking captures events for both variants
- Winner decision is statistically valid
- Deploy winner updates content_asset

---

### Test 3: Cross-Vertical Lead Routing
**File:** `services/orchestration/tests/test_cross_vertical_routing.py`

**Flow:**
```
1. Submit lead with ecom signals (Shopify, cart, checkout)
   ↓ route_lead workflow
2. Verify routed to "ecom" vertical
3. Submit lead with staffing signals (nurse, credentialing)
   ↓ route_lead workflow
4. Verify routed to "staffing" vertical
5. Submit lead with mixed signals
   ↓ route_lead workflow
6. Verify highest-LTV vertical selected
```

**Assertions:**
- Ecom signals → ecom vertical (confidence > 0.8)
- Staffing signals → staffing vertical (confidence > 0.8)
- Mixed signals → correct LTV-based decision

---

### Test 4: Content Strategy → CRO Chain
**File:** `services/media-commerce/tests/test_content_to_cro_chain.py`

**Flow:**
```
1. Generate content strategy (topic: "affiliate marketing")
   ↓ strategy returned
2. Use strategy output as CRO input
   ↓ page optimization
3. Verify CRO recommendations align with strategy
4. Setup A/B test for recommended variant
   ↓ test configured
5. Verify test tracks strategy KPIs
```

**Assertions:**
- Content strategy includes distribution channels
- CRO recommendations reference strategy goals
- A/B test variants test strategy hypotheses

---

### Test 5: Analytics Tracking Verification
**File:** `services/media-commerce/tests/test_analytics_tracking_e2e.py`

**Flow:**
```
1. Define event schema (signup_completed)
   ↓ tracking code generated
2. Simulate event (POST to tracking endpoint)
   ↓ event stored
3. Query events by tenant_id + event_type
   ↓ events returned
4. Verify event_data matches input
```

**Assertions:**
- Tracking code is valid Python/JavaScript
- Events are queryable by tenant
- Event data is preserved accurately

---

### Test 6: Multi-Workflow Concurrent Execution
**File:** `services/orchestration/tests/test_concurrent_workflows.py`

**Flow:**
```
1. Submit 5 lead routing workflows concurrently
2. Submit 3 CRO workflows concurrently
3. Submit 2 A/B test workflows concurrently
4. Wait for all to complete
5. Verify all workflows completed without conflicts
```

**Assertions:**
- No race conditions in checkpoint store
- No workflow state corruption
- All workflows return correct results

---

## E2E Test to Create

### Test 7: Full Media-Commerce Loop
**File:** `services/media-commerce/tests/test_media_commerce_loop_e2e.py`

**Scenario:** Media company optimizing affiliate content

**Flow:**
```
Day 1: Content Creation
1. Create content strategy (topic: "best running shoes")
2. Generate content (article draft)
3. Publish content

Day 2: Optimization
4. Monitor EPC (simulated: $2.50 - underperforming)
5. Auto-retire content (status: retired)
6. Generate new variant (headline change)

Day 3: A/B Test
7. Setup A/B test (original vs new variant)
8. Simulate 200 clicks per variant
9. Decide winner (new variant, +25% EPC)
10. Deploy winner

Day 7: Analytics Review
11. Query events (clicks, conversions, revenue)
12. Calculate EPC lift ($2.50 → $3.15)
13. Generate executive briefing
```

**Assertions:**
- Content lifecycle completes (create → optimize → test → deploy)
- EPC improves after optimization
- Executive briefing includes accurate metrics

---

## Test Infrastructure Needed

### Mock Services

```python
# tests/integration/conftest.py

@pytest.fixture
async def integration_client():
    """FastAPI test client with real orchestration"""
    # Start orchestration service
    # Start media-commerce service
    # Use real PostgreSQL (test database)
    # Use real Redis (test instance)
    yield test_client
    # Cleanup test data

@pytest.fixture
def workflow_poller():
    """Poll workflow status until completion"""
    async def poll(workflow_id, max_attempts=20):
        for i in range(max_attempts):
            status = await get_workflow_status(workflow_id)
            if status == "completed":
                return True
            await asyncio.sleep(0.5)
        return False
    return poll
```

### Test Data Factories

```python
# tests/integration/factories.py

def create_lead(vertical: str, signals: list) -> dict:
    return {
        "tenant_id": "test-tenant",
        "lead_id": f"lead-{uuid4()}",
        "intent_signals": signals,
    }

def create_page_cro_request(page_type: str) -> dict:
    return {
        "tenant_id": "test-tenant",
        "page_id": f"page-{uuid4()}",
        "page_type": page_type,
    }
```

---

## Test Execution Order

### Phase 1: Single Workflow (Existing)
- ✅ Unit tests for executors (46 tests)
- ✅ Workflow submission tests (5 tests)

### Phase 2: Workflow Chains (New - Priority 1)
- [ ] Test 1: Lead-to-Content Journey
- [ ] Test 3: Cross-Vertical Lead Routing
- [ ] Test 4: Content Strategy → CRO Chain

### Phase 3: Full Lifecycle (New - Priority 2)
- [ ] Test 2: A/B Test Full Lifecycle
- [ ] Test 5: Analytics Tracking Verification

### Phase 4: Stress Testing (New - Priority 3)
- [ ] Test 6: Multi-Workflow Concurrent Execution
- [ ] Test 7: Full Media-Commerce Loop (E2E)

---

## Success Criteria

| Phase | Tests | Pass Threshold |
|-------|-------|----------------|
| Phase 1 (Unit) | 51 | 100% (51/51) |
| Phase 2 (Chains) | 3 | 100% (3/3) |
| Phase 3 (Lifecycle) | 2 | 100% (2/2) |
| Phase 4 (Stress) | 2 | 100% (2/2) |
| **Total** | **58** | **100% (58/58)** |

---

## Next Steps

### Before Cycle 3 (MediaCommerce)
1. Create `tests/integration/conftest.py` (test infrastructure)
2. Create Phase 2 tests (workflow chains)
3. Run all tests, verify 100% pass

### During Cycle 3
1. Add MediaCommerce executors
2. Add MediaCommerce workflows
3. Add integration tests for EPC monitoring loop

### After Cycle 3
1. Run full test suite (target: 70+ tests)
2. Verify E2E media-commerce loop works

---

## Files to Create

```
services/media-commerce/tests/
├── integration/
│   ├── conftest.py           # Test fixtures
│   ├── factories.py          # Test data factories
│   ├── test_lead_to_content_journey.py
│   ├── test_content_to_cro_chain.py
│   └── test_ab_test_lifecycle.py
services/orchestration/tests/
├── integration/
│   ├── conftest.py
│   ├── test_cross_vertical_routing.py
│   ├── test_analytics_tracking_e2e.py
│   ├── test_concurrent_workflows.py
│   └── test_media_commerce_loop_e2e.py
```

---

## Timeline

| Task | Time |
|------|------|
| Test infrastructure (conftest, factories) | 30 min |
| Phase 2 tests (3 tests) | 45 min |
| Phase 3 tests (2 tests) | 30 min |
| Phase 4 tests (2 tests) | 30 min |
| **Total** | **~2.5 hours** |

---

## References

- Cycle 1 Compounding Memory: `.qwen/projects/.../memory/cycle1_compounding_memory.md`
- Cycle 2 Compounding Memory: `.qwen/projects/.../memory/cycle2_compounding_memory.md`
- Build Plan: `.agents/MEDIA_COMMERCE_BUILD_PLAN.md`
