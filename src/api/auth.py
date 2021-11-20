from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.controller import user
from src.core.helpers.database import Session, make_session
from src.core.models import Context, Token
from src.core.security import create_access_token
from src.utils.dependencies import context_manager

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def get_token(
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    current_user = user.authenticate(session, credentials.username, credentials.password, context=context)

    token = create_access_token(str(current_user.id), access_level=current_user.access_level)

    return {
        "accessToken": token,
        "grantType": "bearer",
        "user": current_user,
    }
