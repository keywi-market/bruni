from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, schemas
from api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Product)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        product_in: schemas.ProductCreate,
) -> schemas.Product:
    product = crud.product.create(db=db, obj_in=product_in,user_id=product_in.user_id)
    return product
