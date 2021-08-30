import datetime as dt
import json
from typing import Any, Dict, List, TypeVar, Union

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query, Session

from ...schemas.base import QuerySchema, Schema

Base = declarative_base()


DatabaseModel = TypeVar("DatabaseModel", bound="BaseModel")


class BaseModel(Base):
    __abstract__ = True
    __uneditable_fields__ = [
        "id",
    ]
    __dict_exclude_fields__ = []

    def dict(self) -> Dict[str, Any]:
        return {
            col: getattr(self, col) for col in self.__table__.columns.keys() if col not in self.__dict_exclude_fields__
        }

    def json(self, **kwargs) -> str:
        data = self.to_dict()

        for col, value in data.items():
            if isinstance(value, dt.datetime) or isinstance(value, dt.date):
                data[col] = value.isoformat()

        return json.dumps(data, **kwargs)

    @classmethod
    def query(cls, session: Session, schema: Schema) -> Query:
        raise NotImplementedError

    @classmethod
    def create(cls, session: Session, schema: Schema) -> DatabaseModel:
        obj = cls(**schema.dict())
        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj

    @classmethod
    def get(cls, session: Session, obj_id: Union[str, int]) -> Union[None, DatabaseModel]:
        return session.query(cls).filter(cls.id == obj_id).first()

    @classmethod
    def get_all(cls, session: Session, schema: QuerySchema) -> List[DatabaseModel]:
        query = cls.query(session, schema).order_by(cls.id).offset(schema.offset)

        if schema.limit > 0:
            return query.limit(schema.limit).all()

        return query.all()

    def update(
        self, session: Session, schema: Union[Schema, Dict[str, Any]], auto_commit: bool = True
    ) -> DatabaseModel:
        columns = self.__table__.columns.keys()

        if isinstance(schema, dict):
            update_data = schema

        else:
            update_data = schema.dict(exclude_defaults=True, exclude_unset=True)

        for key, value in update_data.items():
            if key not in columns or key in self.__uneditable_fields__:
                continue

            setattr(self, key, value)

        if auto_commit:
            session.add(self)
            session.commit()
            session.refresh(self)

        return self

    def delete(self, session: Session, auto_commit: bool = True) -> DatabaseModel:
        session.delete(self)

        if auto_commit:
            session.commit()

        return self

    @classmethod
    def delete_by_id(cls, session: Session, obj_id: int) -> Union[None, DatabaseModel]:
        if obj := session.query(cls).filter(cls.id == obj_id).first():
            session.delete(obj)
            session.commit()
            return obj

        return None

    @classmethod
    def count(cls, session: Session, schema: Schema) -> int:
        return cls.query(session, schema).count()
