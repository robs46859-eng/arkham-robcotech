import { NextRequest, NextResponse } from 'next/server'
import { createIntegration, getWorkspaceContext, requireSession } from '@/lib/workspace-store.server'

export async function POST(request: NextRequest) {
  const auth = await requireSession(request, 'integration:write')
  if (auth.error) return auth.error

  try {
    const body = await request.json()
    const { user } = await getWorkspaceContext(auth.session)
    const integration = await createIntegration(auth.session.tenantId, user, {
      provider: String(body.provider || ''),
      accountLabel: String(body.accountLabel || ''),
      detail: String(body.detail || ''),
      scopes: Array.isArray(body.scopes) ? body.scopes.map(String) : [],
    })
    return NextResponse.json({ integration })
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to create integration'
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
