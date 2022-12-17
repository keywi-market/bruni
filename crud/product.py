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
        if product is None:
            return product
        product.count += 1
        db.commit()
        return product

    def get_by_user_id(self, db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(self.model).filter(self.model.user_id == user_id, self.model.is_deleted.is_(False)) \
            .offset(skip).limit(limit).all()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return db.query(self.model).filter(self.model.is_deleted.is_(False)).offset(skip).limit(limit).all()

    def remove(self, db: Session, product_id: UUID) -> Optional[Product]:
        product = db.query(self.model).filter(self.model.product_id == product_id).first()
        if product is None:
            return product
        product.is_deleted = True
        db.commit()
        return product


crud_product = CRUDProduct(Product)
