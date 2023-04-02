import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base


class Category(Base):
    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = Column(String(100))

    brands = relationship(
        "Brand",
        back_populates="category",
        cascade="all, delete, delete-orphan",
    )

# Category.__table__.create(engine)
