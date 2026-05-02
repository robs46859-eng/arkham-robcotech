'use client'

import { Bell, CreditCard, Globe, Settings, Shield, User } from 'lucide-react'
import Link from 'next/link'
import { FormEvent, useState } from 'react'
import { AppShell } from '@/components/app-shell'
import { useWorkspaceData } from '@/lib/use-workspace-data'

const tabs = [
  { id: 'general', label: 'General', icon: Settings },
  { id: 'profile', label: 'Profile', icon: User },
  { id: 'security', label: 'Security', icon: Shield },
  { id: 'billing', label: 'Billing', icon: CreditCard },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'tenant', label: 'Workspace', icon: Globe },
]

export default function SettingsPage() {
  const { data, loading, error, refresh } = useWorkspaceData()
  const [activeTab, setActiveTab] = useState('general')
  const [message, setMessage] = useState('')
  const [saving, setSaving] = useState(false)

  async function handleSaveSettings(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setMessage('')
    const form = event.currentTarget
    try {
      const response = await fetch('/api/settings', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workspaceName: (form.elements.namedItem('workspaceName') as HTMLInputElement | null)?.value || '',
          investorRoutingInbox: (form.elements.namedItem('investorRoutingInbox') as HTMLInputElement | null)?.value || '',
          notificationEmail: (form.elements.namedItem('notificationEmail') as HTMLInputElement | null)?.value || '',
        }),
      })
      const payload = await response.json()
      if (!response.ok) throw new Error(payload.error || 'Failed to update settings')
      setMessage(`Saved settings for ${payload.tenant.workspaceName}.`)
      await refresh()
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Failed to update settings')
    } finally {
      setSaving(false)
    }
  }

  async function handleCreateUser(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setMessage('')
    const form = event.currentTarget
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: (form.elements.namedItem('name') as HTMLInputElement | null)?.value || '',
          email: (form.elements.namedItem('email') as HTMLInputElement | null)?.value || '',
          password: (form.elements.namedItem('password') as HTMLInputElement | null)?.value || '',
          role: (form.elements.namedItem('role') as HTMLSelectElement | null)?.value || 'viewer',
        }),
      })
      const payload = await response.json()
      if (!response.ok) throw new Error(payload.error || 'Failed to create user')
      setMessage(`Created ${payload.user.name} (${payload.user.role}).`)
      form.reset()
      await refresh()
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Failed to create user')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <SettingsState message="Loading settings..." />
  if (error || !data) return <SettingsState message={error || 'Failed to load settings'} />

  const canEditSettings = data.permissions.includes('settings:write')
  const canManageUsers = data.permissions.includes('users:write')

  return (
    <AppShell
      eyebrow="Settings"
      title="Workspace controls."
      description={`${data.verticalDefinition.label} / ${data.bundleDefinition.label}. ${data.users.length} users.`}
      projects={data.projects}
      workspaceName={data.tenant.workspaceName}
      operatorName={data.user.name}
      workspaceTag={data.bundleDefinition.label}
      variant="settings"
      meta={[
        { label: 'Users', value: `${data.users.length}` },
        { label: 'Bundle', value: data.bundleDefinition.label },
        { label: 'Domain', value: data.tenant.primaryDomain },
      ]}
    >
      {message ? <div className="panel px-6 py-4 text-sm text-muted-foreground">{message}</div> : null}

      <div className="grid gap-6 grid-cols-1 lg:grid-cols-[280px_1fr] min-w-0">
        <aside className="glass-panel p-4 min-w-0 gothic-corners">
          {tabs.map((tab) => {
            const Icon = tab.icon
            const active = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`mb-2 flex w-full items-center gap-3 border-2 px-4 py-3 text-left text-xs font-bold uppercase tracking-[0.18em] ${
                  active ? 'border-primary bg-primary text-primary-foreground' : 'border-transparent bg-transparent text-muted-foreground hover:border-border hover:text-foreground'
                }`}
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </button>
            )
          })}
        </aside>

        <section className="glass-panel p-8 min-w-0 gothic-corners">
          {activeTab === 'general' ? (
            <form onSubmit={handleSaveSettings}>
              <p className="display-kicker">General</p>
              <h2 className="section-title mt-3">SaaS workspace identity</h2>
              <div className="mt-8 grid gap-5">
                <label>
                  <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Workspace name</span>
                  <input name="workspaceName" type="text" defaultValue={data.tenant.workspaceName} className="brutalist-input max-w-xl" disabled={!canEditSettings || saving} />
                </label>
                <label>
                  <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Primary domain</span>
                  <input type="text" defaultValue={data.tenant.primaryDomain} disabled className="brutalist-input max-w-xl opacity-70" />
                </label>
                <label>
                  <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Investor routing inbox</span>
                  <input name="investorRoutingInbox" type="text" defaultValue={data.tenant.investorRoutingInbox} className="brutalist-input max-w-xl" disabled={!canEditSettings || saving} />
                </label>
                <label>
                  <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Notification email</span>
                  <input name="notificationEmail" type="email" defaultValue={data.tenant.notificationEmail} className="brutalist-input max-w-xl" disabled={!canEditSettings || saving} />
                </label>
                <button className="brutalist-button w-fit" disabled={!canEditSettings || saving}>Save Changes</button>
              </div>
            </form>
          ) : null}

          {activeTab === 'profile' ? (
            <div>
              <p className="display-kicker">Profile</p>
              <h2 className="section-title mt-3">{data.user.name}</h2>
              <div className="mt-6 grid gap-4">
                <InfoRow label="Email" value={data.user.email} />
                <InfoRow label="Role" value={data.user.role} />
                <InfoRow label="Workspace" value={data.tenant.workspaceName} />
                <InfoRow label="Vertical" value={data.verticalDefinition.label} />
                <InfoRow label="Bundle" value={data.bundleDefinition.label} />
                <InfoRow label="Joined" value={new Date(data.user.createdAt).toLocaleDateString()} />
                <InfoRow label="Permissions" value={`${data.permissions.length} enabled`} />
              </div>
            </div>
          ) : null}

          {activeTab === 'security' ? (
            <div>
              <p className="display-kicker">Security</p>
              <h2 className="section-title mt-3">Permission-gated access.</h2>
              <div className="mt-6 grid gap-4">
                <InfoRow label="Session Gate" value="Signed session required." />
                <InfoRow label="API Enforcement" value="Role checks run before mutation." />
                <InfoRow label="Current Role" value={data.user.role} />
              </div>
            </div>
          ) : null}

          {activeTab === 'billing' ? (
            <div>
              <p className="display-kicker">Billing</p>
              <h2 className="section-title mt-3">{data.bundleDefinition.label}</h2>
              <p className="mt-4 max-w-2xl text-sm leading-7 text-muted-foreground">Review bundle options and checkout from pricing.</p>
              <Link href="/pricing" className="brutalist-button mt-6 w-fit">
                Go To Pricing
              </Link>
            </div>
          ) : null}

          {activeTab === 'notifications' ? (
            <div>
              <p className="display-kicker">Notifications</p>
              <h2 className="section-title mt-3">Notification routing</h2>
              <div className="mt-6 grid gap-4">
                <InfoRow label="Primary inbox" value={data.tenant.notificationEmail} />
                <InfoRow label="Investor inbox" value={data.tenant.investorRoutingInbox} />
                <InfoRow label="Connected comms sources" value={`${data.integrations.filter((item) => item.provider === 'slack').length} Slack source(s)`} />
              </div>
            </div>
          ) : null}

          {activeTab === 'tenant' ? (
            <div className="space-y-8">
              <div>
                <p className="display-kicker">Workspace Users</p>
                <h2 className="section-title mt-3">Users and roles</h2>
                <div className="mt-6 space-y-3">
                  {data.users.map((user) => (
                    <div key={user.id} className="glass-panel p-4 gothic-corners min-w-0">
                      <p className="text-sm font-bold uppercase tracking-[0.16em] text-foreground truncate min-w-0">{user.name}</p>
                      <p className="mt-2 text-xs uppercase tracking-[0.2em] text-muted-foreground truncate min-w-0">{user.email}</p>
                      <p className="mt-2 text-[10px] uppercase tracking-[0.2em] text-gold font-bold truncate min-w-0">{user.role}</p>
                    </div>
                  ))}
                </div>
              </div>

              <form className="grid gap-4 md:grid-cols-2" onSubmit={handleCreateUser}>
                <input name="name" className="brutalist-input" placeholder="Operator name" disabled={!canManageUsers || saving} />
                <input name="email" type="email" className="brutalist-input" placeholder="operator@company.com" disabled={!canManageUsers || saving} />
                <input name="password" type="password" className="brutalist-input" placeholder="Temporary password" disabled={!canManageUsers || saving} />
                <select name="role" className="brutalist-input" defaultValue="viewer" disabled={!canManageUsers || saving}>
                  <option value="admin">Admin</option>
                  <option value="operator">Operator</option>
                  <option value="viewer">Viewer</option>
                </select>
                <button className="brutalist-button w-fit" disabled={!canManageUsers || saving}>Create User</button>
              </form>
            </div>
          ) : null}
        </section>
      </div>
    </AppShell>
  )
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="glass-panel p-4 min-w-0 gothic-corners">
      <p className="text-[10px] uppercase tracking-[0.22em] text-muted-foreground font-bold truncate min-w-0">{label}</p>
      <p className="mt-3 text-sm leading-6 text-foreground truncate min-w-0 data-font">{value}</p>
    </div>
  )
}

function SettingsState({ message }: { message: string }) {
  return (
    <main className="page-auth flex min-h-screen items-center justify-center px-4 py-12">
      <div className="glass-panel max-w-2xl p-12 text-center gothic-corners">
        <p className="text-xs font-bold uppercase tracking-[0.2em] text-gold">Settings</p>
        <p className="mt-4 text-sm leading-7 text-muted-foreground data-font animate-pulse">{message}</p>
      </div>
    </main>
  )
}
