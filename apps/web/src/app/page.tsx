'use client'

import Link from 'next/link'
import { ArrowRight, Briefcase, Building2, FileStack, Radar, ShieldCheck } from 'lucide-react'

const activeVertical = process.env.NEXT_PUBLIC_VERTICAL || 'saas'
const isEcom = activeVertical === 'ecommerce'
const isDigitalItGirl = activeVertical === 'digital_it_girl'
const isMedia = activeVertical === 'media'
const isStaffing = activeVertical === 'staffing'
const isStudio = activeVertical === 'studio'

const outcomes = isDigitalItGirl
  ? [
      'Opportunity scoring stays current.',
      'Trend momentum stays visible.',
      'Product gaps stay surfaced.',
    ]
  : isEcom
  ? [
      'Inventory health stays current.',
      'Demand capture stays in view.',
      'Margin risk stays surfaced.',
    ]
  : isMedia
  ? [
      'Content revenue stays current.',
      'Distribution watch stays in view.',
      'Retention stays surfaced.',
    ]
  : isStaffing
  ? [
      'Fill rates stay current.',
      'Margin control stays in view.',
      'Pipeline velocity stays surfaced.',
    ]
  : isStudio
  ? [
      'Project velocity stays current.',
      'Delivery posture stays in view.',
      'Utilization watch stays surfaced.',
    ]
  : [
      'Board material stays current.',
      'Pipeline stays in view.',
      'Churn risk stays surfaced.',
    ]

