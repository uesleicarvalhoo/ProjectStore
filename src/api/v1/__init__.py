from fastapi import APIRouter
from fastapi.param_functions import Depends

from src.utils.dependencies import login_required

from . import balances, client, item, order, types, user

endpoints = APIRouter()

endpoints.include_router(user.router, prefix="/users", tags=["users"], dependencies=[Depends(login_required)])
endpoints.include_router(client.router, prefix="/clients", tags=["clients"], dependencies=[Depends(login_required)])
endpoints.include_router(item.router, prefix="/items", tags=["items"], dependencies=[Depends(login_required)])
endpoints.include_router(order.router, prefix="/orders", tags=["orders"], dependencies=[Depends(login_required)])
endpoints.include_router(balances.router, prefix="/balances", tags=["balances"], dependencies=[Depends(login_required)])
endpoints.include_router(types.router, prefix="/types", tags=["types"])
