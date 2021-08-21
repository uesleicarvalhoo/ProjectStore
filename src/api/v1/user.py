from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.core.database.helpers import master_session, read_session
from src.core.database.models import User as UserModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.schemas import CreateUser, GetUser, User
from src.core.services.streamer import Streamer, default_streamer

router = APIRouter()


@router.get("/", response_model=List[User], response_model_exclude={"password_hash"})
async def get(query: GetUser = Depends(), session: Session = Depends(read_session)):
    return UserModel.get_all(session, query)


@router.get("/{user_id}", response_model=User, response_model_exclude={"password_hash"})
async def get_by_id(
    user_id: int, session: Session = Depends(read_session), streamer: Streamer = Depends(default_streamer)
):
    user = UserModel.get(session, user_id)

    if not user:
        raise NotFoundError(f"Usuário com id {user_id} não encontrado!")

    streamer.send_event(event_code=EventCode.get_user, user=user.dict())

    return user


@router.post("/", response_model=User, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateUser, session: Session = Depends(master_session), streamer: Streamer = Depends(default_streamer)
):

    if UserModel.exists(session, schema.email):
        raise HTTPException(HTTP_400_BAD_REQUEST, "Já existe um usuário cadastrado com o email: %s" % schema.email)

    user = UserModel.create(session, schema)
    streamer.send_event(event_code=EventCode.CREATE_USER, **{"user": user})

    return user
