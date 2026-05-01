# AI Workflows: Cyber Security

## 1. Zero-Day Vulnerability Triage
- **Trigger**: New CVE published matching the company's tech stack.
- **AI Agents Involved**: SecurityAgent, ChiefPulse.
- **Expected Output**: Criticality score and patch prioritization report.

## 2. Phishing Campaign Simulation
- **Trigger**: Monthly scheduled training event.
- **AI Agents Involved**: ContentEngine, SecurityAgent.
- **Expected Output**: Personalized phishing emails and click-rate analytics.

## 3. SIEM Log Anomaly Detection
- **Trigger**: Spikes in outbound traffic to unknown IP ranges.
- **AI Agents Involved**: SecurityAgent, ComplianceGate.
- **Expected Output**: Incident report and firewall rule suggestion.

## 4. Automated Incident Response (SOAR)
- **Trigger**: Verified malware detection on an endpoint.
- **AI Agents Involved**: SecurityAgent, ComplianceGate.
- **Expected Output**: Endpoint isolation and forensic snapshot.

## 5. Security Policy Compliance Audit
- **Trigger**: New AWS/Azure resource created without tags.
- **AI Agents Involved**: ComplianceGate, BudgetMind.
- **Expected Output**: Auto-remediation (tagging) or resource deletion.

## 6. Dark Web Credential Monitoring
- **Trigger**: Data breach dump found on monitored forums.
- **AI Agents Involved**: SecurityAgent, MarketPulse.
- **Expected Output**: List of compromised employee emails and forced password resets.

## 7. Cloud Security Posture Management (CSPM)
- **Trigger**: S3 bucket set to "Public" permission.
- **AI Agents Involved**: ComplianceGate, SecurityAgent.
- **Expected Output**: Instant bucket lockdown and admin alert.

## 8. Third-Party Risk Assessment
- **Trigger**: Onboarding a new software vendor.
- **AI Agents Involved**: ComplianceGate, BoardReady.
- **Expected Output**: Risk score based on the vendor's SOC2 report.

## 9. Identity & Access Management (IAM) Cleanup
- **Trigger**: Employee termination in HR system.
- **AI Agents Involved**: SecurityAgent, ComplianceGate.
- **Expected Output**: Full account deprovisioning across 20+ SaaS apps.

## 10. Penetration Testing Report Synthesis
- **Trigger**: Completion of a manual or automated pentest.
- **AI Agents Involved**: ContentEngine, SecurityAgent.
- **Expected Output**: Executive summary and remediated code snippets for devs.

---

## Template Scripts

```python
# 1. CVE Triage
def triage_cve(cve_id, software_list):
    if any(s in cve_id for s in software_list):
        return {"priority": "critical", "action": "patch_immediately"}

# 2. Phishing Sim
def create_phish(employee_role):
    return {"subject": f"Urgent: {employee_role} Review Required"}

# 3. Log Anomaly
def detect_anomaly(traffic_mb):
    if traffic_mb > 5000:
        return {"threat_level": "high", "action": "block_ip"}

# 4. Incident Response
def isolate_host(hostname):
    return {"action": "quarantine", "host": hostname}

# 5. Policy Audit
def check_tags(tags):
    if not tags:
        return {"action": "delete_resource", "reason": "untagged"}

# 6. Dark Web Monitor
def check_leaks(email):
    return {"leaked": True, "source": "Collection #1", "action": "reset_pwd"}

# 7. CSPM Lockdown
def secure_bucket(policy):
    if "Public" in policy:
        return {"action": "set_private", "status": "remediated"}

# 8. Third Party Risk
def assess_vendor(soc2_status):
    return {"score": 90 if soc2_status == "clean" else 40}

# 9. IAM Provisioning
def deprovision_user(user_id):
    return {"apps": ["slack", "github", "jira"], "status": "disabled"}

# 10. Pentest Synthesis
def summarize_vulns(vuln_list):
    return {"total": len(vuln_list), "high": len([v for v in vuln_list if v['level'] == 'high'])}
```
