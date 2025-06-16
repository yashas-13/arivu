from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class Order(BaseModel):
    id: int
    items: List[int]

orders: Dict[int, Order] = {}

@router.post("/")
async def place_order(order: Order):
    orders[order.id] = order
    return order

@router.get("/{order_id}")
async def get_order(order_id: int):
    return orders.get(order_id, {"error": "Order not found"})
