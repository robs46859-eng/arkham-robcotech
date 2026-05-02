'use client'

import LogisticsDashboard from '@/components/verticals/logistics-dashboard'
import FintechDashboard from '@/components/verticals/fintech-dashboard'

export default function DashboardPage() {
  const activeVertical = process.env.NEXT_PUBLIC_VERTICAL || 'logistics'

  if (activeVertical === 'logistics') {
    return <LogisticsDashboard />
  }

  return <FintechDashboard />
}
