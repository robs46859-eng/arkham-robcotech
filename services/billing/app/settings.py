"""Billing Service settings for founder packages."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Service
    service_name: str = "billing"
    host: str = "0.0.0.0"
    port: int = 8086
    log_level: str = "info"
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/fullstackarkham"
    database_pool_size: int = 10
    
    # Stripe - API Keys
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # Optional Stripe price IDs. Dynamic price_data is used when IDs are not configured.
    stripe_price_id_core: str = os.getenv("STRIPE_PRICE_ID_CORE", os.getenv("STRIPE_PRICE_ID_BASIC", ""))
    stripe_price_id_executive: str = os.getenv("STRIPE_PRICE_ID_EXECUTIVE", os.getenv("STRIPE_PRICE_ID_PRO", ""))
    
    # Stripe - Configuration
    stripe_currency: str = "usd"
    stripe_yearly_discount_percent: int = 43  # Default discount for yearly
    
    # Domain
    domain: str = os.getenv("APP_DOMAIN", "stelar.host")
    
    pricing_core_monthly: int = 7599
    pricing_executive_monthly: int = 12599
    quarterly_commitment_discount_percent: int = 35
    
    @property
    def price_ids(self) -> dict:
        """Get price IDs by plan"""
        return {
            "core": self.stripe_price_id_core,
            "executive": self.stripe_price_id_executive,
        }
    
    @property
    def pricing(self) -> dict:
        """Get pricing display info"""
        quarterly_multiplier = (100 - self.quarterly_commitment_discount_percent) / 100

        return {
            "core": {
                "name": "Core Package",
                "monthly": self.pricing_core_monthly,
                "quarterly_effective_monthly": round(self.pricing_core_monthly * quarterly_multiplier, 2),
                "quarterly_upfront_total": round(self.pricing_core_monthly * quarterly_multiplier * 3, 2),
                "discount_percent": self.quarterly_commitment_discount_percent,
                "features": [
                    "DealFlow",
                    "FulfillmentOps",
                    "MediaCommerce",
                    "BudgetMind",
                    "BoardReady",
                ],
            },
            "executive": {
                "name": "Executive Package",
                "monthly": self.pricing_executive_monthly,
                "quarterly_effective_monthly": round(self.pricing_executive_monthly * quarterly_multiplier, 2),
                "quarterly_upfront_total": round(self.pricing_executive_monthly * quarterly_multiplier * 3, 2),
                "discount_percent": self.quarterly_commitment_discount_percent,
                "features": [
                    "ChiefPulse",
                    "ComplianceGate",
                    "ContentEngine",
                    "BoardReady Executive",
                    "Project Mind",
                ],
            },
        }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
