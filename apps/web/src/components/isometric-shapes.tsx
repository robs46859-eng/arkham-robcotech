'use client'

import React from 'react'

export function DiscoverShape() {
  return (
    <div className="relative w-16 h-16 flex items-center justify-center">
      {/* Glow shadow */}
      <div className="absolute w-12 h-6 bg-[hsl(var(--discover))] blur-xl opacity-20 rounded-full bottom-0 transform translate-y-2"></div>
      
      {/* Floating animation wrapper */}
      <div className="relative animate-[float_4s_ease-in-out_infinite] w-full h-full">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full drop-shadow-[0_0_10px_hsl(var(--discover)/0.5)]">
          {/* Isometric Diamond / Gem */}
          <path d="M50 10 L90 40 L50 90 L10 40 Z" fill="hsl(var(--discover))" fillOpacity="0.2" stroke="hsl(var(--discover))" strokeWidth="2" strokeLinejoin="round" />
          <path d="M50 10 L50 90" stroke="hsl(var(--discover))" strokeWidth="2" strokeOpacity="0.6" />
          <path d="M10 40 L90 40" stroke="hsl(var(--discover))" strokeWidth="2" strokeOpacity="0.6" />
          <path d="M50 10 L25 40 L50 90 L75 40 Z" stroke="hsl(var(--discover))" strokeWidth="1" strokeOpacity="0.8" fill="hsl(var(--discover))" fillOpacity="0.1" />
        </svg>
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-8px) rotate(2deg); }
        }
      `}</style>
    </div>
  )
}

export function MonitorShape() {
  return (
    <div className="relative w-16 h-16 flex items-center justify-center">
      {/* Glow shadow */}
      <div className="absolute w-14 h-6 bg-[hsl(var(--monitor))] blur-xl opacity-20 rounded-full bottom-0 transform translate-y-4"></div>
      
      {/* Floating animation wrapper */}
      <div className="relative animate-[pulse-float_5s_ease-in-out_infinite] w-full h-full">
        <svg viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full drop-shadow-[0_0_10px_hsl(var(--monitor)/0.4)]">
          {/* Top cube */}
          <g transform="translate(0, 0)">
            <path d="M50 10 L85 25 L50 40 L15 25 Z" fill="hsl(var(--monitor))" fillOpacity="0.3" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
            <path d="M15 25 L15 45 L50 60 L50 40 Z" fill="hsl(var(--monitor))" fillOpacity="0.1" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
            <path d="M85 25 L85 45 L50 60 L50 40 Z" fill="hsl(var(--monitor))" fillOpacity="0.2" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
          </g>
          
          {/* Middle cube */}
          <g transform="translate(0, 25)">
            <path d="M50 10 L85 25 L50 40 L15 25 Z" fill="hsl(var(--monitor))" fillOpacity="0.3" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
            <path d="M15 25 L15 45 L50 60 L50 40 Z" fill="hsl(var(--monitor))" fillOpacity="0.1" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
            <path d="M85 25 L85 45 L50 60 L50 40 Z" fill="hsl(var(--monitor))" fillOpacity="0.2" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
            {/* Server lights */}
            <circle cx="25" cy="40" r="2" fill="hsl(var(--discover))" className="animate-pulse" />
            <circle cx="32" cy="43" r="2" fill="hsl(var(--monitor))" />
          </g>

          {/* Bottom cube */}
          <g transform="translate(0, 50)">
            <path d="M50 10 L85 25 L50 40 L15 25 Z" fill="hsl(var(--monitor))" fillOpacity="0.3" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
            <path d="M15 25 L15 45 L50 60 L50 40 Z" fill="hsl(var(--monitor))" fillOpacity="0.1" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
            <path d="M85 25 L85 45 L50 60 L50 40 Z" fill="hsl(var(--monitor))" fillOpacity="0.2" stroke="hsl(var(--monitor))" strokeWidth="1.5" strokeLinejoin="round" />
            {/* Server lights */}
            <circle cx="25" cy="40" r="2" fill="hsl(var(--discover))" className="animate-pulse" style={{animationDelay: '1s'}} />
            <circle cx="32" cy="43" r="2" fill="hsl(var(--monitor))" />
          </g>
        </svg>
      </div>

      <style jsx>{`
        @keyframes pulse-float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-6px); filter: brightness(1.2); }
        }
      `}</style>
    </div>
  )
}

export function ConvertShape() {
  return (
    <div className="relative w-16 h-16 flex items-center justify-center">
      {/* Glow shadow */}
      <div className="absolute w-10 h-6 bg-[hsl(var(--convert))] blur-xl opacity-20 rounded-full bottom-0 transform translate-y-4"></div>
      
      {/* Floating animation wrapper */}
      <div className="relative animate-[heavy-float_3s_ease-in-out_infinite] w-full h-full">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full drop-shadow-[0_0_12px_hsl(var(--convert)/0.6)]">
          {/* Isometric Funnel Base */}
          <path d="M50 10 L90 25 L50 40 L10 25 Z" fill="hsl(var(--convert))" fillOpacity="0.15" stroke="hsl(var(--convert))" strokeWidth="1.5" strokeLinejoin="round" />
          <path d="M10 25 C10 25, 40 60, 45 90 L55 90 C60 60, 90 25, 90 25" fill="hsl(var(--convert))" fillOpacity="0.1" stroke="hsl(var(--convert))" strokeWidth="1.5" strokeLinejoin="round" />
          
          {/* Inside depth */}
          <path d="M50 15 L80 26 L50 35 L20 26 Z" stroke="hsl(var(--convert))" strokeWidth="1" strokeOpacity="0.5" />
          
          {/* Funnel rings */}
          <ellipse cx="50" cy="55" rx="15" ry="5" stroke="hsl(var(--convert))" strokeWidth="1" strokeOpacity="0.4" />
          <ellipse cx="50" cy="75" rx="8" ry="3" stroke="hsl(var(--convert))" strokeWidth="1" strokeOpacity="0.6" />

          {/* Particles */}
          <circle cx="50" cy="15" r="3" fill="hsl(var(--convert))" className="animate-[drop_2s_linear_infinite]" />
          <circle cx="35" cy="20" r="2" fill="hsl(var(--gold))" className="animate-[drop_2.5s_linear_infinite]" style={{animationDelay: '0.5s'}} />
          <circle cx="65" cy="25" r="2" fill="hsl(var(--convert))" className="animate-[drop_1.8s_linear_infinite]" style={{animationDelay: '1.2s'}} />
        </svg>
      </div>

      <style jsx>{`
        @keyframes heavy-float {
          0%, 100% { transform: translateY(0px) scale(1); }
          50% { transform: translateY(-5px) scale(1.02); }
        }
        @keyframes drop {
          0% { transform: translateY(-10px); opacity: 0; }
          20% { opacity: 1; }
          80% { transform: translateY(60px) scale(0.5); opacity: 0.8; }
          100% { transform: translateY(70px) scale(0); opacity: 0; }
        }
      `}</style>
    </div>
  )
}
