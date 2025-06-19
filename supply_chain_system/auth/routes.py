from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import SessionLocal, UserModel, Retailer
from ..utils.logger import logger

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_token(user_id: int, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "role": role, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class TokenResponse(BaseModel):
    token: str
    role: str
    id: int


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == req.email).first()
    role = "manufacturer"
    if not user:
        retailer = db.query(Retailer).filter(Retailer.email == req.email).first()
        if not retailer:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user_id = retailer.id
        role = "retailer"
        hashed = retailer.password_hash
    else:
        user_id = user.id
        hashed = user.hashed_password
    if not verify_password(req.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user_id, role)
    return TokenResponse(token=token, role=role, id=user_id)

