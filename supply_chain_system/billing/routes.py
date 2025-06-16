from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class Invoice(BaseModel):
    id: int
    amount: float
    status: str = "unpaid"

invoices: Dict[int, Invoice] = {}

@router.get("/{invoice_id}")
async def get_invoice(invoice_id: int):
    return invoices.get(invoice_id, {"error": "Invoice not found"})

@router.post("/")
async def create_invoice(invoice: Invoice):
    invoices[invoice.id] = invoice
    return invoice
