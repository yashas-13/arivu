from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..database import SessionLocal, Retailer
from ..utils.logger import logger
from ..auth.routes import hash_password

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Customer(BaseModel):
    id: int
    name: str


customers: dict[int, Customer] = {}


@router.get("/")
async def list_customers():
    return list(customers.values())


@router.post("/")
async def add_customer(customer: Customer):
    customers[customer.id] = customer
    return customer


@router.get("/{customer_id}")
async def get_customer(customer_id: int):
    return customers.get(customer_id, {"error": "Customer not found"})


class RetailerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    password: str


class RetailerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class RetailerOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    location: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


@router.post("/admin/retailers", response_model=RetailerOut)
def create_retailer(ret: RetailerCreate, db: Session = Depends(get_db)):
    if db.query(Retailer).filter(Retailer.email == ret.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    obj = Retailer(
        name=ret.name,
        email=ret.email,
        phone=ret.phone,
        location=ret.location,
        password_hash=hash_password(ret.password),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    logger.info("Retailer created: %s", obj.email)
    return obj


@router.get("/admin/retailers", response_model=List[RetailerOut])
def list_retailers(db: Session = Depends(get_db)):
    rows = db.query(Retailer).all()
    return rows


@router.get("/admin/retailers/{retailer_id}", response_model=RetailerOut)
def get_retailer(retailer_id: int, db: Session = Depends(get_db)):
    obj = db.query(Retailer).filter(Retailer.id == retailer_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Retailer not found")
    return obj


@router.put("/admin/retailers/{retailer_id}", response_model=RetailerOut)
def update_retailer(retailer_id: int, ret: RetailerUpdate, db: Session = Depends(get_db)):
    obj = db.query(Retailer).filter(Retailer.id == retailer_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Retailer not found")
    if ret.name is not None:
        obj.name = ret.name
    if ret.email is not None:
        obj.email = ret.email
    if ret.phone is not None:
        obj.phone = ret.phone
    if ret.location is not None:
        obj.location = ret.location
    if ret.password is not None:
        obj.password_hash = hash_password(ret.password)
    if ret.is_active is not None:
        obj.is_active = ret.is_active
    db.commit()
    logger.info("Retailer updated: %s", obj.email)
    return obj


@router.delete("/admin/retailers/{retailer_id}")
def delete_retailer(retailer_id: int, db: Session = Depends(get_db)):
    obj = db.query(Retailer).filter(Retailer.id == retailer_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Retailer not found")
    db.delete(obj)
    db.commit()
    logger.info("Retailer deleted: %s", obj.email)
    return {"status": "deleted"}

