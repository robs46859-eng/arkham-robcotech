/**
 * Application data and formatting utilities.
 * Recreated based on usage in billing components.
 */

export type Commitment = 'monthly' | 'quarterly';
export type PlanId = 'core' | 'executive';

export const commitmentDiscountRate = 0.20;

export const commitmentOptions = [
  {
    id: 'monthly' as Commitment,
    label: 'Month to Month',
    description: 'No commitment, pay as you go.',
  },
  {
    id: 'quarterly' as Commitment,
    label: '3-Month Lock',
    description: 'Save 20% with quarterly upfront billing.',
  },
];

export interface FeaturePlan {
  id: PlanId;
  name: string;
  price: number;
  narrative: string;
  features: string[];
  cta: string;
  borderClass: string;
  accentClass: string;
}

const baseFeatures = ['Workspace connection', 'Dashboard access'];

export const planDefinitions: FeaturePlan[] = [
  {
    id: 'core',
    name: 'Core Bundle',
    price: 49,
    narrative: 'Essential coverage for early-stage operations.',
    features: [...baseFeatures, '1 active project', 'Community access'],
    cta: 'Select Core',
    borderClass: 'border-border',
    accentClass: 'text-primary',
  },
  {
    id: 'executive',
    name: 'Executive Bundle',
    price: 199,
    narrative: 'Advanced control for scaling founders.',
    features: [...baseFeatures, 'Unlimited projects', 'Priority support', 'Board deck automation'],
    cta: 'Select Executive',
    borderClass: 'border-accent',
    accentClass: 'text-accent',
  },
];

// Vertical-specific plans (pointing to same structure)
export const digPlanDefinitions = planDefinitions;
export const ecomPlanDefinitions = planDefinitions;
export const mediaPlanDefinitions = planDefinitions;
export const staffPlanDefinitions = planDefinitions;

/**
 * Formats a number as USD currency.
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

/**
 * Calculates the monthly effective price for a quarterly commitment.
 */
export function getQuarterlyEffectiveMonthly(monthlyPrice: number): number {
  return monthlyPrice * (1 - commitmentDiscountRate);
}

/**
 * Calculates the quarterly upfront total.
 */
export function getQuarterlyUpfrontTotal(monthlyPrice: number): number {
  return getQuarterlyEffectiveMonthly(monthlyPrice) * 3;
}
