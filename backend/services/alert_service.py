import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class AlertService:
    """Handles sending alerts via Webhooks or Email."""
    
    @staticmethod
    def send_alerts(new_opportunities):
        """Sends alerts through all enabled channels."""
        if not new_opportunities:
            return

        logger.info(f"Sending alerts for {len(new_opportunities)} new items...")
        
        # 1. Webhook Alert (Discord/Slack)
        AlertService.send_webhook_alert(new_opportunities)
        
        # 2. Email Alert (Placeholder)
        AlertService.send_email_alert(new_opportunities)

    @staticmethod
    def send_webhook_alert(opportunities):
        webhook_url = os.getenv('ALERT_WEBHOOK_URL')
        if not webhook_url:
            logger.debug("ALERT_WEBHOOK_URL not set. Skipping webhook alert.")
            return

        count = len(opportunities)
        # Discord format
        message = {
            "content": f"🚀 **{count} New Startup Opportunities Discovered!**",
            "embeds": []
        }

        # Show top 5 items to keep the message clean
        for opp in opportunities[:5]:
            message["embeds"].append({
                "title": opp.get('title', 'New Opportunity'),
                "description": (opp.get('description', '')[:200] + '...') if opp.get('description') else "Curated strategic resource.",
                "url": opp.get('source_link'),
                "color": 3447003, # Blue
                "fields": [
                    {"name": "Type", "value": opp.get('opportunity_type', 'Other'), "inline": True},
                    {"name": "Source", "value": opp.get('source', 'Unknown'), "inline": True},
                    {"name": "Organizer", "value": opp.get('organizer', 'Unknown'), "inline": True}
                ]
            })

        if count > 5:
            message["embeds"].append({
                "title": f"And {count - 5} more...",
                "description": "Visit the dashboard to see all new opportunities."
            })

        try:
            response = requests.post(webhook_url, json=message, timeout=10)
            response.raise_for_status()
            logger.info("Successfully sent webhook alert.")
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")

    @staticmethod
    def send_email_alert(opportunities):
        """Placeholder for email alerts using SMTP or a service like SendGrid."""
        email = os.getenv('ALERT_EMAIL')
        if not email:
            return
            
        logger.info(f"Email alert would be sent to {email} for {len(opportunities)} items.")
        # To implement: Use smtplib or an API-based email provider.
