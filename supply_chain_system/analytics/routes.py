from fastapi import APIRouter

from ..database import SessionLocal
from .service import get_manufacturer_metrics, get_retailer_metrics

router = APIRouter()


@router.get("/manufacturer")
async def manufacturer_dashboard():
    """Aggregate overall KPIs for the manufacturer dashboard from the database."""
    db = SessionLocal()
    metrics = get_manufacturer_metrics(db)
    db.close()
    return metrics


@router.get("/retailer/{customer_id}")
async def retailer_dashboard(customer_id: int):
    """Return KPIs for a specific retailer from the database."""
    db = SessionLocal()
    metrics = get_retailer_metrics(db, customer_id)
    db.close()
    return metrics
