from datetime import date, datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import PositiveFloat, root_validator
from sqlmodel import Column, Enum, Field, SQLModel
from sqlmodel.sql.sqltypes import GUID

from ...utils.date import now_datetime
from ..constants import BalanceType, OperationType
from .base import BaseQuerySchema


class BaseBalance(SQLModel):
    value: PositiveFloat = Field(..., description="Value of operation")
    type: BalanceType = Field(..., description="Type of balance", sa_column=Column(Enum(BalanceType), nullable=False))
    operation: OperationType = Field(
        ..., description="Type of operation", sa_column=Column(Enum(OperationType), nullable=False)
    )
    description: str = Field(..., description="Description of operation", min_length=1)
    created_at: datetime = Field(default_factory=now_datetime)


class CreateBalance(BaseBalance):
    @root_validator(pre=True)
    def prepare_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if operation := values.get("operation"):
            values["type"] = BalanceType.get_by_operation_type(operation)

        return values


class QueryBalance(BaseQuerySchema):
    start_date: Optional[date] = Field(description="Initial date for query")
    end_date: Optional[date] = Field(description="End date for query")


class Balance(BaseBalance, table=True):
    id: UUID = Field(default_factory=uuid4, sa_column=Column("id", GUID(), primary_key=True))
    owner_id: UUID = Field(description="User ID that owns the balance", foreign_key="users.id")

    @property
    def normalized_value(self) -> float:
        if self.type == BalanceType.CREDIT:
            return self.value

        elif self.type == BalanceType.DEBT:
            return self.value * -1

        else:
            raise ValueError(f"Couldn't be determine type of balance for BalanceType {self.type.name}")
