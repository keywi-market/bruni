from datetime import datetime
from enum import Enum
from typing import Optional, Literal, List
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


class ProductImageBase(BaseModel):
    image_url: str


class ProductCreate(ProductBase):
    images: Optional[List[ProductImageBase]]


# Update means using put method, not fetch method.
class ProductUpdate(BaseModel):
    title: Optional[str]
    contents: Optional[str]
    category: Optional[str]
    brand: Optional[str]
    price: Optional[int]
    phone_number: Optional[str]
    status: Optional[Literal["selling", "booked", "sold"]]
    update_user: UUID

    class Config:
        schema_extra = {
            "example": {
                "title": "Optional[str]",
                "contents": "Optional[str]",
                "category": "Optional[str]",
                "brand": "Optional[str]",
                "price": "Optional[str]",
                "phone_number": "Optional[str]",
                "status": "Optional[Literal[\"selling\", \"booked\", \"sold\"]]",
                "update_user": "uuid"
            }
        }


# Properties shared by models stored in DB
class ProductImageInDBBase(ProductImageBase):
    image_url: str

    class Config:
        orm_mode = True


class ProductInDBBase(ProductBase):
    product_id: UUID
    status: str
    count: Optional[int]
    images: Optional[List[ProductImageInDBBase]]
    create_user: UUID
    created_time: datetime
    update_user: UUID
    updated_time: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    pass


class ProductOrderType(str, Enum):
    RECENT = "recent"
    HIGH_PRICE = "high_price"
    LOW_PRICE = "low_price"
    MOST_VIEWED = "most_viewed"
    SELLING = "selling"
