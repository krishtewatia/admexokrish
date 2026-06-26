"""
GET /api/open/{lead_id}  — Email open tracking pixel.
GET /api/track/{lead_id} — Link click tracking + redirect.
"""
import base64
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import Response, RedirectResponse
from loguru import logger

from app.services.lead_service import mark_opened, mark_clicked
from app.utils.pixel import TRANSPARENT_GIF_BYTES, PIXEL_HEADERS

router = APIRouter()


@router.get("/open/{lead_id}")
async def track_open(lead_id: str, bg: BackgroundTasks):
    """Returns 1x1 transparent GIF. Records open in background. No duplicate counting."""
    bg.add_task(_record_open, lead_id)
    return Response(content=TRANSPARENT_GIF_BYTES, media_type="image/gif", headers=PIXEL_HEADERS)


@router.get("/track/{lead_id}")
async def track_click(lead_id: str, bg: BackgroundTasks):
    """Records click and redirects to https://example.com."""
    bg.add_task(_record_click, lead_id)
    return RedirectResponse(url="https://example.com", status_code=302)


async def _record_open(lead_id: str):
    try:
        was_new = await mark_opened(lead_id)
        if was_new:
            logger.info(f"Open tracked: {lead_id}")
    except Exception as e:
        logger.error(f"Open tracking failed: {e}")


async def _record_click(lead_id: str):
    try:
        await mark_clicked(lead_id)
        logger.info(f"Click tracked: {lead_id}")
    except Exception as e:
        logger.error(f"Click tracking failed: {e}")
