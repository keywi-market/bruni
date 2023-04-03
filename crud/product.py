from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Product
from schemas import ProductCreate, ProductUpdate, ProductOrderType


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):

    def get_by_product_id(self, db: Session, product_id: UUID) -> Optional[Product]:
        product = db.query(self.model).filter(self.model.product_id == product_id,
                                              self.model.is_deleted.is_(False)).first()
        if product is None:
            return product
        product.count += 1
        db.commit()
        return product

    def get_by_user_id_and_product_id(self, db: Session, user_id: UUID, product_id: UUID) -> Optional[Product]:
        product = db.query(self.model).filter(self.model.user_id == user_id,
                                              self.model.product_id == product_id,
                                              self.model.is_deleted.is_(False)).first()
        if product is None:
            return product
        product.count += 1
        db.commit()
        return product

    def get_by_user_id(self, db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(self.model).filter(self.model.user_id == user_id, self.model.is_deleted.is_(False)) \
            .offset(skip).limit(limit).all()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100,
            order_by: ProductOrderType = ProductOrderType.RECENT, category_name: str = None, brand_name: str = None
    ) -> List[Product]:

        if category_name is None and brand_name is None:
            q = db.query(self.model).filter(self.model.is_deleted.is_(False))

        elif category_name is not None and brand_name is None:
            q = db.query(self.model) \
                .filter(
                self.model.is_deleted.is_(False),
                self.model.category == category_name
            )

        elif category_name is None and brand_name is not None:
            q = db.query(self.model) \
                .filter(
                self.model.is_deleted.is_(False),
                self.model.brand == brand_name
            )

        else:
            q = db.query(self.model) \
                .filter(
                self.model.is_deleted.is_(False),
                self.model.category == category_name,
                self.model.brand == brand_name
            )

        if order_by == ProductOrderType.RECENT:
            return q.order_by(self.model.created_time.desc()) \
                .offset(skip).limit(limit).all()

        elif order_by == ProductOrderType.HIGH_PRICE:
            return q.order_by(self.model.price.desc()) \
                .offset(skip).limit(limit).all()

        elif order_by == ProductOrderType.LOW_PRICE:
            return q.order_by(self.model.price.asc()) \
                .offset(skip).limit(limit).all()

        elif order_by == ProductOrderType.MOST_VIEWED:
            return q.order_by(self.model.count.desc()) \
                .offset(skip).limit(limit).all()

        elif order_by == ProductOrderType.SELLING:
            return q.filter(self.model.status == Product.STATUS_DEFAULT_VALUE) \
                .order_by(self.model.created_time.desc()) \
                .offset(skip).limit(limit).all()

        return q.order_by(self.model.created_time.desc())

    # todo product 테이블에서는 flag 처리하지만, product image는 어떻게 할지 고민해야봐야함.
    def remove_user_id_and_product_id(self, db: Session, user_id: UUID, product_id: UUID) -> Optional[Product]:
        product = db.query(self.model).filter(self.model.user_id == user_id,
                                              self.model.product_id == product_id,
                                              self.model.is_deleted.is_(False)).first()
        if product is None:
            return product
        product.is_deleted = True
        product.images = []
        db.commit()
        return product


crud_product = CRUDProduct(Product)
