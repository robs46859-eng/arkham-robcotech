import { NextRequest, NextResponse } from 'next/server'
import { requireSession, updateWorkspaceSettings } from '@/lib/workspace-store.server'

export async function PATCH(request: NextRequest) {
  const auth = await requireSession(request, 'settings:write')
  if (auth.error) return auth.error

  try {
    const body = await request.json()
    const tenant = await updateWorkspaceSettings(auth.session.tenantId, {
      workspaceName: String(body.workspaceName || ''),
      investorRoutingInbox: String(body.investorRoutingInbox || ''),
      notificationEmail: String(body.notificationEmail || ''),
    })
    return NextResponse.json({ tenant })
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to update settings'
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
