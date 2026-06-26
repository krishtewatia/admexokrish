"""Pydantic schemas for validation."""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class LeadCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=200)
    requirement: Optional[str] = Field(None, max_length=2000)


class LeadResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    requirement: Optional[str] = None
    submittedAt: datetime
    emailSent: bool
    opened: bool
    clicked: bool
    category: Optional[str] = None
    priority: Optional[str] = None


class DashboardResponse(BaseModel):
    total_leads: int
    emails_sent: int
    emails_opened: int
    open_rate: float
    links_clicked: int
    click_rate: float
    recent_leads: List[LeadResponse]
