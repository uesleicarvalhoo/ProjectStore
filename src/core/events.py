from enum import Enum


class EventCode(str, Enum):
    # User range 100 ~ 199
    CREATE_USER: int = 100
    UPDATE_USER: int = 101
    DELETE_USER: int = 102

    # Client range 200 ~ 299
    CREATE_CLIENT: int = 200
    UPDATE_CLIENT: int = 101
    DELETE_CLIENT: int = 102

    # Item range 300~399
    CREATE_ITEM: int = 300
    UPDATE_ITEM: int = 301
    DELETE_ITEM: int = 302

    # FiscalNote range 400~499
    CREATE_FISCAL_NOTE: int = 400
    UPDATE_FISCAL_NOTE: int = 401
    DELETE_FISCAL_NOTE: int = 402

    # File range 500~599
    UPLOAD_FILE: int = 500
    DELETE_FILE: int = 502

    # Order range 600~699
    CREATE_ORDER: int = 600
    UPDATE_ORDER: int = 601
    DELETE_ORDER: int = 602
