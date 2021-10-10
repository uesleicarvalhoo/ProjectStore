from fastapi import APIRouter, Form, Request
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_303_SEE_OTHER

from src.core import controller
from src.core.helpers.exceptions import NotFoundError
from src.core.models import Context, Token
from src.core.security import (
    create_access_token,
    generate_password_reset_token,
    invalidate_access_token,
    verify_password_reset_token,
)
from src.core.services import DefaultEmailClient, EmailClient
from src.utils.dependencies import get_token, make_session, set_token_on_response, web_context_manager

from ..utils import send_message, templates

router = APIRouter()


@router.get("/login")
async def login(
    request: Request,
    context: Context = Depends(web_context_manager),
):
    return templates.TemplateResponse("login.html", context={"request": request, "context": context})


@router.get("/logout")
async def logout(request: Request, token: Token = Depends(get_token)):
    response = RedirectResponse(request.url_for("web:login"))
    await invalidate_access_token(response=response, jwt_token=token)
    return response


@router.post("/auth/login")
async def auth(
    request: Request,
    session: Session = Depends(make_session),
    credentials: OAuth2PasswordRequestForm = Depends(),
    context: Context = Depends(web_context_manager),
):
    user = controller.user.authenticate(session, credentials.username, credentials.password, context=context)

    response = RedirectResponse(request.url_for("web:index"), status_code=HTTP_303_SEE_OTHER)
    await set_token_on_response(
        response=response, token=create_access_token(str(user.id), access_level=user.access_level)
    )

    return response


@router.get("/forgot_password")
async def forgot_password(request: Request, context: Context = Depends(web_context_manager)):
    return templates.TemplateResponse("forgot_password.html", context={"request": request, "context": context})


@router.post("/forgot_password")
async def forgot_password_post(
    request: Request,
    email: EmailStr = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
    email_client: EmailClient = Depends(DefaultEmailClient),
):
    try:
        user = controller.user.get_by_email(session, email, context=context)

    except NotFoundError as err:
        send_message(request, "Email não localizado", text=err.detail)
        return RedirectResponse(request.url_for("web:recovery_password"), status_code=HTTP_303_SEE_OTHER)

    password_reset_token = generate_password_reset_token(user.email)
    email_client.send_email(
        user.email,
        template="recovery_password",
        environment={
            "token": password_reset_token,
            "user": {"name": user.name, "email": user.email, "first_name": user.first_name},
            "subject": "Recuperação de senha",
        },
    )

    send_message(
        request, "Senha enviada!", "Em breve você receberá um email com as instruções para a recuperação de sua senha"
    )
    return RedirectResponse(request.url_for("web:login"), status_code=HTTP_303_SEE_OTHER)


@router.get("/recovery_password/{password_reset_token}")
async def recovery_password(
    request: Request, password_reset_token: str, context: Context = Depends(web_context_manager)
):
    return templates.TemplateResponse(
        "recovery_password.hmtl",
        context={"request": request, "context": context, "password_reset_token": password_reset_token},
    )


@router.post("/recovery_password/{password_reset_token}")
async def recovery_password_post(
    request: Request,
    password_reset_token: str,
    new_password: str = Form(...),
    session: Session = Depends(make_session),
    context: Context = Depends(web_context_manager),
):
    email = verify_password_reset_token(password_reset_token)

    if not email:
        send_message(request, "Token invalido", "Token invalido ou expirado!")
        return RedirectResponse(request.url_for("web:login"), status_code=HTTP_303_SEE_OTHER)

    user = controller.user.get_by_email(session, email, context=context)
    controller.user.update_password(session, user.id, new_password)
    send_message(request, "Senha atualizada", "Senha atualizada com sucesso!")
    return RedirectResponse(request.url_for("web:login"), status_code=HTTP_303_SEE_OTHER)
