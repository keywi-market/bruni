from uuid import UUID

from pydantic import BaseModel


class BrandBase(BaseModel):
    brand_name: str


class BrandCreate(BrandBase):
    pass


# Update means using put method, not fetch method.
class BrandUpdate(BrandBase):
    pass


# Properties shared by models stored in DB
class BrandInDBBase(BrandBase):
    brand_id: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Brand(BrandInDBBase):
    pass
