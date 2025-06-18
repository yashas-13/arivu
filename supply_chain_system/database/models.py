"""SQLAlchemy models for core data."""

from sqlalchemy import Column, Integer, String, Float

from .core import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String)
    uom = Column(String, nullable=False)
    quantity_per_unit = Column(Float, nullable=False)
    mrp = Column(Float, nullable=False)

