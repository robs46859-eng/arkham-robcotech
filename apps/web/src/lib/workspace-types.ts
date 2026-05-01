/**
 * Common workspace type definitions.
 * Recreated based on usage in component and API routes.
 */

export type WorkspaceRole = 'admin' | 'operator' | 'viewer';

export interface Workspace {
  id: string;
  name: string;
  vertical: string;
}

export interface WorkspaceUser {
  id: string;
  email: string;
  name: string;
  role: WorkspaceRole;
}

export interface WorkflowNode {
  id: string;
  accent: 'orange' | 'blue' | 'slate';
  x: number;
  y: number;
  lane: string;
  title: string;
}

export interface WorkflowRecord {
  id: string;
  name: string;
  effectiveness: number;
  outcome: string;
  status: string;
  updatedAt: string;
  category: string;
  vertical: string;
  bundle: string;
  orchestrationStatus: string;
  externalWorkflowId?: string;
  cadence: string;
  automations: number;
  nodes: WorkflowNode[];
}

export interface WorkflowTemplate {
  key: string;
  label: string;
  category: string;
}

export interface ProjectRecord {
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
}
