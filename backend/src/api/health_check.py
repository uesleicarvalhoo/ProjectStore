from fastapi import APIRouter

from src.core.config import settings

router = APIRouter()


@router.get("/")
async def version():
    return {
        "status": "ok",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }
