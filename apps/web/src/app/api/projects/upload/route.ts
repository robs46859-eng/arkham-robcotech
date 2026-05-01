import { NextRequest, NextResponse } from 'next/server'
import { createProjectUpload, getWorkspaceContext, requireSession } from '@/lib/workspace-store.server'

export async function POST(request: NextRequest) {
  const auth = await requireSession(request, 'upload:write')
  if (auth.error) return auth.error

  try {
    const form = await request.formData()
    const file = form.get('file')
    const category = String(form.get('category') || 'Operations') as 'Board' | 'Finance' | 'Growth' | 'Operations'
    if (!(file instanceof File)) {
      return NextResponse.json({ error: 'A file is required' }, { status: 400 })
    }

    const { user } = await getWorkspaceContext(auth.session)
    const project = await createProjectUpload(auth.session.tenantId, user, {
      fileName: file.name,
      bytes: await file.arrayBuffer(),
      category,
    })
    return NextResponse.json({ project })
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Upload failed'
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
