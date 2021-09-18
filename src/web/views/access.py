from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_303_SEE_OTHER

from src.core import crud
from src.core.schemas import Context, Token
from src.core.security import create_access_token, invalidate_access_token, set_token_on_response

from ..dependencies import context_manager, get_token, make_session
from ..utils import templates

router = APIRouter()


@router.get("/login")
async def login(
    request: Request,
    context: Context = Depends(context_manager),
):
    return templates.TemplateResponse("login.html", {"request": request, "context": context})


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
    context: Context = Depends(context_manager),
):
    user = crud.user.authenticate(session, credentials.username, credentials.password, context=context)

    response = RedirectResponse(request.url_for("web:index"), status_code=HTTP_303_SEE_OTHER)
    await set_token_on_response(response=response, token=create_access_token(str(user.id)))

    return response
