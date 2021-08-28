from typing import List, Union

from sqlalchemy import Column, Integer, String, exists, or_
from sqlalchemy.orm import Query, Session, relationship
from sqlalchemy.sql.sqltypes import BigInteger, DateTime

from src.utils.date import now_datetime

from ...schemas import CreateClient, GetClient
from .base import BaseModel


class Client(BaseModel):
    __tablename__ = "clients"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(100), nullable=False)
    email = Column("email", String(100), nullable=True)
    phone = Column("phone", BigInteger, nullable=True)
    created_at = Column("created_at", DateTime, default=now_datetime())

    orders = relationship("Order", back_populates="client", cascade="all,delete", lazy="selectin", passive_deletes=True)

    @classmethod
    def query(cls, session: Session, schema: GetClient) -> Query:
        query = session.query(cls)

        if schema.id:
            return query.filter(cls.id == schema.id)

        if schema.name:
            return query.filter(cls.name == schema.name)

        return query

    @classmethod
    def create(cls, session: Session, schema: CreateClient) -> "Client":
        return super().create(session, schema)

    @classmethod
    def get(cls, session: Session, client_id: int) -> Union[None, "Client"]:
        return super().get(session, client_id)

    @classmethod
    def get_all(cls, session: Session, schema: GetClient) -> List["Client"]:
        return super().get_all(session, schema)

    @classmethod
    def delete_by_id(cls, session: Session, client_id: int) -> Union[None, "Client"]:
        return super().delete_by_id(session, client_id)

    @classmethod
    def exists(cls, session: Session, email: str = None, phone: str = None) -> bool:
        if not email and not phone:
            raise ValueError("You must be pass email or phone!")

        args = []

        if email:
            args.append(cls.email == email)

        if phone:
            args.append(cls.phone == phone)

        return bool(session.query(exists().where(or_(*args))).scalar())
