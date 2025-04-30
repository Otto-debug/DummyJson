from pydantic import BaseModel, Field, HttpUrl
from typing import List


class ProductInCartBase(BaseModel):
    id: int
    title: str
    price: float
    quantity: int
    total: float
    discountPercentage: float
    thumbnail: HttpUrl

class ProductInCartGET(ProductInCartBase):
    discountedTotal: float

class ProductInCartPOSTPUT(ProductInCartBase):
    discountedPrice: float


class CartGET(BaseModel):
    id: int
    products: List[ProductInCartGET]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int

class CartPOSTPUT(BaseModel):
    id: int
    products: List[ProductInCartPOSTPUT]
    total: float
    userId: int
    totalProducts: int
    totalQuantity: int