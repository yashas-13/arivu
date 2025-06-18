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

# Simple log list kept in memory
inventory_logs: List[str] = [
    "Preloaded Rice(1) qty 50",
    "Preloaded Oil(2) qty 20",
    "Preloaded Spices(3) qty 30",
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def list_items(db: Session = Depends(get_db)):
    rows = db.query(InventoryItemModel).all()
    return [InventoryItem(id=r.id, name=r.name, quantity=r.quantity) for r in rows]


@router.get("/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    row = db.query(InventoryItemModel).filter(InventoryItemModel.id == item_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return InventoryItem(id=row.id, name=row.name, quantity=row.quantity)

@router.post("/")
async def add_item(item: InventoryItem, db: Session = Depends(get_db)):
    obj = InventoryItemModel(id=item.id, name=item.name, quantity=item.quantity)
    db.merge(obj)
    db.commit()
    inventory_logs.append(f"Added {item.name}({item.id}) qty {item.quantity}")
    return item


@router.put("/{item_id}")
async def update_item(item_id: int, item: InventoryItem, db: Session = Depends(get_db)):
    row = db.query(InventoryItemModel).filter(InventoryItemModel.id == item_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    row.name = item.name
    row.quantity = item.quantity
    db.commit()
    inventory_logs.append(f"Updated {item.name}({item.id}) qty {item.quantity}")
    return item

@router.post("/update")  # backward compatibility
async def update_item_post(item: InventoryItem, db: Session = Depends(get_db)):
    row = db.query(InventoryItemModel).filter(InventoryItemModel.id == item.id).first()
    if row:
        row.name = item.name
        row.quantity = item.quantity
    else:
        row = InventoryItemModel(id=item.id, name=item.name, quantity=item.quantity)
        db.add(row)
    db.commit()
    inventory_logs.append(f"Updated {item.name}({item.id}) qty {item.quantity}")
    return item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    row = db.query(InventoryItemModel).filter(InventoryItemModel.id == item_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(row)
    db.commit()
    inventory_logs.append(f"Deleted {row.name}({row.id})")
    return {"status": "deleted"}


@router.get("/logs")
async def get_logs():
    return {"logs": inventory_logs}
