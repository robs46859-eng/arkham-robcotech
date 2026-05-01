'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ArrowRight, Building2, Files, Lock, Mail, User } from 'lucide-react'
import { useEffect, useState } from 'react'
import { saveWorkspaceProfile } from '@/lib/workspace'

export default function SignupPage() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [organization, setOrganization] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [returnPath, setReturnPath] = useState('/pricing')
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)
  const [selectedCommitment, setSelectedCommitment] = useState<string | null>(null)

  useEffect(() => {
    if (typeof window === 'undefined') return
    const params = new URLSearchParams(window.location.search)
    const next = params.get('next')
    const plan = params.get('plan')
    const commitment = params.get('commitment')

    if (next && next.startsWith('/')) {
      setReturnPath(next)
    }
    if (plan) setSelectedPlan(plan)
    if (commitment) setSelectedCommitment(commitment)
  }, [])

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const res = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, organization }),
      })

      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.error || 'Signup failed')
      }

      saveWorkspaceProfile({
        tenantId: data.tenant.id,
        workspaceName: data.tenant.name,
        customerName: data.user.name,
        customerEmail: data.user.email,
      })

      if (selectedPlan) {
        const params = new URLSearchParams({
          plan: selectedPlan,
          commitment: selectedCommitment || 'monthly',
          autostart: '1',
        })
        router.push(`/pricing?${params.toString()}`)
      } else {
        router.push(returnPath)
      }
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page-auth flex min-h-screen items-center justify-center px-4 py-12">
      <div className="panel w-full max-w-4xl overflow-hidden">
        <div className="grid md:grid-cols-[0.44fr_0.56fr]">
          <section className="border-b-2 border-border bg-card p-8 md:border-b-0 md:border-r-2 md:p-10">
            <p className="display-kicker">Workspace Intake</p>
            <h1 className="section-title mt-3">Create the founder workspace.</h1>
            <p className="mt-4 text-sm leading-7 text-muted-foreground">
              Set up the account that will own board cycles, investor updates, workflow approvals, and source syncs.
            </p>

            <div className="mt-8 border-2 border-accent/60 bg-background p-5">
              <Files className="h-5 w-5 text-accent" />
              <p className="mt-3 text-sm font-bold uppercase tracking-[0.16em]">What unlocks next</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Pricing checkout, project source connections, workflow design, and the investor reporting dashboard.
              </p>
            </div>
          </section>

          <section className="p-8 md:p-10">
            <form className="grid gap-5 md:grid-cols-2" onSubmit={handleSignup}>
              {error ? (
                <div className="border-2 border-destructive bg-destructive/10 px-4 py-3 text-sm text-red-200 md:col-span-2">
                  {error}
                </div>
              ) : null}

              <label className="block">
                <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Name</span>
                <div className="relative">
                  <User className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="brutalist-input pl-11"
                    placeholder="Founder or operator"
                    required
                  />
                </div>
              </label>

              <label className="block">
                <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Work email</span>
                <div className="relative">
                  <Mail className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="brutalist-input pl-11"
                    placeholder="founder@startup.com"
                    required
                  />
                </div>
              </label>

              <label className="block">
                <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-muted-foreground">Company</span>
                <div className="relative">
                  <Building2 className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <input
                    type="text"
                    value={organization}
                    onChange={(e) => setOrganization(e.target.value)}
                    className="brutalist-input pl-11"
                    placeholder="Startup name"
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

              <div className="md:col-span-2">
                <button type="submit" disabled={loading} className="brutalist-button w-full md:w-auto">
                  {loading ? 'Creating Workspace' : 'Create Workspace'}
                  <ArrowRight className="ml-2 h-4 w-4" />
                </button>
              </div>
            </form>

            <p className="mt-6 text-sm text-muted-foreground">
              Already have a workspace?{' '}
              <Link href="/login" className="font-bold uppercase tracking-[0.18em] text-accent hover:text-foreground">
                Log in
              </Link>
            </p>
          </section>
        </div>
      </div>
    </main>
  )
}
