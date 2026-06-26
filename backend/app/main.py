"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import sys

from app.config import settings
from app.database import create_indexes, close_client

logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {message}", level="INFO")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    yield
    await close_client()


app = FastAPI(title="Lead Management & Email Tracking API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
async def health():
    return {"status": "ok"}


from app.routes.leads import router as leads_router
from app.routes.dashboard import router as dashboard_router
from app.routes.tracking import router as tracking_router

app.include_router(leads_router, prefix="/api", tags=["Leads"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])
app.include_router(tracking_router, prefix="/api", tags=["Tracking"])
