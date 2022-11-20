from typing import Generator

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from core.config import settings
from db.base_class import Base
from db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
