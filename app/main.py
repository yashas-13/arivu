from fastapi import FastAPI

from .inventory.routes import router as inventory_router
from .orders.routes import router as orders_router
from .customers.routes import router as customers_router
from .auth.routes import router as auth_router

app = FastAPI(title="Arivu Supply Chain")

app.include_router(auth_router, prefix="/auth")
app.include_router(inventory_router, prefix="/inventory")
app.include_router(orders_router, prefix="/orders")
app.include_router(customers_router, prefix="/customers")


@app.get("/")
async def root():
    return {"message": "Arivu Supply Chain API"}
