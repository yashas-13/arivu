from sqlalchemy.orm import Session

from .models import InventoryItem
from ..database.core import Base, engine, SessionLocal


def init_inventory():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    if db.query(InventoryItem).count() == 0:
        samples = [
            InventoryItem(id=1, name="Flour", quantity=100),
            InventoryItem(id=2, name="Oil", quantity=50),
        ]
        db.add_all(samples)
        db.commit()
    db.close()
