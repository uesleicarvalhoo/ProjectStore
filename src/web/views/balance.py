from fastapi import APIRouter, Form, Request, status
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from src.core import controller
from src.core.constants import OperationType
from src.core.helpers.database import make_session
from src.core.models import Context
from src.core.models.balance import CreateBalance, QueryBalance
from src.utils.dependencies import web_context_manager

from ..utils import send_message, templates

router = APIRouter()


@router.get("/")
async def view_balance(
    request: Request,
    session: Session = Depends(make_session),
    query: QueryBalance = Depends(),
    context: Context = Depends(web_context_manager),
):

    balances = controller.balance.get_all(session, query, context=context)
    return templates.TemplateResponse(
        "balances/view.html",
        context={
            "request": request,
            "context": context,
            "balances": balances,
            "current_page": query.page,
            "items_per_page": query.limit,
            "total_items": len(balances),
        },
    )


@router.get("/cadastro")
async def create_balance(
    request: Request,
    context: Context = Depends(web_context_manager),
):
    return templates.TemplateResponse("balances/create.html", context={"request": request, "context": context})


@router.post("/cadastro")
async def create_balance_post(
    request: Request,
    operation_type: OperationType = Form(...),
    description: str = Form(...),
    value: float = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    schema = CreateBalance(value=value, operation=operation_type, description=description)
    balance = controller.balance.create(session, schema, context=context)
    send_message(request, header="Registro incluido com sucesso!", text=f"Registro incluido com ID: {balance.id}")

    return RedirectResponse(request.url_for("web:view_balance"), status_code=status.HTTP_303_SEE_OTHER)
