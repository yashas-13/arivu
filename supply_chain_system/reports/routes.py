from fastapi import APIRouter

router = APIRouter()

@router.get("/sales")
async def sales_report(range: str = "monthly"):
    return {"range": range, "total": 0}
