import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

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

    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete, delete-orphan",
    )

    # todo 그런데 이렇게 keyword arguments로 받는건 좋지 않은것 같은데.... key에 대한 하드코딩이 이루어지니깐....
    def __init__(self, **kwargs):
        images_from_request = kwargs.pop("images")
        user_id = kwargs.get("user_id")
        self.images = []
        for image_from_request in images_from_request:
            image = ProductImage(**image_from_request, create_user=user_id)
            self.images.append(image)
        super(Product, self).__init__(**kwargs)


class ProductImage(Base):
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.product_id"), primary_key=True)
    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_url = Column(String(200))
    create_user = Column(UUID(as_uuid=True))
    created_time = Column(DateTime, default=datetime.utcnow)

    product = relationship(
        "Product",
        back_populates="images"
    )

    def __init__(self, **kwargs):
        super(ProductImage, self).__init__(**kwargs)

# Product.__table__.create(engine)
# ProductImage.__table__.create(engine)
