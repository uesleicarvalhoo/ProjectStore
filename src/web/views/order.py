import json
from datetime import date
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.param_functions import Form
from fastapi.params import Depends
from sqlmodel import Session
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED

from src.core import controller
from src.core.constants import OperationType, OrderStatus
from src.core.models import (
    Client,
    Context,
    CreateOrder,
    CreateOrderDetail,
    QueryClient,
    QueryFiscalNoteItem,
    QueryOrder,
    UpdateOrderStatus,
    User,
)
from src.utils.dependencies import get_current_user, make_session, web_context_manager

from ..utils import send_message, templates

router = APIRouter()


@router.get("")
async def order_view(
    request: Request,
    query: QueryOrder = Depends(),
    session: Session = Depends(make_session),
    current_user: User = Depends(get_current_user),
    context: Context = Depends(web_context_manager),
):
    orders = controller.order.get_all(session, query, context)
    return templates.TemplateResponse(
        "orders/view.html",
        context={
            "request": request,
            "context": context,
            "orders": orders,
            "current_user": current_user,
            "current_page": query.page,
            "items_per_page": query.limit,
            "total_items": len(orders),
        },
    )


@router.get("/create")
async def order_create(
    request: Request, session: Session = Depends(make_session), context: Context = Depends(web_context_manager)
):
    clients = controller.client.get_all(session, QueryClient(), context=context)
    items = controller.item.get_all(session, QueryFiscalNoteItem(avaliable=True), context=context)

    return templates.TemplateResponse(
        "orders/create.html",
        context={
            "request": request,
            "context": context,
            "clients": [c.json() for c in clients],
            "items": [i.json() for i in items],
            "sale_types": OperationType.list_sale_types(),
        },
    )


@router.post("/create", status_code=HTTP_201_CREATED)
async def order_create_post(
    request: Request, session: Session = Depends(make_session), context: Context = Depends(web_context_manager)
):
    items = []
    data = await request.json()
    description = data["description"]

    operation_type = data.get("operation_type", None)

    if operation_type:
        operation_type = OperationType(operation_type)

    client = Client(**json.loads(data.get("client", {})))

    for item in data.get("items", []):
        item["sell_value"] = item.pop("value", None)
        item["item_id"] = item.pop("id", None)
        item["item_name"] = item.pop("name", None)
        item["item_amount"] = item.pop("amount", None)
        items.append(item)

    order = controller.order.register_sale(
        session,
        CreateOrder(
            client_id=client.id,
            date=date.today(),
            status=OrderStatus.COMPLETED,
            description=description,
            operation_type=operation_type,
            details=[CreateOrderDetail(**detail) for detail in items],
        ),
        context=context,
    )

    send_message(request, "Venda registrada", f"Venda {order.id} registrada com sucesso!")
    return RedirectResponse(request.url_for("web:order_create"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{order_id}")
async def order_detail(
    request: Request,
    order_id: UUID,
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    order = controller.order.get_by_id(session, order_id, context=context)

    return templates.TemplateResponse(
        "orders/view_detail.html", context={"request": request, "context": context, "order": order}
    )


@router.post("/status", status_code=HTTP_202_ACCEPTED)
async def order_update_status(
    schema: UpdateOrderStatus,
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    controller.order.update_status(session, schema, context=context)


@router.post("/delete")
async def order_delete(
    request: Request,
    id: UUID = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    controller.order.delete_by_id(session, order_id=id, context=context)

    return RedirectResponse(
        request.url_for("web:order_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
