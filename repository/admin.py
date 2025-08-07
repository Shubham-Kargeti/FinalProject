import models
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from utils.cache import clear_cache 

async def repo_admin_update_claim(claim_id: int, admin_update: schemas.AdminClaimUpdate, db: AsyncSession):
    try:
        result = await db.execute(select(models.Claim).where(models.Claim.id == claim_id))
        claim = result.scalar_one_or_none()

        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        claim.status = admin_update.status
        claim.approved_amount = admin_update.approved_amount

        await db.commit()
        await db.refresh(claim)

        clear_cache("all_claims")
        clear_cache(f"user_claims_{claim.user_id}")

        return claim

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
