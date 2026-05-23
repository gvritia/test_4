"""Роуты для работы с товарами.

Относится к заданиям:
- 9.1: использует SQLAlchemy-модель Product и данные из Alembic-миграций;
- 10.1: выбрасывает кастомную ошибку, если товар не найден;
- 11.1: покрывается тестами на успешные и ошибочные сценарии.
"""

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.response_docs import PRODUCT_CREATE_RESPONSES, PRODUCT_GET_RESPONSES, PRODUCT_LIST_RESPONSES
from app.core.database import get_db
from app.exceptions.product_not_found_error import ProductNotFoundError
from app.models.model_product import Product
from app.models.model_product_create_request import ProductCreateRequest
from app.models.model_product_response import ProductResponse

# Этот роутер отвечает только за ресурс products.
router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список товаров",
    description=(
        "Возвращает список товаров из базы данных.\n\n"
        "**Относится к заданиям:** `9.1`, `11.1`.\n\n"
        "Здесь демонстрируются:\n"
        "- работа с SQLAlchemy-моделью `Product`;\n"
        "- чтение данных, созданных Alembic-миграциями;\n"
        "- REST-получение коллекции через `GET`."
    ),
    responses=PRODUCT_LIST_RESPONSES,
)
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    # select(Product) строит SQL-запрос на получение всех товаров из таблицы.
    # order_by(Product.id) нужен для стабильного порядка элементов в ответе.
    return db.execute(select(Product).order_by(Product.id)).scalars().all()


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать товар",
    description=(
        "Создает новый товар в базе данных.\n\n"
        "**Относится к заданиям:** `9.1`, `11.1`.\n\n"
        "Здесь демонстрируются:\n"
        "- создание записи через SQLAlchemy;\n"
        "- REST-создание ресурса через `POST`;\n"
        "- валидация JSON-тела перед сохранением в БД."
    ),
    responses=PRODUCT_CREATE_RESPONSES,
)
def create_product(payload: ProductCreateRequest, db: Session = Depends(get_db)) -> Product:
    # Преобразуем Pydantic-модель в словарь и на его основе создаем ORM-объект.
    product = Product(**payload.model_dump())
    # add - кладет объект в текущую сессию,
    # commit - сохраняет изменения в БД,
    # refresh - перечитывает объект, чтобы получить актуальные поля из БД.
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить товар по идентификатору",
    description=(
        "Возвращает товар по его идентификатору.\n\n"
        "**Относится к заданиям:** `9.1`, `10.1`, `11.1`.\n\n"
        "Здесь демонстрируются:\n"
        "- получение одной записи из БД;\n"
        "- пользовательская ошибка `404`, если товар не найден;\n"
        "- валидация path-параметра `product_id`."
    ),
    responses=PRODUCT_GET_RESPONSES,
)
def get_product(
    product_id: int = Path(gt=0, description="Положительный идентификатор товара."),
    db: Session = Depends(get_db),
) -> Product:
    # Ищем товар по первичному ключу.
    product = db.get(Product, product_id)
    if product is None:
        # Вместо сырого HTTPException используем кастомную предметную ошибку.
        raise ProductNotFoundError(product_id)
    return product
