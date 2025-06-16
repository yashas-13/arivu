from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class Token(BaseModel):
    token: str

users_db: Dict[str, Dict[str, str]] = {
    "admin": {"password": "password"}
}

def create_token(username: str) -> str:
    return f"token-{username}"

@router.post("/register")
async def register(username: str, password: str):
    if username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[username] = {"password": password}
    return {"message": "registered"}

@router.post("/login")
async def login(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return Token(token=create_token(username))
    raise HTTPException(status_code=401, detail="Invalid credentials")
