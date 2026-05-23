"""Модель JSON-запроса для создания товара.

Относится к заданиям 9.1 и 10.2: продукт хранится в БД, а входные данные валидируются.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, condecimal, conint, constr


class ProductCreateRequest(BaseModel):
    # Запрещаем лишние поля и автоматически убираем пробелы по краям строк.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    # Название товара не должно быть пустым и слишком длинным.
    title: constr(min_length=2, max_length=150)
    # Цена должна быть больше нуля и содержать максимум 2 знака после запятой.
    price: condecimal(gt=Decimal("0"), max_digits=10, decimal_places=2)
    # Остаток на складе не может быть отрицательным.
    count: conint(ge=0, le=100000)
    # description обязателен, потому что так требует задание 9.1.
    description: constr(min_length=5, max_length=500)
    # check - логический флаг, который хранится в БД как Boolean.
    check: bool
