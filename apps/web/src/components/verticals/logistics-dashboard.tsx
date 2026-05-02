'use client'

import { useMemo, useState } from 'react'
import { AppShell } from '@/components/app-shell'
import { useWorkspaceData } from '@/lib/use-workspace-data'
import { Activity, AlertTriangle, Building, CheckCircle2, ChevronRight, FileText, ShieldAlert, Zap, ArrowUpRight, Clock, Box, Truck, Anchor, Ship } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts'
import { DiscoverShape, MonitorShape, ConvertShape } from '@/components/isometric-shapes'

const landedCostData = [
  { name: '1st', cost: 120, margin: 80 },
  { name: '5th', cost: 135, margin: 75 },
  { name: '10th', cost: 125, margin: 85 },
  { name: '15th', cost: 140, margin: 70 },
  { name: '20th', cost: 155, margin: 65 },
  { name: '25th', cost: 145, margin: 75 },
  { name: '30th', cost: 160, margin: 60 },
]

const carrierData = [
  { name: 'Maersk', value: 92, color: 'hsl(var(--monitor))' },
  { name: 'FedEx', value: 88, color: 'hsl(var(--discover))' },
  { name: 'DHL', value: 95, color: 'hsl(var(--convert))' },
  { name: 'UPS', value: 85, color: 'hsl(var(--gold))' },
]

const recentFreight = [
  { id: 'BOL-9923A', entity: 'Shenzhen Port', type: 'Ocean', status: 'Cleared', time: 'Just now', delay: false },
  { id: 'BOL-9923B', entity: 'LAX Customs', type: 'Air', status: 'Pending', time: '14m ago', delay: true },
  { id: 'BOL-9923C', entity: 'Chicago Rail', type: 'Rail', status: 'Flagged', time: '1h ago', delay: true },
  { id: 'BOL-9923D', entity: 'Dallas Hub', type: 'LTL', status: 'Cleared', time: '2h ago', delay: false },
]

