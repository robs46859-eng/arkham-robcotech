'use client'

import Link from 'next/link'
import { ArrowRight, Briefcase, Building2, FileStack, Radar, ShieldCheck, BarChart3, PieChart, Activity, TrendingUp } from 'lucide-react'

const activeVertical = process.env.NEXT_PUBLIC_VERTICAL || 'saas'
const isEcom = activeVertical === 'ecommerce'
const isDigitalItGirl = activeVertical === 'digital_it_girl'
const isMedia = activeVertical === 'media'
const isStaffing = activeVertical === 'staffing'
const isStudio = activeVertical === 'studio'

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
                {isDigitalItGirl ? 'Market Intelligence' : isEcom ? 'Commerce Systems' : isMedia ? 'Content Yield' : isStaffing ? 'Talent Throughput' : isStudio ? 'Delivery Standards' : 'Operational Control'}
              </h1>
            </div>
          </Link>

          <nav className="flex flex-wrap items-center gap-6 text-xs font-black uppercase tracking-widest text-black">
            <Link href="/legal" className="hover:underline">Legal</Link>
            <Link href="/pricing" className="hover:underline">Pricing</Link>
            <Link href="/login" className="hover:underline">Login</Link>
            <Link href="/signup" className="brutalist-button-blue py-2 px-4 border-2">Initialize</Link>
          </nav>
        </div>
      </header>

      <section className="shell grid gap-8 py-12 md:grid-cols-[1.35fr_0.65fr] md:py-20">
        <div className="brutalist-card">
          <p className="font-black text-secondary uppercase tracking-[0.2em] text-xs">
            {isDigitalItGirl ? 'Authority Framework' : isEcom ? 'Commerce OS' : isMedia ? 'Yield System' : isStaffing ? 'Resource Engine' : isStudio ? 'Delivery OS' : 'Control System'}
          </p>
          <h2 className="text-4xl md:text-7xl font-black mt-6 leading-[0.85] uppercase">
            {isDigitalItGirl
              ? 'DEPLOY AUTHORITY.'
              : isEcom
              ? 'PRESERVE MARGIN.'
              : isMedia
              ? 'OPTIMIZE YIELD.'
              : isStaffing
              ? 'MAXIMIZE THROUGHPUT.'
              : isStudio
              ? 'STANDARDIZE DELIVERY.'
              : 'ESTABLISH OVERSIGHT.'}
          </h2>
          
          {/* VISUAL CHART SECTION */}
          <div className="mt-12 grid grid-cols-3 gap-4 border-4 border-black bg-gray-100 p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
             <div className="flex flex-col items-center">
                <BarChart3 size={32} className="text-primary mb-2" />
                <div className="h-16 w-full flex items-end gap-1">
                   <div className="bg-primary w-1/4 h-[40%] border-2 border-black"></div>
                   <div className="bg-primary w-1/4 h-[70%] border-2 border-black"></div>
                   <div className="bg-primary w-1/4 h-[90%] border-2 border-black"></div>
                   <div className="bg-primary w-1/4 h-[60%] border-2 border-black"></div>
                </div>
             </div>
             <div className="flex flex-col items-center border-l-2 border-black px-4">
                <PieChart size={32} className="text-secondary mb-2" />
                <div className="relative h-16 w-16 rounded-full border-4 border-black bg-white overflow-hidden">
                   <div className="absolute top-0 left-0 w-full h-full bg-secondary rotate-45 origin-center"></div>
                </div>
             </div>
             <div className="flex flex-col items-center border-l-2 border-black">
                <Activity size={32} className="text-black mb-2" />
                <div className="h-16 w-full flex items-center justify-center">
                   <TrendingUp size={48} strokeWidth={3} className="text-primary" />
                </div>
             </div>
          </div>

          <div className="mt-12 flex flex-wrap gap-4">
            <Link href="/pricing" className="brutalist-button">
              DEPLOY TIER
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </div>
        </div>

        <aside className="brutalist-card flex flex-col justify-center bg-gray-50">
          <p className="font-black text-xs uppercase tracking-[0.2em] mb-6">Snapshot</p>
          <div className="space-y-6">
            <div className="border-4 border-black bg-white p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
              <p className="text-[10px] font-black uppercase tracking-widest text-muted-foreground">Confidence Rating</p>
              <p className="mt-3 text-6xl font-black text-primary">93%</p>
              <div className="mt-4 h-4 w-full bg-gray-200 border-2 border-black overflow-hidden">
                 <div className="h-full bg-primary border-r-2 border-black" style={{width: '93%'}}></div>
              </div>
            </div>
            <div className="border-4 border-black bg-secondary p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] text-white">
              <p className="text-[10px] font-black uppercase tracking-widest opacity-80">Sync Status</p>
              <div className="mt-3 flex items-center gap-4">
                 <div className="h-3 w-3 rounded-full bg-primary animate-pulse border border-white"></div>
                 <p className="text-lg font-black uppercase tracking-tighter">ALL LANES ACTIVE</p>
              </div>
            </div>
          </div>
        </aside>
      </section>

      <section id="offer" className="shell py-6">
        <div className="brutalist-card bg-white">
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
             <div className="border-4 border-black p-4 text-center hover:bg-primary/10 transition-colors">
                <Radar size={32} className="mx-auto text-secondary mb-3" />
                <p className="text-[10px] font-black uppercase">Market Audit</p>
             </div>
             <div className="border-4 border-black p-4 text-center hover:bg-primary/10 transition-colors">
                <ShieldCheck size={32} className="mx-auto text-secondary mb-3" />
                <p className="text-[10px] font-black uppercase">Governance</p>
             </div>
             <div className="border-4 border-black p-4 text-center hover:bg-primary/10 transition-colors">
                <Briefcase size={32} className="mx-auto text-secondary mb-3" />
                <p className="text-[10px] font-black uppercase">Acquisition</p>
             </div>
             <div className="border-4 border-black p-4 text-center hover:bg-primary/10 transition-colors">
                <FileStack size={32} className="mx-auto text-secondary mb-3" />
                <p className="text-[10px] font-black uppercase">Reporting</p>
             </div>
          </div>
        </div>
      </section>

      <section id="systems" className="shell py-6">
        <div className="brutalist-card bg-black text-white p-12">
          <div className="flex flex-col gap-12 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="font-black text-xs uppercase tracking-[0.5em] text-primary">Operational Matrix</p>
              <h3 className="text-4xl md:text-6xl font-black uppercase mt-6 max-w-2xl leading-none">
                {isDigitalItGirl ? 'AUTHORITY.' : isEcom ? 'MARGIN.' : isMedia ? 'YIELD.' : isStaffing ? 'THROUGHPUT.' : isStudio ? 'DELIVERY.' : 'OVERSIGHT.'}
              </h3>
            </div>
            <div className="bg-white p-8 border-4 border-primary text-black shadow-[12px_12px_0px_0px_rgba(255,255,255,0.2)]">
              <Activity className="h-12 w-12 text-primary" />
              <p className="mt-4 text-xl font-black uppercase">CONNECTED</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
