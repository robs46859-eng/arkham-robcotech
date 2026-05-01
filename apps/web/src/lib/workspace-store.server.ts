/**
 * Server-side workspace store and authentication utilities.
 * Recreated based on exhaustive usage in API routes.
 */

import { NextResponse } from 'next/server';

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  permissions: string[];
}

export interface Tenant {
  id: string;
  workspaceName: string;
}

export interface Session {
  userId: string;
  email: string;
  expires: string;
  session?: any; // Added for briefing/route.ts compatibility
}

export interface AuthResponse extends Session {
  error?: NextResponse;
}

/**
 * MOCK implementation of user authentication.
 */
export async function authenticateWorkspaceUser(email: string, password: string): Promise<{ user: User; tenant: Tenant }> {
  if (email && password.length >= 8) {
    return {
      user: {
        id: 'user-001',
        email: email,
        name: 'Workspace Operator',
        role: 'admin',
        permissions: ['workflow:write', 'project:read', 'billing:admin'],
      },
      tenant: {
        id: 'tenant-abc',
        workspaceName: 'Arkham Robcotech',
      },
    };
  }
  throw new Error('Invalid email or password');
}

/**
 * MOCK implementation of account creation.
 */
export async function createWorkspaceAccount(data: any): Promise<{ user: User; tenant: Tenant }> {
  return {
    user: {
      id: 'user-' + Math.random().toString(36).substr(2, 9),
      email: data.email,
      name: data.name,
      role: 'admin',
      permissions: ['workflow:write', 'project:read', 'billing:admin'],
    },
    tenant: {
      id: 'tenant-' + Math.random().toString(36).substr(2, 9),
      workspaceName: data.companyName || 'New Workspace',
    },
  };
}

/**
 * Builds a session object for a validated user.
 */
export function buildSessionForUser(user: User): Session {
  const expires = new Date();
  expires.setHours(expires.getHours() + 24);
  return {
    userId: user.id,
    email: user.email,
    expires: expires.toISOString(),
  };
}

/**
 * Sets the session cookie in the response.
 */
export function setSessionCookie(response: NextResponse, session: Session): void {
  response.cookies.set('arkham_session', JSON.stringify(session), {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60 * 24,
  });
}

/**
 * Clears the session cookie.
 */
export function clearSessionCookie(response: NextResponse): void {
  response.cookies.delete('arkham_session');
}

/**
 * MOCK: Ensures a valid session exists.
 * Returns AuthResponse which can contain an error for early return.
 */
export async function requireSession(request: Request, permission?: string): Promise<AuthResponse> {
  // Mock success. In real app, check cookies and return error if missing.
  return {
    userId: 'user-001',
    email: 'operator@robcotech.pro',
    expires: new Date(Date.now() + 86400000).toISOString(),
    session: 'tenant-abc'
  };
}

/**
 * MOCK: Retrieves workspace snapshot.
 */
export async function getWorkspaceSnapshot(tenantId: string): Promise<any> {
  return { status: 'healthy', lastUpdate: new Date().toISOString() };
}

/**
 * MOCK: Retrieves workspace context.
 */
export async function getWorkspaceContext(tenantId: string): Promise<any> {
  return { tenantId, environment: 'production' };
}

/**
 * MOCK: Creates an integration.
 */
export async function createIntegration(tenantId: string, user: User, data: any): Promise<any> {
  return { id: 'int-123', status: 'connected' };
}

/**
 * MOCK: Handles project uploads.
 */
export async function createProjectUpload(tenantId: string, user: User, data: any): Promise<any> {
  return { id: 'upload-456', status: 'processing' };
}

/**
 * MOCK: Updates settings.
 */
export async function updateWorkspaceSettings(tenantId: string, data: any): Promise<any> {
  return { success: true };
}

/**
 * MOCK: Creates a user.
 */
export async function createWorkspaceUser(tenantId: string, data: any): Promise<any> {
  return { id: 'user-789', status: 'active' };
}

/**
 * MOCK: Creates a workflow.
 */
export async function createWorkflow(tenantId: string, user: User, data: any): Promise<any> {
  return { id: 'wf-999', status: 'queued', workflow: { name: data.name } };
}
