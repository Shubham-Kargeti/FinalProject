from fastapi import APIRouter, HTTPException, Depends, status
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


@router.get("/admin/users", response_model=list[schemas.UserResponse], tags=["Admin"])
async def get_all_users(db: AsyncSession = Depends(get_db), current_admin = Depends(require_role("admin"))):
    return await admin.repo_get_all_users(db)

@router.get("/admin/users/{user_id}", response_model=schemas.UserResponse, tags=["Admin"])
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db), current_admin = Depends(require_role("admin"))):
    return await admin.repo_get_user_by_id(user_id, db)

@router.put("/admin/users/{user_id}", response_model=schemas.UserResponse, tags=["Admin"])
async def update_user(user_id: int, updated_user: schemas.UserCreate, db: AsyncSession = Depends(get_db), current_admin = Depends(require_role("admin"))):
    return await admin.repo_update_user(user_id, updated_user, db)

@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Admin"])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_admin = Depends(require_role("admin"))):
    return await admin.repo_delete_user(user_id, db)

@router.get("/admin/users/{user_id}/claims", response_model=list[schemas.ClaimResponse], tags=["Admin"])
async def get_claims_by_user_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_role("admin"))
):
    return await admin.repo_get_claims_by_user_id(user_id, db)