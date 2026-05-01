'use client'

import Link from 'next/link'
import { ArrowLeft, ArrowRight, Gavel, Scale, ShieldAlert, Zap, Clock, Users, Database, Globe, Lock, CheckCircle2 } from 'lucide-react'

export default function LegalVertical() {
  return (
    <main className="min-h-screen pt-24 pb-16 px-4 md:px-8">
      {/* TICKER */}
      <div className="ticker-wrap">
        <div className="ticker">
          LEGAL PRACTICE AUTHORITY // CASE DATA SYNCED // REGULATORY COMPLIANCE SECURED // ZERO-TRUST ENCRYPTION ACTIVE // DOCUMENT AUTOMATION ENGINE: READY //
        </div>
      </div>

      <div className="mx-auto max-w-6xl">
        {/* NAV */}
        <div className="mb-12 flex items-center justify-between">
          <Link href="/" className="brutalist-button bg-white text-black">
            <ArrowLeft className="mr-2 h-4 w-4" />
            BACK
          </Link>
          <Link href="/pricing?vertical=legal" className="brutalist-button-blue">
            ESTABLISH FIRM
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </div>

        {/* HERO */}
        <section className="brutalist-card mb-12">
          <div className="grid gap-12 lg:grid-cols-[1.2fr_0.8fr]">
            <div>
              <p className="display-kicker">Legal Practice Infrastructure</p>
              <h1 className="mt-6 text-5xl md:text-7xl leading-[0.85]">
                MODERNIZE THE PRACTICE. SECURE THE PRECEDENT.
              </h1>
              <p className="mt-8 text-xl font-bold uppercase tracking-tight text-muted-foreground leading-tight">
                ELIMINATE ADMINISTRATIVE FRICTION THROUGH AUTONOMOUS LEGAL OPERATIONS.
              </p>
              
              <div className="mt-12 grid grid-cols-2 gap-4">
                <div className="border-4 border-black p-4 bg-primary text-black font-black uppercase text-center text-xs">
                   90% TASK AUTOMATION
                </div>
                <div className="border-4 border-black p-4 bg-secondary text-white font-black uppercase text-center text-xs">
                   ISO 27001 ALIGNED
                </div>
              </div>
            </div>

            <div className="flex items-center justify-center bg-gray-100 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-8">
               <Scale size={180} strokeWidth={1} className="text-black" />
            </div>
          </div>
        </section>

        {/* VALUE PROPS - ICONS & POINTED COPY */}
        <section className="grid gap-8 md:grid-cols-2 lg:grid-cols-3 mb-16">
           <div className="brutalist-card flex flex-col items-center text-center">
              <Zap size={48} className="text-primary mb-6" />
              <h3 className="font-black uppercase mb-4">Increased Efficiency</h3>
              <p className="text-xs font-bold uppercase leading-tight opacity-70">
                Automate document review, legal research, and timekeeping. focus on complex billable work.
              </p>
           </div>
           <div className="brutalist-card flex flex-col items-center text-center">
              <Users size={48} className="text-secondary mb-6" />
              <h3 className="font-black uppercase mb-4">Enhanced Service</h3>
              <p className="text-xs font-bold uppercase leading-tight opacity-70">
                Deliver faster, accurate, cost-effective services. Meet modern client expectations.
              </p>
           </div>
           <div className="brutalist-card flex flex-col items-center text-center">
              <Globe size={48} className="text-black mb-6" />
              <h3 className="font-black uppercase mb-4">Competitive Benefit</h3>
              <p className="text-xs font-bold uppercase leading-tight opacity-70">
                Surpass competitors through innovation. Attract and retain high-value clients.
              </p>
           </div>
           <div className="brutalist-card flex flex-col items-center text-center">
              <Clock size={48} className="text-primary mb-6" />
              <h3 className="font-black uppercase mb-4">Cost Savings</h3>
              <p className="text-xs font-bold uppercase leading-tight opacity-70">
                Eliminate on-premise hardware. Use AI-powered research to slash convention expenses.
              </p>
           </div>
           <div className="brutalist-card flex flex-col items-center text-center">
              <Lock size={48} className="text-secondary mb-6" />
              <h3 className="font-black uppercase mb-4">Data Protection</h3>
              <p className="text-xs font-bold uppercase leading-tight opacity-70">
                Implement best-in-class tools to maintain confidentiality and secure client data.
              </p>
           </div>
           <div className="brutalist-card flex flex-col items-center text-center">
              <CheckCircle2 size={48} className="text-black mb-6" />
              <h3 className="font-black uppercase mb-4">Compliance</h3>
              <p className="text-xs font-bold uppercase leading-tight opacity-70">
                Track deadlines and manage legal documents with automated regulatory oversight.
              </p>
           </div>
        </section>

        {/* VIRTUAL ASSISTANTS SECTION */}
        <section className="brutalist-card bg-black text-white mb-12">
          <div className="flex flex-col lg:flex-row items-center gap-12">
             <div className="lg:w-1/2">
                <Gavel size={64} className="text-primary mb-6" />
                <h2 className="text-4xl font-black mb-6">VIRTUAL LEGAL ASSISTANTS.</h2>
                <p className="text-sm font-bold uppercase leading-relaxed opacity-80">
                   Enhance productivity with technology-based legal support. 
                   Paralegal-grade assistance for document management, research, and drafting.
                </p>
             </div>
             <div className="lg:w-1/2 grid grid-cols-1 gap-4">
                <div className="border-2 border-white/20 p-4 font-black uppercase tracking-widest text-xs">
                   // RESEARCH AUTOMATION: ACTIVE
                </div>
                <div className="border-2 border-white/20 p-4 font-black uppercase tracking-widest text-xs">
                   // DRAFTING ENGINE: ACTIVE
                </div>
                <div className="border-2 border-white/20 p-4 font-black uppercase tracking-widest text-xs">
                   // DOCUMENT MGMT: ACTIVE
                </div>
             </div>
          </div>
        </section>

        {/* CALL TO ACTION */}
        <div className="text-center mt-20">
           <Link href="/pricing?vertical=legal" className="brutalist-button px-16">
              INITIALIZE LEGAL STACK
           </Link>
        </div>
      </div>
    </main>
  )
}
