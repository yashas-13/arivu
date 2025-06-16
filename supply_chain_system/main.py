from fastapi import FastAPI

from .inventory.routes import router as inventory_router
from .orders.routes import router as orders_router
from .customers.routes import router as customers_router
from .auth.routes import router as auth_router
from .billing.routes import router as billing_router
from .analytics.routes import router as analytics_router
from .notifications.routes import router as notifications_router
from .audit.routes import router as audit_router
from .users.routes import router as users_router
from .reports.routes import router as reports_router

app = FastAPI(title="Arivu Supply Chain")

app.include_router(auth_router, prefix="/auth")
app.include_router(inventory_router, prefix="/inventory")
app.include_router(orders_router, prefix="/orders")
app.include_router(customers_router, prefix="/customers")
app.include_router(users_router, prefix="/users")
app.include_router(billing_router, prefix="/invoices")
app.include_router(analytics_router, prefix="/dashboard")
app.include_router(notifications_router, prefix="/notify")
app.include_router(audit_router, prefix="/audit")
app.include_router(reports_router, prefix="/reports")


@app.get("/")
async def root():
    return {"message": "Arivu Supply Chain API"}
