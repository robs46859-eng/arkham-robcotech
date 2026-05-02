'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Briefcase, FileDigit, LayoutDashboard, LogOut, Settings2, Sparkles } from 'lucide-react'
import { ReactNode, useState } from 'react'
import { ProjectRail } from '@/components/project-rail'
import { ProjectRecord } from '@/lib/workspace-types'

const navigation = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '#', label: 'Transactions', icon: LayoutDashboard },
  { href: '/projects', label: 'Customers', icon: Briefcase },
  { href: '/workflows', label: 'Analytics', icon: FileDigit },
  { href: '#', label: 'Reports', icon: FileDigit },
  { href: '#', label: 'Alerts', icon: FileDigit },
  { href: '/settings', label: 'Settings', icon: Settings2 },
]

interface AppShellProps {
  title: string
  eyebrow: string
  description?: string
  children: ReactNode
  projects?: ProjectRecord[]
  workspaceName?: string
  operatorName?: string
  variant?: 'dashboard' | 'projects' | 'workflows' | 'settings'
  meta?: Array<{ label: string; value: string }>
  workspaceTag?: string
  rightPanel?: ReactNode
}

export function AppShell({
  title,
  eyebrow,
  description,
  children,
  projects = [],
  workspaceName = 'Founder Office',
  operatorName = 'Operator',
  variant = 'dashboard',
  meta = [],
  workspaceTag = 'Founder Office',
  rightPanel,
}: AppShellProps) {
  const pathname = usePathname()
  const [sidebarTab, setSidebarTab] = useState<'nav' | 'telemetry'>('nav')

  async function handleLogout() {
    await fetch('/api/auth/logout', { method: 'POST' })
    window.location.href = '/login'
  }

  return (
    <main className="app-canvas flex h-screen flex-col overflow-hidden bg-background relative">
      <div className="shell flex flex-1 overflow-hidden py-6 relative z-10">
        <div className="app-shell flex h-full w-full gap-6">
          {/* Main Navigation Sidebar */}
          <aside className="app-nav flex h-full w-64 shrink-0 flex-col overflow-y-auto bg-card border border-white/5 z-20 relative glass-panel rounded-2xl">
            <div className="border-b border-white/5 px-5 py-6 shrink-0 relative">
              <p className="text-[10px] uppercase tracking-[0.24em] text-muted-foreground font-bold">{workspaceName}</p>
              <div className="mt-3 flex items-center gap-2">
                <h2 className="text-xl font-bold uppercase tracking-[0.14em] text-gold">{workspaceTag}</h2>
              </div>
              
              {/* Sidebar Tabs */}
              <div className="mt-6 flex gap-1 p-1 bg-black/20 rounded-lg border border-white/5">
                <button 
                  onClick={() => setSidebarTab('nav')}
                  className={`flex-1 py-1.5 text-[10px] font-bold uppercase tracking-wider rounded transition-all ${sidebarTab === 'nav' ? 'bg-white/10 text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
                >
                  Menu
                </button>
                <button 
                  onClick={() => setSidebarTab('telemetry')}
                  className={`flex-1 py-1.5 text-[10px] font-bold uppercase tracking-wider rounded transition-all ${sidebarTab === 'telemetry' ? 'bg-white/10 text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
                >
                  Stats
                </button>
              </div>

              <div className="gothic-corners absolute inset-0 rounded-2xl pointer-events-none"></div>
            </div>

            {sidebarTab === 'nav' ? (
              <nav className="px-3 py-6 shrink-0 flex-1">
                {navigation.map((item) => {
                  const Icon = item.icon
                  const active = pathname === item.href
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`group relative mb-1.5 flex items-center gap-3 px-4 py-2.5 text-[11px] font-bold uppercase tracking-[0.18em] transition-all overflow-hidden rounded-lg ${
                        active ? 'text-primary bg-white/5' : 'text-muted-foreground hover:text-foreground hover:bg-white/[0.02]'
                      }`}
                    >
                      <Icon className={`h-3.5 w-3.5 relative z-10 ${active ? 'text-discover' : 'text-muted-foreground group-hover:text-foreground'}`} />
                      <span className="relative z-10">{item.label}</span>
                    </Link>
                  )
                })}
              </nav>
            ) : (
              <div className="px-5 py-6 flex-1 space-y-6">
                <div>
                  <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em] mb-3">System Health</p>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] text-muted-foreground uppercase tracking-wider">Gateway</span>
                      <span className="text-[10px] font-bold text-discover uppercase tracking-wider">Active</span>
                    </div>
                    <div className="w-full bg-white/5 rounded-full h-1 overflow-hidden">
                      <div className="bg-discover h-full w-[94%]" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] text-muted-foreground uppercase tracking-wider">Memory</span>
                      <span className="text-[10px] font-bold text-monitor uppercase tracking-wider">82%</span>
                    </div>
                    <div className="w-full bg-white/5 rounded-full h-1 overflow-hidden">
                      <div className="bg-monitor h-full w-[82%]" />
                    </div>
                  </div>
                </div>
                <div>
                  <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em] mb-3">Recent Events</p>
                  <div className="space-y-3">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="flex gap-3 items-start opacity-70">
                        <div className="w-1.5 h-1.5 rounded-full bg-gold mt-1 shrink-0" />
                        <p className="text-[10px] text-muted-foreground uppercase tracking-wider leading-tight">Sync completed for Node_{i}52</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            <div className="mt-auto border-t border-white/5 px-5 py-5 shrink-0 bg-black/10 rounded-b-2xl">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 rounded bg-white/5 border border-white/10 flex items-center justify-center shrink-0">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase">{operatorName.slice(0, 2)}</span>
                </div>
                <div className="min-w-0">
                  <p className="text-xs font-bold uppercase tracking-[0.18em] text-foreground truncate">{operatorName}</p>
                  <p className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground truncate data-font">Operator</p>
                </div>
              </div>
              <button
                type="button"
                onClick={handleLogout}
                className="flex w-full items-center justify-center gap-2 rounded-md border border-white/5 bg-transparent px-4 py-2 text-[10px] font-bold uppercase tracking-[0.18em] text-muted-foreground hover:border-convert/30 hover:text-convert hover:bg-convert/5 transition-all"
              >
                <LogOut className="h-3.5 w-3.5" />
                Log Out
              </button>
            </div>
          </aside>

          {/* Center Main Content */}
          <section className="app-main flex h-full flex-1 flex-col overflow-hidden bg-transparent relative z-10 min-w-0">
            <header className={`shell-header p-6 shrink-0 z-10 border-b border-white/5 glass-panel rounded-2xl mb-6`}>
              <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                  <p className="text-[10px] uppercase tracking-[0.24em] text-gold font-bold">{eyebrow}</p>
                  <h1 className="text-3xl font-black mt-2 tracking-wide display-font text-foreground">{title}</h1>
                  {description ? <p className="mt-3 max-w-3xl text-sm leading-6 text-muted-foreground data-font">{description}</p> : null}
                </div>
                {meta.length ? (
                  <div className="flex gap-4 items-center border border-white/10 bg-black/40 px-4 py-2 rounded-lg">
                    {meta.map((item, i) => (
                      <div key={item.label} className={`flex items-center gap-2 ${i !== 0 ? 'border-l border-white/10 pl-4' : ''}`}>
                        <span className="text-[10px] uppercase tracking-wider text-muted-foreground">{item.label}</span>
                        <strong className="text-sm font-bold text-foreground data-font">{item.value}</strong>
                      </div>
                    ))}
                  </div>
                ) : null}
              </div>
              <div className="gothic-corners absolute inset-0 rounded-2xl pointer-events-none"></div>
            </header>

            <div className="flex-1 overflow-y-auto pb-12 custom-scrollbar">
              {children}
            </div>
          </section>

          {/* Right Panel / Rail */}
          <div className="h-full w-[340px] shrink-0 overflow-y-auto hidden xl:block custom-scrollbar">
            {rightPanel || (
              <ProjectRail
                projects={projects}
                collapsed={projectsCollapsed}
                onToggle={() => setProjectsCollapsed((value) => !value)}
                title={variant === 'workflows' ? 'Source feed' : 'Active sources'}
                subtitle={workspaceTag}
              />
            )}
          </div>
        </div>
      </div>
    </main>
  )
}
