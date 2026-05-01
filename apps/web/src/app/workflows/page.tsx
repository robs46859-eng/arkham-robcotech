'use client'

import { FormEvent, useEffect, useMemo, useState } from 'react'
import { AppShell } from '@/components/app-shell'
import { useWorkspaceData } from '@/lib/use-workspace-data'
import { WorkflowRecord } from '@/lib/workspace-types'

export default function WorkflowsPage() {
  const { data, loading, error, refresh } = useWorkspaceData()
  const [selectedCategory, setSelectedCategory] = useState<WorkflowRecord['category']>('Admin/Billing')
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string>('')
  const [creating, setCreating] = useState(false)
  const [message, setMessage] = useState('')

  const categories = useMemo(() => {
    const workflowCategories = (data?.workflows || []).map((workflow) => workflow.category)
    const templateCategories = (data?.workflowTemplates || []).map((template) => template.category)
    return Array.from(new Set([...workflowCategories, ...templateCategories])) as WorkflowRecord['category'][]
  }, [data])

  useEffect(() => {
    if (!data) return
    const firstCategory = data.workflows[0]?.category || data.workflowTemplates[0]?.category || 'Admin/Billing'
    setSelectedCategory(firstCategory)
    setSelectedWorkflowId(data.workflows[0]?.id || '')
  }, [data])

  const filteredWorkflows = useMemo(
    () => (data?.workflows || []).filter((workflow) => workflow.category === selectedCategory),
    [data, selectedCategory]
  )

  const activeWorkflow =
    filteredWorkflows.find((workflow) => workflow.id === selectedWorkflowId) ||
    filteredWorkflows[0] ||
    data?.workflows[0]

  async function handleCreateWorkflow(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const name = (form.elements.namedItem('name') as HTMLInputElement | null)?.value || ''
    const templateKey = (form.elements.namedItem('templateKey') as HTMLSelectElement | null)?.value || ''
    const sourceProjectId = (form.elements.namedItem('sourceProjectId') as HTMLSelectElement | null)?.value || undefined

    setCreating(true)
    setMessage('')

    try {
      const response = await fetch('/api/workflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, templateKey, sourceProjectId }),
      })
      const payload = await response.json()
      if (!response.ok) throw new Error(payload.error || 'Failed to create workflow')
      setMessage(`Created workflow ${payload.workflow.name}.`)
      form.reset()
      await refresh()
      setSelectedCategory(payload.workflow.category)
      setSelectedWorkflowId(payload.workflow.id)
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Failed to create workflow')
    } finally {
      setCreating(false)
    }
  }

  async function handleAutomaticWorkflow() {
    setCreating(true)
    setMessage('')
    try {
      const templateKey = data?.workflowTemplates.find((item) => item.category === 'Marketing')?.key || data?.workflowTemplates[0]?.key || 'saas-signup-conversion'
      const response = await fetch('/api/workflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: `${data?.tenant.workspaceName || 'Workspace'} Automatic Workflow`,
          templateKey,
          automatic: true,
          sourceProjectId: data?.projects[0]?.id,
        }),
      })
      const payload = await response.json()
      if (!response.ok) throw new Error(payload.error || 'Automatic workflow creation failed')
      setMessage(`Created recommended workflow ${payload.workflow.name}.`)
      await refresh()
      setSelectedCategory(payload.workflow.category)
      setSelectedWorkflowId(payload.workflow.id)
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Automatic workflow creation failed')
    } finally {
      setCreating(false)
    }
  }

  if (loading) return <WorkflowState message="Loading workflows..." />
  if (error || !data) return <WorkflowState message={error || 'Failed to load workflows'} />

  const canCreate = data.permissions.includes('workflow:write')
  const isDigitalItGirl = data.tenant.vertical === 'digital_it_girl'
  const title = isDigitalItGirl ? 'Predictive niche workflows.' : 'Tenant-approved operating flows.'
  const toolbarCopy = isDigitalItGirl
    ? 'Launch audience scans, product gap hunts, and niche research workflows.'
    : 'Launch, recommend, or refresh operating flows.'
  const emptyState = isDigitalItGirl
    ? 'No Digital IT Girl workflows yet. Start with an audience scan or gap hunt.'
    : 'No workflows in this category yet.'

  return (
    <AppShell
      eyebrow="Workflows"
      title={title}
      description={`${data.bundleDefinition.label}. ${data.workflows.length} workflows in ${data.tenant.workspaceName}.`}
      projects={data.projects}
      workspaceName={data.tenant.workspaceName}
      operatorName={data.user.name}
      workspaceTag={data.bundleDefinition.label}
      variant="workflows"
      meta={[
        { label: 'Live', value: `${data.workflows.length}` },
        { label: 'Templates', value: `${data.workflowTemplates.length}` },
        { label: 'Bundle', value: data.bundleDefinition.label },
      ]}
    >
      {message ? <div className="panel px-6 py-4 text-sm text-muted-foreground">{message}</div> : null}

      <section className="workflow-toolbar">
        <div>
          <p className="display-kicker">Workflow Actions</p>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">{toolbarCopy}</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button type="button" className="brutalist-button" onClick={() => document.getElementById('workflow-create-form')?.scrollIntoView({ behavior: 'smooth' })}>
            New Flow
          </button>
          <button type="button" className="brutalist-button-muted" disabled={!canCreate || creating} onClick={() => void handleAutomaticWorkflow()}>
            Recommend Flow
          </button>
          <button type="button" className="brutalist-button-muted" onClick={() => void refresh()}>
            Refresh Scores
          </button>
        </div>
      </section>

      <form id="workflow-create-form" className="panel grid gap-4 p-6 md:grid-cols-4" onSubmit={handleCreateWorkflow}>
        <input name="name" className="brutalist-input" placeholder="Workflow name" disabled={!canCreate || creating} />
        <select name="templateKey" className="brutalist-input" defaultValue={data.workflowTemplates[0]?.key} disabled={!canCreate || creating}>
          {data.workflowTemplates.map((template) => (
            <option key={template.key} value={template.key}>{template.label}</option>
          ))}
        </select>
        <select name="sourceProjectId" className="brutalist-input" defaultValue="" disabled={!canCreate || creating}>
          <option value="">No linked project</option>
          {data.projects.map((project) => (
            <option key={project.id} value={project.id}>{project.name}</option>
          ))}
        </select>
        <button type="submit" className="brutalist-button" disabled={!canCreate || creating}>
          {creating ? 'Creating...' : 'Save Workflow'}
        </button>
      </form>

      <section className="workflow-grid">
        <div className="space-y-6">
          <div className="panel p-5">
            <p className="display-kicker">Categories</p>
            <div className="mt-5 space-y-3">
              {categories.map((category) => (
                <button
                  key={category}
                  type="button"
                  onClick={() => {
                    setSelectedCategory(category)
                    setSelectedWorkflowId((data.workflows.find((workflow) => workflow.category === category)?.id) || '')
                  }}
                  className={`flex w-full items-center justify-between border-2 px-4 py-3 text-left text-xs font-bold uppercase tracking-[0.18em] ${
                    selectedCategory === category ? 'border-primary bg-primary text-primary-foreground' : 'border-border bg-background text-muted-foreground'
                  }`}
                >
                  {category}
                  <span>{data.workflows.filter((workflow) => workflow.category === category).length}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="panel p-5">
            <p className="display-kicker">Workflow List</p>
            <div className="mt-5 space-y-3">
              {filteredWorkflows.length ? (
                filteredWorkflows.map((workflow) => (
                  <button
                    key={workflow.id}
                    type="button"
                    onClick={() => setSelectedWorkflowId(workflow.id)}
                    className={`w-full border-2 px-4 py-4 text-left ${
                      workflow.id === activeWorkflow?.id ? 'border-accent bg-background' : 'border-border bg-card'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-4">
                      <p className="text-xs font-bold uppercase tracking-[0.18em]">{workflow.name}</p>
                      <span className="status-badge">{workflow.effectiveness}%</span>
                    </div>
                    <p className="mt-2 text-[10px] uppercase tracking-[0.22em] text-muted-foreground">{workflow.vertical} / {workflow.bundle}</p>
                    <p className="mt-3 text-sm leading-6 text-muted-foreground">{workflow.outcome}</p>
                  </button>
                ))
              ) : (
                <p className="border-2 border-border bg-background px-4 py-5 text-sm leading-6 text-muted-foreground">
                  {emptyState}
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="workflow-lab">
          {activeWorkflow ? (
            <>
              <div className="border-b-2 border-border px-6 py-5">
                <p className="display-kicker">Flow Lab</p>
                <div className="mt-3 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                  <div>
                    <h2 className="text-xl font-black uppercase tracking-[0.14em]">{activeWorkflow.name}</h2>
                    <p className="mt-2 text-sm leading-6 text-muted-foreground">{activeWorkflow.outcome}</p>
                    <p className="mt-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">
                      Status: {activeWorkflow.orchestrationStatus}{activeWorkflow.externalWorkflowId ? ` / ${activeWorkflow.externalWorkflowId}` : ''}
                    </p>
                  </div>
                  <div className="grid grid-cols-3 gap-3 text-center">
                    <WorkflowStat label="Cadence" value={activeWorkflow.cadence} />
                    <WorkflowStat label="Agents" value={`${activeWorkflow.automations}`} />
                    <WorkflowStat label="Score" value={`${activeWorkflow.effectiveness}%`} />
                  </div>
                </div>
              </div>

              <div className="workflow-canvas">
                {activeWorkflow.nodes.map((node) => (
                  <WorkflowNodeCard key={node.id} node={node} />
                ))}
              </div>
            </>
          ) : (
            <div className="px-6 py-8 text-sm leading-6 text-muted-foreground">Create your first workflow to populate the canvas.</div>
          )}
        </div>
      </section>
    </AppShell>
  )
}

function WorkflowNodeCard({ node }: { node: WorkflowRecord['nodes'][number] }) {
  const accentClass =
    node.accent === 'orange' ? 'workflow-node-orange' : node.accent === 'blue' ? 'workflow-node-blue' : 'workflow-node-slate'

  return (
    <div
      className={`workflow-node ${accentClass}`}
      style={{ left: `${node.x * 180 + 32}px`, top: `${node.y * 140 + 32}px` }}
    >
      <p className="text-[10px] uppercase tracking-[0.24em] text-muted-foreground">{node.lane}</p>
      <p className="mt-3 text-sm font-bold uppercase tracking-[0.14em]">{node.title}</p>
      <p className="mt-2 text-xs leading-5 text-muted-foreground">Bound to live workspace state.</p>
    </div>
  )
}

function WorkflowStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="border-2 border-border bg-background px-3 py-3">
      <p className="text-[10px] uppercase tracking-[0.24em] text-muted-foreground">{label}</p>
      <p className="mt-2 text-sm font-bold uppercase tracking-[0.12em]">{value}</p>
    </div>
  )
}

function WorkflowState({ message }: { message: string }) {
  return (
    <main className="page-auth flex min-h-screen items-center justify-center px-4 py-12">
      <div className="panel max-w-2xl p-8">
        <p className="display-kicker">Workflows</p>
        <p className="mt-4 text-sm leading-7 text-muted-foreground">{message}</p>
      </div>
    </main>
  )
}
