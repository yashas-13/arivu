from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class FinishedGood(BaseModel):
    id: int
    name: str
    quantity: int

finished_goods: Dict[int, FinishedGood] = {
    1: FinishedGood(id=1, name="Coconut Mixture", quantity=150),
    2: FinishedGood(id=2, name="Multi Seed Chakli", quantity=20),
}

@router.get("/")
async def list_goods():
    return list(finished_goods.values())

@router.post("/")
async def add_good(good: FinishedGood):
    finished_goods[good.id] = good
    return good

@router.put("/{good_id}")
async def update_good(good_id: int, good: FinishedGood):
    if good_id not in finished_goods:
        raise HTTPException(status_code=404, detail="Item not found")
    finished_goods[good_id] = good
    return good

@router.delete("/{good_id}")
async def delete_good(good_id: int):
    item = finished_goods.pop(good_id, None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted"}
