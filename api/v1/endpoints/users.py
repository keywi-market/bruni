from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, schemas
from api import deps

router = APIRouter()


@router.get("/{user_id}/products", response_model=List[schemas.Product])
def read_items(
        user_id: UUID,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    product = crud.product.get_by_user_id(db=db, user_id=user_id, skip=skip, limit=limit)
    if not product:
        raise HTTPException(status_code=204, detail=f"{user_id} has no products")
    return product


@router.post("/{user_id}/products", response_model=schemas.Product, status_code=201)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        product_in: schemas.ProductCreate,
) -> schemas.Product:
    product = crud.product.create(db=db, obj_in=product_in, user_id=product_in.user_id)
    return product


# patch or put ?!?!
@router.patch("/{user_id}/products/{product_id}", response_model=schemas.Product)
def create_item(
        *,
        user_id: UUID,
        product_id: UUID,
        db: Session = Depends(deps.get_db),
        product_in: schemas.ProductUpdate,
) -> schemas.Product:
    product = crud.product.get_by_product_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product
