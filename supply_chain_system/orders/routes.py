from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import SessionLocal, OrderModel, OrderItemModel

router = APIRouter()


class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float


class Order(BaseModel):
    id: int
    retailer_id: int
    order_date: date | None = None
    total_amount: float
    status: str = "pending"
    items: List[OrderItem] | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_orders(db: Session = Depends(get_db)):
    rows = db.query(OrderModel).all()
    return [
        {
            "id": o.id,
            "retailer_id": o.retailer_id,
            "order_date": str(o.order_date),
            "total_amount": o.total_amount,
            "status": o.status,
        }
        for o in rows
    ]


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    o = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    items = (
        db.query(OrderItemModel)
        .filter(OrderItemModel.order_id == order_id)
        .all()
    )
    item_list = [
        {
            "id": i.id,
            "order_id": i.order_id,
            "product_id": i.product_id,
            "quantity": i.quantity,
            "unit_price": i.unit_price,
        }
        for i in items
    ]
    return {
        "id": o.id,
        "retailer_id": o.retailer_id,
        "order_date": str(o.order_date),
        "total_amount": o.total_amount,
        "status": o.status,
        "items": item_list,
    }


class NewOrder(BaseModel):
    id: int
    retailer_id: int
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"


@router.post("/")
def place_order(order: NewOrder, db: Session = Depends(get_db)):
    o = OrderModel(
        id=order.id,
        retailer_id=order.retailer_id,
        order_date=date.today(),
        total_amount=order.total_amount,
        status=order.status,
    )
    db.add(o)
    db.commit()
    for item in order.items:
        obj = OrderItemModel(
            id=item.id,
            order_id=o.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        db.add(obj)
    db.commit()
    return {"status": "created"}


@router.patch("/{order_id}/status")
def update_status(order_id: int, status: str, db: Session = Depends(get_db)):
    o = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    o.status = status
    db.commit()
    return {"status": "updated"}
