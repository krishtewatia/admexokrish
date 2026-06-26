"""Email service — Brevo API."""
import httpx
from loguru import logger
from app.config import settings


EMAIL_TEMPLATE = """
<html>
<body style="font-family: Arial, sans-serif; background: #f4f7fa; padding: 24px;">
  <div style="max-width: 600px; margin: auto; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">
    <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); padding: 32px; text-align: center;">
      <h1 style="color: #fff; margin: 0;">Thank You!</h1>
    </div>
    <div style="padding: 32px;">
      <p style="font-size: 16px;">Hello <strong>{name}</strong>,</p>
      <p>Thank you for contacting us.</p>
      <p>We received your request:</p>
      <blockquote style="border-left: 4px solid #6366f1; padding: 12px 16px; background: #f8f9fc; margin: 16px 0;">
        {requirement}
      </blockquote>
      <p>Our team will review your requirements and get back to you shortly.</p>
      <div style="text-align: center; margin: 24px 0;">
        <a href="{track_url}" style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600;">Learn More</a>
      </div>
    </div>
    <div style="padding: 16px 32px; background: #f8f9fc; text-align: center; color: #9ca3af; font-size: 12px;">
      © 2026 Lead Management System
    </div>
  </div>
  <img src="{open_url}" width="1" height="1" style="display:none;" />
</body>
</html>
"""


async def send_welcome_email(lead: dict) -> bool:
    """Send welcome email via Brevo API. Returns True on success."""
    if not settings.brevo_api_key:
        logger.warning("BREVO_API_KEY not set — skipping email")
        return False

    lead_id = lead["id"]
    base = settings.backend_base_url.rstrip("/")
    track_url = f"{base}/api/track/{lead_id}"
    open_url = f"{base}/api/open/{lead_id}"

    html = EMAIL_TEMPLATE.format(
        name=lead.get("name", "there"),
        requirement=lead.get("requirement", "N/A"),
        track_url=track_url,
        open_url=open_url,
    )

    payload = {
        "sender": {"name": settings.email_from_name, "email": settings.email_from_email},
        "to": [{"email": lead["email"], "name": lead["name"]}],
        "subject": f"Thank you, {lead['name']}! We received your request",
        "htmlContent": html,
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.brevo.com/v3/smtp/email",
                json=payload,
                headers={
                    "api-key": settings.brevo_api_key,
                    "Content-Type": "application/json",
                },
                timeout=10,
            )
            if resp.status_code in (200, 201):
                logger.info(f"Email sent to {lead['email']}")
                return True
            else:
                logger.error(f"Brevo error {resp.status_code}: {resp.text}")
                return False
    except Exception as e:
        logger.error(f"Email failed: {e}")
        return False
