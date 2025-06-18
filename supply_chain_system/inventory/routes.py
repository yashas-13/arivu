from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from ..database import SessionLocal, InventoryItemModel

router = APIRouter()

class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In-memory logs for demo
inventory_logs: List[str] = [
]

@router.get("/")
def list_items(db: Session = Depends(get_db)):
    rows = db.query(InventoryItemModel).all()
    return [InventoryItem(id=r.id, name=r.name, quantity=r.quantity) for r in rows]


@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(InventoryItemModel).filter(InventoryItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return InventoryItem(id=item.id, name=item.name, quantity=item.quantity)

@router.post("/")
def add_item(item: InventoryItem, db: Session = Depends(get_db)):
    obj = InventoryItemModel(**item.dict())
    db.merge(obj)
    db.commit()
    inventory_logs.append(f"Added {item.name}({item.id}) qty {item.quantity}")
    return item


@router.put("/{item_id}")
def update_item(item_id: int, item: InventoryItem, db: Session = Depends(get_db)):
    existing = db.query(InventoryItemModel).filter(InventoryItemModel.id == item_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    existing.name = item.name
    existing.quantity = item.quantity
    db.commit()
    inventory_logs.append(f"Updated {item.name}({item.id}) qty {item.quantity}")
    return item

@router.post("/update")  # backward compatibility
def update_item_post(item: InventoryItem, db: Session = Depends(get_db)):
    return update_item(item.id, item, db)

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(InventoryItemModel).filter(InventoryItemModel.id == item_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(obj)
    db.commit()
    inventory_logs.append(f"Deleted {obj.name}({obj.id})")
    return {"status": "deleted"}


@router.get("/logs")
async def get_logs():
    return {"logs": inventory_logs}
