from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

class Token(BaseModel):
    token: str
    role: str
    id: int

# In-memory user store with sample data
users_db: Dict[str, Dict[str, str | int]] = {
    "admin": {"password": "adminpass", "role": "admin", "id": 1},
    "retailer1": {"password": "retailpass", "role": "retailer", "id": 2},
}

# Simple token that authorizes admin controlled actions (demo only)
ADMIN_TOKEN = "adminsecret"

def create_token(username: str) -> str:
    return f"token-{username}"

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str
    admin_token: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

class UpdateRetailerRequest(BaseModel):
    password: str
    admin_token: str

@router.post("/register")
async def register(req: RegisterRequest):
    """Register a new user.

    Retailer accounts require a valid ``admin_token`` so that only admins can
    create them. Admin accounts can be created without the token for demo
    purposes.
    """
    username = req.username
    password = req.password
    role = req.role
    admin_token = req.admin_token
    if username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    if role not in {"admin", "retailer"}:
        raise HTTPException(status_code=400, detail="Invalid role")
    if role == "retailer" and admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin token required")
    users_db[username] = {"password": password, "role": role}
    return {"message": "registered"}

@router.post("/login")
async def login(req: LoginRequest):
    username = req.username
    password = req.password
    user = users_db.get(username)
    if user and user["password"] == password:
        return Token(token=create_token(username), role=user["role"], id=user["id"])
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/retailers")
async def list_retailers(admin_token: str):
    if admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin token required")
    return [
        {"username": u, "id": info.get("id")}
        for u, info in users_db.items()
        if info["role"] == "retailer"
    ]


@router.put("/retailers/{username}")
async def update_retailer(username: str, req: UpdateRetailerRequest):
    if req.admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin token required")
    user = users_db.get(username)
    if not user or user.get("role") != "retailer":
        raise HTTPException(status_code=404, detail="Retailer not found")
    user["password"] = req.password
    users_db[username] = user
    return {"message": "updated"}


@router.delete("/retailers/{username}")
async def delete_retailer(username: str, admin_token: str):
    if admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin token required")
    user = users_db.get(username)
    if not user or user.get("role") != "retailer":
        raise HTTPException(status_code=404, detail="Retailer not found")
    del users_db[username]
    return {"message": "deleted"}
