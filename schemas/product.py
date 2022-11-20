from abc import abstractmethod, ABCMeta
from datetime import datetime
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel


class ProductBase(BaseModel):
    user_id: UUID
    title: str
    contents: str
    category: str
    brand: str
    price: int
    phone_number: str


class ProductCreate(ProductBase):
    pass


# Update means using put method, not fetch method.
class ProductUpdate(ProductBase):
    status: Literal["selling", "booked", "sold"]
    update_user_id: str


# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    product_id: UUID
    status: str
    count: int
    create_user: UUID
    updated_time: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    pass
