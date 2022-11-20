from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Product
from schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product]):

    def create(
            self, db: Session, *, obj_in: ProductCreate, owner_id: int
    ) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


product = CRUDProduct(Product)
