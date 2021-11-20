from fastapi import APIRouter

from . import balances, client, item, order, user

endpoints = APIRouter()

endpoints.include_router(user.router, prefix="/users", tags=["users"])
endpoints.include_router(client.router, prefix="/clients", tags=["clients"])
endpoints.include_router(item.router, prefix="/items", tags=["items"])
endpoints.include_router(order.router, prefix="/orders", tags=["orders"])
endpoints.include_router(balances.router, prefix="/balances", tags=["balances"])
