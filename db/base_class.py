from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    create_user = Column(UUID(as_uuid=True))
    created_time = Column(DateTime, default=datetime.utcnow)
    update_user = Column(UUID(as_uuid=True))
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
