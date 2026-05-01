import { NextRequest, NextResponse } from 'next/server'
import { getWorkspaceSnapshot, requireSession } from '@/lib/workspace-store.server'

export async function GET(request: NextRequest) {
  const auth = await requireSession(request)
  if (auth.error) return auth.error

  try {
    const snapshot = await getWorkspaceSnapshot(auth.session)
    return NextResponse.json(snapshot.dashboard)
  } catch (error) {
    console.error('Failed to fetch briefing:', error)
    return NextResponse.json({ error: 'Failed to fetch briefing' }, { status: 500 })
  }
}
