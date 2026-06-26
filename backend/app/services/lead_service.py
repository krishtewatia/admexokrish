"""Lead CRUD service."""
from datetime import datetime, timezone
from bson import ObjectId
from app.database import get_db
from loguru import logger


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


async def create_lead(data: dict) -> dict:
    db = get_db()
    doc = {
        "name": data["name"],
        "email": data["email"],
        "phone": data.get("phone"),
        "company": data.get("company"),
        "requirement": data.get("requirement"),
        "submittedAt": datetime.now(timezone.utc),
        "emailSent": False,
        "opened": False,
        "clicked": False,
        "category": None,
        "priority": None,
    }
    result = await db["leads"].insert_one(doc)
    doc["_id"] = result.inserted_id
    logger.info(f"Lead created: {doc['email']}")
    return _serialize(doc)


async def get_lead(lead_id: str) -> dict | None:
    db = get_db()
    doc = await db["leads"].find_one({"_id": ObjectId(lead_id)})
    return _serialize(doc) if doc else None


async def get_all_leads(limit: int = 100) -> list:
    db = get_db()
    cursor = db["leads"].find().sort("submittedAt", -1).limit(limit)
    return [_serialize(doc) async for doc in cursor]


async def mark_email_sent(lead_id: str):
    db = get_db()
    await db["leads"].update_one(
        {"_id": ObjectId(lead_id)}, {"$set": {"emailSent": True}}
    )


async def mark_opened(lead_id: str) -> bool:
    """Mark opened=True. Returns False if already opened (dedup)."""
    db = get_db()
    result = await db["leads"].update_one(
        {"_id": ObjectId(lead_id), "opened": False},
        {"$set": {"opened": True}},
    )
    return result.modified_count > 0


async def mark_clicked(lead_id: str):
    db = get_db()
    await db["leads"].update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": {"clicked": True}},
    )


async def set_ai_classification(lead_id: str, category: str, priority: str):
    db = get_db()
    await db["leads"].update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": {"category": category, "priority": priority}},
    )


async def get_dashboard_stats() -> dict:
    db = get_db()
    total = await db["leads"].count_documents({})
    sent = await db["leads"].count_documents({"emailSent": True})
    opened = await db["leads"].count_documents({"opened": True})
    clicked = await db["leads"].count_documents({"clicked": True})

    open_rate = round((opened / sent * 100), 1) if sent > 0 else 0.0
    click_rate = round((clicked / sent * 100), 1) if sent > 0 else 0.0

    recent = await get_all_leads(limit=10)

    return {
        "total_leads": total,
        "emails_sent": sent,
        "emails_opened": opened,
        "open_rate": open_rate,
        "links_clicked": clicked,
        "click_rate": click_rate,
        "recent_leads": recent,
    }
