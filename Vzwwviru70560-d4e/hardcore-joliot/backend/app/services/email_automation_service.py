"""
EMAIL AUTOMATION SERVICE - Waitlist Email Sequences
====================================================

Service pour envoyer des emails informatifs aux inscrits waitlist:
- J+0: Email de bienvenue
- J+2: Email de découverte (fonctionnalités)
- J+7: Email d'engagement (invitation à explorer)

Features:
- Templates personnalisés
- Tracking des envois
- Respect RGPD (opt-out)
- Intégration avec provider email (SMTP/SendGrid/etc.)
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


# =============================================================================
# TYPES
# =============================================================================

class EmailType(Enum):
    WELCOME = "welcome"           # J+0
    DISCOVERY = "discovery"       # J+2
    ENGAGEMENT = "engagement"     # J+7


@dataclass
class EmailTemplate:
    type: EmailType
    subject: str
    html_content: str
    text_content: str
    delay_days: int


@dataclass
class EmailRecord:
    email: str
    email_type: EmailType
    sent_at: datetime
    status: str
    message_id: Optional[str] = None


# =============================================================================
# EMAIL TEMPLATES
# =============================================================================

TEMPLATES: Dict[EmailType, EmailTemplate] = {
    EmailType.WELCOME: EmailTemplate(
        type=EmailType.WELCOME,
        subject="Bienvenue dans l'univers AT·OM",
        delay_days=0,
        html_content="""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #000; color: #fff; padding: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .logo { color: #D4AF37; font-size: 32px; font-weight: bold; letter-spacing: 0.2em; text-align: center; margin-bottom: 30px; }
        .content { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 30px; }
        h1 { color: #D4AF37; font-size: 24px; margin-bottom: 20px; }
        p { color: rgba(255,255,255,0.8); line-height: 1.8; margin-bottom: 16px; }
        .cta { display: inline-block; padding: 16px 32px; background: #D4AF37; color: #000; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 20px; }
        .footer { text-align: center; margin-top: 40px; color: rgba(255,255,255,0.4); font-size: 12px; }
        .footer a { color: rgba(255,255,255,0.4); }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">AT·OM</div>
        <div class="content">
            <h1>Bienvenue, {{name}} !</h1>
            <p>
                Vous venez de rejoindre la liste d'attente AT·OM. Merci de votre intérêt pour
                notre plateforme d'intelligence collective.
            </p>
            <p>
                <strong>Ce que vous allez découvrir :</strong><br>
                • 350 agents IA prêts à vous assister<br>
                • 9 domaines de vie couverts<br>
                • Une approche souveraine de vos données
            </p>
            <p>
                Nous vous tiendrons informé des prochaines étapes et de l'ouverture de la plateforme.
            </p>
            <a href="{{platform_url}}" class="cta">Explorer AT·OM</a>
        </div>
        <div class="footer">
            <p>© 2026 AT·OM · Jonathan Rodrigue</p>
            <p><a href="{{unsubscribe_url}}">Se désinscrire</a></p>
        </div>
    </div>
</body>
</html>
        """,
        text_content="""
AT·OM - Bienvenue !

Bonjour {{name}},

Vous venez de rejoindre la liste d'attente AT·OM. Merci de votre intérêt pour notre plateforme d'intelligence collective.

Ce que vous allez découvrir :
- 350 agents IA prêts à vous assister
- 9 domaines de vie couverts
- Une approche souveraine de vos données

Nous vous tiendrons informé des prochaines étapes.

Explorer AT·OM : {{platform_url}}

---
© 2026 AT·OM · Jonathan Rodrigue
Se désinscrire : {{unsubscribe_url}}
        """
    ),

    EmailType.DISCOVERY: EmailTemplate(
        type=EmailType.DISCOVERY,
        subject="Découvrez les 9 sphères d'AT·OM",
        delay_days=2,
        html_content="""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #000; color: #fff; padding: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .logo { color: #D4AF37; font-size: 32px; font-weight: bold; letter-spacing: 0.2em; text-align: center; margin-bottom: 30px; }
        .content { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 30px; }
        h1 { color: #D4AF37; font-size: 24px; margin-bottom: 20px; }
        p { color: rgba(255,255,255,0.8); line-height: 1.8; margin-bottom: 16px; }
        .sphere { background: rgba(0,71,171,0.1); border: 1px solid rgba(0,71,171,0.3); border-radius: 8px; padding: 16px; margin-bottom: 12px; }
        .sphere-name { color: #0047AB; font-weight: 600; margin-bottom: 4px; }
        .sphere-desc { color: rgba(255,255,255,0.6); font-size: 14px; }
        .cta { display: inline-block; padding: 16px 32px; background: #0047AB; color: #fff; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 20px; }
        .footer { text-align: center; margin-top: 40px; color: rgba(255,255,255,0.4); font-size: 12px; }
        .footer a { color: rgba(255,255,255,0.4); }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">AT·OM</div>
        <div class="content">
            <h1>Les 9 Sphères de Vie</h1>
            <p>
                AT·OM organise ses 350 agents en 9 sphères thématiques, couvrant tous les aspects de votre vie :
            </p>

            <div class="sphere">
                <div class="sphere-name">🎯 Personal</div>
                <div class="sphere-desc">Productivité, bien-être, développement personnel</div>
            </div>

            <div class="sphere">
                <div class="sphere-name">💼 Business</div>
                <div class="sphere-desc">Entrepreneuriat, marketing, finance</div>
            </div>

            <div class="sphere">
                <div class="sphere-name">🎨 Creative</div>
                <div class="sphere-desc">Art, design, musique, écriture</div>
            </div>

            <div class="sphere">
                <div class="sphere-name">🎓 Scholar</div>
                <div class="sphere-desc">Éducation, recherche, apprentissage</div>
            </div>

            <p style="margin-top: 20px;">
                Et 5 autres sphères à découvrir dans l'Essaim...
            </p>

            <a href="{{platform_url}}/essaim" class="cta">Découvrir l'Essaim</a>
        </div>
        <div class="footer">
            <p>© 2026 AT·OM · Jonathan Rodrigue</p>
            <p><a href="{{unsubscribe_url}}">Se désinscrire</a></p>
        </div>
    </div>
</body>
</html>
        """,
        text_content="""
AT·OM - Les 9 Sphères de Vie

AT·OM organise ses 350 agents en 9 sphères thématiques :

• Personal - Productivité, bien-être, développement personnel
• Business - Entrepreneuriat, marketing, finance
• Creative - Art, design, musique, écriture
• Scholar - Éducation, recherche, apprentissage
• Et 5 autres sphères à découvrir...

Découvrir l'Essaim : {{platform_url}}/essaim

---
© 2026 AT·OM · Jonathan Rodrigue
Se désinscrire : {{unsubscribe_url}}
        """
    ),

    EmailType.ENGAGEMENT: EmailTemplate(
        type=EmailType.ENGAGEMENT,
        subject="Votre premier agent vous attend",
        delay_days=7,
        html_content="""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #000; color: #fff; padding: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .logo { color: #D4AF37; font-size: 32px; font-weight: bold; letter-spacing: 0.2em; text-align: center; margin-bottom: 30px; }
        .content { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 30px; }
        h1 { color: #D4AF37; font-size: 24px; margin-bottom: 20px; }
        p { color: rgba(255,255,255,0.8); line-height: 1.8; margin-bottom: 16px; }
        .highlight { background: rgba(212,175,55,0.1); border: 1px solid rgba(212,175,55,0.3); border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; }
        .highlight-text { color: #D4AF37; font-size: 20px; font-weight: 600; }
        .cta { display: inline-block; padding: 16px 32px; background: #D4AF37; color: #000; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 20px; }
        .footer { text-align: center; margin-top: 40px; color: rgba(255,255,255,0.4); font-size: 12px; }
        .footer a { color: rgba(255,255,255,0.4); }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">AT·OM</div>
        <div class="content">
            <h1>Prêt à commencer ?</h1>
            <p>
                Cela fait une semaine que vous nous avez rejoint.
                Il est temps de faire connaissance avec votre premier agent !
            </p>

            <div class="highlight">
                <div class="highlight-text">Activez le Sceau</div>
                <p style="margin: 10px 0 0; color: rgba(255,255,255,0.6);">
                    Maintenez 2 secondes pour entrer dans l'Essaim
                </p>
            </div>

            <p>
                <strong>3 étapes simples :</strong><br>
                1. Activez le Sceau<br>
                2. Explorez l'Essaim (350 agents)<br>
                3. Choisissez votre premier agent
            </p>

            <p>
                Aucun compte requis. Aucune donnée collectée sans votre consentement.
            </p>

            <a href="{{platform_url}}" class="cta">Activer le Sceau</a>
        </div>
        <div class="footer">
            <p>© 2026 AT·OM · Jonathan Rodrigue</p>
            <p><a href="{{unsubscribe_url}}">Se désinscrire</a></p>
        </div>
    </div>
</body>
</html>
        """,
        text_content="""
AT·OM - Prêt à commencer ?

Cela fait une semaine que vous nous avez rejoint.
Il est temps de faire connaissance avec votre premier agent !

ACTIVEZ LE SCEAU
Maintenez 2 secondes pour entrer dans l'Essaim

3 étapes simples :
1. Activez le Sceau
2. Explorez l'Essaim (350 agents)
3. Choisissez votre premier agent

Aucun compte requis. Aucune donnée collectée sans votre consentement.

Activer le Sceau : {{platform_url}}

---
© 2026 AT·OM · Jonathan Rodrigue
Se désinscrire : {{unsubscribe_url}}
        """
    ),
}


# =============================================================================
# EMAIL AUTOMATION SERVICE
# =============================================================================

class EmailAutomationService:
    """Service pour automatiser les emails de la waitlist."""

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@atom-platform.io")
        self.from_name = os.getenv("FROM_NAME", "AT·OM")
        self.platform_url = os.getenv("PLATFORM_URL", "https://atom-platform.io")

        # In-memory storage (replace with database in production)
        self.sent_emails: List[EmailRecord] = []
        self.unsubscribed: set = set()

    def render_template(
        self,
        template: EmailTemplate,
        email: str,
        name: Optional[str] = None
    ) -> tuple[str, str]:
        """Render email template with variables."""
        variables = {
            "name": name or email.split("@")[0],
            "email": email,
            "platform_url": self.platform_url,
            "unsubscribe_url": f"{self.platform_url}/unsubscribe?email={email}",
        }

        html = template.html_content
        text = template.text_content

        for key, value in variables.items():
            html = html.replace(f"{{{{{key}}}}}", str(value))
            text = text.replace(f"{{{{{key}}}}}", str(value))

        return html, text

    async def send_email(
        self,
        to_email: str,
        email_type: EmailType,
        name: Optional[str] = None
    ) -> bool:
        """Send an email using the specified template."""
        # Check if unsubscribed
        if to_email.lower() in self.unsubscribed:
            logger.info(f"Email {to_email} is unsubscribed, skipping")
            return False

        # Check if already sent this type
        if self._has_received(to_email, email_type):
            logger.info(f"Email {to_email} already received {email_type.value}")
            return False

        template = TEMPLATES[email_type]
        html_content, text_content = self.render_template(template, to_email, name)

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = template.subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            # Attach both text and HTML versions
            part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")
            msg.attach(part1)
            msg.attach(part2)

            # Send (in production, use async SMTP or service like SendGrid)
            if self.smtp_user and self.smtp_password:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
            else:
                # Development mode - just log
                logger.info(f"[DEV] Would send {email_type.value} email to {to_email}")
                logger.debug(f"Subject: {template.subject}")

            # Record sent email
            self.sent_emails.append(EmailRecord(
                email=to_email,
                email_type=email_type,
                sent_at=datetime.utcnow(),
                status="sent"
            ))

            logger.info(f"Sent {email_type.value} email to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            self.sent_emails.append(EmailRecord(
                email=to_email,
                email_type=email_type,
                sent_at=datetime.utcnow(),
                status=f"failed: {str(e)}"
            ))
            return False

    def _has_received(self, email: str, email_type: EmailType) -> bool:
        """Check if email has already received this type of message."""
        return any(
            record.email.lower() == email.lower() and
            record.email_type == email_type and
            record.status == "sent"
            for record in self.sent_emails
        )

    async def process_waitlist_entry(
        self,
        email: str,
        signup_date: datetime,
        name: Optional[str] = None
    ) -> List[str]:
        """Process a waitlist entry and send appropriate emails based on timing."""
        sent = []
        now = datetime.utcnow()

        for email_type, template in TEMPLATES.items():
            target_date = signup_date + timedelta(days=template.delay_days)

            # Check if it's time to send this email
            if now >= target_date:
                success = await self.send_email(email, email_type, name)
                if success:
                    sent.append(email_type.value)

        return sent

    async def process_all_pending(
        self,
        waitlist_entries: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """Process all pending emails for waitlist entries."""
        stats = {
            "processed": 0,
            "sent": 0,
            "skipped": 0,
            "failed": 0
        }

        for entry in waitlist_entries:
            email = entry.get("email")
            signup_date = entry.get("signed_up_at")
            name = entry.get("name")

            if not email or not signup_date:
                continue

            # Convert string date if needed
            if isinstance(signup_date, str):
                signup_date = datetime.fromisoformat(signup_date.replace("Z", "+00:00"))

            stats["processed"] += 1

            try:
                sent = await self.process_waitlist_entry(email, signup_date, name)
                stats["sent"] += len(sent)
                if not sent:
                    stats["skipped"] += 1
            except Exception as e:
                logger.error(f"Failed to process {email}: {e}")
                stats["failed"] += 1

        return stats

    def unsubscribe(self, email: str) -> bool:
        """Unsubscribe an email from all future communications."""
        self.unsubscribed.add(email.lower())
        logger.info(f"Unsubscribed {email}")
        return True

    def resubscribe(self, email: str) -> bool:
        """Re-subscribe an email."""
        self.unsubscribed.discard(email.lower())
        logger.info(f"Re-subscribed {email}")
        return True

    def get_email_history(self, email: str) -> List[Dict[str, Any]]:
        """Get email history for a specific address."""
        return [
            {
                "email_type": record.email_type.value,
                "sent_at": record.sent_at.isoformat(),
                "status": record.status
            }
            for record in self.sent_emails
            if record.email.lower() == email.lower()
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get email automation statistics."""
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        today_sent = sum(
            1 for record in self.sent_emails
            if record.sent_at >= today and record.status == "sent"
        )

        by_type = {}
        for email_type in EmailType:
            by_type[email_type.value] = sum(
                1 for record in self.sent_emails
                if record.email_type == email_type and record.status == "sent"
            )

        return {
            "total_sent": sum(1 for r in self.sent_emails if r.status == "sent"),
            "total_failed": sum(1 for r in self.sent_emails if "failed" in r.status),
            "unsubscribed_count": len(self.unsubscribed),
            "sent_today": today_sent,
            "by_type": by_type
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

email_automation_service = EmailAutomationService()
