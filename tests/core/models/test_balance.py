from src.core.constants import PaymentType, SaleType
from tests.factories.balance import CreateBalanceFactory


def test_normalize_positive_value_of_sale_type_from_create_balance_success():
    balance = CreateBalanceFactory(value=100, operation=SaleType.SALE_IN_PIX.value)

    assert balance.value == 100


def test_normalize_negative_value_of_sale_type_from_create_balance_success():
    balance = CreateBalanceFactory(value=-100, operation=SaleType.SALE_IN_PIX.value)

    assert balance.value == 100


def test_normalize_positive_value_of_payment_type_from_create_balance_success():
    balance = CreateBalanceFactory(value=100, operation=PaymentType.PAYMENT_OF_EMPLOYEES.value)

    assert balance.value == -100


def test_normalize_negative_value_of_payment_type_from_create_balance_success():
    balance = CreateBalanceFactory(value=-100, operation=PaymentType.PAYMENT_OF_EMPLOYEES.value)

    assert balance.value == -100
