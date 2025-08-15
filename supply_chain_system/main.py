from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import date

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
from .leads.routes import router as leads_router
from .database import (
    init_db,
    SessionLocal,
    ProductModel,
    RawMaterialModel,
    ProductionBatchModel,
    OrderModel,
    OrderItemModel,
    InventoryItemModel,
    UserModel,
    Retailer,
    LeadModel,
)

app = FastAPI(title="Arivu Supply Chain")

frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.on_event("startup")
def startup():
    init_db()
    # load sample data if DB is empty
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
                current_stock_quantity=100,
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
                current_stock_quantity=60,
            ),
        ]
        db.add_all(samples)
        db.commit()

        inventory_items = [
            InventoryItemModel(id=1, name="Rice", quantity=50),
            InventoryItemModel(id=2, name="Oil", quantity=20),
            InventoryItemModel(id=3, name="Spices", quantity=30),
        ]
        db.add_all(inventory_items)
        db.commit()
        from .inventory.routes import inventory_logs
        inventory_logs.extend([
            "Preloaded Rice(1) qty 50",
            "Preloaded Oil(2) qty 20",
            "Preloaded Spices(3) qty 30",
        ])

        raw_materials = [
            RawMaterialModel(id=1, name="Flax Seeds", stock_qty=100, reorder_point=20),
            RawMaterialModel(id=2, name="Sunflower Seeds", stock_qty=50, reorder_point=20),
        ]
        db.add_all(raw_materials)

        batches = [
            ProductionBatchModel(id=1, product_id=1, production_date=date.today(), quantity_produced=200, status="completed"),
            ProductionBatchModel(id=2, product_id=2, production_date=date.today(), quantity_produced=150, status="in_progress"),
        ]
        db.add_all(batches)

        orders = [
            OrderModel(id=1, retailer_id=1, order_date=date.today(), total_amount=500.0, status="shipped"),
            OrderModel(id=2, retailer_id=1, order_date=date.today(), total_amount=300.0, status="pending"),
        ]
        db.add_all(orders)

        order_items = [
            OrderItemModel(id=1, order_id=1, product_id=1, quantity=2, unit_price=480),
            OrderItemModel(id=2, order_id=2, product_id=2, quantity=1, unit_price=250),
        ]
        db.add_all(order_items)

        users = [
            UserModel(
                id=1,
                username="manufacturer",
                hashed_password="$2b$12$LsCAdFgjNOrbVXjv71cOCuiCY7C0.cZmCsTPm8vwcmQ94XkCUEP/O",
                role="manufacturer",
            ),
            UserModel(
                id=2,
                username="sales_manager",
                hashed_password="$2b$12$LsCAdFgjNOrbVXjv71cOCuiCY7C0.cZmCsTPm8vwcmQ94XkCUEP/O",
                role="sales_manager",
            )
        ]
        db.add_all(users)

        retailers = [
            Retailer(
                id=1,
                name="Retailer One",
                email="retailer1@example.com",
                phone="1234567890",
                location="City",
                password_hash="$2b$12$YyHfMQQvo.cBZ1bh0GC8KO1JDsHiUupwQppJE7qOrKvEsp7UE2/eK",
            )
        ]
        db.add_all(retailers)

        # Add sample leads for CRM demo
        leads = [
            LeadModel(
                id=1,
                company_name="Fresh Market Groceries",
                contact_person="John Smith",
                email="john@freshmarket.com",
                phone="9876543210",
                location="Downtown",
                business_type="grocery_store",
                expected_volume="high",
                status="new",
                source="website",
                notes="Interested in bulk orders for organic products"
            ),
            LeadModel(
                id=2,
                company_name="Corner Store Plus",
                contact_person="Sarah Johnson",
                email="sarah@cornerstore.com",
                phone="5555551234",
                location="Suburb Area",
                business_type="convenience_store",
                expected_volume="medium",
                status="contacted",
                source="referral",
                notes="Follow up scheduled for next week"
            ),
            LeadModel(
                id=3,
                company_name="Mega Supermart",
                contact_person="Mike Wilson",
                email="mike@megasupermart.com",
                phone="7777777777",
                location="Mall District",
                business_type="supermarket",
                expected_volume="high",
                status="qualified",
                source="trade_show",
                notes="Very interested, ready to discuss terms"
            )
        ]
        db.add_all(leads)
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
app.include_router(leads_router, prefix="/leads")


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
