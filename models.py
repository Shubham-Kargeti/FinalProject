from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

# Role enum
class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

# Status enum
class ClaimStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)

    claims = relationship("Claim", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, nullable=False)
    requested_amount = Column(Float, nullable=False)
    approved_amount = Column(Float, nullable=True)  
    description = Column(String, nullable=True)
    status = Column(Enum(ClaimStatus), default=ClaimStatus.pending)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="claims")
