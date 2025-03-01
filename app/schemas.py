from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    premium_user: bool
    payment_id: str


class UserCreate(UserBase):
    pass 


class User(UserBase):
    id : int
    created_at : datetime

    class Config:
        from_attributes = True
