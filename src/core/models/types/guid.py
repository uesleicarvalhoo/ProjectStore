from typing import Any, Optional, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as PostgreUUID
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import CHAR, TypeDecorator


class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PostgreUUID())

        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value: Optional[Any], dialect: Dialect) -> Union[str, int, None]:
        if value is None:
            return value

        if dialect.name == "postgresql":
            return str(value)

        if not isinstance(value, UUID):
            return "%.32x" % UUID(value).int

        return "%.32x" % value.int

    def process_result_value(self, value: Optional[Any], dialect: Dialect) -> Optional[UUID]:
        if value is None:
            return value

        if not isinstance(value, UUID):
            return UUID(value)

        return value
