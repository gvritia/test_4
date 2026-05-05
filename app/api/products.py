from fastapi import APIRouter, Depends, Path, status
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.api.response_docs import PRODUCT_CREATE_RESPONSES, PRODUCT_GET_RESPONSES, PRODUCT_LIST_RESPONSES
from app.core.database import get_db
from app.exceptions.product_not_found_error import ProductNotFoundError
from app.models.model_product import Product
from app.models.model_product_create_request import ProductCreateRequest
from app.models.model_product_response import ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список товаров",
    responses=PRODUCT_LIST_RESPONSES,
)
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    return db.execute(select(Product).order_by(Product.id)).scalars().all()


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать товар",
    responses=PRODUCT_CREATE_RESPONSES,
)
def create_product(payload: ProductCreateRequest, db: Session = Depends(get_db)) -> Product:
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить товар по идентификатору",
    responses=PRODUCT_GET_RESPONSES,
)
def get_product(
    product_id: int = Path(gt=0, description="Положительный идентификатор товара."),
    db: Session = Depends(get_db),
) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise ProductNotFoundError(product_id)
    return product
