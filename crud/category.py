from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from crud import CRUDBase
from models.brand import Brand
from models.category import Category
from schemas import BrandCreate, BrandUpdate
from schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    # category
    def get_by_category_id(self, db: Session, category_id: UUID) -> Optional[Category]:
        return db.query(self.model).filter(self.model.category_id == category_id).first()

    def remove_category(self, db: Session, *, category_id: UUID) -> Optional[Category]:
        category = self.get_by_category_id(db, category_id)
        if category is None:
            return category
        db.delete(category)
        db.commit()
        return category

    # brand
    def add_brand(self, db: Session, *, category_id: UUID, obj_in: BrandCreate, create_user_id: UUID) -> Optional[
        Category]:
        category = self.get_by_category_id(db, category_id)
        if category is None:
            return category

        brand_db_obj = Brand(
            category_id=category_id,
            brand_name=obj_in.brand_name,
            create_user=create_user_id,
            update_user=create_user_id,
        )
        category.brands.append(brand_db_obj)
        db.commit()
        db.refresh(category)
        return category

    def update_brand(self, db: Session, *, category_id: UUID, brand_id: UUID, obj_in: BrandUpdate, update_user_id: UUID) \
            -> Optional[Category]:
        category = self.get_by_category_id(db, category_id)
        if category is None:
            return category

        target_brand = None

        for brand in category.brands:
            if brand.brand_id == brand_id:
                target_brand = brand

        if target_brand is None:
            return target_brand

        target_brand.brand_name = obj_in.brand_name
        target_brand.update_user = update_user_id

        db.commit()
        db.refresh(category)
        return category

    def remove_brand(self, db: Session, *, category_id: UUID, brand_id: UUID) -> Optional[Category]:
        category = self.get_by_category_id(db, category_id)
        if category is None:
            return category

        target_brand = None

        for brand in category.brands:
            if brand.brand_id == brand_id:
                target_brand = brand

        if target_brand is None:
            return target_brand

        category.brands.remove(target_brand)
        db.commit()
        db.refresh(category)
        return category


crud_category = CRUDCategory(Category)
