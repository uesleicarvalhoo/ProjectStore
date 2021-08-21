from src.core.database import engine
from src.core.database.models.base import BaseModel


def reset_db() -> None:
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
