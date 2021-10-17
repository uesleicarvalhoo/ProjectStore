from uuid import UUID

from fastapi import APIRouter, Request, status
from fastapi.params import Depends, Form
from sqlmodel import Session
from starlette.responses import RedirectResponse

from src.core import controller
from src.core.helpers.database import make_session
from src.core.models import Context, CreateItem, UpdateItem
from src.core.models.item import QueryItem
from src.utils.dependencies import web_context_manager

from ..utils import send_message, templates

router = APIRouter()


@router.get("")
async def items_view(
    request: Request,
    query: QueryItem = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    items = controller.item.get_all(session, query, context=context)
    return templates.TemplateResponse(
        "items/view.html",
        context={
            "request": request,
            "context": context,
            "items": items,
            "current_page": query.page,
            "items_per_page": query.limit,
            "total_items": len(items),
        },
    )


@router.get("/cadastro")
async def items_create(
    request: Request,
    context: Context = Depends(web_context_manager),
):
    return templates.TemplateResponse("items/create.html", context={"request": request, "context": context})


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
async def items_create_post(
    request: Request,
    code: str = Form(...),
    name: str = Form(...),
    amount: int = Form(...),
    cost: float = Form(...),
    value: float = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):

    item = controller.item.create(
        session,
        schema=CreateItem(
            code=code,
            name=name,
            amount=amount,
            cost=cost,
            value=value,
        ),
        context=context,
    )

    send_message(request, header="Sucesso!", text=f"Item cadastrado com sucesso! ID: {item.id}")

    return RedirectResponse(request.url_for("web:items_view"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{item_id}")
async def update_item_by_id(
    request: Request,
    item_id: UUID,
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    item = controller.item.get_by_id(session, item_id, context)

    return templates.TemplateResponse(
        "items/update.html", context={"request": request, "context": context, "item": item}
    )


@router.post("/{item_id}")
async def update_item_by_id_post(
    request: Request,
    item_id: UUID,
    code: str = Form(...),
    name: str = Form(...),
    amount: int = Form(...),
    cost: float = Form(...),
    value: float = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    schema = UpdateItem(id=item_id, code=code, name=name, cost=cost, value=value, amount=amount)
    controller.item.update(session, schema, context)

    return RedirectResponse("web:items_view", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/delete")
async def items_delete(
    request: Request,
    id: UUID = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    controller.item.delete(session, item_id=id, context=context)

    return RedirectResponse(
        request.url_for("web:items_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
