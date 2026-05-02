import { NextResponse } from 'next/server'

export async function GET() {
  const activeVertical = process.env.NEXT_PUBLIC_VERTICAL || 'logistics'

  if (activeVertical === 'logistics') {
    return NextResponse.json({
      tenant: {
        id: "workspace-logistics-01",
        workspaceName: "RobCoTech Logistics",
        vertical: "logistics",
        primaryDomain: "robcotech-logistics.pro",
        investorRoutingInbox: "compliance@robcotech.pro",
        notificationEmail: "ops@robcotech.pro",
      },
      user: {
        name: "Supply Chain Lead",
        email: "ops@robcotech.pro",
        role: "admin",
        createdAt: new Date().toISOString(),
      },
      verticalDefinition: {
        label: "Global Freight Operations",
      },
      bundleDefinition: {
        label: "Enterprise Supply Chain Tier",
      },
      dashboard: {
        boardDate: "Monthly Audit: 12th",
        investorReadiness: 98,
        revenueCoverage: "$42.4M Vol",
        mrrLabel: "30D Volume",
        churnWatch: "Nominal",
        activeTargets: 2,
        diligenceItems: 4,
        verticalFocus: "Supply & Compliance",
        metrics: [
          { label: "On-Time Rate", value: "94.2%", detail: "Trailing 30 Days" },
          { label: "API Gateway Latency", value: "42ms", detail: "Maersk & FedEx Sync" },
          { label: "Active Anomalies", value: "3", detail: "Pending manual review" }
        ],
        approvals: [
          { title: "Customs Clearances", owner: "Risk Team", due: "Today" },
          { title: "Freight Audit", owner: "Finance", due: "Tomorrow" }
        ],
        alerts: [
          { title: "Port Congestion flag", level: "Critical", detail: "LAX Port delays extending." }
        ],
        investorTargets: [
          { name: "Global Carrier API", fit: "Active", reason: "Running every 5 minutes" },
          { name: "Customs Ledger", fit: "Active", reason: "Real-time ledger updates" }
        ],
      },
      projects: [
        {
          id: "proj-1",
          name: "Q3 Customs Audit Prep",
          operatingLane: "Compliance",
          source: "Internal",
          sourceType: "Audit",
          records: "84 controls",
          stage: "Evidence Gathering",
          owner: "Compliance",
          status: "On Track",
          updatedAt: new Date().toISOString(),
        },
        {
          id: "proj-2",
          name: "Cross-border Ocean Freight",
          operatingLane: "Logistics",
          source: "Carrier API",
          sourceType: "Integration",
          records: "$2.1M routed",
          stage: "Live",
          owner: "Engineering",
          status: "Active",
          updatedAt: new Date().toISOString(),
        }
      ],
      integrations: [
        {
          id: "int-1",
          operatingLane: "Reconciliation",
          provider: "Maersk API",
          status: "Active",
          type: "Ocean Gateway",
          detail: "Live Sync",
          accountLabel: "Main Processing",
        },
        {
          id: "int-2",
          operatingLane: "Risk",
          provider: "FedEx API",
          status: "Active",
          type: "Air/Ground Prevention",
          detail: "Live Scoring",
          accountLabel: "Anomaly Detection",
        }
      ],
      workflows: [
        {
          id: "wf-1",
          name: "Auto-Reconciliation Engine",
          effectiveness: 99,
          outcome: "Matched 142k Tx"
        },
        {
          id: "wf-2",
          name: "Customs Automated Check",
          effectiveness: 100,
          outcome: "Cleared 450 accounts"
        }
      ],
      workflowTemplates: [],
      users: [],
      permissions: ["workflow:write", "project:read", "billing:admin"],
    });
  }

  // Default / Fintech
  return NextResponse.json({
    tenant: {
      id: "workspace-fintech-01",
      workspaceName: "RobCoTech Financial",
      vertical: "fintech",
      primaryDomain: "robcotech.pro",
      investorRoutingInbox: "compliance@robcotech.pro",
      notificationEmail: "ops@robcotech.pro",
    },
    user: {
      name: "Ops Lead",
      email: "ops@robcotech.pro",
      role: "admin",
      createdAt: new Date().toISOString(),
    },
    verticalDefinition: {
      label: "Fintech Operations",
    },
    bundleDefinition: {
      label: "Enterprise Tier",
    },
    dashboard: {
      boardDate: "Monthly Audit: 12th",
      investorReadiness: 99,
      revenueCoverage: "$12.4M Vol",
      mrrLabel: "30D Volume",
      churnWatch: "Nominal",
      activeTargets: 4,
      diligenceItems: 14,
      verticalFocus: "Risk & Compliance",
      metrics: [
        { label: "Ledger Match Rate", value: "99.98%", detail: "Automated Reconciliation" },
        { label: "API Gateway Latency", value: "42ms", detail: "Stripe & Plaid Sync" },
        { label: "Active Anomalies", value: "3", detail: "Pending manual review" }
      ],
      approvals: [
        { title: "KYC Ruleset Update", owner: "Risk Team", due: "Today" },
        { title: "Treasury Rebalance", owner: "Finance", due: "Tomorrow" }
      ],
      alerts: [
        { title: "High-Risk Transaction Flag", level: "Critical", detail: "Tx #8849 flagged for OFAC review." }
      ],
      investorTargets: [
        { name: "Plaid Ledger Sync", fit: "Active", reason: "Running every 5 minutes" },
        { name: "Stripe Issuing", fit: "Active", reason: "Real-time ledger updates" }
      ],
    },
    projects: [
      {
        id: "proj-1",
        name: "Q3 SOC2 Audit Prep",
        operatingLane: "Compliance",
        source: "Internal",
        sourceType: "Audit",
        records: "84 controls",
        stage: "Evidence Gathering",
        owner: "Compliance",
        status: "On Track",
        updatedAt: new Date().toISOString(),
      },
      {
        id: "proj-2",
        name: "Cross-border Routing",
        operatingLane: "Treasury",
        source: "Banking API",
        sourceType: "Integration",
        records: "$2.1M routed",
        stage: "Live",
        owner: "Engineering",
        status: "Active",
        updatedAt: new Date().toISOString(),
      }
    ],
    integrations: [
      {
        id: "int-1",
        operatingLane: "Reconciliation",
        provider: "Stripe",
        status: "Active",
        type: "Payment Gateway",
        detail: "Live Sync",
        accountLabel: "Main Processing",
      },
      {
        id: "int-2",
        operatingLane: "Risk",
        provider: "Sardine",
        status: "Active",
        type: "Fraud Prevention",
        detail: "Live Scoring",
        accountLabel: "Anomaly Detection",
      }
    ],
    workflows: [
      {
        id: "wf-1",
        name: "Auto-Reconciliation Engine",
        effectiveness: 99,
        outcome: "Matched 142k Tx"
      },
      {
        id: "wf-2",
        name: "KYC/AML Automated Check",
        effectiveness: 100,
        outcome: "Cleared 450 accounts"
      }
    ],
    workflowTemplates: [],
    users: [],
    permissions: ["workflow:write", "project:read", "billing:admin"],
  });
}
