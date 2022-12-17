from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from api import deps
from crud.brand import crud_brand

router = APIRouter()


@router.get("/", response_model=List[schemas.Brand])
def read_brands(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> List[schemas.Brand]:
    brands = crud_brand.get_multi(db=db, skip=skip, limit=limit)
    if len(brands) == 0:
        raise HTTPException(status_code=204, detail=f"Doesn't exists any brands")
    return brands
