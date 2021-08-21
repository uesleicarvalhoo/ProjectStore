from typing import Any, Dict

from pydantic import BaseModel, EmailStr, Field, validator

from src.core.schemas.base import BaseQuerySchema


class BaseUser(BaseModel):
    name: str = Field(..., description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    admin: bool = Field(False, description="Previlegio de administrador")


class User(BaseUser):
    id: int = Field(..., description="Id do usuário")
    password_hash: str = Field(..., description="Hash da senha")

    class Config:
        orm_mode: bool = True


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
