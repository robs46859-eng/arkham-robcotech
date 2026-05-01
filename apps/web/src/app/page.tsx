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
      'Compliance reporting stays current.',
      'Operational pipeline stays in view.',
      'Market risk stays surfaced.',
    ]

export default function Home() {
  return (
    <main className="page-home min-h-screen pb-16">
      <header className="border-b-4 border-black bg-white">
        <div className="shell flex flex-col gap-6 py-6 md:flex-row md:items-center md:justify-between">
          <Link href="/" className="flex items-start gap-4">
            <div className="flex h-14 w-14 items-center justify-center border-4 border-black bg-primary text-black shadow-[4px_4px_0_rgba(0,0,0,1)]">
              <FileStack className="h-7 w-7" />
            </div>
            <div>
              <p className="font-black text-secondary uppercase tracking-[0.2em] text-[10px]">RobcoTech Pro</p>
              <h1 className="text-2xl font-black uppercase tracking-tighter">
                {isDigitalItGirl ? 'Market Intelligence Systems' : isEcom ? 'Omni-channel Commerce Systems' : isMedia ? 'Content Yield Systems' : isStaffing ? 'Placement Throughput Systems' : isStudio ? 'Delivery Standard Systems' : 'Operational Control Systems'}
              </h1>
            </div>
          </Link>

          <nav className="flex flex-wrap items-center gap-6 text-xs font-black uppercase tracking-widest text-black">
            <a href="#offer" className="hover:underline">Offer</a>
            <a href="#systems" className="hover:underline">Systems</a>
            <Link href="/pricing" className="hover:underline">Pricing</Link>
            <Link href="/login" className="hover:underline">Login</Link>
            <Link href="/signup" className="brutalist-button-blue py-2 px-4 border-2">Initialize</Link>
          </nav>
        </div>
      </header>

      <section className="shell grid gap-8 py-12 md:grid-cols-[1.35fr_0.65fr] md:py-20">
        <div className="brutalist-card">
          <p className="font-black text-secondary uppercase tracking-[0.2em] text-xs">
            {isDigitalItGirl ? 'Market Analysis Framework' : isEcom ? 'Commerce Operating System' : isMedia ? 'Yield Management System' : isStaffing ? 'Resource Management System' : isStudio ? 'Delivery Management System' : 'Executive Control System'}
          </p>
          <h2 className="text-4xl md:text-6xl font-black mt-6 leading-[0.9] uppercase">
            {isDigitalItGirl
              ? 'DEPLOY NICHE AUTHORITY MAPPING.'
              : isEcom
              ? 'PRESERVE MARGIN INTEGRITY.'
              : isMedia
              ? 'OPTIMIZE CONTENT YIELD.'
              : isStaffing
              ? 'MAXIMIZE PLACEMENT THROUGHPUT.'
              : isStudio
              ? 'STANDARDIZE PROJECT DELIVERY.'
              : 'ESTABLISH EXECUTIVE OVERSIGHT.'}
          </h2>
          <p className="mt-8 max-w-2xl text-lg font-bold leading-relaxed text-muted-foreground uppercase">
            {isDigitalItGirl
              ? 'Formalize your operating environment with high-integrity data lanes, audience filters, and trend momentum.'
              : isEcom
              ? 'Formalize your operating environment with multi-channel revenue integrity and inventory health.'
              : isMedia
              ? 'Formalize your operating environment with content distribution watch and subscription retention.'
              : isStaffing
              ? 'Formalize your operating environment with talent acquisition throughput and placement efficiency.'
              : isStudio
              ? 'Formalize your operating environment with project velocity tracking and delivery standards.'
              : 'Formalize your operating environment with institutional reporting, audit trails, and fiscal integrity.'}
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <Link href="/pricing" className="brutalist-button">
              Review Deployment Tiers
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
            <Link href="/signup" className="brutalist-button bg-white text-black">
              System Intake
            </Link>
          </div>
        </div>

        <aside className="brutalist-card flex flex-col justify-center bg-gray-50">
          <p className="font-black text-xs uppercase tracking-[0.2em] mb-6">Operational Snapshot</p>
          <div className="space-y-6">
            <div className="border-4 border-black bg-white p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
              <p className="text-xs font-black uppercase tracking-widest text-muted-foreground">
                {isDigitalItGirl ? 'Authority Confidence' : isEcom ? 'Demand Integrity' : isMedia ? 'Yield Stability' : isStaffing ? 'Throughput Confidence' : isStudio ? 'Delivery Stability' : 'Governance Rating'}
              </p>
              <p className="mt-3 text-5xl font-black text-primary">93%</p>
              <p className="mt-4 text-xs font-bold leading-tight uppercase">
                {isDigitalItGirl ? 'Audience fit, trend velocity, and gap size aligned.' : isEcom ? 'Inventory health and channel revenue aligned.' : isMedia ? 'Content distribution and yield aligned.' : isStaffing ? 'Placements, throughput, and margin aligned.' : isStudio ? 'Velocity, delivery, and utilization aligned.' : 'Governance, fiscal audit, and reporting aligned.'}
              </p>
            </div>
            <div className="border-4 border-black bg-secondary p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] text-white">
              <p className="text-xs font-black uppercase tracking-widest opacity-80">Deployment Layers</p>
              <p className="mt-3 text-xl font-black uppercase tracking-tighter">
                {isDigitalItGirl ? 'Signal / Command' : isEcom ? 'Standard / Growth' : isMedia ? 'Media Standard / Media Growth' : isStaffing ? 'Acquisition / Enterprise' : isStudio ? 'Standard / Enterprise' : 'Core / Executive'}
              </p>
              <p className="mt-2 text-xs font-bold uppercase">Initialize on pricing page.</p>
            </div>
          </div>
        </aside>
      </section>

      <section id="offer" className="shell py-6">
        <div className="brutalist-card bg-white">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="font-black text-xs uppercase tracking-[0.2em] text-secondary">Strategic Integrity</p>
              <h3 className="text-2xl font-black uppercase mt-4">
                {isDigitalItGirl
                  ? 'One operational layer for niche authority and market timing.'
                  : isEcom
                  ? 'One operational layer for margin integrity and product output.'
                  : isMedia
                  ? 'One operational layer for yield management and distribution.'
                  : isStaffing
                  ? 'One operational layer for acquisition and placement throughput.'
                  : isStudio
                  ? 'One operational layer for velocity and delivery standards.'
                  : 'One operational layer for governance and fiscal oversight.'}
              </h3>
            </div>
            <p className="max-w-xl text-xs font-black uppercase tracking-tighter text-muted-foreground">
              Institutional clarity. Performance secured.
            </p>
          </div>

          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {outcomes.map((item, index) => (
              <div key={item} className="border-4 border-black p-6 bg-gray-50 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                <p className="text-xs font-black text-primary">0{index + 1}</p>
                <p className="mt-4 text-sm font-bold uppercase tracking-tighter leading-tight">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="systems" className="shell py-6">
        <div className="grid gap-6 md:grid-cols-3">
          <div className="brutalist-card">
          <Building2 className="h-6 w-6 text-secondary" />
          <p className="mt-6 text-sm font-black uppercase tracking-widest">{isDigitalItGirl ? 'Signal Lane' : isEcom ? 'Revenue Lane' : isMedia ? 'Yield Lane' : isStaffing ? 'Throughput Lane' : isStudio ? 'Velocity Lane' : 'Governance Lane'}</p>
          <p className="mt-4 text-xs font-bold uppercase leading-tight text-muted-foreground">
            {isDigitalItGirl
              ? 'Market signals, audience trends, and competitive gaps stay current.'
              : isEcom
              ? 'Omni-channel revenue, inventory, and campaign integrity stay current.'
              : isMedia
              ? 'Subscription yield, ad revenue, and distribution audit stay current.'
              : isStaffing
              ? 'Fill rates, candidate throughput, and placement audit stay current.'
              : isStudio
              ? 'Project timelines, delivery milestones, and utilization audit stay current.'
              : 'Fiscal reporting, audit trails, and institutional oversight stay current.'}
          </p>
          </div>
          <div className="brutalist-card">
          <Briefcase className="h-6 w-6 text-secondary" />
          <p className="mt-6 text-sm font-black uppercase tracking-widest">{isDigitalItGirl ? 'Gap Lane' : isMedia ? 'Distribution Lane' : isStaffing ? 'Acquisition Lane' : isStudio ? 'Delivery Lane' : 'Executive Lane'}</p>
          <p className="mt-4 text-xs font-bold uppercase leading-tight text-muted-foreground">
            {isDigitalItGirl
              ? 'Strategic positioning and authority mapping stay in line.'
              : isEcom
              ? 'Multi-channel logistics and fulfillment integrity stay in line.'
              : isMedia
              ? 'Content reach and distribution growth stay in line.'
              : isStaffing
              ? 'Acquisition velocity and placement conversion stay in line.'
              : isStudio
              ? 'Delivery standards and quality output stay in line.'
              : 'Operational flows and client integration stay in line.'}
          </p>
          </div>
          <div className="brutalist-card">
          <ShieldCheck className="h-6 w-6 text-primary" />
          <p className="mt-6 text-sm font-black uppercase tracking-widest">Control Lane</p>
          <p className="mt-4 text-xs font-bold uppercase leading-tight text-muted-foreground">
            {isDigitalItGirl
              ? 'Approvals, watchlists, and monetization frameworks stay visible.'
              : isEcom
              ? 'Approvals, supply risk, and margin preservation stay visible.'
              : isMedia
              ? 'Approvals, audience health, and yield risk stay visible.'
              : isStaffing
              ? 'Approvals, compliance, and margin integrity stay visible.'
              : isStudio
              ? 'Approvals, resource allocation, and utilization stay visible.'
              : 'Approvals, governance risk, and fiscal integrity stay visible.'}
          </p>
          </div>
        </div>

        <div className="brutalist-card mt-8 bg-black text-white">
          <div className="flex flex-col gap-8 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="font-black text-xs uppercase tracking-[0.5em] text-primary">System Integrity</p>
              <h3 className="text-3xl font-black uppercase mt-4 max-w-2xl">
                {isDigitalItGirl
                  ? 'ENGINEERED FOR NICHE OPERATORS SECURING MARKET AUTHORITY.'
                  : isEcom
                  ? 'ENGINEERED FOR COMMERCE OPERATORS SECURING MARGIN INTEGRITY.'
                  : isMedia
                  ? 'ENGINEERED FOR MEDIA OPERATORS SECURING CONTENT YIELD.'
                  : isStaffing
                  ? 'ENGINEERED FOR STAFFING OPERATORS SECURING THROUGHPUT.'
                  : isStudio
                  ? 'ENGINEERED FOR STUDIO OPERATORS SECURING DELIVERY STANDARDS.'
                  : 'ENGINEERED FOR EXECUTIVE OPERATORS SECURING INSTITUTIONAL CONTROL.'}
              </h3>
            </div>
            <div className="border-4 border-primary bg-white px-8 py-6 text-black shadow-[4px_4px_0px_0px_rgba(255,255,255,0.3)]">
              <Radar className="h-8 w-8 text-primary" />
              <p className="mt-4 text-xs font-black uppercase tracking-widest text-muted-foreground">Operational Status</p>
              <p className="mt-2 text-sm font-bold uppercase">All systems active and synced.</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
