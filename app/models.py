from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    premium_user = Column(Boolean)
    payment_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=func.now() )
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now() )