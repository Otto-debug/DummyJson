from pydantic import BaseModel, Field
from typing import List

class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    brand: str
    category: str
    thumbnail: str
    images: List[str]

class ProductsList(BaseModel):
    products: List[Product]
    total: int
    skip: int
    limit: int

class ProductCreate(BaseModel):
    title: str