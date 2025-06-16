from fastapi import APIRouter
from typing import List

router = APIRouter()

logs: List[str] = []

@router.post("/record")
async def record(action: str):
    logs.append(action)
    return {"status": "recorded"}

@router.get("/logs")
async def get_logs():
    return {"logs": logs}
