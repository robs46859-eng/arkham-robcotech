import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'RobcoTech Pro',
  description: 'Founder operations, investor reporting, workflow control, and executive visibility in one system.',
  metadataBase: new URL(process.env.APP_URL || 'https://robcotech.pro'),
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