export default function LogisticsDashboard() {
  const { data, loading, error } = useWorkspaceData()
  
  const laneSummary = useMemo(() => {
    if (!data) return []
    // Define logistics-specific lanes rather than fintech ones
    const order = ['Freight', 'Customs', 'Warehousing', 'Last-Mile'] as const
    return order
      .map((lane) => ({
        lane,
        records: Math.floor(Math.random() * 50) + 10, // Mocked for standalone vertical
        sources: Math.floor(Math.random() * 5) + 1,
      }))
  }, [data])

  if (loading) {
    return <DashboardState message="Loading logistics dashboard..." />
  }

  if (error || !data) {
    return <DashboardState message={error || 'Failed to load workspace'} />
  }

  // Right Panel Content (Attention Queue + Quick Actions isolated for Logistics)
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
              <Ship className="w-4 h-4 text-monitor shrink-0" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-foreground truncate">Sync Port APIs</span>
            </div>
            <ChevronRight className="w-3.5 h-3.5 text-muted-foreground group-hover:text-foreground transition-colors" />
          </button>
          <button className="w-full flex items-center justify-between p-3 rounded-lg border border-convert/20 bg-convert/5 hover:bg-convert/10 transition-all group">
            <div className="flex items-center gap-3 min-w-0">
              <ShieldAlert className="w-4 h-4 text-convert shrink-0" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-convert truncate">Review Spoilage</span>
            </div>
            <span className="text-[9px] font-bold text-convert bg-convert/20 px-2 py-0.5 rounded-full">2 Alerts</span>
          </button>
          <button className="w-full flex items-center justify-between p-3 rounded-lg border border-white/5 bg-black/10 hover:bg-white/5 transition-all group">
            <div className="flex items-center gap-3 min-w-0">
              <FileText className="w-4 h-4 text-discover shrink-0" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-foreground truncate">Customs Log</span>
            </div>
            <ChevronRight className="w-3.5 h-3.5 text-muted-foreground group-hover:text-foreground transition-colors" />
          </button>
        </div>
      </div>

      {/* Attention Queue */}
      <div className="glass-panel p-5 min-w-0 flex-1 flex flex-col gothic-corners border-t-2 border-t-red-500/30">
        <div className="flex items-center gap-2 mb-6">
          <AlertTriangle className="w-3.5 h-3.5 text-red-500 shrink-0" />
          <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Exceptions Queue</p>
        </div>
        <div className="flex-1">
          <div className="flex gap-3 items-start border border-red-500/10 bg-red-500/5 rounded-lg p-4">
            <Anchor className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-4">
                <p className="text-[10px] font-bold uppercase tracking-wider text-red-400">Port Congestion</p>
                <span className="text-[9px] font-bold text-red-400 bg-red-500/10 px-1.5 py-0.5 rounded uppercase tracking-widest">Critical</span>
              </div>
              <p className="mt-2 text-xs text-red-300/60 leading-relaxed">LAX Port delay extending to 5 days. 3 shipments affected.</p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Target Fit -> Top Carriers */}
      <div className="glass-panel p-5 min-w-0 flex-1 flex flex-col glow-discover gothic-corners">
        <div className="flex items-center gap-2 mb-6">
          <Truck className="w-3.5 h-3.5 text-discover shrink-0" />
          <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Carrier SLAs</p>
        </div>
        <div className="space-y-3 flex-1">
          {['Maersk', 'FedEx', 'DHL'].map((carrier, i) => (
            <div key={carrier} className="flex flex-col gap-1 border border-white/5 bg-black/10 rounded-lg p-3">
              <div className="flex items-center justify-between">
                <p className="text-[11px] font-bold text-foreground">{carrier}</p>
                <span className="text-[10px] font-bold text-discover bg-discover/5 px-2 py-0.5 rounded truncate">{95 - i}% On-Time</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  return (
    <AppShell
      eyebrow="Logistics Command"
      title="Global Supply Hub"
      description={`Supply chain operations and telemetry.`}
      projects={data.projects}
      workspaceName={data.tenant.workspaceName}
      operatorName={data.user.name}
      workspaceTag={data.bundleDefinition.label}
      variant="dashboard"
      rightPanel={rightRailContent}
      meta={[
        { label: 'On-Time', value: `94.2%` },
        { label: 'Freight Spend', value: `$1.2M` },
        { label: 'Exception Watch', value: `3 Active` },
      ]}
    >
      <section className="grid gap-6 md:grid-cols-3">
        <MetricCard title="Network Readiness" value="99.9%" detail="Last API sync: 2m ago" icon={CheckCircle2} glowClass="glow-discover" textColor="text-discover" />
        <MetricCard title="Active Shipments" value="1,240" detail="Across 4 carriers" icon={Truck} glowClass="glow-monitor" textColor="text-monitor" />
        <MetricCard title="Inventory Spoilage" value="0.2%" detail="Below 1% SLA threshold" icon={Box} glowClass="glow-convert" textColor="text-convert" />
      </section>

      {/* SUPPLY CHAIN INTELLIGENCE SECTION */}
      <section className="mt-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <MonitorShape />
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-monitor">Supply Telemetry</p>
              <h2 className="text-xl font-black text-foreground display-font">Freight Intelligence</h2>
            </div>
          </div>
        </div>
        
        <div className="grid gap-4 xl:grid-cols-[1fr_0.4fr]">
          {/* Chart Column */}
          <div className="glass-panel p-6 min-w-0 flex flex-col glow-monitor gothic-corners">
            <div className="flex items-center justify-between mb-6 min-w-0">
              <div className="min-w-0">
                <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate">Landed Cost Margin Squeeze</p>
                <p className="text-4xl font-black mt-1 text-foreground truncate data-font">18.5%</p>
              </div>
              <div className="flex items-center gap-2 bg-convert/10 text-convert border border-convert/20 px-3 py-1 rounded-md shrink-0">
                <ArrowUpRight className="w-4 h-4" />
                <span className="text-[10px] font-bold uppercase tracking-wider data-font">+2.4% Cost</span>
              </div>
            </div>
            <div className="flex-1 min-h-[260px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={landedCostData} margin={{ top: 5, right: 0, left: -25, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorCost" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--convert))" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="hsl(var(--convert))" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorMargin" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--monitor))" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="hsl(var(--monitor))" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))', fontFamily: 'var(--font-plex-mono)' }} dy={10} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))', fontFamily: 'var(--font-plex-mono)' }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'hsl(var(--card))', borderRadius: '8px', border: '1px solid hsl(var(--border))', boxShadow: '0 8px 32px rgba(0,0,0,0.4)' }}
                    itemStyle={{ fontSize: '12px', fontWeight: 'bold', fontFamily: 'var(--font-plex-mono)' }}
                  />
                  <Area type="monotone" dataKey="cost" stroke="hsl(var(--convert))" strokeWidth={2} fillOpacity={1} fill="url(#colorCost)" />
                  <Area type="monotone" dataKey="margin" stroke="hsl(var(--monitor))" strokeWidth={1} fillOpacity={1} fill="url(#colorMargin)" strokeDasharray="4 4" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Methods & Right Column */}
          <div className="flex flex-col gap-4 min-w-0">
            <div className="glass-panel p-5 min-w-0 flex-1 gothic-corners">
              <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate mb-4">On-Time Rates by Carrier</p>
              <div className="h-[140px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={carrierData} layout="vertical" margin={{ top: 0, right: 0, left: -10, bottom: 0 }}>
                    <XAxis type="number" hide domain={[0, 100]} />
                    <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 'bold', fill: 'hsl(var(--muted-foreground))', fontFamily: 'var(--font-rajdhani)' }} width={50} />
                    <Tooltip cursor={{fill: 'hsl(var(--muted))'}} contentStyle={{ backgroundColor: 'hsl(var(--card))', borderRadius: '8px', border: '1px solid hsl(var(--border))' }} itemStyle={{fontFamily: 'var(--font-plex-mono)'}} />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={12}>
                      {carrierData.map((entry, index) => (
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
                  <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate">Customs Cleared</p>
                  <p className="text-2xl font-black text-foreground mt-1 truncate data-font">100%</p>
                </div>
                <div className="bg-discover/10 p-2 rounded-lg shrink-0 border border-discover/20">
                  <CheckCircle2 className="w-5 h-5 text-discover" />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Recent Freight */}
        <div className="mt-4 glass-panel min-w-0 overflow-hidden gothic-corners">
          <div className="p-4 border-b border-white/5 bg-black/20 flex items-center justify-between">
            <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Live Freight Ledger</p>
            <button className="text-[10px] font-bold uppercase tracking-wider text-monitor hover:text-monitor/80 transition-colors">View All Manifests</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <tbody>
                {recentFreight.map((tx, i) => (
                  <tr key={tx.id} className={`border-b border-white/5 hover:bg-white/5 transition-colors ${i === recentFreight.length - 1 ? 'border-b-0' : ''}`}>
                    <td className="p-4 min-w-[140px]">
                      <p className="font-bold text-foreground text-xs uppercase tracking-wider truncate">{tx.entity}</p>
                      <p className="text-[10px] uppercase tracking-wider text-muted-foreground mt-1 data-font">{tx.id}</p>
                    </td>
                    <td className="p-4 whitespace-nowrap">
                      <span className="bg-black/40 border border-white/10 text-muted-foreground px-2 py-1 rounded text-[10px] uppercase tracking-wider font-bold">{tx.type}</span>
                    </td>
                    <td className="p-4 whitespace-nowrap">
                      {tx.delay ? (
                        <span className="bg-convert/10 border border-convert/20 text-convert px-2 py-1 rounded text-[10px] uppercase tracking-wider font-bold">Delay Detected</span>
                      ) : (
                        <span className="bg-discover/10 border border-discover/20 text-discover px-2 py-1 rounded text-[10px] uppercase tracking-wider font-bold">On Schedule</span>
                      )}
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

      <section className="mt-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <DiscoverShape />
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-discover">Operating Lanes</p>
              <h2 className="text-xl font-black text-foreground display-font">Logistics Nodes</h2>
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
