from fastapi import APIRouter
from fastapi.params import Depends

from ..dependencies import login_required
from . import access, clients, index

endpoints = APIRouter()
endpoints.include_router(access.router)
endpoints.include_router(index.router, dependencies=[Depends(login_required)])
endpoints.include_router(clients.router, prefix="/clientes", dependencies=[Depends(login_required)])