export default function Home() {
  return (
    <main className="page-home min-h-screen pb-16">
      <header className="border-b-2 border-border bg-card/95">
        <div className="shell flex flex-col gap-6 py-6 md:flex-row md:items-center md:justify-between">
          <Link href="/" className="flex items-start gap-4">
            <div className="flex h-14 w-14 items-center justify-center border-2 border-foreground bg-primary text-primary-foreground shadow-[6px_6px_0_rgba(90,169,226,0.35)]">
              <FileStack className="h-7 w-7" />
            </div>
            <div>
              <p className="display-kicker">RobcoTech Pro</p>
              <h1 className="text-2xl font-black">
                {isDigitalItGirl ? 'Digital IT Girl Systems' : isEcom ? 'Ecom Founder Systems' : isMedia ? 'Media Founder Systems' : isStaffing ? 'Staffing Founder Systems' : isStudio ? 'Studio Systems' : 'SaaS Founder Systems'}
              </h1>
            </div>
          </Link>

          <nav className="flex flex-wrap items-center gap-3 text-xs uppercase tracking-[0.25em] text-muted-foreground">
            <a href="#offer" className="hover:text-foreground">Offer</a>
            <a href="#systems" className="hover:text-foreground">Systems</a>
            <Link href="/pricing" className="hover:text-foreground">Pricing</Link>
            <Link href="/login" className="hover:text-foreground">Login</Link>
            <Link href="/signup" className="brutalist-button">Create Workspace</Link>
          </nav>
        </div>
      </header>

      <section className="shell grid gap-8 py-12 md:grid-cols-[1.35fr_0.65fr] md:py-20">
        <div className="panel p-8 md:p-12">
          <p className="display-kicker">{isDigitalItGirl ? 'Predictive Niche Engine' : isEcom ? 'Ecom Operating System' : isMedia ? 'Media Operating System' : isStaffing ? 'Staffing Operating System' : isStudio ? 'Studio Operating System' : 'SaaS Operating System'}</p>
          <h2 className="display-title mt-4 max-w-4xl">
            {isDigitalItGirl
              ? 'Digital niche control for operators turning audience signals into product direction.'
              : isEcom
              ? 'Ecommerce control for founders running revenue and inventory at the same time.'
              : isMedia
              ? 'Media control for founders running revenue and distribution at the same time.'
              : isStaffing
              ? 'High-velocity pipelines and placement control for staffing founders.'
              : isStudio
              ? 'Studio control for founders managing project velocity and team utilization.'
              : 'SaaS control for founders running revenue and board pressure at the same time.'}
          </h2>
          <p className="mt-6 max-w-2xl text-base leading-7 text-muted-foreground md:text-lg">
            {isDigitalItGirl
              ? 'Audience filters, trend momentum, complaints, and product gaps stay in one command layer.'
              : isEcom
              ? 'Demand, inventory, multi-channel revenue, and reporting stay in one command layer.'
              : isMedia
              ? 'Content revenue, audience growth, distribution, and retention stay in one command layer.'
              : isStaffing
              ? 'Placement, candidate pipelines, margin control, and reporting stay in one command layer.'
              : isStudio
              ? 'Project velocity, delivery posture, and team utilization stay in one command layer.'
              : 'Pipeline, onboarding, retention, and investor reporting stay in one command layer.'}
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link href="/pricing" className="brutalist-button">
              Review Packages
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
            <Link href="/signup" className="brutalist-button-muted">
              Start Intake
            </Link>
          </div>
        </div>

        <aside className="panel p-8">
          <p className="display-kicker">Operator Snapshot</p>
          <div className="mt-5 space-y-4">
            <div className="border-2 border-primary bg-background p-5">
              <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">{isDigitalItGirl ? 'Niche confidence' : isEcom ? 'Demand health' : isMedia ? 'Content velocity' : isStaffing ? 'Fill rate confidence' : isStudio ? 'Delivery confidence' : 'Board readiness'}</p>
              <p className="mt-3 text-4xl font-black text-primary">93%</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                {isDigitalItGirl ? 'Audience fit, trend velocity, and gap size aligned.' : isEcom ? 'Inventory, ROAS, and supply aligned.' : isMedia ? 'Revenue, audience, and distribution aligned.' : isStaffing ? 'Placements, candidates, and margin aligned.' : isStudio ? 'Velocity, delivery, and utilization aligned.' : 'Revenue, burn, and target list aligned.'}
              </p>
            </div>
            <div className="border-2 border-accent bg-background p-5">
              <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">Bundles</p>
              <p className="mt-3 text-2xl font-black text-accent">{isDigitalItGirl ? 'Signal / Command' : isEcom ? 'Starter / Growth' : isMedia ? 'Media Starter / Media Growth' : isStaffing ? 'Staffing Starter / Staffing Growth' : isStudio ? 'Studio Starter / Studio Growth' : 'Core / Executive'}</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">Choose the bundle on pricing.</p>
            </div>
          </div>
        </aside>
      </section>

      <section id="offer" className="shell py-6">
        <div className="panel p-8 md:p-10">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="display-kicker">Why It Lands</p>
              <h3 className="section-title mt-2">
                {isDigitalItGirl
                  ? 'One operating layer for segment scoring, product gaps, and market timing.'
                  : isEcom
                  ? 'One operating layer for demand, product, and margin output.'
                  : isMedia
                  ? 'One operating layer for audience, revenue, and distribution output.'
                  : isStaffing
                  ? 'One operating layer for pipeline, candidate, and placement output.'
                  : isStudio
                  ? 'One operating layer for velocity, delivery, and team output.'
                  : 'One operating layer for pipeline, product, and board output.'}
              </h3>
            </div>
            <p className="max-w-xl text-sm leading-6 text-muted-foreground">
              Less chasing. More signal.
            </p>
          </div>

          <div className="mt-8 grid gap-5 md:grid-cols-3">
            {outcomes.map((item, index) => (
              <div key={item} className="metric-card">
                <p className="text-xs uppercase tracking-[0.25em] text-accent">0{index + 1}</p>
                <p className="mt-4 text-sm leading-6 text-foreground">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="systems" className="shell py-6">
        <div className="grid gap-6 md:grid-cols-3">
          <div className="panel p-6">
          {isEcom ? <Radar className="h-5 w-5 text-primary" /> : <Building2 className="h-5 w-5 text-primary" />}
          <p className="mt-4 text-sm font-bold uppercase tracking-[0.18em]">{isDigitalItGirl ? 'Signal lane' : isEcom ? 'Demand lane' : isMedia ? 'Revenue lane' : isStaffing ? 'Fill rate lane' : isStudio ? 'Velocity lane' : 'Board lane'}</p>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">
            {isDigitalItGirl
              ? 'Audience filters, trends, and complaints stay current.'
              : isEcom
              ? 'Inventory, demand, and campaign output stay current.'
              : isMedia
              ? 'Subscriptions, ad revenue, and sponsorship output stay current.'
              : isStaffing
              ? 'Fill rates, candidate sourcing, and market output stay current.'
              : isStudio
              ? 'Project timelines, velocity tracking, and roadmap output stay current.'
              : 'Budget, board, and investor output stay current.'}
          </p>
          </div>
          <div className="panel p-6">
          <Briefcase className="h-5 w-5 text-primary" />
          <p className="mt-4 text-sm font-bold uppercase tracking-[0.18em]">{isDigitalItGirl ? 'Gap lane' : isMedia ? 'Distribution lane' : isStaffing ? 'Pipeline lane' : isStudio ? 'Delivery lane' : 'Revenue lane'}</p>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">
            {isDigitalItGirl
              ? 'Product gaps, pricing angles, and winning product direction stay in line.'
              : isEcom
              ? 'Orders, multi-channel sales, and fulfillment stay in line.'
              : isMedia
              ? 'Content reach, platform distribution, and growth experiments stay in line.'
              : isStaffing
              ? 'Pipeline velocity, placement conversion, and recruiter output stay in line.'
              : isStudio
              ? 'Team output, delivery milestones, and quality output stay in line.'
              : 'Pipeline, signup conversion, and expansion stay in line.'}
          </p>
          </div>
          <div className="panel p-6">
          <ShieldCheck className="h-5 w-5 text-accent" />
          <p className="mt-4 text-sm font-bold uppercase tracking-[0.18em]">{isDigitalItGirl ? 'Playbook lane' : isMedia ? 'Retention lane' : isStaffing ? 'Control lane' : isStudio ? 'Utilization lane' : 'Control lane'}</p>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">
            {isDigitalItGirl
              ? 'Watchlists, monetization playbooks, and approvals stay visible.'
              : isEcom
              ? 'Approvals, supply risk, and margins stay visible.'
              : isMedia
              ? 'Approvals, audience health, and churn stay visible.'
              : isStaffing
              ? 'Approvals, margin risk, and compliance stay visible.'
              : isStudio
              ? 'Approvals, team capacity, and utilization stay visible.'
              : 'Approvals, risk, and churn stay visible.'}
          </p>
          </div>

        </div>

        <div className="panel mt-6 p-8">
          <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="display-kicker">Current focus</p>
              <h3 className="section-title mt-2">
                {isDigitalItGirl
                  ? 'Built to keep niche operators ahead of the next demand pocket.'
                  : isEcom
                  ? 'Built to keep ecommerce operators ready for the next scale cycle.'
                  : isMedia
                  ? 'Built to keep media founders ready for the next growth cycle.'
                  : isStaffing
                  ? 'Built to keep staffing founders ready for the next placement cycle.'
                  : isStudio
                  ? 'Built to keep studio founders ready for the next delivery cycle.'
                  : 'Built to keep founders ready for the next board or fundraise call.'}
              </h3>
            </div>
            <div className="border-2 border-border bg-background px-5 py-4">
              <Radar className="h-5 w-5 text-accent" />
              <p className="mt-3 text-xs uppercase tracking-[0.22em] text-muted-foreground">Live dashboard</p>
              <p className="mt-2 text-sm leading-6 text-foreground">Projects, workflows, approvals, and targets sync after login.</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
