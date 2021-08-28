from fastapi import APIRouter, status
from fastapi.params import Depends
from starlette.requests import Request

from src.core.config import AppSettings
from src.core.schemas import Context

from ..dependencies import context_manager, make_settings
from ..utils import templates

router = APIRouter()


@router.get("/create", status_code=status.HTTP_201_CREATED)
async def create(
    request: Request,
    settings: AppSettings = Depends(make_settings),
    context: Context = Depends(context_manager),
):
    return templates.TemplateResponse(
        "clients/create.html", context={"request": request, "settings": settings, "context": context}
    )
