from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import EmailStr, validator
from sqlmodel import Column, Field, SQLModel

from .base import BaseQuerySchema
from .types import GUID


class BaseUser(SQLModel):
    name: str = Field(..., description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    admin: bool = Field(False, description="Previlegio de administrador")


class CreateUser(BaseUser):
    password: str = Field(..., description="Senha do usuário")
    confirm_password: str = Field(..., description="Confirmação da senha")

    @validator("confirm_password")
    def validate_password(cls, value: str, values: Dict[str, Any]) -> str:
        if value == values["password"]:
            return value

        raise ValueError("A senha e a confirmação não conferem!")


class GetUser(BaseQuerySchema):
    id: int = Field(None, description="ID do Usuário")
    name: str = Field(None, description="Nome do usuário")
    email: EmailStr = Field(None, description="Email do usuário")


class User(BaseUser, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        ..., description="Id do usuário", sa_column=Column("id", GUID(), default=uuid4(), primary_key=True)
    )
    password_hash: str = Field(..., description="Hash da senha")

    @property
    def is_super_user(self) -> bool:
        return self.admin
