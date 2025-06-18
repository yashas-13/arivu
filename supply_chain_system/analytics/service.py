from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import (
    ProductModel,
    RawMaterialModel,
    ProductionBatchModel,
    MachineModel,
    QCCheckModel,
    OrderModel,
    OrderItemModel,
    ReturnRequestModel,
    UserModel,
)


def get_admin_metrics(db: Session) -> dict:
    """Compute dashboard metrics for admin users."""
    total_sales = db.query(func.sum(OrderModel.total_amount)).scalar() or 0

    product_counts = (
        db.query(OrderItemModel.product_id, func.count(OrderItemModel.id))
        .group_by(OrderItemModel.product_id)
        .all()
    )
    top_products = []
    for pid, count in product_counts:
        prod = db.query(ProductModel).filter(ProductModel.id == pid).first()
        name = prod.name if prod else str(pid)
        top_products.append({"product_id": pid, "name": name, "count": count})

    low_stock = [
        {
            "product_id": rm.id,
            "name": rm.name,
            "quantity": rm.stock_qty,
        }
        for rm in db.query(RawMaterialModel)
        .filter(RawMaterialModel.stock_qty < RawMaterialModel.reorder_point)
        .all()
    ]

    customer_count = db.query(UserModel).filter(UserModel.role == "retailer").count()

    today = date.today()
    sales_by_day = []
    for i in range(7):
        day = today - timedelta(days=i)
        day_total = (
            db.query(func.sum(OrderModel.total_amount))
            .filter(OrderModel.order_date == day)
            .scalar()
            or 0
        )
        sales_by_day.append({"date": str(day), "total": day_total})
    sales_by_day.reverse()

    return {
        "total_sales": total_sales,
        "top_products": top_products,
        "low_stock": low_stock,
        "customer_count": customer_count,
        "sales_by_day": sales_by_day,
    }


def get_retailer_metrics(db: Session, retailer_id: int) -> dict:
    """Metrics for a specific retailer."""
    orders = db.query(OrderModel).filter(OrderModel.retailer_id == retailer_id).all()
    order_ids = [o.id for o in orders]
    invoices_total = sum(o.total_amount for o in orders)

    product_counts = (
        db.query(OrderItemModel.product_id, func.count(OrderItemModel.id))
        .filter(OrderItemModel.order_id.in_(order_ids))
        .group_by(OrderItemModel.product_id)
        .all()
    )
    top_products = []
    for pid, count in product_counts:
        prod = db.query(ProductModel).filter(ProductModel.id == pid).first()
        name = prod.name if prod else str(pid)
        top_products.append({"product_id": pid, "name": name, "count": count})

    today = date.today()
    today_sales = (
        db.query(func.sum(OrderModel.total_amount))
        .filter(OrderModel.retailer_id == retailer_id, OrderModel.order_date == today)
        .scalar()
        or 0
    )
    trend = []
    for i in range(7):
        day = today - timedelta(days=i)
        total = (
            db.query(func.sum(OrderModel.total_amount))
            .filter(OrderModel.retailer_id == retailer_id, OrderModel.order_date == day)
            .scalar()
            or 0
        )
        trend.append({"date": str(day), "total": total})
    trend.reverse()

    fg_status = [
        {"id": b.id, "name": prod.name if (prod := db.query(ProductModel).get(b.product_id)) else str(b.product_id), "quantity": b.quantity_produced}
        for b in db.query(ProductionBatchModel).all()
    ]

    fg_low = [g for g in fg_status if g["quantity"] < 30]

    return {
        "orders": len(orders),
        "spend": invoices_total,
        "top_products": top_products,
        "today_sales": today_sales,
        "sales_trend": trend,
        "finished_goods": fg_status,
        "low_fg": fg_low,
    }
