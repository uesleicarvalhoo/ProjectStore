from base64 import b64encode
from datetime import date
from uuid import UUID

from fastapi import APIRouter, File, Request, status
from fastapi.datastructures import UploadFile
from fastapi.params import Depends, Form
from sqlmodel import Session
from starlette.responses import RedirectResponse

from src.core import controller
from src.core.helpers.database import make_session
from src.core.models import Context, CreateFiscalNote, QueryFiscalNote
from src.utils.dependencies import web_context_manager

from ..utils import send_message, templates

router = APIRouter()


@router.get("")
async def fiscal_notes_view(
    request: Request,
    query: QueryFiscalNote = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    fiscal_notes = controller.fiscal_note.get_all(session, query, context=context)
    return templates.TemplateResponse(
        "fiscal_notes/view.html",
        context={
            "request": request,
            "context": context,
            "fiscal_notes": fiscal_notes,
            "current_page": query.page,
            "items_per_page": query.limit,
            "total_items": len(fiscal_notes),
        },
    )


@router.get("/cadastro")
async def fiscal_notes_create(request: Request, context: Context = Depends(web_context_manager)):
    return templates.TemplateResponse("fiscal_notes/create.html", context={"request": request, "context": context})


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
async def fiscal_notes_create_post(
    request: Request,
    description: str = Form(...),
    purchase_date: date = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):

    fiscal_note = controller.fiscal_note.create(
        session,
        schema=CreateFiscalNote(
            description=description,
            purchase_date=purchase_date,
            image=b64encode(await file.read()),
            filename=file.filename,
        ),
        context=context,
    )
    send_message(request, header="Sucesso!", text=f"Nota fiscal cadastrada com sucesso! ID: {fiscal_note.id}")

    return RedirectResponse(
        request.url_for("web:fiscal_note_by_id", fiscal_note_id=fiscal_note.id), status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/{fiscal_note_id}")
async def fiscal_note_by_id(
    request: Request,
    fiscal_note_id: UUID,
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    return templates.TemplateResponse(
        "fiscal_notes/view_detail.html",
        context={
            "request": request,
            "context": context,
            "fiscal_note": controller.fiscal_note.get_by_id(session, fiscal_note_id, context=context),
        },
    )


@router.post("/delete")
async def fiscal_notes_delete(
    request: Request,
    id: UUID = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    fiscal_note = controller.fiscal_note.delete(session, fiscal_note_id=id, context=context)
    send_message(request, "Nota fiscal excluida!", f"Nota fiscal: {fiscal_note.id} excluida com sucesso!")

    return RedirectResponse(request.url_for("web:fiscal_note_view"), status_code=status.HTTP_303_SEE_OTHER)
