import models
from fastapi import HTTPException, Depends
import schemas
from sqlalchemy.orm import Session
from database import get_db

def repo_admin_update_claim(claim_id: int, admin_update: schemas.AdminClaimUpdate, db: Session):
    try:
        claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        claim.status = admin_update.status
        claim.approved_amount = admin_update.approved_amount

        db.commit()
        db.refresh(claim)
        return claim
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))