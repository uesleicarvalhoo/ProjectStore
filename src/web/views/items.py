from base64 import b64encode
from uuid import UUID

from fastapi import APIRouter, File, Request, UploadFile, status
from fastapi.params import Depends, Form
from sqlmodel import Session
from starlette.responses import RedirectResponse

from src.core import controller
from src.core.helpers.database import make_session
from src.core.models import Context, CreateItem
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


@router.get("/{item_id}")
async def item_by_id(
    request: Request,
    item_id: UUID,
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    item = controller.item.get_by_id(session, item_id, context)

    return templates.TemplateResponse(
        "items/view_detail.html", context={"request": request, "context": context, "item": item}
    )


@router.get("/cadastro/{fiscal_note_id}")
async def items_create(
    request: Request,
    fiscal_note_id: UUID,
    context: Context = Depends(web_context_manager),
):
    return templates.TemplateResponse(
        "items/create.html",
        context={"request": request, "context": context, "fiscal_note_id": fiscal_note_id},
    )


@router.post("/cadastro/{fiscal_note_id}", status_code=status.HTTP_201_CREATED)
async def items_create_post(
    request: Request,
    fiscal_note_id: UUID,
    code: str = Form(...),
    name: str = Form(...),
    avaliable: bool = Form(...),
    file: UploadFile = File(...),
    buy_value: float = Form(...),
    sugested_sell_value: float = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):

    item = controller.item.create(
        session,
        schema=CreateItem(
            code=code,
            name=name,
            avaliable=avaliable,
            buy_value=buy_value,
            sugested_sell_value=sugested_sell_value,
            image=b64encode(await file.read()),
            filename=file.filename,
        ),
        fiscal_note_id=fiscal_note_id,
        context=context,
    )

    send_message(request, header="Sucesso!", text=f"Item cadastrado com sucesso! ID: {item.id}")

    return RedirectResponse(
        request.url_for("web:fiscal_note_by_id", fiscal_note_id=fiscal_note_id), status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/delete")
async def items_delete(
    request: Request,
    id: UUID = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    item = controller.item.delete(session, item_id=id, context=context)

    return RedirectResponse(
        request.url_for("web:fiscal_note_by_id", fiscal_note_id=item.fiscal_note_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )
