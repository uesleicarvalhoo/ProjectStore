from fastapi import APIRouter, Request, status
from fastapi.params import Depends, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from src.core import crud
from src.core.config import AppSettings
from src.core.database import make_session
from src.core.schemas import Context, CreateClient, GetClient
from src.core.schemas.client import UpdateClient

from ..dependencies import context_manager, load_app_settings
from ..utils import send_message, templates

router = APIRouter()


@router.get("/")
async def clients_view(
    request: Request,
    query: GetClient = Depends(),
    session: Session = Depends(make_session),
    settings: AppSettings = Depends(load_app_settings),
    context: Context = Depends(context_manager),
):
    clients = crud.client.get_all(session, query, context=context)
    return templates.TemplateResponse(
        "clients/view.html", context={"request": request, "settings": settings, "context": context, "clients": clients}
    )


@router.get("/cadastro")
async def clients_create(
    request: Request,
    settings: AppSettings = Depends(load_app_settings),
    context: Context = Depends(context_manager),
):
    return templates.TemplateResponse(
        "clients/create.html", context={"request": request, "settings": settings, "context": context}
    )


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
async def clients_create_post(
    request: Request,
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone: int = Form(...),
    settings: AppSettings = Depends(load_app_settings),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):

    client = crud.client.create(session, schema=CreateClient(name=name, email=email, phone=phone), context=context)
    context.add_message(header="Sucesso!", text=f"Cliente {client.name} cadastrado com sucesso! ID: {client.id}")

    return templates.TemplateResponse(
        "clients/create.html", context={"request": request, "settings": settings, "context": context}
    )


@router.post("/delete")
async def clients_delete(
    request: Request,
    id: int = Form(...),
    settings: AppSettings = Depends(load_app_settings),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    client = crud.client.delete(session, client_id=id, context=context)
    send_message(request, "Client excluido!", f"Cliente: {client.name} excluido com sucesso!")

    return RedirectResponse("/clientes", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{client_id}")
async def clients_update(
    request: Request,
    client_id: int,
    settings: AppSettings = Depends(load_app_settings),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    client = crud.client.get_by_id(session, client_id, context=context)

    if not client:
        send_message(
            request, header="Cliente não localizado!", text=f"Não foi possível localizar o cliente com ID {client_id}"
        )
        return RedirectResponse(request.url_for("clients_view"), status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "clients/update.html", context={"request": request, "settings": settings, "context": context, "client": client}
    )


@router.post("/{client_id}")
async def clients_update_post(
    request: Request,
    client_id: int,
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone: int = Form(...),
    settings: AppSettings = Depends(load_app_settings),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    client = crud.client.update(
        session, UpdateClient(id=client_id, name=name, email=email, phone=phone), context=context
    )

    if not client:
        send_message(
            request, header="Cliente não localizado!", text=f"Não foi possível localizar o cliente com ID {client_id}"
        )
        return RedirectResponse(request.url_for("clients_view"), status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "clients/update.html", context={"request": request, "settings": settings, "context": context, "client": client}
    )
