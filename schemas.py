from pydantic import BaseModel, EmailStr
from typing import Optional
from models import ClaimStatus, UserRole

# ----------- User -----------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True

# ----------- Claim -----------
class ClaimCreate(BaseModel):
    type: str
    requested_amount: float
    description: Optional[str] = None
    #user_id: int

class ClaimResponse(BaseModel):
    id: int
    type: str
    requested_amount: float
    approved_amount: Optional[float]
    description: Optional[str]
    status: ClaimStatus
    user_id: int

    class Config:
        from_attributes = True

class AdminClaimUpdate(BaseModel):
    status: Optional[ClaimStatus] = None
    approved_amount: Optional[float] = None