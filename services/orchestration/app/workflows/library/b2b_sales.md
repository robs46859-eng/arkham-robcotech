# AI Workflows: B2B Sales

## 1. Intent-Based Lead Scoring
- **Trigger**: Prospect visits pricing page 3 times in 24 hours.
- **AI Agents Involved**: DealFlow, ChiefPulse.
- **Expected Output**: Lead score update and Slack notification to AE.

## 2. Automated Sales Deck Customization
- **Trigger**: New discovery call notes uploaded to CRM.
- **AI Agents Involved**: BoardReady, ContentEngine.
- **Expected Output**: A personalized 10-slide PDF tailored to the prospect's pain points.

## 3. Churn Risk Warning System
- **Trigger**: Logins from a key account drop by 50% week-over-week.
- **AI Agents Involved**: DealFlow, BudgetMind.
- **Expected Output**: Retention strategy and automated "Check-in" email draft.

## 4. Competitive Intelligence Alerts
- **Trigger**: Competitor announces a new feature or price change.
- **AI Agents Involved**: MarketPulse, ContentEngine.
- **Expected Output**: Battlecard update for the sales team.

## 5. Contract Redline Assistant
- **Trigger**: Legal document received from prospect.
- **AI Agents Involved**: ComplianceGate, DealFlow.
- **Expected Output**: Summary of non-standard clauses and risk assessment.

## 6. Outreach Personalization Loop
- **Trigger**: New LinkedIn post from a target account CEO.
- **AI Agents Involved**: ContentEngine, DealFlow.
- **Expected Output**: Personalized introductory sentence for a cold email.

## 7. Sales Forecast Accuracy Check
- **Trigger**: Sales leader updates the quarterly forecast.
- **AI Agents Involved**: BudgetMind, ChiefPulse.
- **Expected Output**: Probability analysis and "at-risk" deal identification.

## 8. Multi-Threaded Stakeholder Mapping
- **Trigger**: Single contact from a Fortune 500 company signs up.
- **AI Agents Involved**: DealFlow, MarketPulse.
- **Expected Output**: Map of other relevant stakeholders (CFO, CTO, VPs).

## 9. Post-Call Action Item Extraction
- **Trigger**: Zoom/Gong transcript available after a demo.
- **AI Agents Involved**: ChiefPulse, ContentEngine.
- **Expected Output**: List of action items synced to CRM and follow-up email draft.

## 10. Partner Ecosystem Matching
- **Trigger**: New lead with a specific tech stack (e.g., Salesforce + AWS).
- **AI Agents Involved**: DealFlow, ComplianceGate.
- **Expected Output**: Recommendation for which partner to co-sell with.

---

## Template Scripts

```python
# 1. Lead Scoring
def score_lead(page_views, time_spent):
    score = (page_views * 10) + (time_spent / 60)
    return {"score": score, "hot": score > 50}

# 2. Deck Customization
def customize_deck(pain_points):
    slides = [{"title": "Solving " + p} for p in pain_points]
    return {"slides": slides}

# 3. Churn Warning
def detect_churn_risk(usage_drop):
    if usage_drop > 0.4:
        return {"risk": "high", "action": "trigger_cs_call"}

# 4. Competitive Intel
def update_battlecard(competitor_news):
    return {"key_rebuttal": "Our API is 2x faster than their new release"}

# 5. Contract Redlines
def summarize_legal(clauses):
    risky = [c for c in clauses if "indemnity" in c.lower()]
    return {"warnings": risky}

# 6. Personalization
def personalize_intro(post_text):
    return {"intro": f"Loved your thoughts on {post_text[:20]}..."}

# 7. Forecast Check
def validate_forecast(deals):
    at_risk = [d for d in deals if d['prob'] < 0.3 and d['value'] > 10000]
    return {"at_risk_count": len(at_risk)}

# 8. Stakeholder Mapping
def map_stakeholders(domain):
    return {"targets": ["cto@" + domain, "vp_sales@" + domain]}

# 9. Action Extraction
def extract_actions(transcript):
    return {"tasks": ["Send NDA", "Schedule tech deep-dive"]}

# 10. Partner Matching
def match_partners(stack):
    if "aws" in stack:
        return {"partner": "CloudConsultants Inc"}
```
