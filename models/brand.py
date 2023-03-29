import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base


class Brand(Base):
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.category_id"), primary_key=True)
    brand_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_name = Column(String(100))
    create_user = Column(UUID(as_uuid=True))
    created_time = Column(DateTime, default=datetime.utcnow)
    update_user = Column(UUID(as_uuid=True))
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="brands")

# Brand.__table__.create(engine)
