'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ArrowLeft, ArrowRight, Check, Loader2, ShieldCheck, Sparkles, MessageSquare, Cloud, Newspaper } from 'lucide-react'
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
  const [showTickerWidget, setShowTickerWidget] = useState<'none' | 'weather' | 'news'>('none')

  const activeVertical = process.env.NEXT_PUBLIC_VERTICAL || 'saas'
  const isEcom = activeVertical === 'ecommerce'
  const isDigitalItGirl = activeVertical === 'digital_it_girl'
  const isMedia = activeVertical === 'media'
  const isStaffing = activeVertical === 'staffing'
  const isStudio = activeVertical === 'studio'
  
  // Professional Language Mapping
  const getVerticalTitle = () => {
    if (isDigitalItGirl) return 'Market Intelligence Suites'
    if (isEcom) return 'Omni-channel Revenue Systems'
    if (isMedia) return 'Content Distribution Frameworks'
    if (isStaffing) return 'Talent Acquisition Engines'
    if (isStudio) return 'Project Delivery Standards'
    return 'Operational Control Suites'
  }

  const getVerticalHero = () => {
    if (isDigitalItGirl) return 'DEPLOY NICHE AUTHORITY MAPPING.'
    if (isEcom) return 'PRESERVE MARGIN INTEGRITY.'
    if (isMedia) return 'OPTIMIZE CONTENT YIELD.'
    if (isStaffing) return 'MAXIMIZE PLACEMENT THROUGHPUT.'
    if (isStudio) return 'STANDARDIZE PROJECT DELIVERY.'
    return 'ESTABLISH EXECUTIVE OVERSIGHT.'
  }

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
  }, [autostart, selectedPlan])

  const comparisonLine = useMemo(
    () => `SECURE ${Math.round(commitmentDiscountRate * 100)}% DISCOUNT WITH 90-DAY OPERATIONAL COMMITMENT.`,
    []
  )

  async function startCheckout(planId: PlanId) {
    const profile = loadWorkspaceProfile()
    if (!profile) {
      const params = new URLSearchParams({ next: '/pricing', plan: planId, commitment })
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
      if (!response.ok) throw new Error(payload.error || 'Checkout failed')
      if (payload.redirect_url) window.location.href = payload.redirect_url
    } catch (error) {
      setLoadingPlan(null)
      window.alert(error instanceof Error ? error.message : 'Checkout failed')
    }
  }

  return (
    <main className="min-h-screen pt-24 pb-16 px-4 md:px-8">
      {/* HEADER TICKER */}
      <div className="ticker-wrap">
        <div className="ticker">
          SYSTEM STATUS: OPTIMAL // {new Date().toLocaleDateString()} // ROBCOTECH PRO VERTICAL DEPLOYMENT ACTIVE // 
          {showTickerWidget === 'weather' ? ' CURRENT WEATHER: 72°F CLEAR SKY //' : ''}
          {showTickerWidget === 'news' ? ' GLOBAL MARKET UPDATE: TRENDING POSITIVE //' : ''}
          OPERATIONAL EXCELLENCE SECURED //
        </div>
        <div className="absolute right-4 flex gap-2 bg-white pl-4">
          <button onClick={() => setShowTickerWidget('weather')} className="hover:text-secondary"><Cloud size={18} /></button>
          <button onClick={() => setShowTickerWidget('news')} className="hover:text-secondary"><Newspaper size={18} /></button>
        </div>
      </div>

      <div className="mx-auto max-w-6xl">
        {/* NAV */}
        <div className="mb-12 flex items-center justify-between">
          <Link href="/" className="brutalist-button bg-white text-black">
            <ArrowLeft className="mr-2 h-4 w-4" />
            RETURN
          </Link>
          <div className="flex gap-4">
             <button onClick={() => setShowTickerWidget('none')} className="text-xs font-black uppercase tracking-tighter hover:underline">Clear Ticker</button>
             <Link href="/signup" className="brutalist-button-blue">
              INITIALIZE
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </div>
        </div>

        {/* HERO SECTION */}
        <section className="brutalist-card mb-12">
          <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
            <div>
              <p className="font-black text-secondary uppercase tracking-[0.2em]">{getVerticalTitle()}</p>
              <h1 className="mt-6 text-5xl md:text-7xl">{getVerticalHero()}</h1>
              <p className="mt-8 max-w-2xl text-lg font-bold leading-relaxed text-muted-foreground">
                Formalize your operating environment with high-integrity data lanes, 
                automated resource coordination, and institutional oversight.
              </p>

              <div className="mt-10 grid gap-4 md:grid-cols-2">
                {commitmentOptions.map((option) => {
                  const active = commitment === option.id
                  return (
                    <button
                      key={option.id}
                      type="button"
                      onClick={() => setCommitment(option.id)}
                      className={`border-4 p-6 text-left transition-all ${active ? 'border-black bg-primary' : 'border-black bg-white hover:bg-gray-50'}`}
                    >
                      <p className="text-sm font-black uppercase tracking-widest">{option.label}</p>
                      <p className="mt-2 text-xs font-bold leading-tight opacity-80 uppercase">{option.description}</p>
                    </button>
                  )
                })}
              </div>
            </div>

            <div className="flex flex-col justify-center border-l-0 lg:border-l-4 border-black lg:pl-10 space-y-6 pt-8 lg:pt-0">
               <div className="bg-secondary p-6 border-4 border-black text-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                  <ShieldCheck size={32} />
                  <p className="mt-4 font-black uppercase tracking-widest">Governance Lane</p>
                  <p className="mt-2 text-sm font-bold opacity-90 uppercase leading-tight">Institutional audit trails, compliance monitoring, and executive visibility.</p>
               </div>
               <div className="bg-primary p-6 border-4 border-black text-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                  <Sparkles size={32} />
                  <p className="mt-4 font-black uppercase tracking-widest">Efficiency Lane</p>
                  <p className="mt-2 text-sm font-bold opacity-90 uppercase leading-tight">Automated throughput optimization and resource allocation frameworks.</p>
               </div>
            </div>
          </div>
        </section>

        {/* PRICING GRID */}
        <section className="grid gap-8 lg:grid-cols-2">
          {activePlans.map((plan) => {
            const quarterlyEffective = getQuarterlyEffectiveMonthly(plan.price)
            const quarterlyTotal = getQuarterlyUpfrontTotal(plan.price)
            const active = loadingPlan === plan.id

            return (
              <article key={plan.id} className="brutalist-card flex flex-col">
                <p className="text-sm font-black text-secondary uppercase tracking-[0.2em]">{plan.name}</p>
                <div className="mt-6 border-4 border-black bg-gray-100 p-8">
                  <p className="text-6xl font-black text-black">{formatCurrency(plan.price)}</p>
                  <p className="mt-2 font-bold uppercase tracking-widest text-muted-foreground">Standard Monthly</p>
                  {commitment === 'quarterly' && (
                    <div className="mt-6 pt-6 border-t-2 border-black/10">
                      <p className="text-2xl font-black text-secondary">{formatCurrency(quarterlyEffective)} / EFF. MONTHLY</p>
                      <p className="text-xs font-black uppercase tracking-widest text-primary mt-1">
                        {formatCurrency(quarterlyTotal)} BILLED UPFRONT (90 DAYS)
                      </p>
                    </div>
                  )}
                </div>

                <div className="mt-8 flex-grow">
                  <p className="text-xs font-black uppercase tracking-widest text-primary mb-6">{comparisonLine}</p>
                  <ul className="space-y-4">
                    {plan.features.map((feature) => (
                      <li key={feature} className="flex gap-3 text-sm font-bold uppercase tracking-tighter">
                        <Check className="h-5 w-5 text-secondary flex-shrink-0" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <button
                  type="button"
                  className="brutalist-button w-full mt-10"
                  onClick={() => void startCheckout(plan.id)}
                  disabled={active}
                >
                  {active ? <Loader2 className="mr-2 h-5 w-5 animate-spin" /> : null}
                  {active ? 'SYNCING STRIPE...' : plan.cta.toUpperCase()}
                </button>
              </article>
            )
          })}
        </section>

        {/* FOOTER MESSAGE */}
        <div className="mt-16 text-center">
           <p className="font-black text-xs uppercase tracking-[0.5em] opacity-40">RobcoTech Pro Infrastructure // All Lanes Active</p>
        </div>
      </div>

      {/* FLOATING ACTION BUTTON */}
      <button className="fab group" title="Support Command">
        <MessageSquare className="group-hover:rotate-12 transition-transform" />
      </button>
    </main>
  )
}
