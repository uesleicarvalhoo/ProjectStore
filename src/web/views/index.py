from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from src.core import controller
from src.core.helpers.database import make_session
from src.core.models import Context, User
from src.core.models.client import QueryClient
from src.core.models.order import QueryOrder
from src.utils.dependencies import get_current_user, web_context_manager

from ..utils import templates

router = APIRouter()


@router.get("/")
async def index(
    request: Request,
    session: Session = Depends(make_session),
    current_user: User = Depends(get_current_user),
    context: Context = Depends(web_context_manager),
):
    clients = controller.client.get_all(session, QueryClient(), context=context)
    orders = controller.order.get_all(session, QueryOrder(), context=context)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "context": context, "current_user": current_user, "clients": clients, "orders": orders},
    )
