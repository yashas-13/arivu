from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from datetime import date

router = APIRouter()

class Invoice(BaseModel):
    id: int
    customer_id: int | None = None
    amount: float
    status: str = "unpaid"
    date: date = date.today()

invoices: Dict[int, Invoice] = {
    1: Invoice(id=1, customer_id=1, amount=150.0, status="paid"),
    2: Invoice(id=2, customer_id=1, amount=200.0, status="unpaid"),
}


@router.get("/")
async def list_invoices():
    return list(invoices.values())

@router.get("/{invoice_id}")
async def get_invoice(invoice_id: int):
    return invoices.get(invoice_id, {"error": "Invoice not found"})

@router.post("/")
async def create_invoice(invoice: Invoice):
    invoices[invoice.id] = invoice
    return invoice


@router.get("/{invoice_id}/pdf")
async def invoice_pdf(invoice_id: int):
    invoice = invoices.get(invoice_id)
    if not invoice:
        return {"error": "Invoice not found"}
    return {"invoice_id": invoice_id, "pdf": f"PDF data for {invoice_id}"}


@router.patch("/{invoice_id}/mark-paid")
async def mark_paid(invoice_id: int):
    invoice = invoices.get(invoice_id)
    if not invoice:
        return {"error": "Invoice not found"}
    invoice.status = "paid"
    invoices[invoice_id] = invoice
    return invoice
