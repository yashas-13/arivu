from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int

# In-memory store for demo
inventory: Dict[int, InventoryItem] = {}
inventory_logs: List[str] = []

@router.get("/")
async def list_items():
    return list(inventory.values())


@router.get("/{item_id}")
async def get_item(item_id: int):
    return inventory.get(item_id, {"error": "Item not found"})

@router.post("/")
async def add_item(item: InventoryItem):
    inventory[item.id] = item
    inventory_logs.append(f"Added {item.name}({item.id}) qty {item.quantity}")
    return item


@router.post("/update")
async def update_item(item: InventoryItem):
    inventory[item.id] = item
    inventory_logs.append(f"Updated {item.name}({item.id}) qty {item.quantity}")
    return item


@router.get("/logs")
async def get_logs():
    return {"logs": inventory_logs}
