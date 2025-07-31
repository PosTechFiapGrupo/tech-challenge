from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.mysql import CHAR
from app.infrastructure.database import Base
import uuid


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image = Column(String(500), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image": self.image,
        }
