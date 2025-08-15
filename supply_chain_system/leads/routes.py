"""CRM Lead management API routes."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..database import SessionLocal, LeadModel, Retailer
from ..auth.routes import hash_password
from ..utils.logger import logger

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LeadCreate(BaseModel):
    company_name: str
    contact_person: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    business_type: Optional[str] = None
    expected_volume: Optional[str] = "medium"
    source: Optional[str] = "website"
    assigned_to: Optional[int] = None
    notes: Optional[str] = None


class LeadUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    business_type: Optional[str] = None
    expected_volume: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    assigned_to: Optional[int] = None
    notes: Optional[str] = None


class LeadOut(BaseModel):
    id: int
    company_name: str
    contact_person: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    business_type: Optional[str]
    expected_volume: Optional[str]
    status: str
    source: Optional[str]
    assigned_to: Optional[int]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    converted_retailer_id: Optional[int]

    class Config:
        orm_mode = True


class LeadConvert(BaseModel):
    password: str  # Password for the new retailer account


@router.get("/", response_model=List[LeadOut])
def list_leads(status: Optional[str] = None, assigned_to: Optional[int] = None, db: Session = Depends(get_db)):
    """List all leads with optional filtering."""
    query = db.query(LeadModel)
    
    if status:
        query = query.filter(LeadModel.status == status)
    if assigned_to:
        query = query.filter(LeadModel.assigned_to == assigned_to)
    
    return query.all()


@router.post("/", response_model=LeadOut)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead."""
    # Check if email already exists in leads or retailers
    existing_lead = db.query(LeadModel).filter(LeadModel.email == lead.email).first()
    if existing_lead:
        raise HTTPException(status_code=400, detail="Email already exists as a lead")
    
    existing_retailer = db.query(Retailer).filter(Retailer.email == lead.email).first()
    if existing_retailer:
        raise HTTPException(status_code=400, detail="Email already exists as an active retailer")

    lead_obj = LeadModel(**lead.dict())
    db.add(lead_obj)
    db.commit()
    db.refresh(lead_obj)
    
    logger.info("Lead created: %s (%s)", lead_obj.company_name, lead_obj.email)
    return lead_obj


@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a specific lead by ID."""
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/{lead_id}", response_model=LeadOut)
def update_lead(lead_id: int, lead_update: LeadUpdate, db: Session = Depends(get_db)):
    """Update a lead."""
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check email uniqueness if email is being updated
    if lead_update.email and lead_update.email != lead.email:
        existing_lead = db.query(LeadModel).filter(LeadModel.email == lead_update.email, LeadModel.id != lead_id).first()
        if existing_lead:
            raise HTTPException(status_code=400, detail="Email already exists as another lead")
        
        existing_retailer = db.query(Retailer).filter(Retailer.email == lead_update.email).first()
        if existing_retailer:
            raise HTTPException(status_code=400, detail="Email already exists as an active retailer")

    # Update fields
    for field, value in lead_update.dict(exclude_unset=True).items():
        setattr(lead, field, value)
    
    lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(lead)
    
    logger.info("Lead updated: %s (%s)", lead.company_name, lead.email)
    return lead


@router.post("/{lead_id}/convert", response_model=dict)
def convert_lead_to_retailer(lead_id: int, convert_data: LeadConvert, db: Session = Depends(get_db)):
    """Convert a lead to an active retailer."""
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if lead.status == "converted":
        raise HTTPException(status_code=400, detail="Lead is already converted")

    # Check if email already exists as retailer
    existing_retailer = db.query(Retailer).filter(Retailer.email == lead.email).first()
    if existing_retailer:
        raise HTTPException(status_code=400, detail="Email already exists as an active retailer")

    # Create new retailer from lead
    retailer = Retailer(
        name=lead.company_name,
        email=lead.email,
        phone=lead.phone,
        location=lead.location,
        password_hash=hash_password(convert_data.password),
        is_active=True
    )
    
    db.add(retailer)
    db.commit()
    db.refresh(retailer)
    
    # Update lead status and link to retailer
    lead.status = "converted"
    lead.converted_retailer_id = retailer.id
    lead.updated_at = datetime.utcnow()
    db.commit()
    
    logger.info("Lead converted to retailer: %s -> Retailer ID %d", lead.email, retailer.id)
    return {"message": "Lead converted successfully", "retailer_id": retailer.id}


@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """Delete a lead."""
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.delete(lead)
    db.commit()
    
    logger.info("Lead deleted: %s (%s)", lead.company_name, lead.email)
    return {"message": "Lead deleted successfully"}


@router.get("/stats/pipeline")
def get_pipeline_stats(db: Session = Depends(get_db)):
    """Get lead pipeline statistics."""
    stats = {}
    
    # Count by status
    statuses = ["new", "contacted", "qualified", "converted", "lost"]
    for status in statuses:
        count = db.query(LeadModel).filter(LeadModel.status == status).count()
        stats[status] = count
    
    # Total leads
    stats["total"] = db.query(LeadModel).count()
    
    # Conversion rate
    converted = stats.get("converted", 0)
    total = stats.get("total", 0)
    stats["conversion_rate"] = (converted / total * 100) if total > 0 else 0
    
    return stats