from typing import Union
from uuid import uuid4

import inject
from sqlmodel import Session, select

from src.core.events import EventDescription
from src.core.models import Context, File
from src.core.services import Storage, Streamer
from src.utils.miscellaneous import get_file_hash


@inject.params(streamer=Streamer, storage=Storage)
def get_or_create_file(
    session: Session,
    preffix: str,
    filename: str,
    file: Union[str, bytes],
    context: Context,
    streamer: Streamer,
    storage: Storage,
) -> File:
    file_hash = get_file_hash(file)
    file_obj = session.exec(select(File).where(File.hash == file_hash)).first()
    extension = filename.split(".")[-1]

    if not file_obj:
        streamer.send_event(
            EventDescription.UPLOAD_FILE, context=context, file={"filename": filename, "hash": file_hash}
        )
        file_obj = File(bucket_key=f"{preffix}-{uuid4()}.{extension}", hash=file_hash)
        session.add(file_obj)

    if not storage.check_file_exists(file_obj.bucket_key):
        storage.upload_file(file, key=file_obj.bucket_key)
        streamer.send_event(
            EventDescription.UPLOAD_FILE,
            context=context,
            file={"filename": filename, "hash": file_hash, "bucket_key": file_obj.bucket_key},
        )

    return file_obj


@inject.params(storage=Storage)
def check_file_exists(bucket_key: str, storage: Storage) -> bool:
    return storage.check_file_exists(bucket_key)
