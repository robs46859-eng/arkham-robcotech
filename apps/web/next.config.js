/** @type {import('next').NextConfig} */
const isProduction = process.env.NODE_ENV === 'production'
const appDomain = process.env.APP_DOMAIN || 'robcotech.pro'
const apiDomain = process.env.API_DOMAIN || `api.${appDomain}`

const nextConfig = {
  reactStrictMode: true,
  env: {
    APP_DOMAIN: appDomain,
    API_DOMAIN: apiDomain,
    APP_URL: process.env.APP_URL || `https://${appDomain}`,
    API_URL: process.env.API_URL || `https://${apiDomain}`,
    GATEWAY_URL: process.env.GATEWAY_URL || (isProduction ? `https://${apiDomain}` : 'http://localhost:8080'),
    BILLING_URL: process.env.BILLING_URL || 'http://localhost:8086',
    BIM_INGESTION_URL: process.env.BIM_INGESTION_URL || 'http://localhost:8082',
    ORCHESTRATION_URL: process.env.ORCHESTRATION_URL || 'http://localhost:8083',
  },
}

module.exports = nextConfig
