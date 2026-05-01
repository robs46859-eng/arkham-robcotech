/**
 * Core workspace data hook.
 * Recreated based on usage in dashboard/page.tsx.
 */

import { useState, useEffect, useCallback } from 'react';
import type { WorkflowRecord, WorkflowTemplate } from './workspace-types';

export interface WorkspaceData {
  tenant: {
    id: string;
    workspaceName: string;
    vertical: string;
    primaryDomain: string;
    investorRoutingInbox: string;
    notificationEmail: string;
  };
  user: {
    name: string;
    email: string;
    role: string;
    createdAt: string;
  };
  verticalDefinition: {
    label: string;
  };
  bundleDefinition: {
    label: string;
  };
  dashboard: {
    boardDate: string;
    investorReadiness: number;
    revenueCoverage: string;
    mrrLabel: string;
    churnWatch: string;
    activeTargets: number;
    diligenceItems: number;
    verticalFocus: string;
    metrics: Array<{ label: string; value: string; detail: string }>;
    approvals: Array<{ title: string; owner: string; due: string }>;
    alerts: Array<{ title: string; level: string; detail: string }>;
    investorTargets: Array<{ name: string; fit: string; reason: string }>;
  };
  projects: Array<{
    id: string;
    name: string;
    operatingLane: string;
    source: string;
    sourceType: string;
    records: string;
    stage: string;
    owner: string;
    status: string;
    updatedAt: string;
  }>;
  integrations: Array<{
    id: string;
    operatingLane: string;
    provider: string;
    status: string;
    type: string;
    detail: string;
    accountLabel: string;
  }>;
  workflows: WorkflowRecord[];
  workflowTemplates: WorkflowTemplate[];
  users: Array<{
    id: string;
    name: string;
    email: string;
    role: string;
  }>;
  permissions: string[];
}

export function useWorkspaceData() {
  const [data, setData] = useState<WorkspaceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/workspace/dashboard');
      if (!response.ok) {
        throw new Error('Failed to fetch workspace data');
      }
      const payload = await response.json();
      setData(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { data, loading, error, refresh };
}
