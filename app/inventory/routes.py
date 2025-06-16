from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int

# In-memory store for demo
inventory: Dict[int, InventoryItem] = {}

@router.get("/{item_id}")
async def get_item(item_id: int):
    return inventory.get(item_id, {"error": "Item not found"})

@router.post("/")
async def add_item(item: InventoryItem):
    inventory[item.id] = item
    return item
