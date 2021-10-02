from fastapi import APIRouter, Form, Request
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_303_SEE_OTHER

from src.core import controller
from src.core.models import Context, CreateUser, GetUser, User

from ..dependencies import context_manager, get_current_user, make_session
from ..utils import send_message, templates

router = APIRouter()


@router.get("")
async def users_view(
    request: Request,
    query: GetUser = Depends(),
    session: Session = Depends(make_session),
    current_user: User = Depends(get_current_user),
    context: Context = Depends(context_manager),
):
    users = controller.user.get_all(session, query, context=context)

    return templates.TemplateResponse(
        "users/view.html",
        context={
            "request": request,
            "context": context,
            "users": users,
            "current_user": current_user,
            "current_page": query.page,
            "items_per_page": query.limit,
            "total_items": len(users),
        },
    )


@router.get("/cadastro")
async def register(request: Request, context: Context = Depends(context_manager)):
    return templates.TemplateResponse("users/create.html", context={"request": request, "context": context})


@router.post("/cadastro")
async def register_post(
    request: Request,
    name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    admin: bool = Form(False),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    create_schema = CreateUser(
        name=name, email=email, admin=admin, password=password, confirm_password=confirm_password
    )

    user = controller.user.create(session, create_schema, context=context)
    send_message(request, "Usuario cadastrado", f'Usuário "{user.name}" cadastrado com sucesso! ID: {user.id}')

    return RedirectResponse(request.url_for("web:index"), status_code=HTTP_303_SEE_OTHER)
