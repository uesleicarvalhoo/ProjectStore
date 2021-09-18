import json
from datetime import date

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED

from src.core import crud
from src.core.constants import OrderEnum
from src.core.database.models import User
from src.core.schemas import (Client, Context, CreateOrder, CreateOrderDetail, GetClient, GetItem, GetOrder,
                              UpdateOrderStatus)

from ..dependencies import context_manager, get_current_user, make_session
from ..utils import send_message, templates

router = APIRouter()


@router.get("/")
async def order_view(
    request: Request,
    query: GetOrder = Depends(),
    session: Session = Depends(make_session),
    current_user: User = Depends(get_current_user),
    context: Context = Depends(context_manager),
):
    orders = crud.order.get_all(session, query, context)
    return templates.TemplateResponse(
        "orders/view.html",
        context={"request": request, "context": context, "orders": orders, "current_user": current_user},
    )


@router.get("/create")
async def order_create(
    request: Request, session: Session = Depends(make_session), context: Context = Depends(context_manager)
):
    clients = crud.client.get_all(session, GetClient(), context=context)
    items = crud.item.get_all(session, query=GetItem(avaliable=True), context=context)

    return templates.TemplateResponse(
        "orders/create.html",
        context={
            "request": request,
            "context": context,
            "clients": [c.json() for c in clients],
            "items": [i.json() for i in items],
        },
    )


@router.get("/{order_id}")
async def order_detail(
    request: Request,
    order_id: str,
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    order = crud.order.get_by_id(session, order_id, context=context)

    return templates.TemplateResponse(
        "orders/view_detail.html", context={"request": request, "context": context, "order": order}
    )


@router.post("/status", status_code=HTTP_202_ACCEPTED)
async def order_update_status(
    schema: UpdateOrderStatus,
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    crud.order.update_status(session, schema, context=context)


@router.post("/", status_code=HTTP_201_CREATED)
async def order_create_post(
    request: Request, session: Session = Depends(make_session), context: Context = Depends(context_manager)
):
    items = []
    data = await request.json()

    client = Client(**json.loads(data.get("client", {})))

    for item in data.get("items", ["{}"]):
        data = json.loads(item)
        data["sell_value"] = data.get("sugested_sell_value")
        data["item_id"] = data.get("id")
        items.append(data)

    order = crud.order.create(
        session,
        CreateOrder(
            client_id=client.id,
            date=date.today(),
            status=OrderEnum.COMPLETED,
            details=[CreateOrderDetail(**detail) for detail in items],
        ),
        context=context,
    )

    send_message(request, "Venda registrada", f"Venda {order.id} registrada com sucesso!")
    return RedirectResponse(request.url_for("web:order_create"), status_code=status.HTTP_303_SEE_OTHER)
