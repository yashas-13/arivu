"""SQLAlchemy models for core data."""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime

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


class RawMaterialModel(Base):
    """Raw material inventory records."""

    __tablename__ = "raw_materials"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stock_qty = Column(Integer, default=0)
    reorder_point = Column(Integer, default=0)
    supplier_id = Column(Integer)


class ProductionBatchModel(Base):
    """Production batch details."""

    __tablename__ = "production_batches"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    production_date = Column(Date)
    quantity_produced = Column(Integer)
    status = Column(String)


class MachineModel(Base):
    """Factory machine state."""

    __tablename__ = "machines"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)


class QCCheckModel(Base):
    """Quality control results."""

    __tablename__ = "qc_checks"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer)
    result = Column(String)
    remarks = Column(String)
    timestamp = Column(DateTime)


class OrderModel(Base):
    """Sales order header."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    retailer_id = Column(Integer)
    order_date = Column(Date)
    total_amount = Column(Float)
    status = Column(String)


class OrderItemModel(Base):
    """Line item belonging to an order."""

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    unit_price = Column(Float)


class ReturnRequestModel(Base):
    """Customer return requests."""

    __tablename__ = "return_requests"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    reason = Column(String)
    status = Column(String)


class UserModel(Base):
    """Application users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

