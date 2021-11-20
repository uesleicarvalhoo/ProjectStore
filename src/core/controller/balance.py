from typing import List
from uuid import UUID

import inject
from sqlmodel import Session, between, select

from src.core.events import EventDescription
from src.core.helpers.exceptions import NotAuthorizedError, NotFoundError
from src.core.models import Balance, Context, CreateBalance, QueryBalance
from src.core.services import Streamer


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateBalance, context: Context, streamer: Streamer) -> Balance:
    balance = Balance(**schema.dict(), owner_id=context.user_id)
    session.add(balance)
    streamer.send_event(EventDescription.CREATE_BALANCE, context=context, client=balance.dict())

    return balance


def get_all(session: Session, query_schema: QueryBalance, context: Context) -> List[Balance]:
    args = []

    if not context.user_is_super_user:
        args.append(Balance.owner_id == context.user_id)

    if query_schema.start_date is not None and query_schema.end_date is not None:
        args.append(between(Balance.created_at, query_schema.start_date, query_schema.end_date))

    return session.exec(select(Balance).where(*args)).all()


@inject.params(streamer=Streamer)
def delete(session: Session, balance_id: UUID, context: Context, streamer: Streamer) -> Balance:
    balance = session.exec(select(Balance).where(Balance.id == balance_id)).first()

    if not balance:
        raise NotFoundError(f"Não foi possível localizar o edtalhamento ID: {balance_id}")

    if not context.user_is_super_user and balance.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para excluir o detalhamento com ID: {balance_id}")

    session.delete(balance)
    session.commit()

    streamer.send_event(description=EventDescription.DELETE_BALANCE, context=context, balance=balance.dict())

    return balance
