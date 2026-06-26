"""
GET /api/dashboard — Analytics overview.
"""
from fastapi import APIRouter
from app.schemas import DashboardResponse
from app.services.lead_service import get_dashboard_stats

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard():
    stats = await get_dashboard_stats()
    return stats
