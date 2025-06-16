from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Token(BaseModel):
    token: str

fake_user = {
    "username": "admin",
    "password": "password",
    "token": "secret-token",
}

@router.post("/login")
async def login(username: str, password: str):
    if username == fake_user["username"] and password == fake_user["password"]:
        return Token(token=fake_user["token"])
    raise HTTPException(status_code=401, detail="Invalid credentials")
