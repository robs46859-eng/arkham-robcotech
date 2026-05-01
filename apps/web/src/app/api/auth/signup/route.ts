import { NextRequest, NextResponse } from 'next/server'
import { buildSessionForUser, createWorkspaceAccount, setSessionCookie } from '@/lib/workspace-store.server'

export async function POST(request: NextRequest) {
  try {
    const { name, email, password, organization } = await request.json()

    if (!name || !email || !password || !organization) {
      return NextResponse.json({ error: 'All fields are required' }, { status: 400 })
    }

    const { tenant, user } = await createWorkspaceAccount({
      name: String(name),
      email: String(email),
      password: String(password),
      organization: String(organization),
    })
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
    const status = message.includes('already exists') ? 409 : 500
    return NextResponse.json({ error: message }, { status })
  }
}
