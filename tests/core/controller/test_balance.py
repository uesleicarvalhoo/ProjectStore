import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.constants import OperationType
from src.core.models.balance import Balance, QueryBalance
from src.core.models.context import Context
from tests.factories.balance import CreateBalanceFactory


def test_create_balance_success(session: Session, context: Context):
    # prepare
    debt_schema = CreateBalanceFactory(operation=OperationType.PAYMENT_OF_SUPPLIERS)
    credit_schema = CreateBalanceFactory(operation=OperationType.SALE_IN_PIX)

    # create
    debt_balance = controller.balance.create(session, debt_schema, context=context)
    credit_balance = controller.balance.create(session, credit_schema, context=context)

    # assert
    assert debt_balance.id is not ...
    assert debt_balance.id is not None
    assert debt_balance.value == debt_schema.value
    assert debt_balance.operation == debt_schema.operation
    assert debt_balance.description == debt_schema.description

    assert credit_balance.id is not None and credit_balance.id is not ...
    assert credit_balance.value == credit_schema.value
    assert credit_balance.operation == credit_schema.operation
    assert credit_balance.description == credit_schema.description


def test_create_balance_fail(session: Session, context: Context):
    with pytest.raises(ValidationError):
        CreateBalanceFactory()

    with pytest.raises(ValidationError):
        CreateBalanceFactory(operation=None)

    with pytest.raises(ValidationError):
        CreateBalanceFactory(value=-1)

    with pytest.raises(ValidationError):
        CreateBalanceFactory(description="")


def test_get_all_success(session: Session, context: Context):
    # prepare
    query = QueryBalance()

    # create
    for _ in range(10):
        schema = CreateBalanceFactory(operation=OperationType.PAYMENT_OF_SUPPLIERS)
        controller.balance.create(session, schema=schema, context=context)

    balances = controller.balance.get_all(session, query_schema=query, context=context)

    # assert
    assert all(isinstance(balance, Balance) for balance in balances)
