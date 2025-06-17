from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from .models import InventoryItem
from ..database.core import get_db

router = APIRouter()

class InventoryCreate(BaseModel):
    id: int
    name: str
    quantity: int

class InventoryUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None

@router.get("/")
async def list_items(db: Session = Depends(get_db)):
    return db.query(InventoryItem).all()

@router.get("/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(InventoryItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/")
async def add_item(item: InventoryCreate, db: Session = Depends(get_db)):
    db_item = InventoryItem(id=item.id, name=item.name, quantity=item.quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/{item_id}")
async def update_item(item_id: int, item: InventoryUpdate, db: Session = Depends(get_db)):
    db_item = db.query(InventoryItem).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.name is not None:
        db_item.name = item.name
    if item.quantity is not None:
        db_item.quantity = item.quantity
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(InventoryItem).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"status": "deleted"}
