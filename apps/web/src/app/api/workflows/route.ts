import { NextRequest, NextResponse } from 'next/server'
import { createWorkflow, getWorkspaceContext, requireSession } from '@/lib/workspace-store.server'

export async function POST(request: NextRequest) {
  const auth = await requireSession(request, 'workflow:write')
  if (auth.error) return auth.error

  try {
    const body = await request.json()
    const { user } = await getWorkspaceContext(auth.session)
    const workflow = await createWorkflow(auth.session.tenantId, user, {
      name: String(body.name || ''),
      templateKey: String(body.templateKey || ''),
      sourceProjectId: body.sourceProjectId ? String(body.sourceProjectId) : undefined,
      automatic: Boolean(body.automatic),
      inputData: body.inputData && typeof body.inputData === 'object' ? body.inputData : undefined,
    })
    return NextResponse.json({ workflow })
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to create workflow'
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
