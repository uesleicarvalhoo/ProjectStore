from datetime import date, timedelta
from typing import List

import factory
from factory import fuzzy

from src.core.models.fiscal_note import CreateFiscalNote
from src.core.models.item import Item

from .fiscal_note_item import CreateFiscalNoteItemFactory


class CreateFiscalNoteFactory(factory.Factory):
    image: bytes = factory.Faker("image")
    filename: str = factory.Faker("file_name", extension="png")
    description: str = factory.Faker("sentence")
    purchase_date: date = fuzzy.FuzzyDate(date.today() - timedelta(days=30), date.today())
    items: List[Item] = factory.List([factory.SubFactory(CreateFiscalNoteItemFactory)])

    class Meta:
        model = CreateFiscalNote
