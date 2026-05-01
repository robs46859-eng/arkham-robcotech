'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Briefcase, FileDigit, LayoutDashboard, LogOut, Settings2, Sparkles } from 'lucide-react'
import { ReactNode, useState } from 'react'
import { ProjectRail } from '@/components/project-rail'
import { ProjectRecord } from '@/lib/workspace-types'

const navigation = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/projects', label: 'Projects', icon: Briefcase },
  { href: '/workflows', label: 'Workflows', icon: FileDigit },
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
}: AppShellProps) {
  const pathname = usePathname()
  const [projectsCollapsed, setProjectsCollapsed] = useState(false)

  async function handleLogout() {
    await fetch('/api/auth/logout', { method: 'POST' })
    window.location.href = '/login'
  }

  return (
    <main className="app-canvas">
      <div className="shell py-8">
        <div className="app-shell">
          <aside className="panel app-nav">
            <div className="border-b-2 border-border px-5 py-5">
              <p className="display-kicker">{workspaceName}</p>
              <h2 className="mt-3 text-xl font-black uppercase tracking-[0.14em]">{workspaceTag}</h2>
              <p className="mt-3 text-xs uppercase tracking-[0.18em] text-muted-foreground">{operatorName}</p>
            </div>

            <nav className="px-3 py-4">
              {navigation.map((item) => {
                const Icon = item.icon
                const active = pathname === item.href
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`mb-2 flex items-center gap-3 border-2 px-4 py-3 text-xs font-bold uppercase tracking-[0.18em] ${
                      active ? 'border-primary bg-primary text-primary-foreground' : 'border-transparent text-muted-foreground hover:border-border hover:bg-background hover:text-foreground'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    {item.label}
                  </Link>
                )
              })}
            </nav>

            <div className="mt-auto border-t-2 border-border px-5 py-4">
              <div className="rounded-[20px] border border-accent/45 bg-[linear-gradient(145deg,rgba(90,169,226,0.2),rgba(255,255,255,0.02))] px-4 py-4">
                <Sparkles className="h-4 w-4 text-accent" />
                <p className="mt-3 text-xs font-bold uppercase tracking-[0.18em]">Signal live</p>
                <p className="mt-2 text-xs leading-5 text-muted-foreground">{projects.length} live records in motion.</p>
              </div>
              <button
                type="button"
                onClick={handleLogout}
                className="mt-4 flex w-full items-center justify-center gap-2 rounded-full border border-border bg-background/80 px-4 py-3 text-xs font-bold uppercase tracking-[0.18em] text-muted-foreground hover:border-accent hover:text-foreground"
              >
                <LogOut className="h-4 w-4" />
                Log Out
              </button>
            </div>
          </aside>

          <section className="app-main">
            <header className={`panel shell-header shell-header-${variant} p-6`}>
              <p className="display-kicker">{eyebrow}</p>
              <h1 className="section-title mt-2">{title}</h1>
              {description ? <p className="mt-3 max-w-3xl text-sm leading-6 text-muted-foreground">{description}</p> : null}
              {meta.length ? (
                <div className="mt-6 flex flex-wrap gap-3">
                  {meta.map((item) => (
                    <div key={item.label} className="shell-meta-chip">
                      <span>{item.label}</span>
                      <strong>{item.value}</strong>
                    </div>
                  ))}
                </div>
              ) : null}
            </header>

            {children}
          </section>

          <ProjectRail
            projects={projects}
            collapsed={projectsCollapsed}
            onToggle={() => setProjectsCollapsed((value) => !value)}
            title={variant === 'workflows' ? 'Source feed' : 'Active sources'}
            subtitle={workspaceTag}
          />
        </div>
      </div>
    </main>
  )
}
