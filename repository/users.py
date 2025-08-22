from fastapi import HTTPException, Depends, Response, status
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from utils.hashing import hash_password
from utils.cache import clear_cache

async def repo_create_user(user: schemas.UserCreate, db: AsyncSession):
    try:
        user_data = user.model_dump()
        user_data["password"] = hash_password(user.password)
        new_user = models.User(**user_data)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        clear_cache("all_users")  # Invalidate user cache
        return new_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

