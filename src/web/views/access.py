from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_303_SEE_OTHER

from src.core import controller
from src.core.models import Context, Token
from src.core.security import create_access_token, invalidate_access_token
from src.utils.dependencies import get_token, make_session, set_token_on_response, web_context_manager

from ..utils import templates

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
