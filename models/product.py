import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from db.base_class import Base


class Product(Base):
    STATUS_DEFAULT_VALUE = "selling"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True)
    title = Column(String)
    contents = Column(String)
    category = Column(String(100), index=True)
    brand = Column(String(100), index=True, nullable=True)
    price = Column(Integer)
    phone_number = Column(String(100))
    status = Column(String(100), default=STATUS_DEFAULT_VALUE)
    count = Column(Integer, default=0)
    is_deleted = Column(Boolean(), default=False)
    create_user = Column(UUID(as_uuid=True))
    created_time = Column(DateTime, default=datetime.utcnow)
    update_user = Column(UUID(as_uuid=True))
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Product.__table__.create(engine)
