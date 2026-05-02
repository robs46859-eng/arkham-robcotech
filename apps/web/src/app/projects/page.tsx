'use client'

import { FormEvent, useMemo, useState } from 'react'
import { AppShell } from '@/components/app-shell'
import { useWorkspaceData } from '@/lib/use-workspace-data'

const providers = [
  { id: 'google', name: 'Google Workspace', scopes: 'drive.readonly, docs.readonly, gmail.readonly' },
  { id: 'slack', name: 'Slack', scopes: 'channels:history, channels:read, users:read' },
  { id: 'stripe', name: 'Stripe', scopes: 'customers.read, subscriptions.read, invoices.read' },
  { id: 'hubspot', name: 'HubSpot', scopes: 'crm.objects.contacts.read, crm.objects.deals.read' },
  { id: 'segment', name: 'Segment', scopes: 'space:read, source:read, warehouse:read' },
  { id: 'quickbooks', name: 'QuickBooks', scopes: 'com.intuit.quickbooks.accounting' },
  { id: 'notion', name: 'Notion', scopes: 'pages.read, databases.read' },
]

export default function ProjectsPage() {
  const { data, loading, error, refresh } = useWorkspaceData()
  const [uploading, setUploading] = useState(false)
  const [connecting, setConnecting] = useState(false)
  const [message, setMessage] = useState('')
  const laneSummary = useMemo(() => {
    const order = ['Pipeline', 'Revenue', 'Activation', 'Retention', 'Reporting'] as const
    return order.map((lane) => ({
      lane,
      count: (data?.projects || []).filter((project) => project.operatingLane === lane).length,
    }))
  }, [data])

  async function handleUpload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const fileInput = form.elements.namedItem('file') as HTMLInputElement | null
    const categoryInput = form.elements.namedItem('category') as HTMLSelectElement | null
    const file = fileInput?.files?.[0]
    if (!file) return

    setUploading(true)
    setMessage('')

    try {
      const body = new FormData()
      body.set('file', file)
      body.set('category', categoryInput?.value || 'Operations')
      const response = await fetch('/api/projects/upload', { method: 'POST', body })
      const payload = await response.json()
      if (!response.ok) throw new Error(payload.error || 'Upload failed')
      setMessage(`Uploaded ${payload.project.name}.`)
      form.reset()
      await refresh()
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  async function handleConnect(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const provider = (form.elements.namedItem('provider') as HTMLSelectElement | null)?.value || 'google'
    const accountLabel = (form.elements.namedItem('accountLabel') as HTMLInputElement | null)?.value || ''
    const detail = (form.elements.namedItem('detail') as HTMLInputElement | null)?.value || ''
    const scopes = (providers.find((item) => item.id === provider)?.scopes || '').split(',').map((item) => item.trim()).filter(Boolean)

    setConnecting(true)
    setMessage('')

    try {
      const response = await fetch('/api/integrations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider, accountLabel, detail, scopes }),
      })
      const payload = await response.json()
      if (!response.ok) throw new Error(payload.error || 'Connection failed')
      setMessage(`Connected ${payload.integration.accountLabel}.`)
      form.reset()
      await refresh()
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Connection failed')
    } finally {
      setConnecting(false)
    }
  }

  if (loading) return <ProjectsState message="Loading workspace projects..." />
  if (error || !data) return <ProjectsState message={error || 'Failed to load workspace'} />

  const canUpload = data.permissions.includes('upload:write')
  const canConnect = data.permissions.includes('integration:write')

  return (
    <AppShell
      eyebrow="Projects"
      title="Sources, files, and live SaaS records."
      description={`${data.verticalDefinition.label} / ${data.bundleDefinition.label}. ${data.projects.length} project records.`}
      projects={data.projects}
      workspaceName={data.tenant.workspaceName}
      operatorName={data.user.name}
      workspaceTag={data.bundleDefinition.label}
      variant="projects"
      meta={[
        { label: 'Uploads', value: `${data.projects.filter((item) => item.sourceType === 'upload').length}` },
        { label: 'Connected', value: `${data.integrations.length}` },
        { label: 'Bundle', value: data.bundleDefinition.label },
      ]}
    >
      {message ? <div className="panel px-6 py-4 text-sm text-muted-foreground">{message}</div> : null}

      <section className="glass-panel p-6 min-w-0 gothic-corners">
        <p className="display-kicker">Lane Coverage</p>
        <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-5 min-w-0">
          {laneSummary.map((lane) => (
            <div key={lane.lane} className="border-2 border-border bg-background p-4">
              <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">{lane.lane}</p>
              <p className="mt-3 text-3xl font-black text-primary">{lane.count}</p>
              <p className="mt-3 text-xs uppercase tracking-[0.18em] text-muted-foreground">records live</p>
            </div>
          ))}
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.94fr_1.06fr] min-w-0">
        <div className="glass-panel p-6 min-w-0 gothic-corners">
          <p className="display-kicker">Connected Sources</p>
          <div className="mt-6 grid gap-4 md:grid-cols-2 min-w-0">
            {data.integrations.length ? (
              data.integrations.map((source) => (
                <div key={source.id} className="source-card">
                  <div className="flex items-center justify-between gap-4">
                    <p className="text-sm font-bold uppercase tracking-[0.16em]">{source.provider}</p>
                    <span className="status-badge">{source.status}</span>
                  </div>
                  <p className="mt-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">{source.type}</p>
                  <p className="mt-3 text-xs uppercase tracking-[0.18em] text-accent">{source.operatingLane}</p>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">{source.detail}</p>
                  <p className="mt-3 text-xs uppercase tracking-[0.18em] text-muted-foreground">{source.accountLabel}</p>
                </div>
              ))
            ) : (
              <div className="source-card md:col-span-2">
                <p className="text-sm leading-6 text-muted-foreground">No SaaS sources connected yet.</p>
              </div>
            )}
          </div>
        </div>

        <div className="glass-panel overflow-hidden min-w-0 gothic-corners">
          <div className="border-b border-white/10 px-6 py-5 bg-black/20">
            <p className="display-kicker">Live Table</p>
            <h2 className="mt-3 text-xl font-black uppercase tracking-[0.14em]">Current workspace assets</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left table-fixed">
              <thead className="bg-white/5 border-b border-white/10">
                <tr>
                  <th className="px-5 py-4 text-[10px] font-bold uppercase tracking-[0.25em] text-muted-foreground w-1/3">Project</th>
                  <th className="px-5 py-4 text-[10px] font-bold uppercase tracking-[0.25em] text-muted-foreground w-1/6">Stage</th>
                  <th className="px-5 py-4 text-[10px] font-bold uppercase tracking-[0.25em] text-muted-foreground w-1/6">Owner</th>
                  <th className="px-5 py-4 text-[10px] font-bold uppercase tracking-[0.25em] text-muted-foreground w-1/6">Source</th>
                  <th className="px-5 py-4 text-[10px] font-bold uppercase tracking-[0.25em] text-muted-foreground w-1/6">Status</th>
                </tr>
              </thead>
              <tbody>
                {data.projects.length ? (
                  data.projects.map((project) => (
                    <tr key={project.id} className="border-b border-border/70">
                      <td className="px-5 py-4 align-top overflow-hidden">
                        <p className="font-bold uppercase tracking-[0.12em] truncate min-w-0">{project.name}</p>
                        <p className="mt-2 text-[10px] uppercase tracking-[0.18em] text-muted-foreground truncate min-w-0 data-font">{project.records}</p>
                        <p className="mt-2 text-[10px] uppercase tracking-[0.18em] text-primary truncate min-w-0">{project.operatingLane}</p>
                      </td>
                      <td className="px-5 py-4 text-[10px] text-muted-foreground uppercase tracking-wider truncate min-w-0 data-font">{project.stage}</td>
                      <td className="px-5 py-4 text-xs text-muted-foreground truncate min-w-0">{project.owner}</td>
                      <td className="px-5 py-4 text-[10px] text-muted-foreground uppercase tracking-wider truncate min-w-0">{project.source}</td>
                      <td className="px-5 py-4 overflow-hidden">
                        <span className="status-badge block truncate min-w-0 max-w-full text-center">{project.status}</span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td className="px-5 py-6 text-sm text-muted-foreground" colSpan={5}>No projects yet. Upload a file or connect a source to populate the workspace.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-2 min-w-0 mt-6">
        <form className="glass-panel p-6 min-w-0 gothic-corners" onSubmit={handleUpload}>
          <p className="display-kicker">Local Uploads</p>
          <p className="mt-4 text-sm leading-7 text-muted-foreground">Decks, models, churn exports, onboarding docs, and board files.</p>
          <div className="mt-6 grid gap-4">
            <input type="file" name="file" className="brutalist-input" disabled={!canUpload || uploading} />
            <select name="category" className="brutalist-input" defaultValue="Operations" disabled={!canUpload || uploading}>
              <option value="Board">Board</option>
              <option value="Finance">Finance</option>
              <option value="Growth">Growth</option>
              <option value="Operations">Operations</option>
            </select>
            <button type="submit" className="brutalist-button w-fit" disabled={!canUpload || uploading}>
              {uploading ? 'Uploading...' : 'Upload Workspace File'}
            </button>
            {!canUpload ? <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Your role does not have upload permission.</p> : null}
          </div>
        </form>

        <form className="glass-panel p-6 min-w-0 gothic-corners" onSubmit={handleConnect}>
          <p className="display-kicker">Connect Source</p>
          <p className="mt-4 text-sm leading-7 text-muted-foreground">Store a source connection record.</p>
          <div className="mt-6 grid gap-4">
            <select name="provider" className="brutalist-input" defaultValue="google" disabled={!canConnect || connecting}>
              {providers.map((provider) => (
                <option key={provider.id} value={provider.id}>{provider.name}</option>
              ))}
            </select>
            <input name="accountLabel" className="brutalist-input" placeholder="workspace@company.com or growth-team" disabled={!canConnect || connecting} />
            <input name="detail" className="brutalist-input" placeholder="Billing workspace, product analytics, pipeline sync..." disabled={!canConnect || connecting} />
            <button type="submit" className="brutalist-button w-fit" disabled={!canConnect || connecting}>
              {connecting ? 'Connecting...' : 'Store Source Connection'}
            </button>
            {!canConnect ? <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Your role does not have integration permission.</p> : null}
          </div>
        </form>
      </section>
    </AppShell>
  )
}

function ProjectsState({ message }: { message: string }) {
  return (
    <main className="page-auth flex min-h-screen items-center justify-center px-4 py-12">
      <div className="panel max-w-2xl p-8">
        <p className="display-kicker">Projects</p>
        <p className="mt-4 text-sm leading-7 text-muted-foreground">{message}</p>
      </div>
    </main>
  )
}
