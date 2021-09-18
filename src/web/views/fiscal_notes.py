from base64 import b64encode
from datetime import date

from fastapi import APIRouter, File, Request, status
from fastapi.datastructures import UploadFile
from fastapi.params import Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from src.core import crud
from src.core.database import make_session
from src.core.schemas import Context, CreateFiscalNote, GetFiscalNote

from ..dependencies import context_manager
from ..utils import send_message, templates

router = APIRouter()


@router.get("/")
async def fiscal_notes_view(
    request: Request,
    query: GetFiscalNote = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    fiscal_notes = crud.fiscal_note.get_all(session, query, context=context)
    return templates.TemplateResponse(
        "fiscal_notes/view.html",
        context={"request": request, "context": context, "fiscal_notes": fiscal_notes},
    )


@router.get("/cadastro")
async def fiscal_notes_create(request: Request, context: Context = Depends(context_manager)):
    return templates.TemplateResponse("fiscal_notes/create.html", context={"request": request, "context": context})


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
async def fiscal_notes_create_post(
    request: Request,
    description: str = Form(...),
    purchase_date: date = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):

    fiscal_note = crud.fiscal_note.create(
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

    return RedirectResponse(request.url_for("fiscal_note_by_id"), fiscal_note_id=fiscal_note.id)


@router.get("/{fiscal_note_id}")
async def fiscal_note_by_id(
    request: Request,
    fiscal_note_id: int,
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    return templates.TemplateResponse(
        "fiscal_notes/view_detail.html",
        context={
            "request": request,
            "context": context,
            "fiscal_note": crud.fiscal_note.get_by_id(session, fiscal_note_id, context=context),
        },
    )


@router.post("/delete")
async def fiscal_notes_delete(
    request: Request,
    id: int = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    fiscal_note = crud.fiscal_note.delete(session, fiscal_note_id=id, context=context)
    send_message(request, "Nota fiscal excluida!", f"Nota fiscal: {fiscal_note.id} excluida com sucesso!")

    return RedirectResponse(request.url_for("web:fiscal_note_view"), status_code=status.HTTP_303_SEE_OTHER)
