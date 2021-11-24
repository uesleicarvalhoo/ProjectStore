from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.controller import user
from src.core.helpers.database import Session, make_session
from src.core.models import Context, Token, User
from src.core.security import create_access_token
from src.utils.dependencies import context_manager, get_current_user

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def get_access_token(
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    current_user = user.authenticate(session, credentials.username, credentials.password, context=context)

    token, expire = create_access_token(str(current_user.id), access_level=current_user.access_level)

    return {"accessToken": token, "grantType": "bearer", "exp": expire}


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(current_user: User = Depends(get_current_user)):
    token, expire = create_access_token(str(current_user.id), access_level=current_user.access_level)

    return {"accessToken": token, "grantType": "bearer", "exp": expire}
