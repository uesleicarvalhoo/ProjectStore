from fastapi import APIRouter, Depends, Request

from src.core.config import AppSettings
from src.core.database.models.user import User
from src.core.schemas import Context

from ..dependencies import context_manager, get_current_user, load_app_settings
from ..utils import templates

router = APIRouter()


@router.get("/")
async def index(
    request: Request,
    settings: AppSettings = Depends(load_app_settings),
    current_user: User = Depends(get_current_user),
    context: Context = Depends(context_manager),
):
    return templates.TemplateResponse("index.html", {"request": request, "settings": settings, "context": context})
