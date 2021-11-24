from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends

from src.core.controller import balance
from src.core.helpers.database import Session, make_session
from src.core.models import Balance, Context, CreateBalance, QueryBalance
from src.utils.dependencies import context_manager

router = APIRouter()


@router.get("/", response_model=List[Balance])
async def get_all(
    query: QueryBalance = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    return balance.get_all(session, query, context)


@router.post("/", response_model=Balance)
async def create(
    data: CreateBalance,
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    return balance.create(session, data, context)


@router.delete("/{balance_id}", response_model=Balance)
async def delete(
    balance_id: UUID, session: Session = Depends(make_session), context: Context = Depends(context_manager)
):
    return balance.delete(session, balance_id, context=context)
