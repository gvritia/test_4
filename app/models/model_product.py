"""SQLAlchemy-модель товара.

Относится к заданию 9.1: по этой модели строятся миграции и таблица products.
"""

from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    # Имя таблицы в базе данных.
    __tablename__ = "products"

    # mapped_column описывает колонки таблицы и их ограничения.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    # Поле description появилось во второй миграции и обязательно по условию задания.
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # Поле check появилось в новой миграции и хранится как логический флаг.
    check: Mapped[bool] = mapped_column(Boolean, nullable=False)
