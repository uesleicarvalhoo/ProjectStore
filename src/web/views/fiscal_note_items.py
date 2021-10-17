from uuid import UUID

from fastapi import APIRouter, File, Request, UploadFile, status
from fastapi.params import Depends, Form
from sqlmodel import Session
from starlette.responses import RedirectResponse

from src.core import controller
from src.core.helpers.database import make_session
from src.core.models import Context, CreateFiscalNoteItem, QueryFiscalNoteItem
from src.utils.dependencies import web_context_manager

from ..utils import send_message, templates

router = APIRouter()


@router.get("")
async def fiscal_note_items_view(
    request: Request,
    query: QueryFiscalNoteItem = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    items = controller.fiscal_note_item.get_all(session, query, context=context)
    return templates.TemplateResponse(
        "fiscal_note_items/view.html",
        context={
            "request": request,
            "context": context,
            "items": items,
            "current_page": query.page,
            "items_per_page": query.limit,
            "total_items": len(items),
        },
    )


@router.get("/{fiscal_note_item_id}")
async def fiscal_note_update_item_by_id(
    request: Request,
    fiscal_note_item_id: UUID,
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    item = controller.fiscal_note_item.get_by_id(session, fiscal_note_item_id, context)

    return templates.TemplateResponse(
        "fiscal_note_items/view_detail.html", context={"request": request, "context": context, "item": item}
    )


@router.get("/cadastro/{fiscal_note_id}")
async def fiscal_note_items_create(
    request: Request,
    fiscal_note_id: UUID,
    context: Context = Depends(web_context_manager),
):
    return templates.TemplateResponse(
        "fiscal_note_items/create.html",
        context={"request": request, "context": context, "fiscal_note_id": fiscal_note_id},
    )


@router.post("/cadastro/{fiscal_note_id}", status_code=status.HTTP_201_CREATED)
async def fiscal_note_items_create_post(
    request: Request,
    fiscal_note_id: UUID,
    code: str = Form(...),
    name: str = Form(...),
    file: UploadFile = File(...),
    buy_value: float = Form(...),
    sugested_sell_value: float = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    image = await file.read()
    item = controller.fiscal_note_item.create(
        session,
        schema=CreateFiscalNoteItem(
            code=code,
            name=name,
            buy_value=buy_value,
            sugested_sell_value=sugested_sell_value,
            image=image,
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
async def fiscal_note_items_delete(
    request: Request,
    id: UUID = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    item = controller.fiscal_note_item.delete(session, item_id=id, context=context)

    return RedirectResponse(
        request.url_for("web:fiscal_note_by_id", fiscal_note_id=item.fiscal_note_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )
