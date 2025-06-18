"""Database initialization using SQLAlchemy and SQLite."""

from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base


DB_FILE = Path(__file__).resolve().parent.parent.parent / "arivu.db"
engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Create database tables, recreating DB if schema changed."""
    recreate = False
    if DB_FILE.exists():
        insp = inspect(engine)
        product_cols = [c["name"] for c in insp.get_columns("products")]
        if "current_stock_quantity" not in product_cols:
            recreate = True
        try:
            insp.get_columns("inventory_items")
        except Exception:
            recreate = True
    if recreate and DB_FILE.exists():
        DB_FILE.unlink()
    Base.metadata.create_all(bind=engine)

