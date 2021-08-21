from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr
from pydantic.types import constr

from .base import BaseQuerySchema


class BaseClient(BaseModel):
    name: str = Field(..., description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    phone: constr(regex=r"^\d{2}9\d{8}$") = Field(..., description="Telefone do cliente")  # noqa


class Client(BaseClient):
    id: int = Field(..., description="Id do Cliente")

    class Config:
        orm_mode: bool = True


class CreateClient(BaseClient):
    pass


class GetClient(BaseQuerySchema):
    id: int = Field(None, description="Id do cliente")
    name: str = Field(None, description="Nome do cliente")
