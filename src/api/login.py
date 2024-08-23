from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import settings
from core.security import create_access_token

login_router = APIRouter(prefix="/login")


class Login(BaseModel):
    username: str
    password: str


@login_router.post("/user")
async def login(data: Login):
    if data.username == settings.LOGIN_USERNAME and data.password == settings.LOGIN_PASSWORD:
        token = create_access_token({"sub": data.username})
        return {"token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
