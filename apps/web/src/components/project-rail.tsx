'use client'

import { ChevronLeft, ChevronRight, Database, FolderKanban } from 'lucide-react'
import { ProjectRecord } from '@/lib/workspace-types'

interface ProjectRailProps {
  collapsed: boolean
  onToggle: () => void
  projects?: ProjectRecord[]
  title?: string
  subtitle?: string
}

export function ProjectRail({
  collapsed,
  onToggle,
  projects = [],
  title = 'Active sources',
  subtitle = 'Workspace',
}: ProjectRailProps) {
  return (
    <aside className={`project-rail ${collapsed ? 'project-rail-collapsed' : ''}`}>
      <button type="button" className="rail-toggle" onClick={onToggle} aria-label="Toggle projects rail">
        {collapsed ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
      </button>

      {collapsed ? (
        <div className="mt-14 flex flex-col items-center gap-4 text-muted-foreground">
          <FolderKanban className="h-5 w-5" />
          <Database className="h-5 w-5" />
        </div>
      ) : (
        <>
          <div className="border-b-2 border-border px-5 py-4">
            <p className="display-kicker">{subtitle}</p>
            <h3 className="mt-3 text-lg font-black uppercase tracking-[0.14em]">{title}</h3>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left">
              <thead className="bg-muted/30">
                <tr>
                  <th className="px-5 py-3 text-[10px] uppercase tracking-[0.24em]">Project</th>
                  <th className="px-5 py-3 text-[10px] uppercase tracking-[0.24em]">Source</th>
                  <th className="px-5 py-3 text-[10px] uppercase tracking-[0.24em]">Status</th>
                </tr>
              </thead>
              <tbody>
                {projects.map((project) => (
                  <tr key={project.id} className="border-t border-border/70">
                    <td className="px-5 py-4 align-top">
                      <p className="text-xs font-bold uppercase tracking-[0.14em]">{project.name}</p>
                      <p className="mt-1 text-[11px] uppercase tracking-[0.18em] text-muted-foreground">{project.operatingLane}</p>
                    </td>
                    <td className="px-5 py-4 text-xs leading-5 text-muted-foreground">{project.source}</td>
                    <td className="px-5 py-4">
                      <span className="inline-flex border border-border bg-background px-2 py-1 text-[10px] uppercase tracking-[0.18em] text-accent">
                        {project.status}
                      </span>
                    </td>
                  </tr>
                ))}
                {!projects.length ? (
                  <tr className="border-t border-border/70">
                    <td colSpan={3} className="px-5 py-5 text-xs uppercase tracking-[0.18em] text-muted-foreground">
                      No sources linked yet.
                    </td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>
        </>
      )}
    </aside>
  )
}
