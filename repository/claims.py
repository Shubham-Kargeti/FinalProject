from fastapi import HTTPException, Depends, Response, status
import schemas
from database import get_db
from sqlalchemy.orm import Session
import models


def repo_submit_claim(claim: schemas.ClaimCreate, db: Session, user_id: int):
    try:
        new_claim = models.Claim(
            type=claim.type,
            requested_amount=claim.requested_amount,
            description=claim.description,
            user_id=user_id
        )
        db.add(new_claim)
        db.commit()
        db.refresh(new_claim)
        return new_claim
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def repo_get_all_claims(db: Session):
    try:
        return db.query(models.Claim).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    

def repo_get_claims_by_user(db: Session, user_id: int):
    try:
        return db.query(models.Claim).filter(models.Claim.user_id == user_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def repo_get_claim_by_id(claim_id: int, db: Session):
    try:
        claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        return claim
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def repo_update_claim(claim_id: int, updated_claim: schemas.ClaimCreate, db: Session, current_user: models.User):
    try:
        claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        if current_user.role != "admin" and claim.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this claim")
        
        claim.type = updated_claim.type
        claim.requested_amount = updated_claim.requested_amount
        claim.description = updated_claim.description

        db.commit()
        db.refresh(claim)
        return claim
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def repo_delete_claim(claim_id: int, db: Session, current_user: models.User):
    try:
        claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        if current_user.role != "admin" and claim.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this claim")
        
        db.delete(claim)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def repo_get_claims_by_user_id(user_id: int, db: Session):
    try:
        claims = db.query(models.Claim).filter(models.Claim.user_id == user_id).all()
        if not claims:
            raise HTTPException(status_code=404, detail=f"No claims found for user ID {user_id}")
        return claims
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))