from enum import Enum


class EventEnum(Enum):
    # User range 100 ~ 199
    CREATE_USER: int = 100, "create-user"
    UPDATE_USER: int = 101, "update-user"
    DELETE_USER: int = 102, "delete-user"

    # Client range 200 ~ 299
    CREATE_CLIENT: int = 200, "create-client"
    UPDATE_CLIENT: int = 101, "update-client"
    DELETE_CLIENT: int = 102, "delete-client"

    # Item range 300~399
    CREATE_ITEM: int = 300, "create-item"
    UPDATE_ITEM: int = 301, "update-item"
    DELETE_ITEM: int = 302, "delete-item"

    # FiscalNote range 400~499
    CREATE_FISCAL_NOTE: int = 400, "create-fiscal-note"
    UPDATE_FISCAL_NOTE: int = 401, "update-fiscal-note"
    DELETE_FISCAL_NOTE: int = 402, "delete-fiscal-note"

    # File range 500~599
    UPLOAD_FILE: int = 500, "upload-file"
    DELETE_FILE: int = 502, "delete-file"

    # Order range 600~699
    CREATE_ORDER: int = 600, "create-order"
    UPDATE_ORDER: int = 601, "update-order"
    DELETE_ORDER: int = 602, "delete-order"
