from base64 import b64encode
from random import choice

from sqlalchemy.orm import Session

from src.core.database.models import Client as ClientModel
from src.core.database.models import File as FileModel
from src.core.database.models import FiscalNote as FiscalNoteModel
from src.core.database.models import Item as ItemModel
from src.core.database.models import Order as OrderModel
from src.core.database.models import OrderDetail as OrderDetailModel
from src.core.schemas import CreateClient, CreateFile, CreateFiscalNote, CreateItem, CreateOrder, CreateOrderDetail
from tests.utils import faker


def test_create_order(session: Session):
    client = ClientModel.create(
        session,
        CreateClient(
            name=faker.random_name(),
            email=faker.random_email(),
            phone=faker.random_phone(),
        ),
    )

    # Create FiscalNote
    with open("tests/static/fiscal_note.png", "rb") as f:
        fn_image = b64encode(f.read())

    fn_file = FileModel.create(
        session,
        CreateFile(
            bucket_key=faker.random_bucket_key(),
            hash=faker.random_hash(),
        ),
    )

    fiscal_note = FiscalNoteModel.create(
        session,
        CreateFiscalNote(
            description=faker.random_description(),
            purchase_date=faker.random_date(),
            file_id=fn_file.bucket_key,
            filename=faker.random_filename("image", "png"),
            image=fn_image,
        ),
        fn_file,
    )

    # Create Item
    with open("tests/static/fiscal_note.png", "rb") as f:
        item_image = b64encode(f.read())

    item = ItemModel.create(
        session,
        CreateItem(
            code=faker.random_lower_string(),
            avaliable=choice([True, False]),
            buy_value=faker.random_float_value(),
            filename=faker.random_filename("image", "png"),
            image=item_image,
        ),
        fiscal_note_id=fiscal_note.id,
        file=FileModel.create(session, CreateFile(bucket_key=faker.random_bucket_key(), hash=faker.random_hash())),
    )

    # Create order and order detail
    order_detail_schema = CreateOrderDetail(item_id=item.id, buy_value=item.buy_value, sell_value=item.buy_value * 0.5)

    schema = CreateOrder(client_id=client.id, date=faker.random_date(), details=[order_detail_schema])

    order = OrderModel.create(session, schema)
    order_detail = OrderDetailModel.create(session, order_detail_schema, order.id)

    order2 = OrderModel.get(session, order.id)

    # Assert Schema
    assert order.client_id == schema.client_id

    # Assert Creation
    assert order2 is not None
    assert order.id == order2.id
    assert order == order2

    # Assert relationship
    assert order.client == client
    assert len(order.details) == 1
    assert order.details == [order_detail]
    assert order_detail.order == order
