from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Dict, List
from sqlalchemy.orm import Session

from ..database import SessionLocal, UserModel
from ..auth.routes import hash_password
from ..utils.logger import logger

router = APIRouter()

class User(BaseModel):
    id: int
    username: str
    role: str

users: Dict[int, User] = {}

@router.post("/")
async def add_user(user: User):
    users[user.id] = user
    return user

@router.get("/{user_id}")
async def get_user(user_id: int):
    return users.get(user_id, {"error": "User not found"})


# Database helpers for manufacturer registration
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ManufacturerCreate(BaseModel):
    username: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True


@router.post("/manufacturers", response_model=UserOut)
def create_manufacturer(man: ManufacturerCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.username == man.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    obj = UserModel(
        username=man.username,
        hashed_password=hash_password(man.password),
        role="manufacturer",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    logger.info("Manufacturer created: %s", obj.username)
    return obj
