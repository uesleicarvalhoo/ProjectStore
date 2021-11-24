from enum import Enum


class EventDescription(str, Enum):
    CREATE_USER: str = "create-user"
    UPDATE_USER: str = "update-user"
    DELETE_USER: str = "delete-user"

    CREATE_CLIENT: str = "create-client"
    UPDATE_CLIENT: str = "update-client"
    DELETE_CLIENT: str = "delete-client"

    CREATE_ITEM: str = "create-item"
    UPDATE_ITEM: str = "update-item"
    DELETE_ITEM: str = "delete-item"

    CREATE_FISCAL_NOTE: str = "create-fiscal-note"
    UPDATE_FISCAL_NOTE: str = "update-fiscal-note"
    DELETE_FISCAL_NOTE: str = "delete-fiscal-note"

    CREATE_FISCAL_NOTE_ITEM: str = "create-fiscal-note-item"
    UPDATE_FISCAL_NOTE_ITEM: str = "update-fiscal-note-item"
    DELETE_FISCAL_NOTE_ITEM: str = "delete-fiscal-note-item"

    UPLOAD_FILE: str = "upload-file"
    DELETE_FILE: str = "delete-file"

    CREATE_ORDER: str = "create-order"
    UPDATE_ORDER: str = "update-order"
    DELETE_ORDER: str = "delete-order"

    CREATE_BALANCE: str = "create-balance"
    UPDATE_BALANCE: str = "update-balance"
    DELETE_BALANCE: str = "delete-balance"
