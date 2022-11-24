import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base


class Product(Base):
    product_id = Column(String(36), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(36), index=True)
    title = Column(String, index=True)
    contents = Column(String, index=True)
    category = Column(String(100), index=True)
    brand = Column(String(100), index=True, nullable=True)
    price = Column(Integer)
    phone_number = Column(String(100))
    status = Column(String(100), default="selling")
    count = Column(Integer, default=0)
    create_user = Column(String(36))
    created_time = Column(DateTime, default=datetime.utcnow)
    update_user = Column(String(36))
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
