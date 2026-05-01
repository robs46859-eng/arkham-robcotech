'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ArrowLeft, ArrowRight, Check, Loader2, ShieldCheck, Sparkles } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import {
  Commitment,
  commitmentDiscountRate,
  commitmentOptions,
  digPlanDefinitions,
  ecomPlanDefinitions,
  mediaPlanDefinitions,
  staffPlanDefinitions,
  formatCurrency,
  getQuarterlyEffectiveMonthly,
  getQuarterlyUpfrontTotal,
  planDefinitions,
  PlanId,
} from '@/lib/app-data'
import { loadWorkspaceProfile } from '@/lib/workspace'

export default function PricingPage() {
  const router = useRouter()
  const [commitment, setCommitment] = useState<Commitment>('monthly')
  const [loadingPlan, setLoadingPlan] = useState<PlanId | null>(null)
  const [selectedPlan, setSelectedPlan] = useState<PlanId | null>(null)
  const [autostart, setAutostart] = useState(false)

  const activeVertical = process.env.NEXT_PUBLIC_VERTICAL || 'saas'
  const isEcom = activeVertical === 'ecommerce'
  const isDigitalItGirl = activeVertical === 'digital_it_girl'
  const isMedia = activeVertical === 'media'
  const isStaffing = activeVertical === 'staffing'
  const isStudio = activeVertical === 'studio'
  const activePlans = isDigitalItGirl ? digPlanDefinitions : isEcom ? ecomPlanDefinitions : isMedia ? mediaPlanDefinitions : isStaffing ? staffPlanDefinitions : isStudio ? planDefinitions : planDefinitions
  useEffect(() => {
    if (typeof window === 'undefined') return
    const params = new URLSearchParams(window.location.search)
    const selectedCommitment = params.get('commitment')
    const plan = params.get('plan')
    if (selectedCommitment === 'quarterly' || selectedCommitment === 'monthly') {
      setCommitment(selectedCommitment)
    }
    if (plan === 'core' || plan === 'executive') {
      setSelectedPlan(plan)
    }
    setAutostart(params.get('autostart') === '1')
  }, [])

  useEffect(() => {
    if (!autostart || !selectedPlan) return
    void startCheckout(selectedPlan)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autostart, selectedPlan])

  const comparisonLine = useMemo(
    () => `Save ${Math.round(commitmentDiscountRate * 100)}% when you lock a 3-month commitment.`,
    []
  )

  async function startCheckout(planId: PlanId) {
    const profile = loadWorkspaceProfile()
    if (!profile) {
      const params = new URLSearchParams({
        next: '/pricing',
        plan: planId,
        commitment,
      })
      router.push(`/signup?${params.toString()}`)
      return
    }

    setLoadingPlan(planId)

    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan: planId,
          commitment,
          tenantId: profile.tenantId,
          customerName: profile.customerName,
          customerEmail: profile.customerEmail,
          companyName: profile.workspaceName,
        }),
      })

      const payload = await response.json()
      if (!response.ok) {
        throw new Error(payload.error || 'Checkout failed')
      }

      if (payload.redirect_url) {
        window.location.href = payload.redirect_url
      }
    } catch (error) {
      setLoadingPlan(null)
      window.alert(error instanceof Error ? error.message : 'Checkout failed')
    }
  }

  return (
    <main className="page-pricing min-h-screen py-12 md:py-16">
      <div className="shell">
        <div className="mb-8 flex items-center justify-between gap-4">
          <Link href="/" className="brutalist-button-muted">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Link>
          <Link href="/signup" className="brutalist-button">
            Create Workspace
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </div>

        <section className="panel overflow-hidden">
          <div className="grid gap-0 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="border-b-2 border-border p-8 lg:border-b-0 lg:border-r-2 lg:p-10">
              <p className="display-kicker">{isDigitalItGirl ? 'Digital IT Girl Packages' : isEcom ? 'Ecom Packages' : isMedia ? 'Media Packages' : isStaffing ? 'Staffing Packages' : isStudio ? 'Studio Packages' : 'SaaS Packages'}</p>
              <h1 className="display-title mt-4">
                {isDigitalItGirl ? 'Choose the predictive niche bundle.' : isEcom ? 'Choose the Ecommerce operating bundle.' : isMedia ? 'Choose the Media operating bundle.' : isStaffing ? 'Choose the Staffing operating bundle.' : isStudio ? 'Choose the Studio operating bundle.' : 'Choose the SaaS operating bundle.'}
              </h1>
              <p className="mt-6 max-w-2xl text-base leading-7 text-muted-foreground">
                {isDigitalItGirl
                  ? 'Pick the coverage level for segment scoring, market research synthesis, and product gap control.'
                  : isEcom
                  ? 'Pick the coverage level for demand, inventory, multi-channel revenue, and margins.'
                  : isMedia
                  ? 'Pick the coverage level for content revenue, audience growth, distribution, and retention.'
                  : isStaffing
                  ? 'Pick the coverage level for candidate pipelines, placement velocity, margins, and reporting.'
                  : isStudio
                  ? 'Pick the coverage level for project velocity, delivery posture, and team utilization.'
                  : 'Pick the coverage level for pipeline, onboarding, revenue, and board work.'}
              </p>

              <div className="mt-8 grid gap-4 md:grid-cols-2">
                {commitmentOptions.map((option) => {
                  const active = commitment === option.id
                  return (
                    <button
                      key={option.id}
                      type="button"
                      onClick={() => setCommitment(option.id)}
                      className={`border-2 p-5 text-left ${active ? 'border-primary bg-primary/10' : 'border-border bg-background'}`}
                    >
                      <p className="text-sm font-black uppercase tracking-[0.18em]">{option.label}</p>
                      <p className="mt-3 text-sm leading-6 text-muted-foreground">{option.description}</p>
                    </button>
                  )
                })}
              </div>

              <div className="mt-8 border-2 border-accent/60 bg-background p-5">
                <p className="text-xs uppercase tracking-[0.24em] text-accent">Commitment leverage</p>
                <p className="mt-3 text-base font-bold uppercase tracking-[0.12em]">{comparisonLine}</p>
              </div>
            </div>

            <div className="bg-card p-8 lg:p-10">
              <p className="display-kicker">Coverage</p>
              <div className="mt-6 space-y-4">
                <div className="border-2 border-border bg-background p-4">
                  <ShieldCheck className="h-5 w-5 text-primary" />
                  <p className="mt-3 text-sm font-bold uppercase tracking-[0.16em]">{isDigitalItGirl ? 'Signal lane' : isEcom ? 'Demand lane' : isMedia ? 'Revenue lane' : isStaffing ? 'Fill rate lane' : isStudio ? 'Velocity lane' : 'Board lane'}</p>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">
                    {isDigitalItGirl
                      ? 'Audience filters, trend momentum, and community language stay current.'
                      : isEcom
                      ? 'Inventory, demand, multi-channel revenue, and supply risk stay current.'
                      : isMedia
                      ? 'Subscriptions, ad revenue, sponsorships, and distribution signals stay current.'
                      : isStaffing
                      ? 'Fill rates, market demand, and recruiter efficiency stay current.'
                      : isStudio
                      ? 'Project timelines, velocity tracking, and roadmap output stay current.'
                      : 'Board decks, investor updates, diligence assets, and target lists stay current.'}
                  </p>
                </div>
                <div className="border-2 border-border bg-background p-4">
                  <Sparkles className="h-5 w-5 text-accent" />
                  <p className="mt-3 text-sm font-bold uppercase tracking-[0.16em]">{isDigitalItGirl ? 'Command lane' : isMedia ? 'Distribution lane' : isStaffing ? 'Pipeline lane' : isStudio ? 'Delivery lane' : 'Revenue lane'}</p>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">
                    {isDigitalItGirl
                      ? 'Gap analysis, product direction, and monetization playbooks stay linked.'
                      : isEcom
                      ? 'Campaigns, order conversion, retention, and logistics stay linked.'
                      : isMedia
                      ? 'Content reach, growth experiments, retention, and feedback loops stay linked.'
                      : isStaffing
                      ? 'Pipeline velocity, placement conversion, and margin control stay linked.'
                      : isStudio
                      ? 'Team output, delivery milestones, and quality output stay linked.'
                      : 'Pipeline, onboarding, retention, and finance workflows stay linked.'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-2">
          {activePlans.map((plan) => {
            const quarterlyEffective = getQuarterlyEffectiveMonthly(plan.price)
            const quarterlyTotal = getQuarterlyUpfrontTotal(plan.price)
            const active = loadingPlan === plan.id

            return (
              <article key={plan.id} className={`panel p-8 ${plan.borderClass}`}>
                <p className="display-kicker">{plan.name}</p>
                <div className="mt-5 border-2 border-border bg-background p-5">
                  <p className={`text-3xl font-black md:text-4xl ${plan.accentClass}`}>{formatCurrency(plan.price)}</p>
                  <p className="mt-2 text-sm uppercase tracking-[0.24em] text-muted-foreground">month to month</p>
                  {commitment === 'quarterly' ? (
                    <>
                      <p className="mt-5 text-xl font-black text-foreground">{formatCurrency(quarterlyEffective)} / month effective</p>
                      <p className="mt-2 text-sm uppercase tracking-[0.2em] text-accent">
                        {formatCurrency(quarterlyTotal)} billed upfront for 3 months
                      </p>
                    </>
                  ) : null}
                </div>

                <p className="mt-6 text-sm leading-6 text-muted-foreground">{plan.narrative}</p>
                <p className="mt-4 text-xs font-bold uppercase tracking-[0.22em] text-accent">
                  {plan.id === 'core'
                    ? isDigitalItGirl
                      ? 'Best for operators validating one niche thesis at a time.'
                      : isEcom
                      ? 'Best for single-channel stores and early scale.'
                      : isMedia
                      ? 'Best for content creators and lean media teams.'
                      : isStaffing
                      ? 'Best for recruiters and early scale staffing agencies.'
                      : isStudio
                      ? 'Best for studios managing one project at a time.'
                      : 'Best for active fundraising and early scale.'
                    : isDigitalItGirl
                      ? 'Best for teams turning niche research into repeatable launches.'
                      : isEcom
                      ? 'Best for multi-channel scaling and supply control.'
                      : isMedia
                      ? 'Best for media companies scaling distribution and sponsorship.'
                      : isStaffing
                      ? 'Best for agencies scaling candidate placement and margin control.'
                      : isStudio
                      ? 'Best for studios scaling delivery teams and project volume.'
                      : 'Best for investor pressure and executive control.'}
                </p>

                <ul className="mt-6 space-y-4">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex gap-3 text-sm leading-6 text-foreground">
                      <Check className={`mt-1 h-4 w-4 ${plan.accentClass}`} />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  type="button"
                  className="brutalist-button mt-8 w-full"
                  onClick={() => void startCheckout(plan.id)}
                  disabled={active}
                >
                  {active ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                  {active ? 'Opening Stripe' : plan.cta}
                </button>
              </article>
            )
          })}
        </section>
      </div>
    </main>
  )
}
