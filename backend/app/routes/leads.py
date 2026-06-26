"""
POST /api/leads — Create lead, send email, classify with AI.
"""
from fastapi import APIRouter, HTTPException
from loguru import logger

from app.schemas import LeadCreate, LeadResponse
from app.services.lead_service import create_lead, mark_email_sent
from app.services.email_service import send_welcome_email
from app.services.ai_service import classify_lead

router = APIRouter()


@router.post("/leads", response_model=LeadResponse, status_code=201)
async def create_new_lead(body: LeadCreate):
    try:
        lead = await create_lead(body.model_dump())
    except Exception as e:
        if "duplicate" in str(e).lower() or "already exists" in str(e).lower():
            raise HTTPException(status_code=409, detail="Email already exists")
        raise HTTPException(status_code=500, detail=str(e))

    # Send welcome email (non-blocking)
    try:
        sent = await send_welcome_email(lead)
        if sent:
            await mark_email_sent(lead["id"])
            lead["emailSent"] = True
            lead["status"] = "contacted"
    except Exception as e:
        logger.error(f"Email error: {e}")

    # AI classification (optional, non-blocking)
    try:
        result = await classify_lead(lead)
        if result:
            lead["category"] = result["category"]
            lead["priority"] = result["priority"]
    except Exception as e:
        logger.error(f"AI error: {e}")

    return lead
