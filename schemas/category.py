from uuid import UUID

from pydantic import BaseModel


class CategoryBase(BaseModel):
    category_name: str


class CategoryCreate(CategoryBase):
    pass


# Update means using put method, not fetch method.
class CategoryUpdate(CategoryBase):
    pass


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    category_id: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass
