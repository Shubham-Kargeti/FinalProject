from fastapi import APIRouter, HTTPException, Depends, status, Response
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repository import users
from authentication.dependencies import require_role

router = APIRouter()

@router.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["User"])
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await users.repo_create_user(user, db)

@router.get("/users", response_model=list[schemas.UserResponse], tags=["User"])
async def get_all_users(db: AsyncSession = Depends(get_db), current_admin = Depends(require_role("admin"))):
    return await users.repo_get_all_users(db)

@router.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["User"])
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db), current_admin = Depends(require_role("admin"))):
    return await users.repo_get_user_by_id(user_id, db)

@router.put("/users/{user_id}", response_model=schemas.UserResponse, tags=["User"])
async def update_user(user_id: int, updated_user: schemas.UserCreate, db: AsyncSession = Depends(get_db), current_admin = Depends(require_role("admin"))):
    return await users.repo_update_user(user_id, updated_user, db)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["User"])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_admin = Depends(require_role("admin"))):
    return await users.repo_delete_user(user_id, db)
