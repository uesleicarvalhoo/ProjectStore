from enum import Enum, unique


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
    TEST: str = "test"
    APPLICATION: str = "application"


@unique
class OrderStatus(str, Enum):
    PENDING: int = "Pendente"
    COMPLETED: int = "Concluido"
    CANCELED: int = "Cancelado"


@unique
class AccessLevel(str, Enum):
    ANONIMOUS: str = "ANONIMOUS"
    USER: str = "USER"
    SUPER_USER: str = "SUPER_USER"


class SaleType(str, Enum):
    SALE_IN_PIX: str = "Venda via PIX"
    SALE_IN_DEBT: str = "Venda no débito"
    SALE_IN_CREDIT: str = "Venda no crédito"
    SALE_IN_MONEY: str = "Venda em dinheiro"
    SALE_IN_TRANSFER: str = "Venda por transferencia bancaria"
    SALE_IN_BILLET: str = "Venda por boleto"
    SALE_OTHERS: str = "Outra tipo de venda"


class PaymentType(str, Enum):
    PAYMENT_OF_EMPLOYEES: str = "Pagamento de funcionarios"
    PAYMENT_OF_SUPPLIERS: str = "Pagamento de fornecedores"
    ANOTHER_PAYMENTS: str = "Outros pagamentos"


@unique
class OperationType(str, Enum):
    SALE_IN_PIX: str = "Venda via PIX"
    SALE_IN_DEBT: str = "Venda no débito"
    SALE_IN_CREDIT: str = "Venda no crédito"
    SALE_IN_MONEY: str = "Venda em dinheiro"
    SALE_IN_TRANSFER: str = "Venda por transferencia bancaria"
    SALE_IN_BILLET: str = "Venda por boleto"
    SALE_OTHERS: str = "Outra tipo de venda"
    PAYMENT_OF_EMPLOYEES: str = "Pagamento de funcionarios"
    PAYMENT_OF_SUPPLIERS: str = "Pagamento de fornecedores"
    ANOTHER_PAYMENTS: str = "Outros pagamentos"
