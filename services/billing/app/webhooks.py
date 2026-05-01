"""
Billing Service Webhooks

Handles Stripe webhook events for:
- Subscription changes
- Payment success/failure
- Dunning management
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, Request, HTTPException, Header
from pydantic import BaseModel

from app.settings import settings
from app.stripe_service import StripeService
from app.metering import UsageMeter
from app.email_service import email_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/billing", tags=["billing"])

# Initialize Stripe service
stripe_service = StripeService(
    secret_key=settings.stripe_secret_key,
    webhook_secret=settings.stripe_webhook_secret,
)

# Initialize usage meter
usage_meter = UsageMeter(settings.database_url)


class WebhookResponse(BaseModel):
    received: bool
    event_type: str
    handled: bool
    data: Dict[str, Any]


@router.post("/webhook", response_model=WebhookResponse)
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
):
    """
    Handle Stripe webhook events
    
    Events handled:
    - checkout.session.completed
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    # Get raw payload
    payload = await request.body()
    
    # Verify signature
    try:
        event = stripe_service.verify_webhook_signature(payload, stripe_signature)
    except Exception as e:
        logger.error(f"Webhook signature verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle event
    try:
        result = await stripe_service.handle_webhook_event(event)
        
        # Process event-specific logic
        if event.type == "invoice.payment_succeeded":
            await _handle_payment_succeeded(event, result)
        
        elif event.type == "invoice.payment_failed":
            await _handle_payment_failed(event, result)
        
        elif event.type == "customer.subscription.updated":
            await _handle_subscription_updated(event, result)
        
        elif event.type == "customer.subscription.deleted":
            await _handle_subscription_deleted(event, result)
        
        return WebhookResponse(
            received=True,
            event_type=event.type,
            handled=result.get("handled", False),
            data=result,
        )
        
    except Exception as e:
        logger.error(f"Webhook handler failed: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")


async def _handle_payment_succeeded(event, result: Dict[str, Any]):
    """Handle successful payment - update billing records"""
    tenant_id = result.get("tenant_id")
    invoice_id = result.get("invoice_id")
    amount = result.get("amount", 0) / 100  # Convert from cents
    
    if tenant_id:
        # Update billing record
        await usage_meter.update_billing_status(
            tenant_id=tenant_id,
            stripe_invoice_id=invoice_id,
            status="paid",
        )
        
        logger.info(f"Payment succeeded for tenant {tenant_id}: ${amount}")


async def _handle_payment_failed(event, result: Dict[str, Any]):
    """Handle failed payment - trigger dunning sequence"""
    tenant_id = result.get("tenant_id")
    invoice_id = result.get("invoice_id")
    customer_id = result.get("customer_id")
    
    if tenant_id:
        # Update billing record
        await usage_meter.update_billing_status(
            tenant_id=tenant_id,
            stripe_invoice_id=invoice_id,
            status="failed",
        )
        
        # Send payment reminder
        await stripe_service.send_payment_reminder(customer_id, invoice_id)
        
        # TODO: Implement dunning sequence logic
        # - Day 1: Send reminder email
        # - Day 3: Send second reminder
        # - Day 7: Suspend service
        # - Day 14: Cancel subscription
        
        logger.warning(f"Payment failed for tenant {tenant_id} - dunning initiated")


async def _handle_subscription_updated(event, result: Dict[str, Any]):
    """Handle subscription update - update tenant plan"""
    tenant_id = result.get("tenant_id")
    subscription_id = result.get("subscription_id")
    status = result.get("status")
    
    if tenant_id:
        # Update tenant subscription in database
        await usage_meter.update_tenant_subscription(
            tenant_id=tenant_id,
            stripe_subscription_id=subscription_id,
            status=status,
        )
        
        logger.info(f"Subscription updated for tenant {tenant_id}: {status}")


async def _handle_subscription_deleted(event, result: Dict[str, Any]):
    """Handle subscription deletion - downgrade tenant to free"""
    tenant_id = result.get("tenant_id")
    
    if tenant_id:
        # Downgrade tenant to free plan
        await usage_meter.downgrade_tenant_plan(tenant_id, "free")
        
        logger.info(f"Subscription deleted for tenant {tenant_id} - downgraded to free")
