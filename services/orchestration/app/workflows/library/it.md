# AI Workflows: IT

## 1. New Employee Hardware Provisioning
- **Trigger**: HR system marks a candidate as "Hired".
- **AI Agents Involved**: SupplyChainAgent, BudgetMind.
- **Expected Output**: MacBook order placed and shipping tracking ID.

## 2. Password Reset Desk Bot
- **Trigger**: Ticket received with keyword "locked account".
- **AI Agents Involved**: SecurityAgent, ContentEngine.
- **Expected Output**: Verified identity check and automated unlock.

## 3. Wi-Fi Connectivity Optimizer
- **Trigger**: Access point signal drops below -70dBm for 10% of users.
- **AI Agents Involved**: SecurityAgent, ChiefPulse.
- **Expected Output**: Mesh network adjustment command or technician alert.

## 4. SaaS License Spend Audit
- **Trigger**: Monthly credit card statement processing.
- **AI Agents Involved**: BudgetMind, ComplianceGate.
- **Expected Output**: List of unused licenses and "Cancel" recommendations.

## 5. Automated Server Patching
- **Trigger**: Maintenance window (Sunday 2 AM).
- **AI Agents Involved**: SecurityAgent, ComplianceGate.
- **Expected Output**: Fleet status report and rollback logs if failed.

## 6. IT Helpdesk Sentiment Analysis
- **Trigger**: Feedback submitted on a closed ticket.
- **AI Agents Involved**: ContentEngine, ChiefPulse.
- **Expected Output**: CSAT (Customer Satisfaction) dashboard update.

## 7. Network Intrusion Prevention
- **Trigger**: Port scan detected from internal workstation.
- **AI Agents Involved**: SecurityAgent, ComplianceGate.
- **Expected Output**: Port disabled and security team paged.

## 8. Legacy Hardware Trade-In Loop
- **Trigger**: Device hits 36 months of age in inventory.
- **AI Agents Involved**: BudgetMind, SupplyChainAgent.
- **Expected Output**: Valuation for trade-in and replacement quote.

## 9. Cloud Storage Over-Usage Alert
- **Trigger**: Google Drive/OneDrive hits 90% capacity.
- **AI Agents Involved**: BudgetMind, ContentEngine.
- **Expected Output**: Cleanup instructions sent to the user.

## 10. Disaster Recovery Drill
- **Trigger**: Quarterly scheduled event.
- **AI Agents Involved**: ChiefPulse, BoardReady.
- **Expected Output**: Success report on backup integrity and RTO/RPO stats.

---

## Template Scripts

```python
# 1. Hardware Provisioning
def provision_laptop(dept):
    model = "M3 Pro" if dept == "Eng" else "M3 Air"
    return {"order": model, "status": "shipped"}

# 2. Password Reset
def reset_pwd(user_id):
    return {"temp_pwd": "REDACTED", "status": "identity_verified"}

# 3. Wi-Fi Optimizer
def adjust_ap(dbm):
    if dbm < -70:
        return {"action": "increase_power", "gain": "3db"}

# 4. SaaS Audit
def audit_saas(users, seats):
    unused = seats - users
    return {"waste_usd": unused * 20, "action": "downgrade"}

# 5. Server Patching
def apply_patches(host):
    return {"host": host, "status": "patched", "reboot": True}

# 6. Helpdesk Sentiment
def score_ticket(comment):
    return {"sentiment": 0.9, "category": "positive"}

# 7. Intrusion Prevention
def block_port(port, mac):
    return {"action": "disable", "port": port, "target": mac}

# 8. Hardware Lifecycle
def check_age(months):
    if months >= 36:
        return {"action": "replace", "budget": 1500}

# 9. Storage Alert
def notify_storage(usage_pct):
    if usage_pct > 90:
        return {"msg": "Please delete large files"}

# 10. DR Drill
def run_dr_drill():
    return {"backups": "verified", "rto_seconds": 300}
```
