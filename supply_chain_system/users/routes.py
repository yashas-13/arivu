from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import SessionLocal, UserModel
from ..auth.routes import hash_password
from ..utils.logger import logger

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ManufacturerCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True


@router.post("/manufacturers", response_model=UserOut, status_code=201)
def register_manufacturer(
    user: ManufacturerCreate, db: Session = Depends(get_db)
):
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    obj = UserModel(
        username=user.username,
        hashed_password=hash_password(user.password),
        role="manufacturer",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    logger.info("Manufacturer registered: %s", obj.username)
    return obj
