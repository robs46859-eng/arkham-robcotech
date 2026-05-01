# AI Workflows: Durables

## 1. Warehouse Inventory Reorder
- **Trigger**: Pallet of washing machines exits the loading dock.
- **AI Agents Involved**: SupplyChainAgent, BudgetMind.
- **Expected Output**: Purchase order to the manufacturing plant.

## 2. Product Warranty Verification
- **Trigger**: Customer submits a repair request with a serial number.
- **AI Agents Involved**: ComplianceGate, ContentEngine.
- **Expected Output**: Warranty status (Active/Expired) and service center list.

## 3. Manufacturing Yield Analysis
- **Trigger**: 1,000th unit of a refrigerator line completed.
- **AI Agents Involved**: DiagnosticAgent, BudgetMind.
- **Expected Output**: Defect rate report and assembly line optimization.

## 4. Retailer Promotion Sync
- **Trigger**: Home Depot/Lowe's announces a holiday sale.
- **AI Agents Involved**: MediaCommerce, MarketPulse.
- **Expected Output**: Automated price match or co-op marketing spend.

## 5. Freight Logistics Optimizer
- **Trigger**: Container ship docking at Port of LA.
- **AI Agents Involved**: SupplyChainAgent, ChiefPulse.
- **Expected Output**: Trucking route assignments for last-mile delivery.

## 6. Spare Parts Demand Prediction
- **Trigger**: Historical failure data update for 5-year-old dishwashers.
- **AI Agents Involved**: MarketPulse, BudgetMind.
- **Expected Output**: Stocking levels for regional repair hubs.

## 7. Product Recalibration Loop
- **Trigger**: Smart oven reports temperature variance of >2 degrees.
- **AI Agents Involved**: DiagnosticAgent, SecurityAgent.
- **Expected Output**: OTA (Over-the-Air) firmware update to fix sensor bias.

## 8. Sustainability Lifecycle Tracker
- **Trigger**: Product returned for recycling.
- **AI Agents Involved**: ComplianceGate, SupplyChainAgent.
- **Expected Output**: Environmental impact credit and raw material recovery report.

## 9. B2B Channel Revenue Pulse
- **Trigger**: Weekly sales report from major appliance distributors.
- **AI Agents Involved**: ChiefPulse, BoardReady.
- **Expected Output**: Revenue dashboard update for the board.

## 10. Design-to-Manufacturing Feedback
- **Trigger**: Recurring defect found in "Handle Design".
- **AI Agents Involved**: DiagnosticAgent, ContentEngine.
- **Expected Output**: Engineering change request (ECR) for the R&D team.

---

## Template Scripts

```python
# 1. Inventory Reorder
def reorder_units(stock):
    if stock < 100:
        return {"action": "order", "qty": 500}

# 2. Warranty Check
def check_warranty(sn):
    return {"sn": sn, "status": "active", "expires": "2027"}

# 3. Yield Analysis
def analyze_yield(defects):
    rate = defects / 1000
    return {"defect_rate": rate, "status": "pass" if rate < 0.02 else "fail"}

# 4. Promotion Sync
def sync_promo(retailer_price):
    return {"match_price": retailer_price * 0.95}

# 5. Logistics Optimization
def optimize_route(shipment_id):
    return {"route": "I-10 East", "eta": "2 days"}

# 6. Spare Parts
def predict_parts(model_year):
    if model_year < 2020:
        return {"stock_increase": "20%", "part": "pump_motor"}

# 7. Recalibration
def recalibrate_iot(temp_error):
    if abs(temp_error) > 2:
        return {"action": "ota_patch", "value": -1.5}

# 8. Sustainability
def track_recycling(weight_kg):
    return {"carbon_offset": weight_kg * 1.2}

# 9. Channel Revenue
def pulse_revenue(dist_sales):
    return {"weekly_total": sum(dist_sales), "growth": "3%"}

# 10. Design Feedback
def engineering_feedback(fail_reason):
    return {"ecr": "handle_reinforcement", "reason": fail_reason}
```
