from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, schemas
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def read_products(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> List[schemas.Product]:
    products = crud.product.get_multi(db=db, skip=skip, limit=limit)
    if len(products) == 0:
        raise HTTPException(status_code=204, detail=f"Doesn't exists any products")
    return products


@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
        product_id: UUID,
        db: Session = Depends(deps.get_db)
) -> schemas.Product:
    product = crud.product.get_by_product_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product is not found")
    if product.is_deleted is True:
        raise HTTPException(status_code=400, detail=f"Product is already deleted")
    return product
