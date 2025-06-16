from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class Customer(BaseModel):
    id: int
    name: str

customers: Dict[int, Customer] = {}

@router.post("/")
async def add_customer(customer: Customer):
    customers[customer.id] = customer
    return customer

@router.get("/{customer_id}")
async def get_customer(customer_id: int):
    return customers.get(customer_id, {"error": "Customer not found"})
