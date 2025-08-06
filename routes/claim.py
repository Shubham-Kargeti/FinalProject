from fastapi import APIRouter, HTTPException, Depends, status, Response
import schemas
from sqlalchemy.orm import Session
import models
from database import get_db
from repository import claims

router= APIRouter()

@router.post("/claims", response_model=schemas.ClaimResponse, status_code=status.HTTP_201_CREATED, tags=["Claims"])
def submit_claim(claim: schemas.ClaimCreate, db: Session = Depends(get_db)):
    return claims.repo_submit_claim(claim, db)

@router.get("/claims", response_model=list[schemas.ClaimResponse], tags=["Claims"])
def get_all_claims(db: Session = Depends(get_db)):
    return claims.repo_get_all_claims(db)

@router.get("/claims/{claim_id}", response_model=schemas.ClaimResponse, tags=["Claims"])
def get_claim_by_id(claim_id: int, db: Session = Depends(get_db)):
    return claims.repo_get_claim_by_id(claim_id, db)

@router.put("/claims/{claim_id}", response_model=schemas.ClaimResponse, tags=["Claims"])
def update_claim(claim_id: int, updated_claim: schemas.ClaimCreate, db: Session = Depends(get_db)):
    return claims.repo_update_claim(claim_id, updated_claim, db)

@router.delete("/claims/{claim_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Claims"])
def delete_claim(claim_id: int, db: Session = Depends(get_db)):
    return claims.repo_delete_claim(claim_id, db)

@router.get("/users/{user_id}/claims", response_model=list[schemas.ClaimResponse], tags=["Claims"])
def get_claims_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return claims.repo_get_claims_by_user_id(user_id, db)


