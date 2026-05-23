"""Ошибка отсутствующего товара.

Относится к заданиям 9.1 и 10.1: ресурс Product хранится в БД,
а ошибка превращается в управляемый HTTP 404.
"""

from app.exceptions.application_error import ApplicationError


class ProductNotFoundError(ApplicationError):
    def __init__(self, product_id: int) -> None:
        super().__init__(
            status_code=404,
            error="product_not_found",
            message=f"Товар с id={product_id} не найден.",
        )
