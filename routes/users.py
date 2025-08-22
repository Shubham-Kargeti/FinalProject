from fastapi import APIRouter, HTTPException, Depends, status, Response
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repository import users
from authentication.dependencies import require_role
import models
from authentication.oauth2 import get_current_user

router = APIRouter()

@router.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["All Users"])
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await users.repo_create_user(user, db)


@router.get("/users/me", response_model=schemas.UserResponse, tags=["All Users"])
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
