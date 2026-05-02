'use client'

import { FormEvent, useMemo, useState } from 'react'
import { AppShell } from '@/components/app-shell'
import { useWorkspaceData } from '@/lib/use-workspace-data'
import { Activity, AlertTriangle, Building, CheckCircle2, ChevronRight, Database, FileText, ShieldAlert, Target, Zap, ArrowUpRight, ArrowDownRight, Clock, ShieldCheck } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts'
import { DiscoverShape, MonitorShape, ConvertShape } from '@/components/isometric-shapes'

const metroOptions = ['New York', 'Los Angeles', 'Chicago', 'Dallas', 'Atlanta', 'Miami', 'Seattle']
const ageOptions = ['18-24', '25-34', '35-44', '45-54', '55+']
const genderOptions = ['Women', 'Men', 'Non-binary', 'Mixed']
const demographicOptions = ['Working professionals', 'Creators', 'Parents', 'Students', 'Solo founders']
const incomeOptions = ['Under 50k', '50k-100k', '100k-150k', '150k+']
const industryOptions = ['Beauty', 'Wellness', 'Productivity', 'Home', 'Fashion', 'Lifestyle']
const householdOptions = ['Single', 'Couple', 'Family with kids', 'Multi-generational']

const financialData = [
  { name: '1st', volume: 2.1, returns: 0.1 },
  { name: '5th', volume: 2.8, returns: 0.15 },
  { name: '10th', volume: 2.5, returns: 0.12 },
  { name: '15th', volume: 3.4, returns: 0.08 },
  { name: '20th', volume: 4.1, returns: 0.15 },
  { name: '25th', volume: 3.8, returns: 0.1 },
  { name: '30th', volume: 5.4, returns: 0.2 },
]

const methodsData = [
  { name: 'ACH', value: 45, color: 'hsl(var(--monitor))' },
  { name: 'Wire', value: 25, color: 'hsl(var(--discover))' },
  { name: 'Cards', value: 20, color: 'hsl(var(--convert))' },
  { name: 'RTP', value: 10, color: 'hsl(var(--gold))' },
]

