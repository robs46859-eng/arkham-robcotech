'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ArrowRight, Briefcase, Lock, Mail, Radar } from 'lucide-react'
import { useEffect, useState } from 'react'
import { saveWorkspaceProfile } from '@/lib/workspace'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [nextPath, setNextPath] = useState('/dashboard')

  useEffect(() => {
    if (typeof window === 'undefined') return
    const next = new URLSearchParams(window.location.search).get('next')
    if (next && next.startsWith('/')) {
      setNextPath(next)
    }
  }, [])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.error || 'Login failed')
      }

      saveWorkspaceProfile({
        tenantId: data.tenant.id,
        workspaceName: data.tenant.name,
        customerName: data.user.name,
        customerEmail: data.user.email,
      })

      router.push(nextPath)
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page-auth flex min-h-screen items-center justify-center px-4 py-12">
      <div className="panel grid w-full max-w-5xl overflow-hidden md:grid-cols-[0.9fr_1.1fr]">
        <section className="border-b-2 border-border bg-primary p-8 text-primary-foreground md:border-b-0 md:border-r-2 md:p-10">
          <p className="display-kicker !text-primary-foreground/80">Operator Access</p>
          <h1 className="mt-4 text-4xl font-black uppercase leading-none">Enter The Founder Office.</h1>
          <p className="mt-6 max-w-sm text-sm leading-7 text-primary-foreground/85">
            Access the workspace for board materials, investor updates, launch controls, and workflow approvals.
          </p>
          <div className="mt-8 border-2 border-primary-foreground/40 bg-background/10 p-5">
            <Radar className="h-5 w-5" />
            <p className="mt-4 text-sm uppercase tracking-[0.2em]">Protected surfaces</p>
            <p className="mt-3 text-sm leading-6 text-primary-foreground/85">
              Dashboard, projects, workflows, and settings require an operator session.
            </p>
          </div>
        </section>

        <section className="bg-card p-8 md:p-10">
          <p className="display-kicker">Login</p>
          <h2 className="section-title mt-3">Open the active workspace.</h2>
          <p className="mt-4 text-sm leading-6 text-muted-foreground">
            Use your workspace email to resume investor reporting, project syncs, and workflow controls.
          </p>

          <form className="mt-8 space-y-5" onSubmit={handleLogin}>
            {error ? (
              <div className="border-2 border-destructive bg-destructive/10 px-4 py-3 text-sm text-red-200">
                {error}
              </div>
            ) : null}

            <label className="block">
              <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Email</span>
              <div className="relative">
                <Mail className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="brutalist-input pl-11"
                  placeholder="operator@startup.com"
                  required
                />
              </div>
            </label>

            <label className="block">
              <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Password</span>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="brutalist-input pl-11"
                  placeholder="••••••••"
                  required
                />
              </div>
            </label>

            <button type="submit" disabled={loading} className="brutalist-button w-full">
              {loading ? 'Opening Workspace' : 'Enter Dashboard'}
              <ArrowRight className="ml-2 h-4 w-4" />
            </button>
          </form>

          <div className="mt-8 border-2 border-border bg-background p-4">
            <Briefcase className="h-5 w-5 text-accent" />
            <p className="mt-3 text-sm font-bold uppercase tracking-[0.16em]">Need a new workspace?</p>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">
              Create a workspace first if you want package checkout, source connections, and a dedicated project rail.
            </p>
          </div>

          <p className="mt-6 text-sm text-muted-foreground">
            Need a workspace?{' '}
            <Link href="/signup" className="font-bold uppercase tracking-[0.18em] text-accent hover:text-foreground">
              Start Intake
            </Link>
          </p>
        </section>
      </div>
    </main>
  )
}
