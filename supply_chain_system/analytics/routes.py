from fastapi import APIRouter

router = APIRouter()

@router.get("/admin")
async def admin_dashboard():
    return {"total_sales": 0, "top_product": None}

@router.get("/retailer")
async def retailer_dashboard():
    return {"orders": 0, "spend": 0}
