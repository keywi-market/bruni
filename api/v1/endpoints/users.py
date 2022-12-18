from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from api import deps
from crud import crud_product

router = APIRouter()


@router.get("/{user_id}/products", response_model=List[schemas.Product])
def read_products(
        user_id: UUID,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    products = crud_product.get_by_user_id(db=db, user_id=user_id, skip=skip, limit=limit)
    if len(products) == 0:
        raise HTTPException(status_code=204, detail=f"{user_id} has no products")
    return products


@router.post("/{user_id}/products", response_model=schemas.Product, status_code=201)
def create_product(
        *,
        db: Session = Depends(deps.get_db),
        product_in: schemas.ProductCreate,
) -> schemas.Product:
    product = crud_product.create(db=db, obj_in=product_in, user_id=product_in.user_id)
    return product


# patch or put ?!?!
@router.patch("/{user_id}/products/{product_id}", response_model=schemas.Product)
def update_product(
        *,
        user_id: UUID,
        product_id: UUID,
        db: Session = Depends(deps.get_db),
        product_in: schemas.ProductUpdate,
) -> schemas.Product:
    product = crud_product.get_by_product_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product is not found")
    if product.is_deleted is True:
        raise HTTPException(status_code=404, detail=f"Product is already deleted")
    product = crud_product.update(db=db, db_obj=product, obj_in=product_in)
    return product


@router.delete("/{user_id}/products/{product_id}", status_code=200)
def delete_product(
        *,
        user_id: UUID,
        product_id: UUID,
        db: Session = Depends(deps.get_db),
):
    product = crud_product.remove(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product is not found")
    return product
