from typing import TypeVar

from pydantic import BaseModel, Field
from pydantic.types import PositiveInt

Schema = TypeVar("Schema", bound=BaseModel)
QuerySchema = TypeVar("QuerySchema", bound="BaseQuerySchema")
GetAllOutputSchema = TypeVar("GetAllOutputSchema", bound="BaseGetAllOutputSchema")


class BaseQuerySchema(BaseModel):
    page: PositiveInt = Field(1, description="Page of consult")
    limit: PositiveInt = Field(50, description="Max items of query")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class BaseGetAllOutputSchema(BaseModel):
    total: int = Field(..., description="Total of items in the query statments")
    pages: int = Field(..., description="Total of pages in the query statments")
    page_total: int = Field(..., description="Total of items in the current page")
