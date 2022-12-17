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
