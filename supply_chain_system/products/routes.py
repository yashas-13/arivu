from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

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

# Sample in-memory store
products: Dict[int, Product] = {
    1: Product(
        id=1,
        name="Low-Carb Multi Seeds Atta",
        sku="AF-LCA-1KG",
        description=(
            "Whole Ground Flax, Sunflower, Melon, Pumpkin Seeds; Rich in Fibre, Protein, Calcium."
        ),
        category="Flour",
        uom="kg",
        quantity_per_unit=1,
        mrp=480,
    ),
    2: Product(
        id=2,
        name="Groundnut Oil",
        sku="AF-GNO-1L",
        description="Cold pressed groundnut oil.",
        category="Oil",
        uom="L",
        quantity_per_unit=1,
        mrp=250,
    ),
}


@router.get("/")
async def list_products():
    return list(products.values())


@router.get("/{product_id}")
async def get_product(product_id: int):
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/")
async def add_product(product: Product):
    products[product.id] = product
    return product


@router.put("/{product_id}")
async def update_product(product_id: int, product: Product):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    products[product_id] = product
    return product


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    item = products.pop(product_id, None)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"status": "deleted"}
