from fastapi import APIRouter, HTTPException, Depends, status, Response
import schemas
from sqlalchemy.orm import Session
import models
from database import get_db
from repository import claims
from authentication.oauth2 import get_current_user
from authentication.dependencies import require_role

router= APIRouter()

@router.post("/claims", response_model=schemas.ClaimResponse, status_code=status.HTTP_201_CREATED, tags=["Claims"])
def submit_claim(claim: schemas.ClaimCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role("user"))):
    return claims.repo_submit_claim(claim, db, current_user.id)

@router.get("/claims", response_model=list[schemas.ClaimResponse], tags=["Claims"])
def get_all_claims(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role == "admin":
        # Admin: see all claims
        return claims.repo_get_all_claims(db)
    else:
        # Normal user: see only own claims
        return claims.repo_get_claims_by_user(db, current_user.id)

@router.get("/claims/{claim_id}", response_model=schemas.ClaimResponse, tags=["Claims"])
def get_claim_by_id(claim_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    claim = claims.repo_get_claim_by_id(claim_id, db)

    if current_user.role != "admin" and claim.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this claim"
        )
    return claim

@router.put("/claims/{claim_id}", response_model=schemas.ClaimResponse, tags=["Claims"])
def update_claim(claim_id: int, updated_claim: schemas.ClaimCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return claims.repo_update_claim(claim_id, updated_claim, db, current_user)

@router.delete("/claims/{claim_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Claims"])
def delete_claim(claim_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return claims.repo_delete_claim(claim_id, db, current_user)

@router.get("/users/{user_id}/claims", response_model=list[schemas.ClaimResponse], tags=["Claims"])
def get_claims_by_user_id(user_id: int, db: Session = Depends(get_db), current_admin=Depends(require_role("admin"))):
    return claims.repo_get_claims_by_user_id(user_id, db)


