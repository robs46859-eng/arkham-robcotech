"""Billing Service Settings - Updated with Stripe"""

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
    
    # Stripe
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    stripe_price_id_basic: str = os.getenv("STRIPE_PRICE_ID_BASIC", "")
    stripe_price_id_pro: str = os.getenv("STRIPE_PRICE_ID_PRO", "")
    stripe_price_id_enterprise: str = os.getenv("STRIPE_PRICE_ID_ENTERPRISE", "")
    stripe_currency: str = "usd"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
