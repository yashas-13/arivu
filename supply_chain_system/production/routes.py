from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import datetime

router = APIRouter()

class ProductionBatch(BaseModel):
    id: int
    product: str
    status: str
    progress: int = 0
    scheduled_start: datetime.date | None = None

# Sample in-memory batches
batches: Dict[int, ProductionBatch] = {
    1: ProductionBatch(id=1, product="Khapli Wheat Flour", status="scheduled", scheduled_start=datetime.date.today()),
    2: ProductionBatch(id=2, product="Multi Seeds Atta", status="in_progress", progress=70, scheduled_start=datetime.date.today()),
}

alerts: List[str] = ["Low Capacity Detected"]

@router.get("/")
async def list_batches():
    return list(batches.values())

@router.post("/")
async def add_batch(batch: ProductionBatch):
    batches[batch.id] = batch
    return batch

@router.patch("/{batch_id}/progress")
async def update_progress(batch_id: int, progress: int):
    batch = batches.get(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    batch.progress = progress
    batches[batch_id] = batch
    return batch

@router.get("/alerts")
async def get_alerts():
    return {"alerts": alerts}
