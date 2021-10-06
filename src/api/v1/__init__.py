from fastapi import APIRouter

from . import client, fiscal_note, item, order, user

endpoints = APIRouter()

endpoints.include_router(user.router, prefix="/users", tags=["users"])
endpoints.include_router(client.router, prefix="/clients", tags=["clients"])
endpoints.include_router(fiscal_note.router, prefix="/fiscal-notes", tags=["fiscal-notes"])
endpoints.include_router(item.router, prefix="/items", tags=["items"])
endpoints.include_router(order.router, prefix="/orders", tags=["orders"])
