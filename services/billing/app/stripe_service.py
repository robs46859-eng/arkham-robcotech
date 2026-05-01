"""
Stripe Service - Single Price ID per Plan

    Handles subscriptions and checkout for founder packages.
"""

import stripe
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from decimal import Decimal

from app.settings import settings

logger = logging.getLogger(__name__)


class StripeService:
    """Stripe payment and billing service"""
    
    def __init__(self, secret_key: str = None, webhook_secret: str = None):
        stripe.api_key = secret_key or settings.stripe_secret_key
        self.webhook_secret = webhook_secret or settings.stripe_webhook_secret
        self.domain = settings.domain
    
    # ==================== SUBSCRIPTION MANAGEMENT ====================
    
    async def create_subscription(
        self,
        customer_id: str,
        plan: str,
        billing_cycle: str = "monthly",
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Create a subscription
        
        """
        if plan not in ["core", "executive"]:
            raise ValueError(f"Invalid plan: {plan}")
        
        # Get price ID for plan
        price_ids = settings.price_ids
        price_id = price_ids.get(plan)
        
        if not price_id:
            raise ValueError(f"No price ID found for plan: {plan}")
        
        try:
            subscription_params = {
                "customer": customer_id,
                "items": [{"price": price_id}],
                "payment_behavior": "default_incomplete",
                "payment_settings": {"save_default_payment_method": "on_subscription"},
                "expand": ["latest_invoice.payment_intent"],
                "metadata": {
                    "plan": plan,
                    "billing_cycle": billing_cycle,
                    "domain": self.domain,
                    **(metadata or {}),
                },
            }
            
            subscription = stripe.Subscription.create(**subscription_params)
            
            plan_name = settings.pricing[plan]["name"]
            logger.info(f"Created subscription for {plan_name}: {subscription.id}")
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "plan": plan,
                "billing_cycle": billing_cycle,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "latest_invoice": subscription.latest_invoice.id if subscription.latest_invoice else None,
                "client_secret": (
                    subscription.latest_invoice.payment_intent.client_secret
                    if subscription.latest_invoice and subscription.latest_invoice.payment_intent
                    else None
                ),
                "hosted_invoice_url": (
                    subscription.latest_invoice.hosted_invoice_url
                    if subscription.latest_invoice
                    else None
                ),
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create subscription: {e}")
            raise
    
    async def create_checkout_session(
        self,
        customer_id: str,
        plan: str,
        success_url: str,
        cancel_url: str,
    ) -> Dict[str, Any]:
        """
        Create a no-trial checkout session for founder packages.
        """
        price_id = settings.price_ids.get(plan)
        
        if not price_id:
            raise ValueError(f"No price ID found for plan: {plan}")
        
        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                mode="subscription",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "plan": plan,
                    "domain": self.domain,
                },
                subscription_data={
                    "metadata": {
                        "plan": plan,
                    }
                },
            )
            
            logger.info(f"Created checkout session: {session.id} for plan {plan}")
            
            return {
                "id": session.id,
                "url": session.url,
                "customer_id": customer_id,
                "plan": plan,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create checkout session: {e}")
            raise
    
    async def get_subscription(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription details"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "plan": subscription.metadata.get("plan"),
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "cancel_at_period_end": subscription.cancel_at_period_end,
            }
            
        except stripe.error.StripeError:
            return None
    
    async def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True,
    ) -> Dict[str, Any]:
        """Cancel a subscription"""
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True,
                )
            else:
                subscription = stripe.Subscription.cancel(subscription_id)
            
            logger.info(f"Cancelled subscription: {subscription_id}")
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "ended_at": subscription.ended_at,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription: {e}")
            raise
    
    # ==================== CUSTOMER MANAGEMENT ====================
    
    async def create_customer(
        self,
        tenant_id: str,
        email: str,
        name: str,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Create a Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    "tenant_id": tenant_id,
                    "domain": self.domain,
                    **(metadata or {}),
                },
            )
            
            logger.info(f"Created Stripe customer: {customer.id} for tenant {tenant_id}")
            
            return {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name,
                "tenant_id": tenant_id,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe customer: {e}")
            raise
    
    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get Stripe customer details"""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            
            return {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name,
                "metadata": customer.metadata,
            }
            
        except stripe.error.StripeError:
            return None
    
    # ==================== WEBHOOK PROCESSING ====================
    
    def verify_webhook_signature(
        self,
        payload: bytes,
        sig_header: str,
    ) -> stripe.Event:
        """Verify webhook signature and return event"""
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                self.webhook_secret,
            )
            
            logger.info(f"Verified webhook event: {event.type}")
            
            return event
            
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Webhook signature verification failed: {e}")
            raise
    
    async def handle_webhook_event(self, event: stripe.Event) -> Dict[str, Any]:
        """Handle webhook event based on type"""
        handlers = {
            "checkout.session.completed": self._handle_checkout_completed,
            "customer.subscription.updated": self._handle_subscription_updated,
            "customer.subscription.deleted": self._handle_subscription_deleted,
            "invoice.payment_succeeded": self._handle_invoice_succeeded,
            "invoice.payment_failed": self._handle_invoice_failed,
        }
        
        handler = handlers.get(event.type)
        
        if handler:
            return await handler(event)
        else:
            logger.info(f"Unhandled webhook event type: {event.type}")
            return {"handled": False, "event_type": event.type}
    
    async def _handle_checkout_completed(self, event: stripe.Event) -> Dict[str, Any]:
        """Handle checkout session completed"""
        session = event.data.object
        
        # Fetch full customer object to get email and name
        customer = stripe.Customer.retrieve(session.customer)
        
        return {
            "handled": True,
            "event_type": "checkout.session.completed",
            "customer_id": session.customer,
            "customer_email": customer.email,
            "customer_name": customer.name or customer.email,
            "subscription_id": session.subscription,
            "plan": session.metadata.get("plan"),
            "domain": session.metadata.get("domain"),
        }
    
    async def _handle_subscription_updated(self, event: stripe.Event) -> Dict[str, Any]:
        """Handle subscription updated"""
        subscription = event.data.object
        
        return {
            "handled": True,
            "event_type": "customer.subscription.updated",
            "subscription_id": subscription.id,
            "status": subscription.status,
            "plan": subscription.metadata.get("plan"),
            "tenant_id": subscription.metadata.get("tenant_id"),
        }
    
    async def _handle_subscription_deleted(self, event: stripe.Event) -> Dict[str, Any]:
        """Handle subscription deleted"""
        subscription = event.data.object
        
        return {
            "handled": True,
            "event_type": "customer.subscription.deleted",
            "subscription_id": subscription.id,
            "tenant_id": subscription.metadata.get("tenant_id"),
            "plan": subscription.metadata.get("plan"),
        }
    
    async def _handle_invoice_succeeded(self, event: stripe.Event) -> Dict[str, Any]:
        """Handle invoice payment succeeded"""
        invoice = event.data.object
        
        # Get customer details for email if needed
        customer = stripe.Customer.retrieve(invoice.customer)
        
        return {
            "handled": True,
            "event_type": "invoice.payment_succeeded",
            "invoice_id": invoice.id,
            "customer_id": invoice.customer,
            "customer_email": customer.email,
            "customer_name": customer.name or customer.email,
            "amount": invoice.amount_paid,
            "tenant_id": invoice.metadata.get("tenant_id"),
        }
    
    async def _handle_invoice_failed(self, event: stripe.Event) -> Dict[str, Any]:
        """Handle invoice payment failed"""
        invoice = event.data.object
        
        return {
            "handled": True,
            "event_type": "invoice.payment_failed",
            "invoice_id": invoice.id,
            "customer_id": invoice.customer,
            "amount": invoice.amount_due,
            "tenant_id": invoice.metadata.get("tenant_id"),
            "action_required": "dunning_sequence",
        }
