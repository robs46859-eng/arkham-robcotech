import type { Metadata } from 'next'
import { Monoton, Roboto } from 'next/font/google'
import './globals.css'

const monoton = Monoton({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-monoton',
  display: 'swap',
})

const roboto = Roboto({
  weight: ['400', '700'],
  subsets: ['latin'],
  variable: '--font-roboto',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'RobcoTech Pro',
  description: 'Enterprise operations, performance reporting, workflow control, and executive oversight in one system.',
  metadataBase: new URL(process.env.APP_URL || 'https://robcotech.pro'),
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${monoton.variable} ${roboto.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}

