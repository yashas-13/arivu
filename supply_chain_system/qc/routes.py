from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import datetime

router = APIRouter()

class QCResult(BaseModel):
    id: int
    batch_id: int
    result: str
    date: datetime.date = datetime.date.today()

qc_results: Dict[int, QCResult] = {
    1: QCResult(id=1, batch_id=1, result="pass"),
}

@router.get("/checks")
async def list_checks():
    return list(qc_results.values())

@router.post("/checks")
async def add_check(check: QCResult):
    qc_results[check.id] = check
    return check

@router.get("/checks/{check_id}")
async def get_check(check_id: int):
    check = qc_results.get(check_id)
    if not check:
        raise HTTPException(status_code=404, detail="Result not found")
    return check
