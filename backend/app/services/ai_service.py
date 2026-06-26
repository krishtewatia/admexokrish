"""Optional AI lead classification using OpenAI."""
from loguru import logger
from app.config import settings
from app.services.lead_service import set_ai_classification


async def classify_lead(lead: dict) -> dict | None:
    """Classify a lead using OpenAI. Returns None if API key is absent."""
    if not settings.openai_api_key:
        logger.info("OPENAI_API_KEY not set — skipping classification")
        return None

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        prompt = f"""Classify this sales lead. Return ONLY valid JSON.

Name: {lead.get("name")}
Email: {lead.get("email")}
Company: {lead.get("company", "Not provided")}
Requirement: {lead.get("requirement", "Not provided")}

Return: {{"category": "Hot|Warm|Cold", "priority": "High|Medium|Low"}}"""

        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        import json
        text = resp.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        result = json.loads(text)
        category = result.get("category", "Cold")
        priority = result.get("priority", "Low")

        await set_ai_classification(lead["id"], category, priority)
        logger.info(f"Lead {lead['id']} classified: {category}/{priority}")
        return {"category": category, "priority": priority}

    except Exception as e:
        logger.error(f"AI classification failed: {e}")
        return None
