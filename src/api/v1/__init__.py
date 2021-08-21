from fastapi import APIRouter

from . import client, fiscal_note, item, order, user

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(client.router, prefix="/clients", tags=["clients"])
router.include_router(fiscal_note.router, prefix="/fiscal-notes", tags=["fiscal-notes"])
router.include_router(item.router, prefix="/items", tags=["items"])
router.include_router(order.router, prefix="/orders", tags=["orders"])
