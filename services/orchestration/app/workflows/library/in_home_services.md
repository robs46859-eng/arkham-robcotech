# AI Workflows: In-home Service Professionals

## 1. Dynamic Appointment Dispatch
- **Trigger**: HVAC technician finishes a job 30 minutes early.
- **AI Agents Involved**: DealFlow, ChiefPulse.
- **Expected Output**: Re-routed next appointment and SMS to the homeowner.

## 2. Visual Estimate Generator
- **Trigger**: Plumber uploads a video of a leaking pipe.
- **AI Agents Involved**: DiagnosticAgent, BudgetMind.
- **Expected Output**: Itemized parts list and labor cost estimate.

## 3. Technician Safety Monitor
- **Trigger**: No GPS movement or "Check-in" for 4 hours at a job site.
- **AI Agents Involved**: SecurityAgent, ChiefPulse.
- **Expected Output**: Phone call to technician and emergency contact alert.

## 4. Upsell Opportunity Detection
- **Trigger**: Photo of an 11-year-old furnace uploaded for "Repair".
- **AI Agents Involved**: DealFlow, MediaCommerce.
- **Expected Output**: Prompt for the tech to offer a replacement quote.

## 5. Review Generation Loop
- **Trigger**: Invoice marked as "Paid" in the field app.
- **AI Agents Involved**: ContentEngine, MediaCommerce.
- **Expected Output**: Personalized text request for a Google/Yelp review.

## 6. Spare Parts Inventory Sync
- **Trigger**: Part "Capacitor-A1" used in a repair.
- **AI Agents Involved**: SupplyChainAgent, BudgetMind.
- **Expected Output**: Inventory deduction and reorder if truck stock is low.

## 7. No-Show Predictor
- **Trigger**: 2 hours before appointment time.
- **AI Agents Involved**: DealFlow, ContentEngine.
- **Expected Output**: Automated confirmation text; escalation if no reply.

## 8. Fleet Fuel Efficiency Analysis
- **Trigger**: Weekly fuel card statement upload.
- **AI Agents Involved**: BudgetMind, ChiefPulse.
- **Expected Output**: Report on idle-time waste and route optimization.

## 9. Compliance / License Expiry Tracker
- **Trigger**: 60 days before an Electrician's state license expires.
- **AI Agents Involved**: ComplianceGate, ChiefPulse.
- **Expected Output**: Automated enrollment in CE (Continuing Education) courses.

## 10. Customer Support Chat-to-Dispatch
- **Trigger**: Homeowner chats "My AC is making a loud banging noise".
- **AI Agents Involved**: DiagnosticAgent, DealFlow.
- **Expected Output**: Issue diagnosis and "Book Now" link for the next available slot.

---

## Template Scripts

```python
# 1. Dispatch
def dispatch_next(tech_id, current_location):
    return {"next_job": "JOB-99", "eta": "15 min"}

# 2. Visual Estimate
def estimate_plumbing(video_url):
    return {"parts": ["pvc_pipe", "sealant"], "total": 150.00}

# 3. Safety Monitor
def safety_check(last_ping_time):
    if last_ping_time > 14400:
        return {"status": "alarm", "action": "contact_supervisor"}

# 4. Upsell
def find_upsell(appliance_age):
    if appliance_age > 10:
        return {"offer": "replacement_discount_15%"}

# 5. Review Loop
def request_review(customer_name):
    return {"msg": f"Hi {customer_name}, how did we do today?"}

# 6. Inventory Sync
def sync_inventory(part_id):
    return {"action": "deduct", "id": part_id, "reorder": True}

# 7. No-Show Predict
def check_confirmation(replied):
    if not replied:
        return {"action": "call_customer", "priority": "medium"}

# 8. Fuel Efficiency
def analyze_fuel(miles, gal):
    return {"mpg": miles / gal, "status": "normal"}

# 9. License Tracker
def track_license(days_left):
    if days_late < 60:
        return {"action": "notify_tech", "link": "renew_now.gov"}

# 10. Chat-to-Dispatch
def handle_support_chat(msg):
    if "noise" in msg:
        return {"diagnosis": "fan_blade_issue", "book": "Schedule Repair"}
```
