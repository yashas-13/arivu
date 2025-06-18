"""Product catalog API backed by SQLite."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import SessionLocal, ProductModel


router = APIRouter()


class Product(BaseModel):
    id: int
    name: str
    sku: str
    description: str | None = None
    category: str | None = None
    uom: str
    quantity_per_unit: float
    mrp: float
    current_stock_quantity: int | None = 0


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_products(db: Session = Depends(get_db)):
    rows = db.query(ProductModel).all()
    return [Product(**row.__dict__) for row in rows]


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**prod.__dict__)


@router.post("/")
def add_product(product: Product, db: Session = Depends(get_db)):
    obj = ProductModel(**product.dict())
    db.merge(obj)
    db.commit()
    return product


@router.put("/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    existing = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in product.dict().items():
        setattr(existing, k, v)
    db.commit()
    return product


class StockUpdate(BaseModel):
    quantity: int


@router.get("/{product_id}/stock")
def get_product_stock(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product_id, "quantity": prod.current_stock_quantity}


@router.put("/{product_id}/stock")
def update_product_stock(product_id: int, stock: StockUpdate, db: Session = Depends(get_db)):
    prod = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    prod.current_stock_quantity = stock.quantity
    db.commit()
    return {"product_id": product_id, "quantity": stock.quantity}


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    obj = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

