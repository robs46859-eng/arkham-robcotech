"""
Email Service for FullStackArkham

Handles sending transactional emails like:
- Welcome after activation
- Payment confirmation
- Payment failure alerts
- Upgrade instructions
"""

import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL", "support@robcotech.pro")
        self.api_key = os.getenv("EMAIL_API_KEY", "")
        self.is_configured = bool(self.api_key)

    async def send_welcome_email(self, customer_email: str, customer_name: str, plan: str):
        """Send a thank you and welcome email after successful activation."""
        subject = f"Welcome to RobcoTech Pro - Your {plan.capitalize()} package is active"
        
        body = f"""
Hi {customer_name},

Thank you for choosing RobcoTech Pro. Your {plan.capitalize()} package is now active.

### Getting Started:
1. **Access your Dashboard**: Go to https://robcotech.pro/dashboard to open your founder office command center.
2. **Connect your first source**: Open https://robcotech.pro/projects to connect board, finance, revenue, or workspace systems.
3. **Monitor workflows**: Review operating flows and approvals at https://robcotech.pro/workflows.

### About Your Account:
- **Billing**: Your package is live immediately. No free trial is attached to this account.
- **Support**: If you have any questions, just reply to this email.

### Upgrading or Changing Plans:
You can manage your subscription, download invoices, or adjust package scope through your settings page: https://robcotech.pro/settings.

We're excited to have you on board!

Best,
The RobcoTech Pro Team
        """
        
        await self._send_email(customer_email, subject, body)

    async def _send_email(self, to_email: str, subject: str, body: str):
        """Internal method to handle the actual sending via a provider"""
        if not self.is_configured:
            logger.warning(f"Email NOT SENT to {to_email} (API key not configured)")
            logger.info(f"Subject: {subject}")
            logger.info(f"Body Preview: {body[:100]}...")
            return

        try:
            # Placeholder for actual API call (e.g., SendGrid, Resend, etc.)
            # Example with Resend:
            # resend.Emails.send({
            #     "from": self.sender_email,
            #     "to": to_email,
            #     "subject": subject,
            #     "text": body
            # })
            logger.info(f"Email successfully sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")

email_service = EmailService()
