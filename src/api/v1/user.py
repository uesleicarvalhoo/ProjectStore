from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.crud import user
from src.core.database import make_session
from src.core.schemas import Context, CreateUser, GetUser, User
from src.core.services.streamer import Streamer, default_streamer

router = APIRouter()


@router.get("/", response_model=List[User], response_model_exclude={"password_hash"})
async def get(
    query: GetUser = Depends(), session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)
):
    return user.get_all(session, query, context=Context.API, streamer=streamer)


@router.get("/{user_id}", response_model=User, response_model_exclude={"password_hash"})
async def get_by_id(
    user_id: int, session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)
):
    return user.get_by_id(session, user_id, context=Context.API, streamer=streamer)


@router.post("/", response_model=User, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateUser, session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)
):

    return user.create(session, schema, context=Context.API, streamer=streamer)
