from fastapi import APIRouter

# import in-memory stores from other modules
from ..billing.routes import invoices
from ..inventory.routes import inventory
from ..orders.routes import orders
from ..customers.routes import customers
from ..finished_goods.routes import finished_goods
from datetime import date, timedelta

router = APIRouter()


@router.get("/admin")
async def admin_dashboard():
    """Aggregate overall KPIs for the admin dashboard."""
    total_sales = sum(inv.amount for inv in invoices.values())

    # count ordered items to determine top products
    product_counts = {}
    for order in orders.values():
        for item_id in order.items:
            product_counts[item_id] = product_counts.get(item_id, 0) + 1

    top_products = [
        {"product_id": pid, "count": count}
        for pid, count in sorted(
            product_counts.items(), key=lambda x: x[1], reverse=True
        )
    ]

    low_stock = [
        {"product_id": item.id, "quantity": item.quantity}
        for item in inventory.values()
        if item.quantity < 5
    ]

    # compute sales for last 7 days
    today = date.today()
    sales_by_day = []
    for i in range(7):
        day = today - timedelta(days=i)
        day_total = sum(
            inv.amount for inv in invoices.values() if inv.date == day
        )
        sales_by_day.append({"date": str(day), "total": day_total})

    sales_by_day.reverse()

    return {
        "total_sales": total_sales,
        "top_products": top_products,
        "low_stock": low_stock,
        "customer_count": len(customers),
        "sales_by_day": sales_by_day,
    }


@router.get("/retailer/{customer_id}")
async def retailer_dashboard(customer_id: int):
    """Return KPIs for a specific retailer."""
    cust_orders = [o for o in orders.values() if o.customer_id == customer_id]
    cust_invoices = [i for i in invoices.values() if i.customer_id == customer_id]

    product_counts = {}
    for order in cust_orders:
        for item_id in order.items:
            product_counts[item_id] = product_counts.get(item_id, 0) + 1

    top_products = [
        {"product_id": pid, "count": count}
        for pid, count in sorted(
            product_counts.items(), key=lambda x: x[1], reverse=True
        )
    ]

    spend = sum(inv.amount for inv in cust_invoices)

    today = date.today()
    today_sales = sum(inv.amount for inv in cust_invoices if inv.date == today)
    trend = []
    for i in range(7):
        day = today - timedelta(days=i)
        total = sum(inv.amount for inv in cust_invoices if inv.date == day)
        trend.append({"date": str(day), "total": total})
    trend.reverse()

    fg_status = [
        {"id": g.id, "name": g.name, "quantity": g.quantity}
        for g in finished_goods.values()
    ]
    fg_low = [g for g in fg_status if g["quantity"] < 30]

    return {
        "orders": len(cust_orders),
        "spend": spend,
        "top_products": top_products,
        "today_sales": today_sales,
        "sales_trend": trend,
        "finished_goods": fg_status,
        "low_fg": fg_low,
    }
