from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

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
