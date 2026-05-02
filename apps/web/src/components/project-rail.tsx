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
    <aside className={`h-full flex flex-col bg-card border border-white/5 glass-panel rounded-2xl overflow-hidden transition-all duration-300 ${collapsed ? 'w-16' : 'w-[340px]'}`}>
      <div className="p-5 border-b border-white/5 flex items-center justify-between">
        {!collapsed && (
          <div>
            <p className="text-[10px] uppercase tracking-[0.2em] text-gold font-bold">{subtitle}</p>
            <h3 className="mt-1 text-sm font-black uppercase tracking-wider text-foreground">{title}</h3>
          </div>
        )}
        <button type="button" onClick={onToggle} className="p-1.5 hover:bg-white/5 rounded-lg transition-colors text-muted-foreground hover:text-foreground ml-auto">
          {collapsed ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
        </button>
      </div>

      {!collapsed && (
        <div className="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-2">
          {projects.map((project) => (
            <div key={project.id} className="group p-4 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/5 transition-all">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-foreground">{project.name}</p>
                  <p className="text-[9px] uppercase tracking-widest text-muted-foreground mt-1">{project.operatingLane}</p>
                </div>
                <span className="text-[9px] font-bold uppercase tracking-widest text-discover bg-discover/10 border border-discover/10 px-1.5 py-0.5 rounded">
                  {project.status}
                </span>
              </div>
              <p className="text-[10px] text-muted-foreground truncate opacity-60">{project.source}</p>
            </div>
          ))}
          {!projects.length && (
            <div className="p-8 text-center border border-dashed border-white/10 rounded-xl">
              <p className="text-[10px] uppercase tracking-widest text-muted-foreground">No sources linked</p>
            </div>
          )}
        </div>
      )}
    </aside>
  )
}
