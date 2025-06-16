from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int

# In-memory store for demo with sample data
inventory: Dict[int, InventoryItem] = {
    1: InventoryItem(id=1, name="Rice", quantity=50),
    2: InventoryItem(id=2, name="Oil", quantity=20),
    3: InventoryItem(id=3, name="Spices", quantity=30),
}
inventory_logs: List[str] = [
    "Preloaded Rice(1) qty 50",
    "Preloaded Oil(2) qty 20",
    "Preloaded Spices(3) qty 30",
]

@router.get("/")
async def list_items():
    return list(inventory.values())


@router.get("/{item_id}")
async def get_item(item_id: int):
    item = inventory.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/")
async def add_item(item: InventoryItem):
    inventory[item.id] = item
    inventory_logs.append(f"Added {item.name}({item.id}) qty {item.quantity}")
    return item


@router.put("/{item_id}")
async def update_item(item_id: int, item: InventoryItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    inventory[item_id] = item
    inventory_logs.append(f"Updated {item.name}({item.id}) qty {item.quantity}")
    return item

@router.post("/update")  # backward compatibility
async def update_item_post(item: InventoryItem):
    inventory[item.id] = item
    inventory_logs.append(f"Updated {item.name}({item.id}) qty {item.quantity}")
    return item

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    item = inventory.pop(item_id, None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    inventory_logs.append(f"Deleted {item.name}({item.id})")
    return {"status": "deleted"}


@router.get("/logs")
async def get_logs():
    return {"logs": inventory_logs}
