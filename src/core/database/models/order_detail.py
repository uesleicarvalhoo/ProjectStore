from typing import List, Union

from sqlalchemy import Column, Float, ForeignKey, Integer, exists
from sqlalchemy.orm import Query, Session, relationship

from ...schemas import CreateOrderDetail, GetOrderDetail
from .base import BaseModel


class OrderDetail(BaseModel):
    __tablename__ = "order_details"

    id = Column("id", Integer, primary_key=True)
    item_id = Column("item_id", Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    order_id = Column("order_id", Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    buy_value = Column("buy_value", Float, nullable=False)
    sell_value = Column("sell_value", Float, nullable=False)

    order = relationship("Order", back_populates="details", cascade="all,delete", lazy="selectin", passive_deletes=True)
    item = relationship("Item", cascade="all,delete", lazy="selectin", passive_deletes=True)

    @classmethod
    def query(cls, session: Session, schema: GetOrderDetail) -> Query:
        query = session.query(cls)

        if schema.client_id:
            return query.filter(cls.client_id == schema.client_id)

        return query

    @classmethod
    def create(cls, session: Session, schema: CreateOrderDetail, order_id: int) -> "OrderDetail":
        obj = OrderDetail(**schema.dict(), order_id=order_id)
        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj

    @classmethod
    def get(cls, session: Session, order_id: int) -> Union[None, "OrderDetail"]:
        return session.query(cls).filter(cls.id == order_id).first()

    @classmethod
    def get_all(cls, session: Session, schema: GetOrderDetail) -> List["OrderDetail"]:
        return super().get_all(session, schema)

    @classmethod
    def delete_by_id(cls, session: Session, order_id: int) -> Union[None, "OrderDetail"]:
        return super().delete_by_id(session, order_id)

    @classmethod
    def exists(cls, session: Session, order_id: int) -> bool:
        return session.query(exists().where(cls.order_id == order_id)).scalar()

    @property
    def profit(self) -> float:
        return self.sell_value - self.buy_value
