from typing import TYPE_CHECKING, Any, Dict, Optional, Union
from uuid import UUID, uuid4

from pydantic import PositiveFloat, validator
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from .base import BaseQuerySchema

if TYPE_CHECKING:
    from .user import User


class BaseItem(SQLModel):
    code: str = Field(..., description="Item code", min_length=1)
    name: str = Field(..., description="Item Name", min_length=1)
    cost: Optional[float] = Field(description="Production/Buy cost of the item", ge=0)
    value: PositiveFloat = Field(..., description="Sugested sell value of item")
    amount: int = Field(default=0, description="Quantity of itens avaliable", ge=0)


class CreateItem(BaseItem):
    @validator("value")
    def validate_value(cls, value: Union[str, float], values: Dict[str, Any]) -> float:
        if isinstance(value, str):
            if "," in value and "." not in value:
                value = value.replace(",", ".")

            value = float(value)

        if values.get("cost", 0) >= value:
            raise ValueError("The sugested sell value must be higher then buy value!")

        return value


class UpdateItem(BaseItem):
    id: UUID = Field(default_factory=uuid4, description="ID do item")

    @validator("value")
    def validate_value(cls, value: Union[str, float], values: Dict[str, Any]) -> float:
        if isinstance(value, str):
            value = float(value)

        if values.get("cost", 0) >= value:
            raise ValueError("The sugested sell value must be higher then buy value!")

        return value


class QueryItem(BaseQuerySchema):
    avaliable: Optional[bool] = Field(description="Flag to identify if the item is avaliable")


class Item(BaseItem, table=True):
    __tablename__ = "items"

    id: UUID = Field(default_factory=uuid4, description="ID do item", sa_column=Column("id", GUID(), primary_key=True))
    owner_id: UUID = Field(description="User ID that owns the file", foreign_key="users.id")
    owner: "User" = Relationship()

    @property
    def avaliable(self) -> bool:
        return self.amount > 0
