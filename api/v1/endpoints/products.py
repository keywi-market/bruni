from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, schemas
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def read_items(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> List[schemas.Product]:
    return crud.product.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas.Product)
def read_items(
        product_id: UUID,
        db: Session = Depends(deps.get_db)
) -> schemas.Product:
    product = crud.product.get_by_product_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
