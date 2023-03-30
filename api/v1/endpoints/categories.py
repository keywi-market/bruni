from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from api import deps
from crud.category import crud_category

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def read_categories(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> List[schemas.Category]:
    categories = crud_category.get_multi(db=db, skip=skip, limit=limit)
    if len(categories) == 0:
        raise HTTPException(status_code=204, detail=f"Doesn't exists any categories")
    return categories


@router.post("/", response_model=schemas.Category, status_code=201)
def create_category(
        *,
        db: Session = Depends(deps.get_db),
        category_in: schemas.CategoryCreate
) -> schemas.Category:
    requset_user_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    category = crud_category.create(db=db, obj_in=category_in, create_user_id=requset_user_id)
    return category


@router.patch("/{category_id}", response_model=schemas.Category)
def update_category(
        *,
        category_id: UUID,
        db: Session = Depends(deps.get_db),
        category_in: schemas.CategoryUpdate
) -> schemas.Category:
    requset_user_id = "856a95ea-c48e-4ba3-b322-69d7c810fb08"
    category = crud_category.get_by_category_id(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category is not found")
    category = crud_category.update(db=db, db_obj=category, obj_in=category_in, update_user_id=requset_user_id)
    return category


@router.delete("/{category_id}", status_code=200)
def delete_category(
        *,
        category_id: UUID,
        db: Session = Depends(deps.get_db),
):
    category = crud_category.remove_category(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category is not found")
    return


@router.get("/{category_id}/brands", response_model=List[schemas.Brand])
def read_brands(
        *,
        category_id: UUID,
        db: Session = Depends(deps.get_db)
) -> List[schemas.Brand]:
    category = crud_category.get_by_category_id(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category doesn't exist")

    brands = category.brands
    if len(brands) == 0:
        raise HTTPException(status_code=204, detail="Category doesn't have any brands")
    return category.brands


@router.post("/{category_id}/brands", response_model=schemas.Category, status_code=201)
def create_brand(
        *,
        category_id: UUID,
        db: Session = Depends(deps.get_db),
        brand_in: schemas.BrandCreate
) -> schemas.Category:
    requset_user_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    category = crud_category.add_brand(db=db, category_id=category_id, obj_in=brand_in,
                                       create_user_id=requset_user_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category doesn't exist")
    return category


@router.patch("/{category_id}/brands/{brand_id}", response_model=schemas.Category)
def update_brand(
        *,
        category_id: UUID,
        brand_id: UUID,
        db: Session = Depends(deps.get_db),
        brand_in: schemas.BrandUpdate
) -> schemas.Category:
    requset_user_id = "856a95ea-c48e-4ba3-b322-69d7c810fb08"
    category = crud_category.update_brand(db=db, category_id=category_id, brand_id=brand_id, obj_in=brand_in,
                                          update_user_id=requset_user_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category or Brand doesn't exist")
    return category


@router.delete("/{category_id}/brands/{brand_id}", response_model=schemas.Category)
def delete_brand(
        *,
        category_id: UUID,
        brand_id: UUID,
        db: Session = Depends(deps.get_db),
) -> schemas.Category:
    category = crud_category.remove_brand(db=db, category_id=category_id, brand_id=brand_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category or Brand doesn't exist")
    return category
