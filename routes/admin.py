from fastapi import APIRouter, HTTPException, Depends
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repository import admin
from authentication.dependencies import require_role

router = APIRouter()

@router.put("/admin/claims/{claim_id}", response_model=schemas.ClaimResponse, tags=["Admin"])
async def admin_update_claim(
    claim_id: int,
    admin_update: schemas.AdminClaimUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_role("admin"))
):
    return await admin.repo_admin_update_claim(claim_id, admin_update, db)
