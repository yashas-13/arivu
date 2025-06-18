from fastapi import APIRouter

from ..database import SessionLocal
from .service import get_admin_metrics, get_retailer_metrics

router = APIRouter()


@router.get("/admin")
async def admin_dashboard():
    """Aggregate overall KPIs for the admin dashboard from the database."""
    db = SessionLocal()
    metrics = get_admin_metrics(db)
    db.close()
    return metrics


@router.get("/retailer/{customer_id}")
async def retailer_dashboard(customer_id: int):
    """Return KPIs for a specific retailer from the database."""
    db = SessionLocal()
    metrics = get_retailer_metrics(db, customer_id)
    db.close()
    return metrics
