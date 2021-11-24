from fastapi import APIRouter

from src.core.constants import OperationType, PaymentType, SaleType

router = APIRouter()


@router.get("/payments")
async def get_payment_types():
    return {payment.name: payment.value for payment in PaymentType}


@router.get("/sales")
async def get_sale_types():
    return {sale.name: sale.value for sale in SaleType}


@router.get("/operations")
async def get_operation_types():
    return {operation.name: operation.value for operation in OperationType}
