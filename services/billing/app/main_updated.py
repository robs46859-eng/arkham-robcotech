"""Billing Service Main - Updated with webhooks"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import settings
from app.webhooks import router as webhooks_router
from app.main import router as billing_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger.info("Starting Billing Service")
    
    # Initialize database connections
    # await init_database()
    
    yield
    
    logger.info("Shutting down Billing Service")


app = FastAPI(
    title="Billing Service",
    description="Usage metering and Stripe integration",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(billing_router)
app.include_router(webhooks_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "billing"}


@app.get("/ready")
async def ready_check():
    return {"status": "ready"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8086,
        reload=True,
    )
