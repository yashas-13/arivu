from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class Token(BaseModel):
    token: str
    role: str

users_db: Dict[str, Dict[str, str]] = {
    "admin": {"password": "adminpass", "role": "admin"},
    "retailer1": {"password": "retailpass", "role": "retailer"},
}

def create_token(username: str) -> str:
    return f"token-{username}"

@router.post("/register")
async def register(username: str, password: str, role: str):
    if username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    if role not in {"admin", "retailer"}:
        raise HTTPException(status_code=400, detail="Invalid role")
    users_db[username] = {"password": password, "role": role}
    return {"message": "registered"}

@router.post("/login")
async def login(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return Token(token=create_token(username), role=user["role"])
    raise HTTPException(status_code=401, detail="Invalid credentials")
