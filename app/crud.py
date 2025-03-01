from sqlalchemy.orm import Session
from fastapi import HTTPException
import schemas, models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_users(db: Session, skip:int=0, limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user:schemas.UserCreate):
    existing_user = get_user_by_name(db, name=user.name)
    if existing_user: 
        raise HTTPException(status_code=400, detail="Username already taken")
    db_user = models.User(name=user.name,
                          premium_user=user.premium_user,
                          payment_id=user.payment_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, updated_user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = updated_user.name
        db_user.premium_user = updated_user.premium_user
        db_user.payment_id = updated_user.payment_id
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user    
