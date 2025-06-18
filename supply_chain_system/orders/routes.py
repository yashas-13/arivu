from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import SessionLocal, OrderModel, OrderItemModel


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float


class Order(BaseModel):
    id: int
    retailer_id: int | None = None
    order_date: date | None = None
    total_amount: float | None = None
    status: str = "pending"
    items: List[OrderItem] = []


@router.get("/")
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderModel).all()
    results = []
    for o in orders:
        items = (
            db.query(OrderItemModel)
            .filter(OrderItemModel.order_id == o.id)
            .all()
        )
        results.append(
            Order(
                id=o.id,
                retailer_id=o.retailer_id,
                order_date=o.order_date,
                total_amount=o.total_amount,
                status=o.status,
                items=[
                    OrderItem(
                        id=i.id,
                        order_id=i.order_id,
                        product_id=i.product_id,
                        quantity=i.quantity,
                        unit_price=i.unit_price,
                    )
                    for i in items
                ],
            )
        )
    return results


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    items = (
        db.query(OrderItemModel)
        .filter(OrderItemModel.order_id == order.id)
        .all()
    )
    return Order(
        id=order.id,
        retailer_id=order.retailer_id,
        order_date=order.order_date,
        total_amount=order.total_amount,
        status=order.status,
        items=[
            OrderItem(
                id=i.id,
                order_id=i.order_id,
                product_id=i.product_id,
                quantity=i.quantity,
                unit_price=i.unit_price,
            )
            for i in items
        ],
    )


class NewOrderItem(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class NewOrder(BaseModel):
    id: int
    retailer_id: int
    order_date: date | None = None
    items: List[NewOrderItem]
    total_amount: float
    status: str = "pending"


@router.post("/")
def create_order(order: NewOrder, db: Session = Depends(get_db)):
    obj = OrderModel(
        id=order.id,
        retailer_id=order.retailer_id,
        order_date=order.order_date or date.today(),
        total_amount=order.total_amount,
        status=order.status,
    )
    db.add(obj)
    for item in order.items:
        db.add(
            OrderItemModel(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        )
    db.commit()
    return {"status": "created", "id": order.id}


@router.patch("/{order_id}/status")
def update_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    return {"status": status}
