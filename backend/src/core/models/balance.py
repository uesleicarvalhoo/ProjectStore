from datetime import date, datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic.class_validators import root_validator
from sqlmodel import Column, Enum, Field, SQLModel
from sqlmodel.sql.sqltypes import GUID

from ...utils.date import now_datetime
from ..constants import OperationType, PaymentType, SaleType


class BaseBalance(SQLModel):
    value: float = Field(description="Value of operation")
    operation: OperationType = Field(
        description="Type of operation", sa_column=Column(Enum(OperationType), nullable=False)
    )
    description: str = Field(description="Description of operation", min_length=1)
    created_at: datetime = Field(default_factory=now_datetime)


class CreateBalance(BaseBalance):
    @root_validator()
    def normalize_value(cls, values: Dict[str, Any]) -> float:
        operation_type = values.get("operation")
        value = values.get("value")

        if not operation_type or not value:
            return values

        if any(operation_type.name == payment_type.name for payment_type in PaymentType) and value > 0:
            values["value"] = value * -1

        if any(operation_type.name == sale_type.name for sale_type in SaleType) and value < 0:
            values["value"] = value * -1

        return values


class QueryBalance(SQLModel):
    start_date: Optional[date] = Field(description="Initial date for query")
    end_date: Optional[date] = Field(description="End date for query")


class Balance(BaseBalance, table=True):
    id: UUID = Field(default_factory=uuid4, sa_column=Column("id", GUID(), primary_key=True))
    owner_id: UUID = Field(description="User ID that owns the balance", foreign_key="users.id")
