from fastapi import HTTPException, Depends, Response, status
import schemas
from database import get_db
from sqlalchemy.orm import Session
import models
from authentication.hashing import hash_password


def repo_create_user(user: schemas.UserCreate, db: Session):
    try:
        user_data= user.model_dump()
        user_data["password"] = hash_password(user.password)
        print("hashed paswword = ", user_data["password"])

        new_user = models.User(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def repo_get_all_users(db: Session = Depends(get_db)):
    try:
        return db.query(models.User).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def repo_get_user_by_id(user_id: int, db: Session):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def repo_update_user(user_id: int, updated_user: schemas.UserCreate, db: Session):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.username = updated_user.username
        user.email = updated_user.email
        user.password = updated_user.password 

        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def repo_delete_user(user_id: int, db: Session):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(user)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))