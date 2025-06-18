"""Database initialization using SQLAlchemy and SQLite."""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_FILE = Path(__file__).resolve().parent.parent.parent / "arivu.db"
engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)

