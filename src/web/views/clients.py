from uuid import UUID

from fastapi import APIRouter, Request, status
from fastapi.params import Depends, Form
from pydantic import EmailStr
from sqlmodel import Session
from starlette.responses import RedirectResponse

from src.core import controller
from src.core.helpers.database import make_session
from src.core.models import Context, CreateClient, GetClient, UpdateClient

from ..dependencies import context_manager
from ..utils import send_message, templates

router = APIRouter()


@router.get("")
async def clients_view(
    request: Request,
    query: GetClient = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    clients = controller.client.get_all(session, query, context=context)
    return templates.TemplateResponse(
        "clients/view.html",
        context={
            "request": request,
            "context": context,
            "clients": clients,
            "current_page": query.page,
            "items_per_page": query.limit,
            "total_items": len(clients),
        },
    )


@router.get("/cadastro")
async def clients_create(request: Request, context: Context = Depends(context_manager)):
    return templates.TemplateResponse("clients/create.html", context={"request": request, "context": context})


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
async def clients_create_post(
    request: Request,
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone: int = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):

    client = controller.client.create(
        session, schema=CreateClient(name=name, email=email, phone=phone), context=context
    )
    context.send_message(header="Sucesso!", text=f"Cliente {client.name} cadastrado com sucesso! ID: {client.id}")

    return templates.TemplateResponse("clients/create.html", context={"request": request, "context": context})


@router.post("/delete")
async def clients_delete(
    request: Request,
    id: UUID = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    client = controller.client.delete(session, client_id=id, context=context)
    send_message(request, "Client excluido!", f"Cliente: {client.name} excluido com sucesso!")

    return RedirectResponse(request.url_for("web:clients_view"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{client_id}")
async def client_detail(
    request: Request,
    client_id: UUID,
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    client = controller.client.get_by_id(session, client_id, context=context)

    return templates.TemplateResponse(
        "clients/view_detail.html", context={"request": request, "context": context, "client": client}
    )


@router.get("/update/{client_id}")
async def clients_update(
    request: Request,
    client_id: UUID,
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    client = controller.client.get_by_id(session, client_id, context=context)

    if not client:
        send_message(
            request, header="Cliente não localizado!", text=f"Não foi possível localizar o cliente com ID {client_id}"
        )
        return RedirectResponse(request.url_for("web:clients_view"), status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "clients/update.html", context={"request": request, "context": context, "client": client}
    )


@router.post("/update/{client_id}")
async def clients_update_post(
    request: Request,
    client_id: UUID,
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone: int = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    client = controller.client.update(
        session, UpdateClient(id=client_id, name=name, email=email, phone=phone), context=context
    )

    if not client:
        send_message(
            request, header="Cliente não localizado!", text=f"Não foi possível localizar o cliente com ID {client_id}"
        )
        return RedirectResponse(request.url_for("web:clients_view"), status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "clients/update.html", context={"request": request, "context": context, "client": client}
    )
