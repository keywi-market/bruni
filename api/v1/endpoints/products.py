from typing import Any, List, Optional, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import schemas
from api import deps
from crud.product import crud_product
from schemas import ProductOrderType

router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def read_products(
        db: Session = Depends(deps.get_db),
        category_name: Optional[str] = Query(None),
        brand_name: Optional[str] = Query(None),
        order: Literal[
            ProductOrderType.RECENT,
            ProductOrderType.HIGH_PRICE,
            ProductOrderType.LOW_PRICE,
            ProductOrderType.MOST_VIEWED,
            ProductOrderType.SELLING]
        = ProductOrderType.RECENT,
        skip: int = 0,
        limit: int = 100,
) -> List[schemas.Product]:
    products = crud_product.get_multi(db=db, skip=skip, limit=limit, order_by=order,
                                      category_name=category_name, brand_name=brand_name)
    if len(products) == 0:
        raise HTTPException(status_code=204, detail=f"Doesn't exists any products")
    return products


@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
        product_id: UUID,
        db: Session = Depends(deps.get_db)
) -> schemas.Product:
    product = crud_product.get_by_product_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product is not found")
    if product.is_deleted is True:
        raise HTTPException(status_code=400, detail=f"Product is already deleted")
    return product
