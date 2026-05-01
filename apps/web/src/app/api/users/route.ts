import { NextRequest, NextResponse } from 'next/server'
import { createWorkspaceUser, requireSession } from '@/lib/workspace-store.server'
import { WorkspaceRole } from '@/lib/workspace-types'

export async function POST(request: NextRequest) {
  const auth = await requireSession(request, 'users:write')
  if (auth.error) return auth.error

  try {
    const body = await request.json()
    const role = (String(body.role || 'viewer') as WorkspaceRole)
    if (!['admin', 'operator', 'viewer'].includes(role)) {
      return NextResponse.json({ error: 'Invalid role' }, { status: 400 })
    }

    const user = await createWorkspaceUser(auth.session.tenantId, {
      name: String(body.name || ''),
      email: String(body.email || ''),
      password: String(body.password || ''),
      role,
    })
    return NextResponse.json({ user })
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to create user'
    const status = message.includes('already exists') ? 409 : 500
    return NextResponse.json({ error: message }, { status })
  }
}
