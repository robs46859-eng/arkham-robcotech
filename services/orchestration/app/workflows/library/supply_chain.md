# AI Workflows: Supply Chain

## 1. Global Port Congestion Re-Route
- **Trigger**: Wait times at Port of Long Beach exceed 5 days.
- **AI Agents Involved**: SupplyChainAgent, MarketPulse.
- **Expected Output**: Shipments diverted to Port of Oakland or Ensenada.

## 2. Supplier Risk Scoring
- **Trigger**: Political instability or labor strike in a supplier's region.
- **AI Agents Involved**: ComplianceGate, ChiefPulse.
- **Expected Output**: Immediate risk rating update and secondary source activation.

## 3. Cold-Chain Temperature Breach
- **Trigger**: IoT sensor reports >4°C in a vaccine shipment.
- **AI Agents Involved**: SecurityAgent, SupplyChainAgent.
- **Expected Output**: Shipment marked as "Spoiled" and replacement order triggered.

## 4. Automated Customs Documentation
- **Trigger**: Cargo manifest finalized at departure.
- **AI Agents Involved**: ComplianceGate, ContentEngine.
- **Expected Output**: Completed Bill of Lading, Commercial Invoice, and Packing List.

## 5. Inventory Stock-Out Predictor
- **Trigger**: Demand spike for "Product X" on TikTok/Social Media.
- **AI Agents Involved**: MediaCommerce, BudgetMind.
- **Expected Output**: Safety stock increase and air-freight expedited order.

## 6. ESG (Sustainability) Audit
- **Trigger**: Quarterly reporting deadline.
- **AI Agents Involved**: ComplianceGate, BoardReady.
- **Expected Output**: Carbon footprint report across the entire tier-1/2 supplier base.

## 7. Warehouse Labor Demand Forecast
- **Trigger**: Projection of 2x order volume for "Black Friday".
- **AI Agents Involved**: BudgetMind, ChiefPulse.
- **Expected Output**: Staffing plan and temporary agency outreach.

## 8. Freight Spend Anomaly Detection
- **Trigger**: Logistics invoice $500 higher than the quoted spot rate.
- **AI Agents Involved**: BudgetMind, ComplianceGate.
- **Expected Output**: Automated dispute filed with the carrier.

## 9. Last-Mile Delivery Optimization
- **Trigger**: Morning traffic and weather data.
- **AI Agents Involved**: SupplyChainAgent, ChiefPulse.
- **Expected Output**: Dynamically updated route plans for 200 delivery vans.

## 10. Supplier Contract Renewal Loop
- **Trigger**: 90 days before contract expiration.
- **AI Agents Involved**: ComplianceGate, BudgetMind.
- **Expected Output**: Performance scorecard and negotiation talking points.

---

## Template Scripts

```python
# 1. Port Re-Route
def reroute_shipment(wait_days):
    if wait_days > 5:
        return {"new_port": "Oakland", "est_delay": "2 days"}

# 2. Supplier Risk
def score_supplier(news_event):
    if "strike" in news_event:
        return {"risk": 9, "action": "find_alternate"}

# 3. Temperature Breach
def monitor_temp(temp):
    if temp > 4:
        return {"status": "discard", "action": "reorder"}

# 4. Customs Docs
def generate_customs_docs(order_data):
    return {"docs": ["invoice.pdf", "packing_list.pdf"], "status": "filed"}

# 5. Stock-Out Predict
def predict_stock(trend_pct):
    if trend_pct > 0.5:
        return {"action": "increase_stock", "qty": 1000}

# 6. ESG Audit
def audit_carbon(suppliers):
    return {"total_co2": sum(s['emissions'] for s in suppliers)}

# 7. Labor Forecast
def forecast_labor(vol):
    return {"temp_workers_needed": int(vol / 100)}

# 8. Spend Anomaly
def check_invoice(quote, actual):
    if actual > quote * 1.1:
        return {"action": "dispute", "diff": actual - quote}

# 9. Last Mile
def update_route(weather):
    if weather == "snow":
        return {"add_buffer_mins": 30, "chains_required": True}

# 10. Contract Renewal
def prepare_negotiation(score):
    return {"rating": score, "ask": "5% discount based on on-time rate"}
```
