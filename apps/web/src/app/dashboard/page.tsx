'use client'

import { FormEvent, useMemo, useState } from 'react'
import { AppShell } from '@/components/app-shell'
import { useWorkspaceData } from '@/lib/use-workspace-data'

const metroOptions = ['New York', 'Los Angeles', 'Chicago', 'Dallas', 'Atlanta', 'Miami', 'Seattle']
const ageOptions = ['18-24', '25-34', '35-44', '45-54', '55+']
const genderOptions = ['Women', 'Men', 'Non-binary', 'Mixed']
const demographicOptions = ['Working professionals', 'Creators', 'Parents', 'Students', 'Solo founders']
const incomeOptions = ['Under 50k', '50k-100k', '100k-150k', '150k+']
const industryOptions = ['Beauty', 'Wellness', 'Productivity', 'Home', 'Fashion', 'Lifestyle']
const householdOptions = ['Single', 'Couple', 'Family with kids', 'Multi-generational']

export default function ExecutiveDashboard() {
  const { data, loading, error, refresh } = useWorkspaceData()
  const [scanFilters, setScanFilters] = useState({
    region: metroOptions[0],
    ageRange: ageOptions[1],
    gender: genderOptions[0],
    demographic: demographicOptions[0],
    incomeBand: incomeOptions[1],
    industry: industryOptions[0],
    householdType: householdOptions[0],
  })
  const [scanMessage, setScanMessage] = useState('')
  const [submittingScan, setSubmittingScan] = useState(false)
  const laneSummary = useMemo(() => {
    if (!data) return []
    const order = ['Pipeline', 'Revenue', 'Activation', 'Retention', 'Reporting'] as const
    return order
      .map((lane) => ({
        lane,
        records: data.projects.filter((project) => project.operatingLane === lane).length,
        sources: data.integrations.filter((integration) => integration.operatingLane === lane).length,
      }))
      .filter((item) => item.records || item.sources)
  }, [data])

  if (loading) {
    return <DashboardState message="Loading workspace dashboard..." />
  }

  if (error || !data) {
    return <DashboardState message={error || 'Failed to load workspace'} />
  }

  const activeVertical = data.tenant.vertical || 'saas'
  const isEcom = activeVertical === 'ecommerce'
  const isDigitalItGirl = activeVertical === 'digital_it_girl'
  const isMedia = activeVertical === 'media'
  const isStaffing = activeVertical === 'staffing'
  const isStudio = activeVertical === 'studio'
  const dashboardEyebrow = isDigitalItGirl ? 'Digital IT Girl Command' : isEcom ? 'Ecom Founder Dashboard' : isMedia ? 'Media Founder Dashboard' : isStaffing ? 'Staffing Founder Dashboard' : isStudio ? 'Studio Founder Dashboard' : 'SaaS Founder Dashboard'
  const readinessLabel = isDigitalItGirl ? 'Niche Readiness' : isStaffing ? 'Agency Readiness' : isStudio ? 'Delivery Readiness' : 'Board Readiness'
  const dashboardFocusLabel = isDigitalItGirl ? 'Niche Targets' : isStaffing ? 'Placement Targets' : isStudio ? 'Studio Targets' : 'Target Accounts'
  const pressureLabel = isDigitalItGirl ? 'Signal Pressure' : isStaffing ? 'Pipeline Velocity' : isStudio ? 'Velocity Pressure' : 'Pipeline Pressure'
  const workspaceDepthLabel = isDigitalItGirl ? 'Research Depth' : 'Workspace Depth'
  const tertiaryMetaLabel = isDigitalItGirl ? 'Gap Queue' : isEcom ? 'Margin Watch' : isMedia ? 'Retention Watch' : isStaffing ? 'Fill Rate' : isStudio ? 'Utilization Watch' : 'Churn Watch'
  const canRunNicheScan = data.permissions.includes('workflow:write')

  async function handleDigitalItGirlScan(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!isDigitalItGirl) return
    setSubmittingScan(true)
    setScanMessage('')
    try {
      const response = await fetch('/api/workflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: `${scanFilters.industry} ${scanFilters.demographic} Niche Scan`,
          templateKey: 'dig-audience-segment-scan',
          inputData: {
            segment_filters: {
              region: scanFilters.region,
              age_range: scanFilters.ageRange,
              gender: scanFilters.gender,
              demographic: scanFilters.demographic,
              income_band: scanFilters.incomeBand,
              industry: scanFilters.industry,
              household_type: scanFilters.householdType,
            },
          },
        }),
      })
      const payload = await response.json()
      if (!response.ok) throw new Error(payload.error || 'Failed to launch niche scan')
      setScanMessage(`Queued ${payload.workflow.name}.`)
      await refresh()
    } catch (err) {
      setScanMessage(err instanceof Error ? err.message : 'Failed to launch niche scan')
    } finally {
      setSubmittingScan(false)
    }
  }

  return (
    <AppShell
      eyebrow={dashboardEyebrow}
      title={`${data.tenant.workspaceName} at a glance.`}
      description={`${data.verticalDefinition.label} / ${data.bundleDefinition.label}. Board date ${data.dashboard.boardDate}.`}
      projects={data.projects}
      workspaceName={data.tenant.workspaceName}
      operatorName={data.user.name}
      workspaceTag={data.bundleDefinition.label}
      variant="dashboard"
      meta={[
        { label: 'Readiness', value: `${data.dashboard.investorReadiness}%` },
        { label: data.dashboard.mrrLabel, value: isEcom ? `${data.dashboard.revenueCoverage}` : `${data.dashboard.revenueCoverage}` },
        { label: tertiaryMetaLabel, value: `${data.dashboard.churnWatch}` },
      ]}
    >
      <section className="grid gap-5 md:grid-cols-3">
        <MetricCard title={readinessLabel} value={`${data.dashboard.investorReadiness}%`} detail={`Board date ${data.dashboard.boardDate}`} />
        <MetricCard title={pressureLabel} value={`${data.dashboard.activeTargets}`} detail={`${data.workflows.length} workflows, ${data.integrations.length} connected sources`} />
        <MetricCard title={workspaceDepthLabel} value={`${data.dashboard.diligenceItems}`} detail={`${data.projects.length} live records in workspace`} />
      </section>

      <section className="panel p-6">
        <p className="display-kicker">Operating Lanes</p>
        <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          {laneSummary.map((lane) => (
            <div key={lane.lane} className="border-2 border-border bg-background p-4">
              <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">{lane.lane}</p>
              <p className="mt-3 text-3xl font-black text-primary">{lane.records}</p>
              <p className="mt-3 text-xs uppercase tracking-[0.18em] text-muted-foreground">{lane.sources} linked sources</p>
            </div>
          ))}
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="panel p-6">
          <p className="display-kicker">{data.dashboard.verticalFocus}</p>
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            {data.dashboard.metrics.map((metric) => (
              <div key={metric.label} className="border-2 border-border bg-background p-4">
                <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">{metric.label}</p>
                <p className="mt-3 text-3xl font-black text-primary">{metric.value}</p>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">{metric.detail}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="panel p-6">
          <p className="display-kicker">Approvals</p>
          <div className="mt-6 space-y-4">
            {data.dashboard.approvals.length ? (
              data.dashboard.approvals.map((approval) => (
                <div key={`${approval.title}-${approval.owner}`} className="border-2 border-border bg-background p-4">
                  <p className="text-sm font-bold uppercase tracking-[0.16em]">{approval.title}</p>
                  <p className="mt-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">{approval.owner}</p>
                  <p className="mt-3 text-sm leading-6 text-foreground">{approval.due}</p>
                </div>
              ))
            ) : (
              <EmptyBlock label="No approvals in queue." />
            )}
          </div>
        </div>
      </section>

      {isDigitalItGirl ? (
        <section className="panel p-6">
          <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="display-kicker">Audience Segment Scan</p>
              <h2 className="section-title mt-3">Launch the first predictive niche pass.</h2>
              <p className="mt-3 max-w-3xl text-sm leading-6 text-muted-foreground">
                This is the first operator entrypoint for Digital IT Girl. It sends structured audience filters into the predictive niche workflow and queues the brief in orchestration.
              </p>
            </div>
            {scanMessage ? <p className="text-sm leading-6 text-muted-foreground">{scanMessage}</p> : null}
          </div>

          <form className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4" onSubmit={handleDigitalItGirlScan}>
            <SegmentSelect
              label="US Metro"
              value={scanFilters.region}
              options={metroOptions}
              onChange={(value) => setScanFilters((current) => ({ ...current, region: value }))}
            />
            <SegmentSelect
              label="Age"
              value={scanFilters.ageRange}
              options={ageOptions}
              onChange={(value) => setScanFilters((current) => ({ ...current, ageRange: value }))}
            />
            <SegmentSelect
              label="Gender"
              value={scanFilters.gender}
              options={genderOptions}
              onChange={(value) => setScanFilters((current) => ({ ...current, gender: value }))}
            />
            <SegmentSelect
              label="Demographic"
              value={scanFilters.demographic}
              options={demographicOptions}
              onChange={(value) => setScanFilters((current) => ({ ...current, demographic: value }))}
            />
            <SegmentSelect
              label="Income"
              value={scanFilters.incomeBand}
              options={incomeOptions}
              onChange={(value) => setScanFilters((current) => ({ ...current, incomeBand: value }))}
            />
            <SegmentSelect
              label="Industry"
              value={scanFilters.industry}
              options={industryOptions}
              onChange={(value) => setScanFilters((current) => ({ ...current, industry: value }))}
            />
            <SegmentSelect
              label="Household"
              value={scanFilters.householdType}
              options={householdOptions}
              onChange={(value) => setScanFilters((current) => ({ ...current, householdType: value }))}
            />
            <div className="flex items-end">
              <button type="submit" className="brutalist-button w-full" disabled={!canRunNicheScan || submittingScan}>
                {submittingScan ? 'Queueing...' : canRunNicheScan ? 'Run Niche Scan' : 'Workflow Access Required'}
              </button>
            </div>
          </form>
        </section>
      ) : null}

      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="panel p-6">
          <p className="display-kicker">Attention Queue</p>
          <div className="mt-6 space-y-4">
            {data.dashboard.alerts.length ? (
              data.dashboard.alerts.map((alert) => (
                <div key={alert.title} className="border-2 border-border bg-background p-4">
                  <div className="flex items-center justify-between gap-4">
                    <p className="text-sm font-bold uppercase tracking-[0.16em]">{alert.title}</p>
                    <span className="status-badge">{alert.level}</span>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">{alert.detail}</p>
                </div>
              ))
            ) : (
              <EmptyBlock label="No active alerts." />
            )}
          </div>
        </div>

        <div className="panel p-6">
          <p className="display-kicker">{dashboardFocusLabel}</p>
          <div className="mt-6 space-y-4">
            {data.dashboard.investorTargets.map((target) => (
              <div key={target.name} className="border-2 border-border bg-background p-4">
                <div className="flex items-center justify-between gap-4">
                  <p className="text-sm font-bold uppercase tracking-[0.16em]">{target.name}</p>
                  <span className="status-badge">{target.fit}</span>
                </div>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">{target.reason}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <div className="panel p-6">
          <p className="display-kicker">Project Watch</p>
          <div className="mt-6 space-y-4">
            {data.projects.length ? (
              data.projects.slice(0, 3).map((project) => (
                <div key={project.id} className="grid gap-3 border-2 border-border bg-background p-4 md:grid-cols-[1fr_auto] md:items-center">
                  <div>
                    <p className="text-sm font-bold uppercase tracking-[0.16em]">{project.name}</p>
                    <p className="mt-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">{project.operatingLane} / {project.source}</p>
                  </div>
                  <div className="text-right">
                    <span className="status-badge">{project.status}</span>
                    <p className="mt-2 text-xs uppercase tracking-[0.18em] text-muted-foreground">{new Date(project.updatedAt).toLocaleDateString()}</p>
                  </div>
                </div>
              ))
            ) : (
              <EmptyBlock label="No projects yet." />
            )}
          </div>
        </div>

        <div className="panel p-6">
          <p className="display-kicker">Workflow Watch</p>
          <div className="mt-6 space-y-4">
            {data.workflows.length ? (
              data.workflows.slice(0, 3).map((workflow) => (
                <div key={workflow.id} className="border-2 border-border bg-background p-4">
                  <div className="flex items-center justify-between gap-4">
                    <p className="text-sm font-bold uppercase tracking-[0.16em]">{workflow.name}</p>
                    <span className="status-badge">{workflow.effectiveness}% effective</span>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">{workflow.outcome}</p>
                </div>
              ))
            ) : (
              <EmptyBlock label="No workflows yet." />
            )}
          </div>
        </div>
      </section>
    </AppShell>
  )
}

function MetricCard({ title, value, detail }: { title: string; value: string; detail: string }) {
  return (
    <div className="metric-card">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">{title}</p>
      <p className="mt-4 text-4xl font-black">{value}</p>
      <p className="mt-3 text-sm leading-6 text-muted-foreground">{detail}</p>
    </div>
  )
}

function SegmentSelect({
  label,
  value,
  options,
  onChange,
}: {
  label: string
  value: string
  options: string[]
  onChange: (value: string) => void
}) {
  return (
    <label className="grid gap-2">
      <span className="text-xs uppercase tracking-[0.22em] text-muted-foreground">{label}</span>
      <select className="brutalist-input" value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  )
}

function DashboardState({ message }: { message: string }) {
  return (
    <main className="page-auth flex min-h-screen items-center justify-center px-4 py-12">
      <div className="panel max-w-2xl p-8">
        <p className="display-kicker">Workspace</p>
        <p className="mt-4 text-sm leading-7 text-muted-foreground">{message}</p>
      </div>
    </main>
  )
}

function EmptyBlock({ label }: { label: string }) {
  return <p className="border-2 border-border bg-background px-4 py-5 text-sm leading-6 text-muted-foreground">{label}</p>
}
