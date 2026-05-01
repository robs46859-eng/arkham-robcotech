// Checkout API route for subscription creation
import { NextRequest, NextResponse } from 'next/server'

const BILLING_URL = process.env.BILLING_URL || 'http://localhost:8086'
const APP_DOMAIN = process.env.APP_DOMAIN || 'robcotech.pro'
const BASE_URL = process.env.NODE_ENV === 'production' 
  ? `https://${APP_DOMAIN}`
  : 'http://localhost:3000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { plan, commitment, tenantId, customerName, customerEmail, companyName } = body

    if (!plan || !tenantId || !customerName || !customerEmail || !companyName) {
      return NextResponse.json(
        { error: 'Missing required fields: plan, tenantId, customerName, customerEmail, companyName' },
        { status: 400 }
      )
    }

    const validPlans = ['core', 'executive']
    if (!validPlans.includes(plan)) {
      return NextResponse.json(
        { error: `Invalid plan. Must be one of: ${validPlans.join(', ')}` },
        { status: 400 }
      )
    }

    const validCommitments = ['monthly', 'quarterly']
    const resolvedCommitment = validCommitments.includes(commitment) ? commitment : 'monthly'

    const response = await fetch(`${BILLING_URL}/api/v1/billing/checkout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tenant_id: tenantId,
        plan,
        commitment: resolvedCommitment,
        customer_email: customerEmail,
        customer_name: customerName,
        company_name: companyName,
        success_url: `${BASE_URL}/billing/success?plan=${plan}&commitment=${resolvedCommitment}`,
        cancel_url: `${BASE_URL}/pricing`,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      return NextResponse.json(
        { error: error.message || 'Failed to create checkout session' },
        { status: response.status }
      )
    }

    const session = await response.json()

    return NextResponse.json({
      subscription: {
        id: session.id,
        url: session.url,
      },
      redirect_url: session.url,
    })

  } catch (error) {
    console.error('Checkout error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
