from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class Order(BaseModel):
    id: int
    customer_id: int | None = None
    items: List[int]
    status: str = "pending"

orders: Dict[int, Order] = {}

@router.post("/")
async def place_order(order: Order):
    orders[order.id] = order
    return order

@router.get("/{order_id}")
async def get_order(order_id: int):
    return orders.get(order_id, {"error": "Order not found"})


@router.patch("/{order_id}/status")
async def update_status(order_id: int, status: str):
    order = orders.get(order_id)
    if not order:
        return {"error": "Order not found"}
    order.status = status
    orders[order_id] = order
    return order
