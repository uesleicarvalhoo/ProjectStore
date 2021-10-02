from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from src.core import controller
from src.core.helpers.database import make_session
from src.core.models import Context, User
from src.core.models.client import GetClient
from src.core.models.order import GetOrder

from ..dependencies import context_manager, get_current_user
from ..utils import templates

router = APIRouter()


@router.get("/")
async def index(
    request: Request,
    session: Session = Depends(make_session),
    current_user: User = Depends(get_current_user),
    context: Context = Depends(context_manager),
):
    clients = controller.client.get_all(session, GetClient(), context=context)
    orders = controller.order.get_all(session, GetOrder(), context=context)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "context": context, "current_user": current_user, "clients": clients, "orders": orders},
    )
