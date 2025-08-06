from fastapi import APIRouter, HTTPException, Depends, status
import schemas
from sqlalchemy.orm import Session
import models
from database import get_db
from repository import admin

router= APIRouter()

@router.put("/admin/claims/{claim_id}", response_model=schemas.ClaimResponse, tags=["Admin"])
def admin_update_claim(claim_id: int, admin_update: schemas.AdminClaimUpdate, db: Session = Depends(get_db)):
    return admin.repo_admin_update_claim(claim_id, admin_update, db)