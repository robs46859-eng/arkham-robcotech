"""Stripe integration for founder package checkout."""

import logging
from typing import Dict, Any, Optional
from decimal import Decimal

from app.settings import settings

logger = logging.getLogger(__name__)


class StripeService:
    """Stripe payment integration"""
    
    def __init__(
        self,
        secret_key: str,
        webhook_secret: str,
    ):
        self.secret_key = secret_key
        self.webhook_secret = webhook_secret
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization of Stripe client"""
        if self._client is None:
            import stripe
            stripe.api_key = self.secret_key
            self._client = stripe
        return self._client
    
    async def create_customer(
        self,
        email: str,
        name: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Create a Stripe customer"""
        try:
            existing = self.client.Customer.list(email=email, limit=1)
            if getattr(existing, "data", None):
                customer = existing.data[0]
                return {
                    "id": customer.id,
                    "email": customer.email,
                    "name": customer.name,
                }

            customer = self.client.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {},
            )
            
            logger.info(f"Created Stripe customer: {customer.id}")
            
            return {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name,
            }
        except Exception as e:
            logger.error(f"Failed to create Stripe customer: {e}")
            raise
    
    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
    ) -> Dict[str, Any]:
        """Create a subscription for a customer"""
        try:
            subscription = self.client.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.payment_intent"],
            )
            
            logger.info(f"Created Stripe subscription: {subscription.id}")
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
            }
        except Exception as e:
            logger.error(f"Failed to create Stripe subscription: {e}")
            raise

    async def create_checkout_session(
        self,
        customer_id: str,
        plan: str,
        commitment: str,
        amount: Decimal,
        success_url: str,
        cancel_url: str,
        customer_email: str,
        customer_name: str,
        company_name: str,
    ) -> Dict[str, Any]:
        """Create a no-trial Stripe Checkout session for monthly or 3-month billing."""
        plan_catalog = settings.pricing
        plan_config = plan_catalog.get(plan)

        if not plan_config:
            raise ValueError(f"Invalid plan: {plan}")

        amount_cents = int((amount * Decimal("100")).quantize(Decimal("1")))
        metadata = {
            "plan": plan,
            "commitment": commitment,
            "customer_email": customer_email,
            "customer_name": customer_name,
            "company_name": company_name,
        }

        try:
            if commitment == "quarterly":
                session = self.client.checkout.Session.create(
                    customer=customer_id,
                    mode="payment",
                    line_items=[{
                        "quantity": 1,
                        "price_data": {
                            "currency": settings.stripe_currency,
                            "unit_amount": amount_cents,
                            "product_data": {
                                "name": f"{plan_config['name']} - 3-Month Commitment",
                                "description": "35% discount applied to the 3-month founder package commitment.",
                            },
                        },
                    }],
                    success_url=success_url,
                    cancel_url=cancel_url,
                    metadata=metadata,
                    invoice_creation={"enabled": True},
                )
            else:
                session = self.client.checkout.Session.create(
                    customer=customer_id,
                    mode="subscription",
                    line_items=[{
                        "quantity": 1,
                        "price_data": {
                            "currency": settings.stripe_currency,
                            "unit_amount": amount_cents,
                            "recurring": {"interval": "month"},
                            "product_data": {
                                "name": plan_config["name"],
                                "description": plan_config["name"],
                            },
                        },
                    }],
                    success_url=success_url,
                    cancel_url=cancel_url,
                    metadata=metadata,
                    subscription_data={"metadata": metadata},
                )

            return {
                "id": session.id,
                "url": session.url,
                "plan": plan,
                "commitment": commitment,
                "amount": float(amount),
            }
        except Exception as e:
            logger.error(f"Failed to create checkout session: {e}")
            raise
    
    async def create_invoice(
        self,
        customer_id: str,
        amount: float,
        description: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Create an invoice for usage-based billing"""
        try:
            invoice = self.client.Invoice.create(
                customer=customer_id,
                description=description,
                metadata=metadata or {},
            )
            
            # Add line item
            self.client.InvoiceItem.create(
                customer=customer_id,
                invoice=invoice.id,
                amount=int(amount * 100),  # Convert to cents
                currency="usd",
                description=description,
            )
            
            # Finalize invoice
            invoice = self.client.Invoice.finalize_invoice(invoice.id)
            
            logger.info(f"Created Stripe invoice: {invoice.id}")
            
            return {
                "id": invoice.id,
                "status": invoice.status,
                "amount_due": invoice.amount_due,
                "hosted_invoice_url": invoice.hosted_invoice_url,
            }
        except Exception as e:
            logger.error(f"Failed to create Stripe invoice: {e}")
            raise
    
    async def cancel_subscription(
        self,
        subscription_id: str,
    ) -> Dict[str, Any]:
        """Cancel a subscription"""
        try:
            subscription = self.client.Subscription.cancel(subscription_id)
            
            logger.info(f"Cancelled Stripe subscription: {subscription_id}")
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "ended_at": subscription.ended_at,
            }
        except Exception as e:
            logger.error(f"Failed to cancel Stripe subscription: {e}")
            raise
    
    def verify_webhook(
        self,
        payload: bytes,
        sig_header: str,
    ) -> Dict[str, Any]:
        """Verify webhook signature and return event"""
        try:
            event = self.client.Webhook.construct_event(
                payload,
                sig_header,
                self.webhook_secret,
            )
            
            return {
                "id": event.id,
                "type": event.type,
                "data": event.data.object,
            }
        except Exception as e:
            logger.error(f"Failed to verify webhook: {e}")
            raise
    
    async def get_usage_record(
        self,
        subscription_item_id: str,
        timestamp: int,
    ) -> Optional[Dict[str, Any]]:
        """Get usage record for a subscription item"""
        # Implementation for metered billing
        pass
    
    async def create_usage_record(
        self,
        subscription_item_id: str,
        quantity: int,
        timestamp: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create usage record for metered billing"""
        try:
            usage_record = self.client.SubscriptionItem.create_usage_record(
                subscription_item_id,
                quantity=quantity,
                timestamp=timestamp,
                action="set",
            )
            
            return {
                "id": usage_record.id,
                "quantity": usage_record.quantity,
                "timestamp": usage_record.timestamp,
            }
        except Exception as e:
            logger.error(f"Failed to create usage record: {e}")
            raise
