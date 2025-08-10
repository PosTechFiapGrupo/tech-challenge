from sqlalchemy import Column, Integer, String, ForeignKey
from app.infrastructure.database import Base

class VehicleModel(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    license_plate = Column(String(10), unique=True, nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)