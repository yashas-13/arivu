from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

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
from .products.routes import router as products_router
from .production.routes import router as production_router
from .qc.routes import router as qc_router
from .finished_goods.routes import router as fg_router
from .database import init_db, SessionLocal, ProductModel

app = FastAPI(title="Arivu Supply Chain")

frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.on_event("startup")
def startup():
    init_db()
    # load sample products if DB is empty
    db = SessionLocal()
    if not db.query(ProductModel).first():
        samples = [
            ProductModel(
                id=1,
                name="Low-Carb Multi Seeds Atta",
                sku="AF-LCA-1KG",
                description="Whole Ground Flax, Sunflower, Melon, Pumpkin Seeds; Rich in Fibre, Protein, Calcium.",
                category="Flour",
                uom="kg",
                quantity_per_unit=1,
                mrp=480,
            ),
            ProductModel(
                id=2,
                name="Groundnut Oil",
                sku="AF-GNO-1L",
                description="Cold pressed groundnut oil.",
                category="Oil",
                uom="L",
                quantity_per_unit=1,
                mrp=250,
            ),
        ]
        db.add_all(samples)
        db.commit()
    db.close()

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
app.include_router(products_router, prefix="/products")
app.include_router(production_router, prefix="/production")
app.include_router(qc_router, prefix="/qc")
app.include_router(fg_router, prefix="/finished_goods")


@app.get("/")
async def root():
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="Frontend not found")


@app.get("/{page_name}.html")
async def html_page(page_name: str):
    file_path = frontend_path / f"{page_name}.html"
    if file_path.exists():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Page not found")
