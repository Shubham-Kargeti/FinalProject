from fastapi import HTTPException, Depends, Response, status
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from utils.hashing import hash_password
from utils.cache import get_cache, set_cache, clear_cache

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


async def repo_get_all_users(db: AsyncSession):
    cache_key = "all_users"
    cached_users = get_cache(cache_key)

    if cached_users is not None:
        return cached_users

    try:
        result = await db.execute(select(models.User))
        users = result.scalars().all()
        set_cache(cache_key, users, ttl=60)  # Cache for 60 seconds
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def repo_get_user_by_id(user_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(models.User).where(models.User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def repo_update_user(user_id: int, updated_user: schemas.UserCreate, db: AsyncSession):
    try:
        result = await db.execute(select(models.User).where(models.User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.username = updated_user.username
        user.email = updated_user.email
        user.password = updated_user.password

        await db.commit()
        await db.refresh(user)
        clear_cache("all_users")
        return user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def repo_delete_user(user_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(models.User).where(models.User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(user)
        await db.commit()

        
        clear_cache("all_users")
        #even if user is deleted the claims still be showing without this line due to cache
        clear_cache(f"user_claims_{user_id}")

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
