# AI Workflows: FinTech / FinServ

## 1. Credit Score Anomaly Detection
- **Trigger**: Sudden 50-point drop in a user's credit score.
- **AI Agents Involved**: SecurityAgent, BudgetMind.
- **Expected Output**: Fraud investigation and user alert.

## 2. AML Transaction Monitoring
- **Trigger**: Wire transfer >$10k to a high-risk jurisdiction.
- **AI Agents Involved**: ComplianceGate, SecurityAgent.
- **Expected Output**: SAR (Suspicious Activity Report) draft and transaction hold.

## 3. Automated Loan Underwriting
- **Trigger**: New mortgage application submitted.
- **AI Agents Involved**: BudgetMind, BoardReady.
- **Expected Output**: Risk rating and recommended interest rate.

## 4. Market Volatility Trading Halt
- **Trigger**: S&P 500 index drops 7% in 10 minutes.
- **AI Agents Involved**: MarketPulse, ChiefPulse.
- **Expected Output**: Portfolio sell-offs paused and hedge execution.

## 5. Customer Onboarding (KYC)
- **Trigger**: User uploads a photo of their ID.
- **AI Agents Involved**: ComplianceGate, SecurityAgent.
- **Expected Output**: Verified identity and account activation.

## 6. Expense Management Categorization
- **Trigger**: Transaction posted to corporate card.
- **AI Agents Involved**: BudgetMind, ContentEngine.
- **Expected Output**: Auto-mapping to "Travel", "Meals", or "Software".

## 7. Wealth Management Portfolio Rebalance
- **Trigger**: Deviation of >5% from the user's risk profile.
- **AI Agents Involved**: BudgetMind, MarketPulse.
- **Expected Output**: Trade execution for ETFs and bonds.

## 8. Insurance Claim Estimation
- **Trigger**: Photo of car damage uploaded via app.
- **AI Agents Involved**: DiagnosticAgent, BudgetMind.
- **Expected Output**: Cost estimate and local repair shop referral.

## 9. Regulatory Reporting (RegTech)
- **Trigger**: End of fiscal quarter.
- **AI Agents Involved**: ComplianceGate, BoardReady.
- **Expected Output**: Completed 10-Q filing draft.

## 10. Micro-Lending Default Prediction
- **Trigger**: User misses a $50 payment by 24 hours.
- **AI Agents Involved**: DealFlow, BudgetMind.
- **Expected Output**: Grace period extension or collections trigger.

---

## Template Scripts

```python
# 1. Credit Anomaly
def check_credit(prev, current):
    if prev - current > 50:
        return {"risk": "fraud", "action": "freeze_card"}

# 2. AML Monitor
def monitor_wire(amount, country):
    if amount > 10000 and country == "HighRisk":
        return {"status": "held", "report": "SAR_REQUIRED"}

# 3. Loan Underwriting
def underwrite_loan(dti, score):
    if dti < 0.4 and score > 700:
        return {"approve": True, "rate": 0.065}

# 4. Volatility Halt
def check_market(drop_pct):
    if drop_pct > 0.07:
        return {"action": "halt_trading", "msg": "Circuit breaker hit"}

# 5. KYC Verify
def verify_id(id_image_url):
    return {"verified": True, "expiry": "2030-01-01"}

# 6. Expense Categorization
def categorize_exp(merchant):
    if "AWS" in merchant: return "Software"
    if "Delta" in merchant: return "Travel"

# 7. Portfolio Rebalance
def balance_wealth(stock_pct, target):
    if stock_pct > target + 5:
        return {"action": "sell_stocks", "amount": stock_pct - target}

# 8. Insurance Claim
def estimate_damage(img):
    return {"est_cost": 2500, "part": "bumper"}

# 9. RegTech Reporting
def prepare_filing(quarter):
    return {"filing": f"10-Q-{quarter}", "status": "draft"}

# 10. Default Prediction
def predict_default(days_late):
    if days_late > 3:
        return {"action": "call_user", "priority": "high"}
```
