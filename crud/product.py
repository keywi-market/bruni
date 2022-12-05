from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Product
from schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_product_id(self, db: Session, product_id: UUID) -> Optional[Product]:
        product = db.query(self.model).filter(self.model.product_id == product_id).first()
        product.count += 1
        db.commit()
        return product

    def get_by_user_id(self, db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()


product = CRUDProduct(Product)