const recentTransactions = [
  { id: 'TX-892A', entity: 'Stripe Settlement', type: 'Wire In', amount: '+$145,000.00', status: 'Cleared', time: 'Just now' },
  { id: 'TX-892B', entity: 'AWS Overage', type: 'ACH Out', amount: '-$12,400.00', status: 'Pending', time: '14m ago' },
  { id: 'TX-892C', entity: 'Unrecognized IP Auth', type: 'Card', amount: '$850.00', status: 'Flagged', time: '1h ago' },
  { id: 'TX-892D', entity: 'Mercury Treasury', type: 'RTP Out', amount: '-$25,000.00', status: 'Cleared', time: '2h ago' },
]

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
    const order = ['Treasury', 'Compliance', 'Reconciliation', 'Risk'] as const
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
  const isFintech = activeVertical === 'fintech' || !isDigitalItGirl

  const dashboardEyebrow = isDigitalItGirl ? 'Digital IT Girl Command' : 'Fintech Ops Command'
  const readinessLabel = isDigitalItGirl ? 'Niche Readiness' : 'Audit Readiness'
  const pressureLabel = isDigitalItGirl ? 'Signal Pressure' : 'API Throughput'
  const workspaceDepthLabel = isDigitalItGirl ? 'Research Depth' : 'Operational Depth'
  const tertiaryMetaLabel = isDigitalItGirl ? 'Gap Queue' : 'Fraud Watch'
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
            segment_filters: { region: scanFilters.region, age_range: scanFilters.ageRange, gender: scanFilters.gender, demographic: scanFilters.demographic, income_band: scanFilters.incomeBand, industry: scanFilters.industry, household_type: scanFilters.householdType },
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

  // Define Right Panel Content
  const rightRailContent = (
    <div className="flex flex-col gap-4 h-full pr-4 pb-12">
      {/* Quick Actions */}
      <div className="glass-panel p-5 min-w-0 flex-1 flex flex-col glow-convert gothic-corners">
        <div className="flex items-center gap-2 mb-6">
          <Zap className="w-3.5 h-3.5 text-convert shrink-0" />
          <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Quick Actions</p>
        </div>
        <div className="space-y-2.5 flex-1">
          <button className="w-full flex items-center justify-between p-3 rounded-lg border border-white/5 bg-black/10 hover:bg-white/5 transition-all group">
            <div className="flex items-center gap-3 min-w-0">
              <Activity className="w-4 h-4 text-monitor shrink-0" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-foreground truncate">Run Recon Sync</span>
            </div>
            <ChevronRight className="w-3.5 h-3.5 text-muted-foreground group-hover:text-foreground transition-colors" />
          </button>
          <button className="w-full flex items-center justify-between p-3 rounded-lg border border-convert/20 bg-convert/5 hover:bg-convert/10 transition-all group">
            <div className="flex items-center gap-3 min-w-0">
              <ShieldAlert className="w-4 h-4 text-convert shrink-0" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-convert truncate">Review Risk Queue</span>
            </div>
            <span className="text-[9px] font-bold text-convert bg-convert/20 px-2 py-0.5 rounded-full">3 Pending</span>
          </button>
          <button className="w-full flex items-center justify-between p-3 rounded-lg border border-white/5 bg-black/10 hover:bg-white/5 transition-all group">
            <div className="flex items-center gap-3 min-w-0">
              <FileText className="w-4 h-4 text-discover shrink-0" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-foreground truncate">Audit Log</span>
            </div>
            <ChevronRight className="w-3.5 h-3.5 text-muted-foreground group-hover:text-foreground transition-colors" />
          </button>
        </div>
      </div>

      {/* Attention Queue */}
      <div className="glass-panel p-5 min-w-0 flex-1 flex flex-col gothic-corners border-t-2 border-t-red-500/30">
        <div className="flex items-center gap-2 mb-6">
          <AlertTriangle className="w-3.5 h-3.5 text-red-500 shrink-0" />
          <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Attention Queue</p>
        </div>
        <div className="space-y-3 flex-1 overflow-y-auto custom-scrollbar">
          {data.dashboard.alerts.length ? (
            data.dashboard.alerts.map((alert) => (
              <div key={alert.title} className="flex gap-3 items-start border border-red-500/10 bg-red-500/5 rounded-lg p-3">
                <ShieldAlert className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-4">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-red-400 truncate">{alert.title}</p>
                    <span className="text-[9px] font-bold text-red-400 bg-red-500/10 px-1.5 py-0.5 rounded uppercase">{alert.level}</span>
                  </div>
                  <p className="mt-1.5 text-xs text-red-300/60 line-clamp-2 leading-relaxed">{alert.detail}</p>
                </div>
              </div>
            ))
          ) : (
            <EmptyBlock label="No active alerts." />
          )}
        </div>
      </div>
      
      {/* Target Fit */}
      <div className="glass-panel p-5 min-w-0 flex-1 flex flex-col glow-discover gothic-corners">
        <div className="flex items-center gap-2 mb-6">
          <Building className="w-3.5 h-3.5 text-discover shrink-0" />
          <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Active Targets</p>
        </div>
        <div className="space-y-2.5 flex-1 overflow-y-auto custom-scrollbar">
          {data.dashboard.investorTargets.map((target) => (
            <div key={target.name} className="flex flex-col gap-1 border border-white/5 bg-black/10 rounded-lg p-3">
              <div className="flex items-center justify-between">
                <p className="text-[11px] font-bold text-foreground truncate">{target.name}</p>
                <span className="text-[9px] font-bold text-discover bg-discover/5 px-1.5 py-0.5 rounded border border-discover/10">{target.fit}</span>
              </div>
              <p className="text-[10px] text-muted-foreground truncate opacity-60">{target.reason}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  return (
    <AppShell
      eyebrow={dashboardEyebrow}
      title="Global Intelligence Desk"
      description={`${data.verticalDefinition.label} operations block.`}
      projects={data.projects}
      workspaceName={data.tenant.workspaceName}
      operatorName={data.user.name}
      workspaceTag={data.bundleDefinition.label}
      variant="dashboard"
      rightPanel={rightRailContent}
      meta={[
        { label: 'Readiness', value: `${data.dashboard.investorReadiness}%` },
        { label: data.dashboard.mrrLabel, value: `${data.dashboard.revenueCoverage}` },
        { label: tertiaryMetaLabel, value: `${data.dashboard.churnWatch}` },
      ]}
    >
      <section className="grid gap-6 md:grid-cols-3">
        <MetricCard title={readinessLabel} value={`${data.dashboard.investorReadiness}%`} detail={`${data.dashboard.boardDate}`} icon={CheckCircle2} glowClass="glow-discover" textColor="text-discover" />
        <MetricCard title={pressureLabel} value={`${data.dashboard.activeTargets}`} detail={`${data.workflows.length} active workflows`} icon={Activity} glowClass="glow-monitor" textColor="text-monitor" />
        <MetricCard title={workspaceDepthLabel} value={`${data.dashboard.diligenceItems}`} detail={`${data.projects.length} live records`} icon={Database} glowClass="glow-convert" textColor="text-convert" />
      </section>

      {/* FINTECH INTELLIGENCE SECTION */}
      {isFintech && (
        <section className="mt-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <MonitorShape />
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-monitor">Financial Intelligence</p>
                <h2 className="text-xl font-black text-foreground display-font">Core Telemetry</h2>
              </div>
            </div>
          </div>
          
          <div className="grid gap-4 xl:grid-cols-[1fr_0.4fr]">
            {/* Chart Column */}
            <div className="glass-panel p-6 min-w-0 flex flex-col glow-monitor gothic-corners">
              <div className="flex items-center justify-between mb-6 min-w-0">
                <div className="min-w-0">
                  <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate">30-Day Volume (Millions)</p>
                  <p className="text-4xl font-black mt-1 text-foreground truncate data-font">$12.4M</p>
                </div>
                <div className="flex items-center gap-2 bg-discover/10 text-discover border border-discover/20 px-3 py-1 rounded-md shrink-0">
                  <ArrowUpRight className="w-4 h-4" />
                  <span className="text-[10px] font-bold uppercase tracking-wider data-font">+14.2%</span>
                </div>
              </div>
              <div className="flex-1 min-h-[260px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={financialData} margin={{ top: 5, right: 0, left: -25, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorVolume" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(var(--monitor))" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="hsl(var(--monitor))" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorReturns" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(var(--convert))" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="hsl(var(--convert))" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))', fontFamily: 'var(--font-plex-mono)' }} dy={10} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))', fontFamily: 'var(--font-plex-mono)' }} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'hsl(var(--card))', borderRadius: '8px', border: '1px solid hsl(var(--border))', boxShadow: '0 8px 32px rgba(0,0,0,0.4)' }}
                      itemStyle={{ fontSize: '12px', fontWeight: 'bold', fontFamily: 'var(--font-plex-mono)' }}
                    />
                    <Area type="monotone" dataKey="volume" stroke="hsl(var(--monitor))" strokeWidth={2} fillOpacity={1} fill="url(#colorVolume)" />
                    <Area type="monotone" dataKey="returns" stroke="hsl(var(--convert))" strokeWidth={1} fillOpacity={1} fill="url(#colorReturns)" strokeDasharray="4 4" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Methods & Right Column */}
            <div className="flex flex-col gap-4 min-w-0">
              <div className="glass-panel p-5 min-w-0 flex-1 gothic-corners">
                <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate mb-4">Routing Methods</p>
                <div className="h-[140px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={methodsData} layout="vertical" margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                      <XAxis type="number" hide />
                      <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 'bold', fill: 'hsl(var(--muted-foreground))', fontFamily: 'var(--font-rajdhani)' }} width={60} />
                      <Tooltip cursor={{fill: 'hsl(var(--muted))'}} contentStyle={{ backgroundColor: 'hsl(var(--card))', borderRadius: '8px', border: '1px solid hsl(var(--border))' }} itemStyle={{fontFamily: 'var(--font-plex-mono)'}} />
                      <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={12}>
                        {methodsData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
              <div className="glass-panel p-5 min-w-0 border-l-2 border-l-discover gothic-corners">
                <div className="flex items-center justify-between min-w-0">
                  <div className="min-w-0">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate">Auto-Reconciled</p>
                    <p className="text-2xl font-black text-foreground mt-1 truncate data-font">99.98%</p>
                  </div>
                  <div className="bg-discover/10 p-2 rounded-lg shrink-0 border border-discover/20">
                    <ShieldCheck className="w-5 h-5 text-discover" />
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Recent Transactions */}
          <div className="mt-4 glass-panel min-w-0 overflow-hidden gothic-corners">
            <div className="p-4 border-b border-white/5 bg-black/20 flex items-center justify-between">
              <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Recent Ledger Activity</p>
              <button className="text-[10px] font-bold uppercase tracking-wider text-monitor hover:text-monitor/80 transition-colors">View All</button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <tbody>
                  {recentTransactions.map((tx, i) => (
                    <tr key={tx.id} className={`border-b border-white/5 hover:bg-white/5 transition-colors ${i === recentTransactions.length - 1 ? 'border-b-0' : ''}`}>
                      <td className="p-4 min-w-[140px]">
                        <p className="font-bold text-foreground text-xs uppercase tracking-wider truncate">{tx.entity}</p>
                        <p className="text-[10px] uppercase tracking-wider text-muted-foreground mt-1 data-font">{tx.id}</p>
                      </td>
                      <td className="p-4 whitespace-nowrap">
                        <span className="bg-black/40 border border-white/10 text-muted-foreground px-2 py-1 rounded text-[10px] uppercase tracking-wider font-bold">{tx.type}</span>
                      </td>
                      <td className="p-4 whitespace-nowrap text-right font-black text-foreground data-font">
                        {tx.amount}
                      </td>
                      <td className="p-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          {tx.status === 'Cleared' && <div className="w-1.5 h-1.5 rounded-full bg-discover shadow-[0_0_8px_hsl(var(--discover))]" />}
                          {tx.status === 'Pending' && <div className="w-1.5 h-1.5 rounded-full bg-monitor shadow-[0_0_8px_hsl(var(--monitor))]" />}
                          {tx.status === 'Flagged' && <div className="w-1.5 h-1.5 rounded-full bg-convert shadow-[0_0_8px_hsl(var(--convert))] animate-pulse" />}
                          <span className={`text-[10px] font-bold uppercase tracking-wider ${tx.status === 'Cleared' ? 'text-discover' : tx.status === 'Pending' ? 'text-monitor' : 'text-convert'}`}>{tx.status}</span>
                        </div>
                      </td>
                      <td className="p-4 whitespace-nowrap text-right text-[10px] uppercase tracking-wider text-muted-foreground">
                        <div className="flex items-center justify-end gap-1.5">
                          <Clock className="w-3 h-3" />
                          {tx.time}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      )}

      {isDigitalItGirl ? (
        <section className="mt-8 glass-panel p-6 shadow-sm min-w-0 glow-convert gothic-corners">
          <div className="flex items-center gap-3 mb-6">
            <ConvertShape />
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-convert">Audience Segment Scan</p>
              <h2 className="text-xl font-black text-foreground display-font">Predictive Pass</h2>
            </div>
          </div>

          <form className="grid gap-4 md:grid-cols-2 xl:grid-cols-4" onSubmit={handleDigitalItGirlScan}>
            <SegmentSelect label="US Metro" value={scanFilters.region} options={metroOptions} onChange={(value) => setScanFilters((c) => ({ ...c, region: value }))} />
            <SegmentSelect label="Age" value={scanFilters.ageRange} options={ageOptions} onChange={(value) => setScanFilters((c) => ({ ...c, ageRange: value }))} />
            <SegmentSelect label="Gender" value={scanFilters.gender} options={genderOptions} onChange={(value) => setScanFilters((c) => ({ ...c, gender: value }))} />
            <SegmentSelect label="Demographic" value={scanFilters.demographic} options={demographicOptions} onChange={(value) => setScanFilters((c) => ({ ...c, demographic: value }))} />
            <div className="flex items-end">
              <button type="submit" className="premium-button w-full py-2.5 truncate text-[10px]" disabled={!canRunNicheScan || submittingScan}>
                {submittingScan ? 'Queueing...' : canRunNicheScan ? 'Run Niche Scan' : 'Workflow Access Required'}
              </button>
            </div>
          </form>
        </section>
      ) : null}

      <section className="mt-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <DiscoverShape />
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-discover">Operating Lanes</p>
              <h2 className="text-xl font-black text-foreground display-font">Data Sources</h2>
            </div>
          </div>
        </div>
        <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
          {laneSummary.map((lane) => (
            <div key={lane.lane} className="glass-panel p-5 min-w-0 gothic-corners group hover:border-white/20 transition-all">
              <div className="flex items-center justify-between min-w-0">
                <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate flex-1 min-w-0">{lane.lane}</p>
                <div className="bg-white/5 border border-white/10 rounded-md p-1.5 ml-2 shrink-0 group-hover:bg-discover/10 group-hover:border-discover/20 transition-colors"><Zap className="h-3 w-3 text-muted-foreground group-hover:text-discover transition-colors" /></div>
              </div>
              <p className="mt-4 text-3xl font-black text-foreground truncate min-w-0 data-font">{lane.records}</p>
              <p className="mt-2 text-[10px] uppercase tracking-wider text-muted-foreground truncate min-w-0">{lane.sources} linked sources</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="glass-panel p-6 min-w-0 gothic-corners">
          <div className="flex items-center gap-2 mb-6">
            <CheckCircle2 className="w-4 h-4 text-discover shrink-0" />
            <p className="text-xs font-bold uppercase tracking-wider text-discover truncate min-w-0">Audit & Project Watch</p>
          </div>
          <div className="space-y-4">
            {data.projects.length ? (
              data.projects.slice(0, 3).map((project) => (
                <div key={project.id} className="flex gap-4 items-center border border-white/5 bg-black/20 rounded-lg p-4 min-w-0">
                  <div className="bg-white/5 border border-white/10 p-2.5 rounded-lg shrink-0">
                    <FileText className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold uppercase tracking-wider truncate text-foreground min-w-0">{project.name}</p>
                    <p className="mt-1 text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate min-w-0">{project.operatingLane} / {project.source}</p>
                  </div>
                  <div className="text-right shrink-0 ml-2">
                    <span className="text-[10px] font-bold text-discover bg-discover/10 border border-discover/20 px-2 py-0.5 rounded block text-center mb-1 truncate max-w-[80px] uppercase tracking-wider">{project.status}</span>
                    <p className="text-[10px] text-muted-foreground data-font">{new Date(project.updatedAt).toLocaleDateString()}</p>
                  </div>
                </div>
              ))
            ) : (
              <EmptyBlock label="No projects active." />
            )}
          </div>
        </div>

        <div className="glass-panel p-6 min-w-0 gothic-corners">
          <div className="flex items-center gap-2 mb-6">
            <Activity className="w-4 h-4 text-monitor shrink-0" />
            <p className="text-xs font-bold uppercase tracking-wider text-monitor truncate min-w-0">Workflow Telemetry</p>
          </div>
          <div className="space-y-4">
            {data.workflows.length ? (
              data.workflows.slice(0, 3).map((workflow) => (
                <div key={workflow.id} className="flex gap-4 items-center border border-white/5 bg-black/20 rounded-lg p-4 min-w-0">
                  <div className="bg-white/5 border border-white/10 p-2.5 rounded-lg shrink-0">
                    <Zap className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold uppercase tracking-wider truncate text-foreground min-w-0">{workflow.name}</p>
                    <p className="mt-1 text-xs text-muted-foreground truncate min-w-0">{workflow.outcome}</p>
                  </div>
                  <div className="shrink-0 ml-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-monitor bg-monitor/10 border border-monitor/20 px-2 py-0.5 rounded whitespace-nowrap">{workflow.effectiveness}%</span>
                  </div>
                </div>
              ))
            ) : (
              <EmptyBlock label="No active workflows." />
            )}
          </div>
        </div>
      </section>
    </AppShell>
  )
}

function MetricCard({ title, value, detail, icon: Icon, glowClass, textColor }: { title: string; value: string; detail: string; icon: any; glowClass: string; textColor: string }) {
  return (
    <div className={`glass-panel p-6 flex flex-col justify-between ${glowClass} gothic-corners group hover:bg-white/[0.04] transition-all`}>
      <div className="flex items-center justify-between mb-8">
        <div className="bg-white/5 border border-white/10 p-2 rounded-lg group-hover:border-white/20 transition-colors">
          <Icon className={`h-4 w-4 ${textColor}`} />
        </div>
        <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground text-right">{title}</p>
      </div>
      <div>
        <p className="text-4xl font-black text-foreground data-font tracking-tight">{value}</p>
        <p className="mt-2 text-[10px] uppercase tracking-[0.15em] text-muted-foreground">{detail}</p>
      </div>
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
    <label className="grid gap-1.5 min-w-0">
      <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate min-w-0">{label}</span>
      <select className="brutalist-input h-10 truncate min-w-0" value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option} className="bg-card text-foreground">
            {option}
          </option>
        ))}
      </select>
    </label>
  )
}

function DashboardState({ message }: { message: string }) {
  return (
    <main className="page-auth flex min-h-screen items-center justify-center px-4 py-12 bg-background">
      <div className="glass-panel max-w-2xl p-12 text-center gothic-corners">
        <p className="text-xs font-bold uppercase tracking-[0.2em] text-gold">System</p>
        <p className="mt-4 text-sm leading-7 text-muted-foreground data-font animate-pulse">{message}</p>
      </div>
    </main>
  )
}

function EmptyBlock({ label }: { label: string }) {
  return <p className="border border-dashed border-white/10 bg-black/20 rounded-lg px-4 py-5 text-xs uppercase tracking-wider text-center text-muted-foreground">{label}</p>
}
