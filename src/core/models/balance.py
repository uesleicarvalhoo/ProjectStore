from datetime import date, datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic.class_validators import validator
from sqlmodel import Column, Enum, Field, SQLModel
from sqlmodel.sql.sqltypes import GUID

from ...utils.date import now_datetime
from ..constants import OperationType, PaymentType


class BaseBalance(SQLModel):
    value: float = Field(..., description="Value of operation")
    operation: OperationType = Field(
        ..., description="Type of operation", sa_column=Column(Enum(OperationType), nullable=False)
    )
    description: str = Field(..., description="Description of operation", min_length=1)
    created_at: datetime = Field(default_factory=now_datetime)


class CreateBalance(BaseBalance):
    @validator("value")
    def normalize_value(cls, value: float, values: Dict[str, Any]) -> float:

        if operation_type := value.get("operation"):
            if any(operation_type.name == name for name, _ in PaymentType) and value > 0:
                return value * -1


class QueryBalance(SQLModel):
    start_date: Optional[date] = Field(description="Initial date for query")
    end_date: Optional[date] = Field(description="End date for query")


class Balance(BaseBalance, table=True):
    id: UUID = Field(default_factory=uuid4, sa_column=Column("id", GUID(), primary_key=True))
    owner_id: UUID = Field(description="User ID that owns the balance", foreign_key="users.id")
