from enum import Enum, IntEnum, unique
from typing import List, Union

from elasticapm.conf.constants import BASE_SANITIZE_FIELD_NAMES_UNPROCESSED

APM_SANITIZE_FIELDS = [] + BASE_SANITIZE_FIELD_NAMES_UNPROCESSED


@unique
class EnvironmentEnum(str, Enum):
    production = "prod"
    development = "dev"
    testing = "test"

    def __str__(self) -> str:
        return self.name


@unique
class ContextEnum(str, Enum):
    API: str = "api"
    WEB: str = "web"
    TEST: str = "test"
    APPLICATION: str = "application"


@unique
class OrderStatus(IntEnum):
    PENDING: int = 1
    COMPLETED: int = 2
    CANCELED: int = 3


@unique
class AccessLevel(str, Enum):
    ANONIMOUS: str = "ANONIMOUS"
    USER: str = "USER"
    SUPER_USER: str = "SUPER_USER"


@unique
class OperationType(str, Enum):
    PAYMENT_OF_EMPLOYEES: str = "Pagamento de funcionarios"
    PAYMENT_OF_SUPPLIERS: str = "Pagamento de fornecedores"
    ANOTHER_PAYMENTS: str = "Outros pagamentos"
    SALE_IN_PIX: str = "Venda via PIX"
    SALE_IN_DEBT: str = "Venda no débito"
    SALE_IN_CREDIT: str = "Venda no crédito"
    SALE_IN_MONEY: str = "Venda em dinheiro"

    @staticmethod
    def list_sale_types() -> List["OperationType"]:
        return [
            OperationType.SALE_IN_PIX,
            OperationType.SALE_IN_CREDIT,
            OperationType.SALE_IN_DEBT,
            OperationType.SALE_IN_MONEY,
            OperationType.SALE_IN_MONEY,
        ]

    @staticmethod
    def list_all() -> List["OperationType"]:
        return [
            OperationType.PAYMENT_OF_EMPLOYEES,
            OperationType.PAYMENT_OF_SUPPLIERS,
            OperationType.SALE_IN_PIX,
            OperationType.SALE_IN_DEBT,
            OperationType.SALE_IN_CREDIT,
            OperationType.SALE_IN_MONEY,
        ]

    @staticmethod
    def list_payment_types() -> List["OperationType"]:
        return [
            OperationType.PAYMENT_OF_EMPLOYEES,
            OperationType.PAYMENT_OF_SUPPLIERS,
            OperationType.ANOTHER_PAYMENTS,
        ]


@unique
class BalanceType(str, Enum):
    DEBT: str = "Saida"
    CREDIT: str = "Entrada"

    @staticmethod
    def list_all() -> List["BalanceType"]:
        return [BalanceType.DEBT, BalanceType.CREDIT]

    @staticmethod
    def get_by_operation_type(operation_type: Union[None, OperationType]) -> Union["BalanceType", None]:
        if operation_type in OperationType.list_sale_types():
            return BalanceType.CREDIT

        elif operation_type in OperationType.list_payment_types():
            return BalanceType.DEBT
