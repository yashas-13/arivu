from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class Token(BaseModel):
    token: str
    role: str

# In-memory user store with sample data
users_db: Dict[str, Dict[str, str]] = {
    "admin": {"password": "adminpass", "role": "admin"},
    "retailer1": {"password": "retailpass", "role": "retailer"},
}

# Simple token that authorizes admin controlled actions (demo only)
ADMIN_TOKEN = "adminsecret"

def create_token(username: str) -> str:
    return f"token-{username}"

@router.post("/register")
async def register(
    username: str,
    password: str,
    role: str,
    admin_token: str | None = None,
):
    """Register a new user.

    Retailer accounts require a valid ``admin_token`` so that only admins can
    create them. Admin accounts can be created without the token for demo
    purposes.
    """
    if username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    if role not in {"admin", "retailer"}:
        raise HTTPException(status_code=400, detail="Invalid role")
    if role == "retailer" and admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin token required")
    users_db[username] = {"password": password, "role": role}
    return {"message": "registered"}

@router.post("/login")
async def login(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return Token(token=create_token(username), role=user["role"])
    raise HTTPException(status_code=401, detail="Invalid credentials")
