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
      {/* HEADLESS HEADER */}
      <header className="fixed top-0 left-0 w-full z-50 bg-transparent">
        <div className="shell flex flex-col gap-6 py-6 md:flex-row md:items-center md:justify-between">
          <Link href="/" className="flex items-start gap-4 group">
            <div className="flex h-12 w-12 items-center justify-center border-4 border-black bg-primary text-black shadow-[4px_4px_0_rgba(0,0,0,1)] group-hover:bg-secondary transition-colors">
              <FileStack className="h-6 w-6" />
            </div>
            <div>
              <p className="font-black text-secondary uppercase tracking-[0.2em] text-[10px]">RobcoTech Pro</p>
              <h1 className="text-xl font-black uppercase tracking-tighter">
                {isDigitalItGirl ? 'Market Intelligence' : isEcom ? 'Commerce Systems' : isMedia ? 'Content Yield' : isStaffing ? 'Talent Throughput' : isStudio ? 'Delivery Standards' : 'Operational Control'}
              </h1>
            </div>
          </Link>

          <nav className="flex flex-wrap items-center gap-6 text-xs font-black uppercase tracking-widest text-black">
            <Link href="/legal" className="hover:underline">Legal</Link>
            <Link href="/pricing" className="hover:underline">Pricing</Link>
            <Link href="/login" className="hover:underline">Login</Link>
            <Link href="/signup" className="brutalist-button-blue py-2 px-4 border-2 !shadow-[2px_2px_0_rgba(0,0,0,1)] hover:!shadow-[4px_4px_0_rgba(0,0,0,1)]">Initialize</Link>
          </nav>
        </div>
      </header>

      {/* HERO SECTION WITH FADE-IN */}
      <section className="shell grid gap-8 pt-32 pb-12 md:grid-cols-[1.35fr_0.65fr] md:pt-48 md:pb-20 animate-fade-in opacity-0">
        <div className="brutalist-card">
          <p className="font-black text-secondary uppercase tracking-[0.3em] text-xs mb-4">
            {isDigitalItGirl ? 'Authority Framework' : isEcom ? 'Commerce OS' : isMedia ? 'Yield System' : isStaffing ? 'Resource Engine' : isStudio ? 'Delivery OS' : 'Control System'}
          </p>
          
          <h2 className="text-5xl md:text-8xl font-black leading-[0.8] uppercase mb-8">
            <span className="block text-2xl md:text-4xl mb-2 text-primary">RobCoTech</span>
            FullStackAi Systems
          </h2>

          <p className="text-xl md:text-2xl font-black uppercase tracking-tight text-black mb-6">
            Architecting the technical foundation for next-generation businesses.
          </p>

          <p className="mt-8 max-w-3xl text-sm md:text-base font-bold leading-relaxed text-muted-foreground uppercase mb-10">
            From HIPAA-compliant data architectures and secure payment gateways to scalable cloud infrastructure, 
            we deliver enterprise-grade engineering. Build with confidence on a platform designed for zero-trust security, 
            seamless integration, and uncompromised performance.
          </p>

          <div className="flex flex-wrap gap-4">
            <Link href="/pricing" className="brutalist-button text-lg">
              VIEW PRICING & DEPLOYMENT
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </div>

          {/* VISUAL CHART SECTION (ICONIFIED) */}
          <div className="mt-16 grid grid-cols-4 gap-6 border-4 border-black bg-gray-100 p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
             <div className="flex flex-col items-center gap-3">
                <BarChart3 size={32} className="text-primary" />
                <p className="text-[10px] font-black uppercase">Analytics</p>
             </div>
             <div className="flex flex-col items-center gap-3 border-l-2 border-black">
                <PieChart size={32} className="text-secondary" />
                <p className="text-[10px] font-black uppercase">Segmentation</p>
             </div>
             <div className="flex flex-col items-center gap-3 border-l-2 border-black">
                <Activity size={32} className="text-black" />
                <p className="text-[10px] font-black uppercase">Live Ops</p>
             </div>
             <div className="flex flex-col items-center gap-3 border-l-2 border-black">
                <TrendingUp size={32} className="text-primary" />
                <p className="text-[10px] font-black uppercase">Growth</p>
             </div>
          </div>
        </div>

        <aside className="brutalist-card flex flex-col justify-center bg-gray-50/50 backdrop-blur-sm">
          <p className="font-black text-xs uppercase tracking-[0.2em] mb-6">Operational Pulse</p>
          <div className="space-y-8">
            <div className="border-4 border-black bg-white p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
              <p className="text-[10px] font-black uppercase tracking-widest text-muted-foreground mb-4 text-center">System Integrity</p>
              <div className="relative h-32 w-32 mx-auto">
                 {/* CSS Radial Chart Placeholder */}
                 <div className="absolute inset-0 rounded-full border-[12px] border-gray-200"></div>
                 <div className="absolute inset-0 rounded-full border-[12px] border-primary border-t-transparent border-r-transparent rotate-45"></div>
                 <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-3xl font-black">93%</span>
                 </div>
              </div>
            </div>
            
            <div className="border-4 border-black bg-secondary p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] text-white">
              <p className="text-[10px] font-black uppercase tracking-widest opacity-80 mb-4">Network Status</p>
              <div className="space-y-3">
                 <div className="flex items-center justify-between text-[10px] font-black">
                    <span>GATEWAY</span>
                    <span className="text-primary">ONLINE</span>
                 </div>
                 <div className="h-2 w-full bg-black/20 border border-white/20">
                    <div className="h-full bg-primary w-[88%]"></div>
                 </div>
                 <div className="flex items-center justify-between text-[10px] font-black">
                    <span>ORCHESTRATION</span>
                    <span className="text-primary">ACTIVE</span>
                 </div>
                 <div className="h-2 w-full bg-black/20 border border-white/20">
                    <div className="h-full bg-primary w-[94%]"></div>
                 </div>
              </div>
            </div>
          </div>
        </aside>
      </section>

      {/* SYSTEMS MATRIX */}
      <section id="systems" className="shell py-12">
        <div className="brutalist-card bg-black text-white p-12">
          <div className="flex flex-col gap-12 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="font-black text-xs uppercase tracking-[0.5em] text-primary mb-6">Execution Matrix</p>
              <h3 className="text-5xl md:text-7xl font-black uppercase leading-none">
                {isDigitalItGirl ? 'AUTHORITY' : isEcom ? 'REVENUE' : isMedia ? 'MONETIZE' : isStaffing ? 'ACQUIRE' : isStudio ? 'DELIVER' : 'CONTROL'}
                <br />
                <span className="text-primary">SECURED.</span>
              </h3>
            </div>
            <div className="grid grid-cols-2 gap-4">
               <div className="bg-white p-6 border-4 border-primary text-black flex flex-col items-center gap-2">
                  <ShieldCheck size={40} className="text-primary" />
                  <span className="text-[10px] font-black">AUDIT</span>
               </div>
               <div className="bg-white p-6 border-4 border-primary text-black flex flex-col items-center gap-2">
                  <Building2 size={40} className="text-primary" />
                  <span className="text-[10px] font-black">INFRA</span>
               </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
