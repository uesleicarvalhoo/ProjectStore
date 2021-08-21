from typing import TypeVar

from pydantic import BaseModel, Field
from pydantic.types import PositiveInt

Schema = TypeVar("Schema", bound=BaseModel)
QuerySchema = TypeVar("QuerySchema", bound="BaseQuerySchema")
GetAllOutputSchema = TypeVar("GetAllOutputSchema", bound="BaseGetAllOutputSchema")


class BaseSchema(BaseModel):
    pass


class BaseQuerySchema(BaseModel):
    page: PositiveInt = Field(1, description="Pagina da consulta")
    limit: PositiveInt = Field(50, description="Limite de items na consulta")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class BaseGetAllOutputSchema(BaseModel):
    total: int = Field(..., description="Total de items disponíveis para consulta")
    pages: int = Field(..., description="Total de paginas disponíveis para consulta")
    page_total: int = Field(..., description="Total de items na pagina")
