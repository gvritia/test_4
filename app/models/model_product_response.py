"""Модель ответа с данными товара.

Относится к заданиям 9.1 и 10.1.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    # from_attributes=True позволяет строить ответ напрямую из ORM-объекта Product.
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: Decimal
    count: int
    description: str
    # В ответе тоже показываем check как логическое значение.
    check: bool
