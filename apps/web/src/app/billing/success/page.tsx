'use client'

import Link from 'next/link'
import { ArrowRight, CheckCircle2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { formatCurrency, planDefinitions, getQuarterlyUpfrontTotal } from '@/lib/app-data'

export default function BillingSuccessPage() {
  const [planId, setPlanId] = useState<string | null>(null)
  const [commitment, setCommitment] = useState<string | null>(null)

  useEffect(() => {
    if (typeof window === 'undefined') return
    const params = new URLSearchParams(window.location.search)
    setPlanId(params.get('plan'))
    setCommitment(params.get('commitment'))
  }, [])

  const plan = planDefinitions.find((entry) => entry.id === planId) || planDefinitions[0]
  const amountLabel =
    commitment === 'quarterly' ? formatCurrency(getQuarterlyUpfrontTotal(plan.price)) : formatCurrency(plan.price)

  return (
    <main className="page-success flex min-h-screen items-center justify-center px-4 py-12">
      <div className="panel w-full max-w-2xl p-8 md:p-10">
        <p className="display-kicker">Activation Confirmed</p>
        <CheckCircle2 className="mt-5 h-12 w-12 text-primary" />
        <h1 className="section-title mt-5">{plan.name} is locked in.</h1>
        <p className="mt-4 text-sm leading-7 text-muted-foreground">
          Billing completed for {amountLabel}. Your workspace can now connect sources, assemble projects, and run live workflows.
        </p>

        <div className="mt-8 flex flex-wrap gap-4">
          <Link href="/dashboard" className="brutalist-button">
            Open Dashboard
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
          <Link href="/projects" className="brutalist-button-muted">
            Connect Sources
          </Link>
        </div>
      </div>
    </main>
  )
}
