from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_303_SEE_OTHER

from src.core import crud
from src.core.config import AppSettings
from src.core.schemas import Context, Token
from src.core.security import create_access_token, invalidate_access_token, set_token_on_response
from src.core.services.streamer import Streamer, default_streamer

from ..dependencies import context_manager, get_token, make_session, make_settings
from ..utils import templates

router = APIRouter()


@router.get("/login")
async def login(
    request: Request,
    settings: AppSettings = Depends(make_settings),
    context: Context = Depends(context_manager),
):
    return templates.TemplateResponse("login.html", {"request": request, "settings": settings, "context": context})


@router.get("/logout")
async def logout(request: Request, token: Token = Depends(get_token)):
    response = RedirectResponse("/login")
    await invalidate_access_token(response=response, jwt_token=token)
    return response


@router.post("/auth/login")
async def auth(
    session: Session = Depends(make_session),
    credentials: OAuth2PasswordRequestForm = Depends(),
    streamer: Streamer = Depends(default_streamer),
    context: Context = Depends(context_manager),
):
    user = crud.user.authenticate(
        session, credentials.username, credentials.password, context=context, streamer=streamer
    )

    response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    await set_token_on_response(response=response, token=create_access_token(str(user.id)))

    return response
