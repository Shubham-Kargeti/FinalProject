from fastapi import HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import schemas
import models
from utils.cache import get_cache, set_cache, clear_cache


async def repo_submit_claim(claim: schemas.ClaimCreate, db: AsyncSession, user_id: int):
    try:
        new_claim = models.Claim(
            type=claim.type,
            requested_amount=claim.requested_amount,
            description=claim.description,
            user_id=user_id
        )
        db.add(new_claim)
        await db.commit()
        await db.refresh(new_claim)

        # Invalidate related caches
        clear_cache("all_claims")
        clear_cache(f"user_claims_{user_id}")

        return new_claim
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def repo_get_all_claims(db: AsyncSession):
    cache_key = "all_claims"
    cached_claims = get_cache(cache_key)

    if cached_claims is not None:
        return cached_claims

    try:
        result = await db.execute(select(models.Claim))
        claims = result.scalars().all()
        set_cache(cache_key, claims, ttl=60)
        return claims
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def repo_get_claim_by_id(claim_id: int, db: AsyncSession):
    cache_key = f"claim_id_{claim_id}"
    cached_claim = get_cache(cache_key)

    if cached_claim is not None:
        return cached_claim

    try:
        result = await db.execute(select(models.Claim).where(models.Claim.id == claim_id))
        claim = result.scalar_one_or_none()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        set_cache(cache_key, claim, ttl=60)
        return claim
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def repo_update_claim(claim_id: int, updated_claim: schemas.ClaimCreate, db: AsyncSession, current_user: models.User):
    try:
        result = await db.execute(select(models.Claim).where(models.Claim.id == claim_id))
        claim = result.scalar_one_or_none()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")

        if current_user.role != "admin" and claim.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this claim")

        claim.type = updated_claim.type
        claim.requested_amount = updated_claim.requested_amount
        claim.description = updated_claim.description

        await db.commit()
        await db.refresh(claim)

        # Invalidate related caches
        clear_cache("all_claims")
        clear_cache(f"user_claims_{claim.user_id}")
        clear_cache(f"claim_id_{claim_id}")

        return claim
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def repo_delete_claim(claim_id: int, db: AsyncSession, current_user: models.User):
    try:
        result = await db.execute(select(models.Claim).where(models.Claim.id == claim_id))
        claim = result.scalar_one_or_none()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")

        if current_user.role != "admin" and claim.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this claim")

        await db.delete(claim)
        await db.commit()

        # Invalidate related caches
        clear_cache("all_claims")
        clear_cache(f"user_claims_{claim.user_id}")
        clear_cache(f"claim_id_{claim_id}")

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def repo_get_claims_by_user_id(user_id: int, db: AsyncSession):
    cache_key = f"user_claims_{user_id}"
    cached = get_cache(cache_key)

    if cached is not None:
        return cached

    try:
        result = await db.execute(select(models.Claim).where(models.Claim.user_id == user_id))
        claims = result.scalars().all()
        if not claims:
            raise HTTPException(status_code=404, detail=f"No claims found for user ID {user_id}")
        set_cache(cache_key, claims, ttl=60)
        return claims
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
