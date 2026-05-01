import { NextRequest, NextResponse } from 'next/server'
import { getWorkspaceSnapshot, requireSession } from '@/lib/workspace-store.server'

export async function GET(request: NextRequest) {
  const auth = await requireSession(request)
  if (auth.error) return auth.error

  try {
    const snapshot = await getWorkspaceSnapshot(auth.session)
    return NextResponse.json(snapshot)
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to load workspace'
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
