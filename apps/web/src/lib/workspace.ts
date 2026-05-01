/**
 * Workspace management utilities.
 * Recreated based on usage in login/page.tsx.
 */

export interface WorkspaceProfile {
  tenantId: string;
  workspaceName: string;
  customerName: string;
  customerEmail: string;
}

/**
 * Persists the workspace profile to local storage.
 */
export function saveWorkspaceProfile(profile: WorkspaceProfile): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('arkham_workspace_profile', JSON.stringify(profile));
  }
}

/**
 * Loads the workspace profile from local storage.
 */
export function loadWorkspaceProfile(): WorkspaceProfile | null {
  if (typeof window === 'undefined') return null;
  const raw = localStorage.getItem('arkham_workspace_profile');
  if (!raw) return null;
  try {
    return JSON.parse(raw) as WorkspaceProfile;
  } catch {
    return null;
  }
}

/**
 * Clears the workspace profile from local storage.
 */
export function clearWorkspaceProfile(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('arkham_workspace_profile');
  }
}
