from decimal import Decimal

from pydantic import BaseModel, ConfigDict, condecimal, conint, constr


class ProductCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: constr(min_length=2, max_length=150)
    price: condecimal(gt=Decimal("0"), max_digits=10, decimal_places=2)
    count: conint(ge=0, le=100000)
    description: constr(min_length=5, max_length=500)
