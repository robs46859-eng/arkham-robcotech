import { NextRequest, NextResponse } from 'next/server'
import { authenticateWorkspaceUser, buildSessionForUser, setSessionCookie } from '@/lib/workspace-store.server'

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json()

    if (!email || !password) {
      return NextResponse.json({ error: 'Email and password are required' }, { status: 400 })
    }

    const { user, tenant } = await authenticateWorkspaceUser(String(email), String(password))
    const session = buildSessionForUser(user)

    const response = NextResponse.json({
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        permissions: user.permissions,
      },
      tenant: { id: tenant.id, name: tenant.workspaceName },
    })
    setSessionCookie(response, session)
    return response

  } catch (error) {
    const message = error instanceof Error ? error.message : 'Internal server error'
    const status = message === 'Invalid email or password' ? 401 : 500
    return NextResponse.json({ error: message }, { status })
  }
}
